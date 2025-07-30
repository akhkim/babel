"""
Audio processing module for Enhanced Babel - Real-time Audio Translation

This module contains audio capture and NLP processing classes for real-time
speech recognition and translation.
"""

import queue, threading, platform, time, traceback
import numpy as np
import sounddevice as sd
from faster_whisper import WhisperModel
from googletrans import Translator
from scipy import signal
import torch

from PyQt5 import QtCore

from config import (
    config, WASAPI_HOST_API, WASAPI_SETTINGS, CHUNK_SECONDS, DEBUG_MODE,
    MAX_QUEUE_SIZE, DEFAULT_AUDIO_THRESHOLD, get_loopback_device,
    convert_whisper_to_googletrans_code
)


class AudioWorker(threading.Thread):
    """
    Captures CHUNK_SECONDS of stereo PCM from the selected device,
    down-mixes to mono, and puts it on a queue for the NLP worker.
    Optimized for low latency and memory usage.
    """
    def __init__(self, q: queue.Queue, stop_evt: threading.Event, device_index=None):
        super().__init__(daemon=True)
        self.q, self.stop_evt = q, stop_evt
        self.device, self.rate = get_loopback_device(device_index)
        # Store sample rate in queue for NLP worker to access
        self.q._audio_rate = self.rate

    def run(self):
        try:
            frames = int(CHUNK_SECONDS * self.rate)
            print(f"AudioWorker: Starting capture with device {self.device}, rate {self.rate}, frames {frames}")
            
            # Configure stream settings for better compatibility during calls
            stream_settings = {
                'device': self.device,
                'samplerate': self.rate,
                'channels': 2,
                'dtype': "float32",
                'blocksize': frames,
                'latency': 'low'
            }
            
            # Add WASAPI-specific settings for Windows to ensure shared mode
            if platform.system() == "Windows" and WASAPI_HOST_API is not None and WASAPI_SETTINGS is not None:
                try:
                    # Check if the selected device supports WASAPI
                    device_info = sd.query_devices(self.device)
                    if device_info['hostapi'] == WASAPI_HOST_API:
                        stream_settings['extra_settings'] = WASAPI_SETTINGS
                        if DEBUG_MODE:
                            print(f"AudioWorker: Using WASAPI shared mode for device {self.device}")
                    else:
                        if DEBUG_MODE:
                            print(f"AudioWorker: Device {self.device} not on WASAPI host API, using default settings")
                except Exception as e:
                    if DEBUG_MODE:
                        print(f"AudioWorker: Could not apply WASAPI settings: {e}")
            
            with sd.InputStream(**stream_settings) as stream:
                chunk_count = 0
                while not self.stop_evt.is_set():
                    buf, overflowed = stream.read(frames)
                    if overflowed and DEBUG_MODE:
                        print("Audio buffer overflow detected!")
                    
                    mono = buf.mean(axis=1)          # L+R → mono
                    
                    # Check if we're getting actual audio data
                    audio_level = np.abs(mono).max()
                    if DEBUG_MODE and chunk_count % 10 == 0:  # Reduced debug frequency
                        print(f"Audio chunk {chunk_count}: level={audio_level:.4f}, size={len(mono)}")
                    
                    # Skip if queue is too full to prevent memory buildup
                    if self.q.qsize() >= MAX_QUEUE_SIZE:
                        if DEBUG_MODE:
                            print("Queue full, dropping audio chunk")
                        continue
                    
                    self.q.put_nowait(mono.copy())
                    chunk_count += 1
        except Exception as e:
            print(f"AudioWorker error: {e}")
            if DEBUG_MODE:
                traceback.print_exc()


class NLPWorker(QtCore.QObject, threading.Thread):
    """
    Thread + QObject so we get Qt signals *and* easy Python threading.
    Uses Faster-Whisper for improved performance.
    """
    new_line = QtCore.pyqtSignal(str)
    clear_overlay = QtCore.pyqtSignal()

    def __init__(self, q: queue.Queue, stop_evt: threading.Event, target_code: str, source_lang: str = None, audio_threshold: float = DEFAULT_AUDIO_THRESHOLD, model_name: str = "turbo"):
        QtCore.QObject.__init__(self)
        threading.Thread.__init__(self, daemon=True)
        self.q, self.stop_evt = q, stop_evt
        self.target_lang = target_code
        self.source_lang = source_lang
        self.audio_threshold = audio_threshold
        self.model_name = model_name
        self.last_speech_time = time.time()
        self.clear_delay = 2.0
        
        print(f"Loading Faster-Whisper model '{model_name}'...")
        compute_type = "int8" if model_name in ["large-v3", "distil-large-v3"] else "float16"
        self.model = WhisperModel(
            model_name, 
            device="cuda" if torch.cuda.is_available() else "cpu", 
            compute_type=compute_type,
            num_workers=1,
            download_root=None,
            local_files_only=False
        )
        print(f"Faster-Whisper model '{model_name}' loaded successfully!")
        
        self.translator = Translator()
        print("Translator initialized!")
        
        if self.source_lang:
            print(f"Whisper will transcribe from: {self.source_lang}")
        else:
            print("Whisper will auto-detect source language")
        
        self._resample_ratio = None
        self._target_sample_rate = 16000

    def _languages_match(self, detected_lang, target_lang):
        """
        Check if the detected language matches the target language.
        Handles language code mappings and variations.
        """
        if not detected_lang or not target_lang:
            return False
        
        # Normalize language codes to lowercase
        detected_lang = detected_lang.lower()
        target_lang = target_lang.lower()
        
        # Direct match
        if detected_lang == target_lang:
            return True
        
        # Language code mappings for common variations
        language_mappings = {
            'en': ['en', 'english'],
            'es': ['es', 'spanish', 'castilian'],
            'fr': ['fr', 'french'],
            'de': ['de', 'german'],
            'it': ['it', 'italian'],
            'pt': ['pt', 'portuguese'],
            'ru': ['ru', 'russian'],
            'zh': ['zh', 'zh-cn', 'zh-tw', 'chinese'],
            'ja': ['ja', 'japanese'],
            'ko': ['ko', 'korean'],
            'ar': ['ar', 'arabic'],
            'hi': ['hi', 'hindi'],
            'nl': ['nl', 'dutch', 'flemish'],
            'ca': ['ca', 'catalan', 'valencian'],
            'no': ['no', 'norwegian', 'nynorsk'],
            'sv': ['sv', 'swedish'],
            'da': ['da', 'danish'],
            'fi': ['fi', 'finnish'],
            'pl': ['pl', 'polish'],
            'tr': ['tr', 'turkish'],
            'he': ['he', 'iw', 'hebrew'],
            'th': ['th', 'thai'],
            'vi': ['vi', 'vietnamese'],
            'uk': ['uk', 'ukrainian'],
            'cs': ['cs', 'czech'],
            'hu': ['hu', 'hungarian'],
            'ro': ['ro', 'romanian'],
            'bg': ['bg', 'bulgarian'],
            'hr': ['hr', 'croatian'],
            'sk': ['sk', 'slovak'],
            'sl': ['sl', 'slovenian'],
            'et': ['et', 'estonian'],
            'lv': ['lv', 'latvian'],
            'lt': ['lt', 'lithuanian'],
            'mt': ['mt', 'maltese'],
            'ga': ['ga', 'irish'],
            'cy': ['cy', 'welsh'],
            'eu': ['eu', 'basque'],
            'gl': ['gl', 'galician'],
            'is': ['is', 'icelandic'],
            'mk': ['mk', 'macedonian'],
            'be': ['be', 'belarusian'],
            'sq': ['sq', 'albanian'],
            'sr': ['sr', 'serbian'],
            'bs': ['bs', 'bosnian'],
            'el': ['el', 'greek'],
            'fa': ['fa', 'persian'],
            'ur': ['ur', 'urdu'],
            'bn': ['bn', 'bengali'],
            'ta': ['ta', 'tamil'],
            'te': ['te', 'telugu'],
            'kn': ['kn', 'kannada'],
            'ml': ['ml', 'malayalam'],
            'gu': ['gu', 'gujarati'],
            'pa': ['pa', 'punjabi'],
            'mr': ['mr', 'marathi'],
            'ne': ['ne', 'nepali'],
            'si': ['si', 'sinhala'],
            'my': ['my', 'burmese', 'myanmar'],
            'km': ['km', 'khmer'],
            'lo': ['lo', 'lao'],
            'ka': ['ka', 'georgian'],
            'am': ['am', 'amharic'],
            'sw': ['sw', 'swahili'],
            'zu': ['zu', 'zulu'],
            'af': ['af', 'afrikaans'],
            'ms': ['ms', 'malay'],
            'tl': ['tl', 'tagalog'],
            'id': ['id', 'indonesian'],
            'jv': ['jv', 'jw', 'javanese'],
            'su': ['su', 'sundanese']
        }
        
        # Check if both languages belong to the same group
        for lang_code, variations in language_mappings.items():
            if detected_lang in variations and target_lang in variations:
                return True
        
        # Handle Chinese variants specifically
        chinese_variants = ['zh', 'zh-cn', 'zh-tw', 'chinese']
        if detected_lang in chinese_variants and target_lang in chinese_variants:
            return True
        
        return False

    def run(self):
        print("NLPWorker: Starting processing loop...")
        processed_count = 0
        
        while not self.stop_evt.is_set():
            try:
                audio = self.q.get(timeout=0.1)
            except queue.Empty:
                # Check if we should clear the overlay due to silence
                current_time = time.time()
                if (current_time - self.last_speech_time) > self.clear_delay:
                    if DEBUG_MODE:
                        print(f"Clearing overlay due to {self.clear_delay}s of silence")
                    self.clear_overlay.emit()
                    self.last_speech_time = current_time  # Reset to prevent repeated clearing
                continue

            try:
                # Check audio data quality
                audio_level = np.abs(audio).max()
                
                if DEBUG_MODE:
                    print(f"Processing audio chunk {processed_count}: level={audio_level:.4f}, length={len(audio)}")
                
                # Skip if audio is too quiet (likely silence)
                if audio_level < self.audio_threshold:
                    if DEBUG_MODE:
                        print(f"Skipping quiet audio chunk (level {audio_level:.4f} < threshold {self.audio_threshold:.4f})")
                    continue

                if DEBUG_MODE:
                    print(f"Transcribing audio chunk {processed_count}...")
                
                # Optimized audio preprocessing
                current_sample_rate = self.q._audio_rate if hasattr(self.q, '_audio_rate') else 48000
                
                if self._resample_ratio is None:
                    self._resample_ratio = self._target_sample_rate / current_sample_rate
                
                if current_sample_rate != self._target_sample_rate:
                    # More efficient resampling
                    target_length = int(len(audio) * self._resample_ratio)
                    audio = signal.resample(audio, target_length).astype(np.float32)
                
                # Normalize audio more efficiently
                max_val = np.abs(audio).max()
                if max_val > 0:
                    audio = audio * (0.9 / max_val)
                
                # Use faster-whisper API with optimized settings
                segments, info = self.model.transcribe(
                    audio, 
                    language=self.source_lang,
                    beam_size=1,  # Keep beam size low for speed
                    no_speech_threshold=0.6,
                    condition_on_previous_text=False,
                    vad_filter=True,  # Enable VAD filtering
                    vad_parameters=dict(min_silence_duration_ms=500)  # Faster VAD response
                )
                
                # More efficient text extraction
                transcribed_text = " ".join(segment.text for segment in segments).strip()
                
                # Get detected language if auto-detecting
                detected_language = None
                if self.source_lang is None and hasattr(info, 'language'):
                    detected_language = info.language
                    if DEBUG_MODE:
                        print(f"Detected language: {detected_language}")
                
                if DEBUG_MODE:
                    print(f"Transcription result: '{transcribed_text}'")
                
                if not transcribed_text:
                    if DEBUG_MODE:
                        print("Skipping empty transcription")
                    continue
                
                # Check if detected language matches target language (skip translation if same)
                if (detected_language and 
                    self._languages_match(detected_language, self.target_lang)):
                    if DEBUG_MODE:
                        print(f"🔄 Detected language '{detected_language}' matches target '{self.target_lang}', skipping subtitle display")
                    # Update speech time but don't show subtitle
                    self.last_speech_time = time.time()
                    continue
                
                # Optimized translation logic
                if DEBUG_MODE:
                    print(f"🔄 Translating from '{transcribed_text}' to {self.target_lang}...")
                
                try:
                    translation_result = self.translator.translate(transcribed_text, dest=self.target_lang)
                    translated = translation_result.text
                    
                    if DEBUG_MODE:
                        print(f"✅ Translation successful: '{translated}'")
                    
                except Exception as e:
                    if DEBUG_MODE:
                        print(f"❌ TRANSLATION FAILED: {e}")
                    translated = transcribed_text
                
                if DEBUG_MODE:
                    print(f"Final output to overlay: '{translated}'")
                
                # Update the last speech time since we successfully processed speech
                self.last_speech_time = time.time()
                
                self.new_line.emit(translated)
                processed_count += 1
                
            except Exception as e:
                if DEBUG_MODE:
                    print(f"Error processing audio chunk: {e}")
                    traceback.print_exc()
