# main.py  –  "Babel" live subtitle translator (Windows/Linux/macOS)
# ───────────────────────────────────────────────────────────────────
"""
Enhanced Babel - Real-time Audio Translation with Faster-Whisper

Features:
  • PyQt5 control window with full language control
  • Audio device selection (Auto-detect or manual selection)
  • Source language selection for Whisper transcription
  • Target language selection for translation output
  • Configurable audio level threshold
  • Uses Faster-Whisper for improved speed and performance
  • Real-time translation and subtitle overlay
  • Optimized for low latency and memory usage

Requirements (Python >= 3.9):
    pip install PyQt5 sounddevice numpy scipy pillow faster-whisper googletrans==4.0.0rc1
"""
import sys, queue, threading, platform, ctypes, time, gc, json
from pathlib import Path

import numpy as np
import sounddevice as sd
from faster_whisper import WhisperModel
from googletrans import Translator
from scipy import signal

from PyQt5 import QtCore, QtGui, QtWidgets
import torch

# ──────────────────────────── USER SETTINGS ─────────────────────────── #
DEVICE_INDEX = 23      # Use Virtual Audio Cable if specify one app
SAMPLE_RATE  = 48_000
CHUNK_SECONDS           = 3     # Reduced from 4 to 2 for lower latency
MODEL_NAME              = "turbo"    # Use turbo model by default
DEBUG_MODE              = False     # Disable debug output for performance
DEFAULT_AUDIO_THRESHOLD = 0.001     # Increased threshold to reduce processing
MAX_QUEUE_SIZE          = 3         # Limit queue size to reduce memory usage

# Available Whisper models
WHISPER_MODELS = {
    "tiny": "Fast but basic accuracy",
    "turbo": "Balanced speed/accuracy", 
    "large-v3": "High accuracy but slower",
    "distil-large-v3": "Optimized large model"
}

TARGETS = {
    "Afrikaans": "af",
    "Albanian": "sq",
    "Amharic": "am",
    "Arabic": "ar",
    "Armenian": "hy",
    "Azerbaijani": "az",
    "Basque": "eu",
    "Belarusian": "be",
    "Bengali": "bn",
    "Bosnian": "bs",
    "Bulgarian": "bg",
    "Catalan": "ca",
    "Cebuano": "ceb",
    "Chinese (Simplified)": "zh-cn",
    "Chinese (Traditional)": "zh-tw",
    "Corsican": "co",
    "Croatian": "hr",
    "Czech": "cs",
    "Danish": "da",
    "Dutch": "nl",
    "English": "en",
    "Esperanto": "eo",
    "Estonian": "et",
    "Finnish": "fi",
    "French": "fr",
    "Frisian": "fy",
    "Galician": "gl",
    "Georgian": "ka",
    "German": "de",
    "Greek": "el",
    "Gujarati": "gu",
    "Haitian Creole": "ht",
    "Hausa": "ha",
    "Hawaiian": "haw",
    "Hebrew": "iw",
    "Hindi": "hi",
    "Hmong": "hmn",
    "Hungarian": "hu",
    "Icelandic": "is",
    "Igbo": "ig",
    "Indonesian": "id",
    "Irish": "ga",
    "Italian": "it",
    "Japanese": "ja",
    "Javanese": "jw",
    "Kannada": "kn",
    "Kazakh": "kk",
    "Khmer": "km",
    "Korean": "ko",
    "Kurdish": "ku",
    "Kyrgyz": "ky",
    "Lao": "lo",
    "Latin": "la",
    "Latvian": "lv",
    "Lithuanian": "lt",
    "Luxembourgish": "lb",
    "Macedonian": "mk",
    "Malagasy": "mg",
    "Malay": "ms",
    "Malayalam": "ml",
    "Maltese": "mt",
    "Maori": "mi",
    "Marathi": "mr",
    "Mongolian": "mn",
    "Myanmar (Burmese)": "my",
    "Nepali": "ne",
    "Norwegian": "no",
    "Odia (Oriya)": "or",
    "Pashto": "ps",
    "Persian": "fa",
    "Polish": "pl",
    "Portuguese": "pt",
    "Punjabi": "pa",
    "Romanian": "ro",
    "Russian": "ru",
    "Samoan": "sm",
    "Scots Gaelic": "gd",
    "Serbian": "sr",
    "Sesotho": "st",
    "Shona": "sn",
    "Sindhi": "sd",
    "Sinhala": "si",
    "Slovak": "sk",
    "Slovenian": "sl",
    "Somali": "so",
    "Spanish": "es",
    "Sundanese": "su",
    "Swahili": "sw",
    "Swedish": "sv",
    "Tagalog": "tl",
    "Tajik": "tg",
    "Tamil": "ta",
    "Tatar": "tt",
    "Telugu": "te",
    "Thai": "th",
    "Turkish": "tr",
    "Turkmen": "tk",
    "Ukrainian": "uk",
    "Urdu": "ur",
    "Uyghur": "ug",
    "Uzbek": "uz",
    "Vietnamese": "vi",
    "Welsh": "cy",
    "Xhosa": "xh",
    "Yiddish": "yi",
    "Yoruba": "yo",
    "Zulu": "zu"
}

# Source languages that Whisper can transcribe from
WHISPER_SOURCE_LANGUAGES = {
    "Auto-detect": None,  # Let Whisper auto-detect
    "Afrikaans": "af",
    "Albanian": "sq",
    "Amharic": "am",
    "Arabic": "ar",
    "Armenian": "hy",
    "Assamese": "as",
    "Azerbaijani": "az",
    "Bashkir": "ba",
    "Basque": "eu",
    "Belarusian": "be",
    "Bengali": "bn",
    "Bosnian": "bs",
    "Breton": "br",
    "Bulgarian": "bg",
    "Burmese": "my",
    "Castilian": "es",
    "Catalan": "ca",
    "Chinese": "zh",
    "Croatian": "hr",
    "Czech": "cs",
    "Danish": "da",
    "Dutch": "nl",
    "English": "en",
    "Estonian": "et",
    "Faroese": "fo",
    "Finnish": "fi",
    "Flemish": "nl",
    "French": "fr",
    "Galician": "gl",
    "Georgian": "ka",
    "German": "de",
    "Greek": "el",
    "Gujarati": "gu",
    "Haitian": "ht",
    "Hausa": "ha",
    "Hawaiian": "haw",
    "Hebrew": "he",
    "Hindi": "hi",
    "Hungarian": "hu",
    "Icelandic": "is",
    "Indonesian": "id",
    "Italian": "it",
    "Japanese": "ja",
    "Javanese": "jv",
    "Kannada": "kn",
    "Kazakh": "kk",
    "Khmer": "km",
    "Korean": "ko",
    "Lao": "lo",
    "Latin": "la",
    "Latvian": "lv",
    "Letzeburgesch": "lb",
    "Lingala": "ln",
    "Lithuanian": "lt",
    "Luxembourgish": "lb",
    "Macedonian": "mk",
    "Malagasy": "mg",
    "Malay": "ms",
    "Malayalam": "ml",
    "Maltese": "mt",
    "Maori": "mi",
    "Marathi": "mr",
    "Mongolian": "mn",
    "Nepali": "ne",
    "Norwegian": "no",
    "Nynorsk": "nn",
    "Occitan": "oc",
    "Pashto": "ps",
    "Persian": "fa",
    "Polish": "pl",
    "Portuguese": "pt",
    "Punjabi": "pa",
    "Pushto": "ps",
    "Romanian": "ro",
    "Russian": "ru",
    "Sanskrit": "sa",
    "Serbian": "sr",
    "Shona": "sn",
    "Sindhi": "sd",
    "Sinhala": "si",
    "Slovak": "sk",
    "Slovenian": "sl",
    "Somali": "so",
    "Spanish": "es",
    "Sundanese": "su",
    "Swahili": "sw",
    "Swedish": "sv",
    "Tagalog": "tl",
    "Tajik": "tg",
    "Tamil": "ta",
    "Tatar": "tt",
    "Telugu": "te",
    "Thai": "th",
    "Tibetan": "bo",
    "Turkish": "tr",
    "Turkmen": "tk",
    "Ukrainian": "uk",
    "Urdu": "ur",
    "Uzbek": "uz",
    "Valencian": "ca",
    "Vietnamese": "vi",
    "Welsh": "cy",
    "Yiddish": "yi",
    "Yoruba": "yo"
}

# Mapping from Whisper language codes to Google Translate language codes
WHISPER_TO_GOOGLETRANS_MAPPING = {
    "zh": "zh-cn",  # Chinese simplified
    "he": "iw",     # Hebrew
    "jv": "jw",     # Javanese
    "nn": "no",     # Norwegian Nynorsk -> Norwegian
    "oc": "ca",     # Occitan -> Catalan (closest match)
    "ps": "ps",     # Pashto
    "sa": "hi",     # Sanskrit -> Hindi (closest match)
    "bo": "zh-cn",  # Tibetan -> Chinese (closest match)
    "ca": "ca",     # Valencian -> Catalan
}

def convert_whisper_to_googletrans_code(whisper_code):
    """Convert Whisper language code to Google Translate language code if needed"""
    if whisper_code is None:
        return None
    return WHISPER_TO_GOOGLETRANS_MAPPING.get(whisper_code, whisper_code)

# ──────────────────────────── AUDIO DEVICE MANAGEMENT ───────────────── #
def get_available_input_devices():
    """Get list of available input audio devices"""
    devices = sd.query_devices()
    input_devices = []
    
    for idx, device in enumerate(devices):
        if device['max_input_channels'] > 0:
            name = device['name']
            # Mark special device types
            if 'loopback' in name.lower():
                name += " (System Audio)"
            elif 'stereo mix' in name.lower():
                name += " (System Audio)"
            elif 'monitor' in name.lower():
                name += " (System Audio)"
            elif 'cable' in name.lower():
                name += " (Virtual Cable)"
            elif 'vac' in name.lower():
                name += " (Virtual Audio Cable)"
            
            input_devices.append({
                'index': idx,
                'name': name,
                'channels': device['max_input_channels'],
                'samplerate': int(device['default_samplerate']),
                'is_loopback': any(keyword in device['name'].lower() 
                                 for keyword in ['loopback', 'stereo mix', 'monitor']),
                'is_virtual_cable': any(keyword in device['name'].lower() 
                                      for keyword in ['cable', 'vac', 'virtual'])
            })
    
    return input_devices

def auto_detect_loopback_device():
    """Auto-detect the best loopback device"""
    devices = get_available_input_devices()
    
    # First priority: Stereo Mix with 2ch 48000Hz (ideal configuration)
    for device in devices:
        if (device['is_loopback'] and 
            device['channels'] == 2 and 
            device['samplerate'] == 48000 and
            'stereo mix' in device['name'].lower()):
            print(f"Found ideal Stereo Mix device: {device['name']}")
            return device['index'], device['samplerate']
    
    # Second priority: Virtual Audio Cables (best for app-specific capture)
    for device in devices:
        if device.get('is_virtual_cable', False):
            print(f"Found Virtual Audio Cable: {device['name']}")
            return device['index'], device['samplerate']
    
    # Third priority: Any Stereo Mix device
    for device in devices:
        if device['is_loopback'] and 'stereo mix' in device['name'].lower():
            print(f"Found Stereo Mix device: {device['name']}")
            return device['index'], device['samplerate']
    
    # Fourth priority: Other loopback devices
    for device in devices:
        if device['is_loopback']:
            return device['index'], device['samplerate']
    
    # Fallback to the hard-coded device if available
    if DEVICE_INDEX is not None:
        return DEVICE_INDEX, SAMPLE_RATE
    
    # Last resort: use any input device with 2+ channels
    for device in devices:
        if device['channels'] >= 2:
            return device['index'], device['samplerate']
    
    raise RuntimeError("No suitable audio input device found!")

# ──────────────────────────── LOOP-BACK DISCOVERY ───────────────────── #
def get_loopback_device(device_index=None) -> tuple[int, int]:
    """
    Return (device_index, samplerate) of specified device or auto-detect.
    """
    if device_index is not None and device_index != -1:  # -1 means auto
        device_info = sd.query_devices(device_index)
        print(f"Using specified device {device_index}: {device_info['name']}")
        return device_index, int(device_info['default_samplerate'])
    
    # Auto-detection
    if DEBUG_MODE:
        print("=== Audio Device Auto-Detection ===")
        devices = sd.query_devices()
        print(f"Found {len(devices)} audio devices:")
        for idx, dev in enumerate(devices):
            if dev['max_input_channels'] > 0:
                print(f"  {idx}: {dev['name']} (inputs: {dev['max_input_channels']}, rate: {dev['default_samplerate']})")
    
    return auto_detect_loopback_device()

# ────────────────────────────   THREADS   ───────────────────────────── #
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
            
            with sd.InputStream(device=self.device,
                                samplerate=self.rate,
                                channels=2,
                                dtype="float32",
                                blocksize=frames,
                                latency='low') as stream:
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
                import traceback
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
                
                # Log detected language if auto-detecting
                if self.source_lang is None and hasattr(info, 'language') and DEBUG_MODE:
                    print(f"Detected language: {info.language}")
                
                if DEBUG_MODE:
                    print(f"Transcription result: '{transcribed_text}'")
                
                if not transcribed_text:
                    if DEBUG_MODE:
                        print("Skipping empty transcription")
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
                    import traceback
                    traceback.print_exc()

# ─────────────────────────────   UI   ───────────────────────────────── #
class Overlay(QtWidgets.QWidget):
    """
    Transparent, frameless, always-on-top window that shows the last
    few translated lines at the bottom of the screen.
    Optimized for low latency and memory usage.
    """
    def __init__(self):
        super().__init__(flags=QtCore.Qt.FramelessWindowHint |
                                QtCore.Qt.WindowStaysOnTopHint |
                                QtCore.Qt.Tool)

        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        self.resize(QtWidgets.QApplication.primaryScreen().size())
        self.texts = []
        self.font_family = "Segoe UI"
        self.font_size = 16
        self.font = QtGui.QFont(self.font_family, self.font_size, QtGui.QFont.Bold)
        self._font_metrics = QtGui.QFontMetrics(self.font)  # Pre-calculate metrics
        self._last_text = None  # Cache last text to avoid unnecessary redraws
        
        # Positioning settings
        self.subtitle_y_offset = 50
        self.subtitle_x_offset = 0
        self.positioning_mode = False
        self.example_text = "Example subtitle - drag to reposition"
        self.drag_start_pos = None
        
        # Load saved position if available
        self.load_position()

    def update_font(self, font_family, font_size):
        """Update the subtitle font"""
        self.font_family = font_family
        self.font_size = font_size
        self.font = QtGui.QFont(font_family, font_size, QtGui.QFont.Bold)
        self._font_metrics = QtGui.QFontMetrics(self.font)
        self.update()

    def set_positioning_mode(self, enabled):
        """Enable/disable positioning mode with example subtitle"""
        self.positioning_mode = enabled
        if enabled:
            self.texts = [self.example_text]
        else:
            self.texts = []
            self.save_position()
        self.update()

    def save_position(self):
        """Save the current subtitle position and font settings"""
        try:
            settings = {}
            try:
                with open("babel_settings.json", "r") as f:
                    settings = json.load(f)
            except (FileNotFoundError, json.JSONDecodeError):
                pass
            
            # Update position settings
            settings["subtitle_y_offset"] = self.subtitle_y_offset
            settings["subtitle_x_offset"] = self.subtitle_x_offset
            settings["font_family"] = self.font_family
            settings["font_size"] = self.font_size
            
            # Save back to file
            with open("babel_settings.json", "w") as f:
                json.dump(settings, f, indent=2)
        except Exception as e:
            if DEBUG_MODE:
                print(f"Could not save position: {e}")

    def load_position(self):
        """Load saved subtitle position and font settings"""
        try:
            with open("babel_settings.json", "r") as f:
                settings = json.load(f)
                self.subtitle_y_offset = settings.get("subtitle_y_offset", 50)
                self.subtitle_x_offset = settings.get("subtitle_x_offset", 0)
                self.font_family = settings.get("font_family", "Segoe UI")
                self.font_size = settings.get("font_size", 16)
                # Update font with loaded settings
                self.font = QtGui.QFont(self.font_family, self.font_size, QtGui.QFont.Bold)
                self._font_metrics = QtGui.QFontMetrics(self.font)
        except (FileNotFoundError, json.JSONDecodeError, Exception):
            # Use default values if file doesn't exist or is corrupted
            self.subtitle_y_offset = 50
            self.subtitle_x_offset = 0
            self.font_family = "Segoe UI"
            self.font_size = 16

    def mousePressEvent(self, event):
        """Handle mouse press for dragging in positioning mode"""
        if self.positioning_mode and event.button() == QtCore.Qt.LeftButton:
            self.drag_start_pos = event.pos()

    def mouseMoveEvent(self, event):
        """Handle mouse drag for repositioning subtitles"""
        if (self.positioning_mode and 
            self.drag_start_pos is not None and 
            event.buttons() & QtCore.Qt.LeftButton):
            
            # Calculate new position based on mouse movement
            delta_y = event.pos().y() - self.drag_start_pos.y()
            delta_x = event.pos().x() - self.drag_start_pos.x()
            
            # Update vertical position (distance from bottom)
            new_y_offset = max(10, min(self.height() - 100, 
                                     self.subtitle_y_offset - delta_y))
            
            # Update horizontal position (offset from center)
            # Allow movement within reasonable bounds (not off-screen)
            max_x_offset = self.width() // 3
            new_x_offset = max(-max_x_offset, min(max_x_offset, 
                                                self.subtitle_x_offset + delta_x))
            
            # Only update if position actually changed
            if new_y_offset != self.subtitle_y_offset or new_x_offset != self.subtitle_x_offset:
                self.subtitle_y_offset = new_y_offset
                self.subtitle_x_offset = new_x_offset
                self.update()
                self.drag_start_pos = event.pos()

    def mouseReleaseEvent(self, event):
        """Handle mouse release"""
        if self.positioning_mode:
            self.drag_start_pos = None

    @QtCore.pyqtSlot(str)
    def push(self, line: str):
        # Don't update text in positioning mode
        if self.positioning_mode:
            return
            
        # Only update if text actually changed
        if line != self._last_text:
            self.texts.append(line)
            if len(self.texts) > 2:
                self.texts.pop(0)
            self._last_text = line
            self.update()

    @QtCore.pyqtSlot()
    def clear(self):
        """Clear all subtitle text"""
        if self.positioning_mode:
            return
            
        if self.texts:
            self.texts.clear()
            self._last_text = None
            self.update()
            if DEBUG_MODE:
                print("Overlay cleared due to silence")

    def paintEvent(self, ev):
        if not self.texts:
            return
        painter = QtGui.QPainter(self)
        painter.setRenderHint(QtGui.QPainter.Antialiasing)
        painter.setFont(self.font)

        total_h = sum(self._font_metrics.height() for _ in self.texts)
        y = self.height() - total_h - self.subtitle_y_offset

        # Modern styling colors
        if self.positioning_mode:
            # Positioning mode: subtle gray background for better positioning visibility
            outline_color = QtCore.Qt.black
            text_color = QtCore.Qt.white
            bg_color = QtGui.QColor(128, 128, 128, 120)
        else:
            # Normal mode: clean modern appearance
            outline_color = QtCore.Qt.black
            text_color = QtCore.Qt.white
            bg_color = QtGui.QColor(0, 0, 0, 140)

        for t in self.texts:
            w = self._font_metrics.boundingRect(t).width() + 40
            # Apply horizontal offset from center
            x = (self.width() - w) // 2 + self.subtitle_x_offset
            
            # Ensure subtitle doesn't go off-screen
            x = max(10, min(self.width() - w - 10, x))
            
            rect = QtCore.QRect(x, y, w, self._font_metrics.height() + 20)

            # Draw modern background with rounded corners
            painter.setPen(QtCore.Qt.NoPen)
            painter.setBrush(QtGui.QBrush(bg_color))
            painter.drawRoundedRect(rect, 12, 12)
            
            # Add subtle shadow effect for positioning mode
            if self.positioning_mode:
                shadow_rect = rect.adjusted(2, 2, 2, 2)
                shadow_color = QtGui.QColor(0, 0, 0, 60)
                painter.setBrush(QtGui.QBrush(shadow_color))
                painter.drawRoundedRect(shadow_rect, 12, 12)
                painter.setBrush(QtGui.QBrush(bg_color))
                painter.drawRoundedRect(rect, 12, 12)
            
            # Draw text with subtle outline for better readability
            painter.setPen(QtGui.QPen(outline_color, 1))
            for dx, dy in [(-1, -1), (-1, 1), (1, -1), (1, 1)]:
                outline_rect = rect.adjusted(dx, dy, dx, dy)
                painter.drawText(outline_rect, QtCore.Qt.AlignCenter, t)
            
            # Draw main text
            painter.setPen(QtGui.QPen(text_color))
            painter.drawText(rect, QtCore.Qt.AlignCenter, t)
            y += self._font_metrics.height() + 10

# Custom combo box with alphabetical navigation
class AlphabetComboBox(QtWidgets.QComboBox):
    """Custom combo box that supports alphabetical navigation"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self._last_key_time = 0
        self._search_string = ""
        self._search_timeout = 1000
    
    def keyPressEvent(self, event):
        """Handle key press events for alphabetical navigation"""
        if event.key() >= QtCore.Qt.Key_A and event.key() <= QtCore.Qt.Key_Z:
            # Get the letter pressed
            letter = event.text().upper()
            current_time = time.time() * 1000
            
            # If more than 1 second has passed, start a new search
            if current_time - self._last_key_time > self._search_timeout:
                self._search_string = letter
            else:
                self._search_string += letter
            
            self._last_key_time = current_time
            
            # Find the first item that starts with the search string
            for i in range(self.count()):
                item_text = self.itemText(i).lstrip("\u00A0")
                if item_text.upper().startswith(self._search_string):
                    self.setCurrentIndex(i)
                    break
        else:
            # For other keys, use default behavior
            super().keyPressEvent(event)

class ControlPanel(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Babel - Live Translation")
        self.setMinimumWidth(420)
        self.setMinimumHeight(620)
        self.resize(420, 620)
        
        # Set modern dark theme styling
        self.setStyleSheet("""
            QWidget {
                background-color: #1e1e1e;
                color: #ffffff;
                font-family: 'Segoe UI', Arial, sans-serif;
                font-size: 10px;
            }
            QLabel {
                color: #e0e0e0;
                font-weight: 500;
                margin: 1px 0px;
            }
            QComboBox {
                background-color: #2d2d2d;
                border: 2px solid #404040;
                border-radius: 6px;
                padding: 8px 12px 8px 20px;
                padding-right: 28px;
                color: #ffffff;
                min-height: 16px;
            }
            QComboBox:hover {
                border-color: #0078d4;
                background-color: #333333;
            }
            QComboBox:focus {
                border-color: #0078d4;
                background-color: #333333;
            }
            QComboBox::drop-down {
                subcontrol-origin: padding;
                subcontrol-position: top right;
                width: 20px;
                border: none;
                background: transparent;
            }
            QComboBox QAbstractItemView {
                background-color: #2d2d2d;
                border: 1px solid #404040;
                border-radius: 6px;
                padding: 3px;
                selection-background-color: #0078d4;
                outline: none;
                max-height: 200px;
                show-decoration-selected: 1;
            }
            QComboBox QAbstractItemView::item {
                padding: 6px 10px 6px 20px;
                border: 2px solid #404040;
                border-radius: 3px;
                margin: 3px;
                min-height: 20px;
            }
            QComboBox QAbstractItemView::item:selected {
                background-color: #0078d4;
                color: white;
            }
            QComboBox QAbstractItemView::item:hover {
                background-color: #404040;
            }
            QPushButton {
                background-color: #0078d4;
                border: none;
                border-radius: 6px;
                color: white;
                font-weight: 600;
                padding: 8px 12px;
                font-size: 11px;
            }
            QPushButton:hover {
                background-color: #106ebe;
            }
            QPushButton:pressed {
                background-color: #005a9e;
            }
            QPushButton#refresh_btn {
                background-color: #404040;
                padding: 6px 10px;
                font-size: 9px;
                min-width: 50px;
            }
            QPushButton#refresh_btn:hover {
                background-color: #505050;
            }
            QSlider::groove:horizontal {
                border: none;
                height: 6px;
                background-color: #404040;
                border-radius: 3px;
            }
            QSlider::handle:horizontal {
                background-color: #0078d4;
                border: none;
                width: 18px;
                height: 18px;
                border-radius: 9px;
                margin: -6px 0;
            }
            QSlider::handle:horizontal:hover {
                background-color: #106ebe;
            }
            QSlider::sub-page:horizontal {
                background-color: #0078d4;
                border-radius: 3px;
            }
            QCheckBox {
                spacing: 6px;
                color: #e0e0e0;
            }
            QCheckBox::indicator {
                width: 16px;
                height: 16px;
                border-radius: 3px;
                border: 2px solid #404040;
                background-color: #2d2d2d;
            }
            QCheckBox::indicator:checked {
                background-color: #0078d4;
                border-color: #0078d4;
                image: url(data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iMTIiIGhlaWdodD0iOSIgdmlld0JveD0iMCAwIDEyIDkiIGZpbGw9Im5vbmUiIHhtbG5zPSJodHRwOi8vd3d3LnczLm9yZy8yMDAwL3N2ZyI+CjxwYXRoIGQ9Ik0xIDQuNUw0LjUgOEwxMSAxIiBzdHJva2U9IndoaXRlIiBzdHJva2Utd2lkdGg9IjIiIHN0cm9rZS1saW5lY2FwPSJyb3VuZCIgc3Ryb2tlLWxpbmVqb2luPSJyb3VuZCIvPgo8L3N2Zz4K);
            }
            QCheckBox::indicator:hover {
                border-color: #0078d4;
            }
            QScrollBar:vertical {
                background-color: #2d2d2d;
                width: 12px;
                border-radius: 6px;
            }
            QScrollBar::handle:vertical {
                background-color: #404040;
                border-radius: 6px;
                min-height: 20px;
            }
            QScrollBar::handle:vertical:hover {
                background-color: #505050;
            }
            QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
                height: 0px;
            }
        """)

        # Main layout with modern spacing
        main_layout = QtWidgets.QVBoxLayout(self)
        main_layout.setSpacing(15)
        main_layout.setContentsMargins(20, 20, 20, 20)
        
        # Audio device selection section
        device_section_widget, device_section = self.create_section("Audio Input")
        
        device_layout = QtWidgets.QHBoxLayout()
        device_layout.setSpacing(8)
        
        self.device_combo = AlphabetComboBox()
        self.device_combo.setToolTip("Select audio input device or 'Auto' for automatic detection")
        self.device_combo.currentTextChanged.connect(self.save_all_settings)
        device_layout.addWidget(self.device_combo, 1)
        
        device_section.addLayout(device_layout)
        main_layout.addWidget(device_section_widget)
        
        # Language settings section
        lang_section_widget, lang_section = self.create_section("Languages")
        
        # Source language selection
        source_layout = QtWidgets.QVBoxLayout()
        source_layout.setSpacing(4)
        source_layout.addWidget(QtWidgets.QLabel("Transcribe from"))
        
        self.source_combo = AlphabetComboBox()
        # Add invisible space to each language option
        source_items = [f"\u00A0\u00A0{lang}" for lang in WHISPER_SOURCE_LANGUAGES.keys()]
        self.source_combo.addItems(source_items)
        self.source_combo.setToolTip("Language that Whisper should transcribe from")
        self.source_combo.currentTextChanged.connect(self.save_all_settings)
        source_layout.addWidget(self.source_combo)
        
        # Target language selection
        target_layout = QtWidgets.QVBoxLayout()
        target_layout.setSpacing(4)
        target_layout.addWidget(QtWidgets.QLabel("Translate to"))
        
        self.combo = AlphabetComboBox()
        # Add invisible space to each language option
        target_items = [f"\u00A0\u00A0{lang}" for lang in TARGETS.keys()]
        self.combo.addItems(target_items)
        # Set English as default (will be overridden by load_language_settings if saved)
        english_index = self.combo.findText("\u00A0\u00A0English")
        if english_index >= 0:
            self.combo.setCurrentIndex(english_index)
        self.combo.currentTextChanged.connect(self.save_all_settings)
        target_layout.addWidget(self.combo)
        
        # Create horizontal layout for both language selections
        lang_layout = QtWidgets.QHBoxLayout()
        lang_layout.addLayout(source_layout)
        lang_layout.addLayout(target_layout)
        
        lang_section.addLayout(lang_layout)
        main_layout.addWidget(lang_section_widget)
        
        # AI Model section
        model_section_widget, model_section = self.create_section("AI Model")
        
        model_layout = QtWidgets.QVBoxLayout()
        model_layout.setSpacing(4)
        model_layout.addWidget(QtWidgets.QLabel("Whisper Model"))
        
        self.model_combo = AlphabetComboBox()
        for model_name, model_desc in WHISPER_MODELS.items():
            self.model_combo.addItem(f"\u00A0\u00A0{model_name} • {model_desc}", model_name)
        # Set turbo as default by finding its index
        turbo_index = self.model_combo.findData("turbo")
        if turbo_index >= 0:
            self.model_combo.setCurrentIndex(turbo_index)
        self.model_combo.setToolTip("Choose Whisper model for transcription")
        self.model_combo.currentTextChanged.connect(self.save_all_settings)
        model_layout.addWidget(self.model_combo)
        
        model_section.addLayout(model_layout)
        main_layout.addWidget(model_section_widget)
        
        # Settings section
        settings_section_widget, settings_section = self.create_section("Settings")
        
        # Audio threshold control
        threshold_layout = QtWidgets.QVBoxLayout()
        threshold_layout.setSpacing(6)
        
        threshold_header = QtWidgets.QHBoxLayout()
        threshold_header.addWidget(QtWidgets.QLabel("Audio Sensitivity"))
        self.threshold_label = QtWidgets.QLabel(f"{DEFAULT_AUDIO_THRESHOLD:.3f}")
        self.threshold_label.setAlignment(QtCore.Qt.AlignRight)
        self.threshold_label.setStyleSheet("color: #0078d4; font-weight: 600; min-width: 60px;")
        threshold_header.addWidget(self.threshold_label)
        threshold_layout.addLayout(threshold_header)
        
        self.threshold_slider = QtWidgets.QSlider(QtCore.Qt.Horizontal)
        self.threshold_slider.setMinimum(1)    # 0.001
        self.threshold_slider.setMaximum(100)  # 0.100
        self.threshold_slider.setValue(int(DEFAULT_AUDIO_THRESHOLD * 1000))  # Convert to slider scale
        self.threshold_slider.setToolTip("Adjust audio sensitivity (lower = more sensitive)")
        self.threshold_slider.valueChanged.connect(self.update_threshold_label)
        self.threshold_slider.valueChanged.connect(self.save_all_settings)
        threshold_layout.addWidget(self.threshold_slider)
        
        settings_section.addLayout(threshold_layout)
        
        # Performance mode toggle
        self.performance_mode = QtWidgets.QCheckBox("Performance Mode")
        self.performance_mode.setChecked(False)  # Default to performance mode
        self.performance_mode.setToolTip("Optimize for speed and lower memory usage")
        self.performance_mode.stateChanged.connect(self.save_all_settings)
        settings_section.addWidget(self.performance_mode)
        
        main_layout.addWidget(settings_section_widget)
        
        # Action buttons section
        actions_section_widget, actions_section = self.create_section("Subtitle Customization")
        
        # Font settings
        font_layout = QtWidgets.QHBoxLayout()
        
        # Font family selection
        font_family_layout = QtWidgets.QVBoxLayout()
        font_family_layout.setSpacing(4)
        font_family_layout.addWidget(QtWidgets.QLabel("Font"))
        
        self.font_combo = AlphabetComboBox()
        # Add commonly available fonts
        fonts = ["Segoe UI", "Arial", "Helvetica", "Times New Roman", "Calibri", 
                "Trebuchet MS", "Verdana", "Georgia", "Comic Sans MS", "Impact"]
        # Add invisible space to each font option
        font_items = [f"\u00A0\u00A0{font}" for font in fonts]
        self.font_combo.addItems(font_items)
        self.font_combo.setCurrentText("\u00A0\u00A0Segoe UI")  # Default with space
        self.font_combo.setToolTip("Choose subtitle font family")
        self.font_combo.currentTextChanged.connect(self.update_subtitle_font)
        self.font_combo.currentTextChanged.connect(self.save_all_settings)
        font_family_layout.addWidget(self.font_combo)
        
        # Font size selection
        font_size_layout = QtWidgets.QVBoxLayout()
        font_size_layout.setSpacing(4)
        font_size_layout.addWidget(QtWidgets.QLabel("Size"))
        
        self.font_size_combo = AlphabetComboBox()
        sizes = ["10", "12", "14", "16", "18", "20", "22", "24", "28", "32", "36", "40", "48"]
        # Add invisible space to each size option
        size_items = [f"\u00A0\u00A0{size}" for size in sizes]
        self.font_size_combo.addItems(size_items)
        self.font_size_combo.setCurrentText("\u00A0\u00A016")  # Default with space
        self.font_size_combo.setToolTip("Choose subtitle font size")
        self.font_size_combo.currentTextChanged.connect(self.update_subtitle_font)
        self.font_size_combo.currentTextChanged.connect(self.save_all_settings)
        font_size_layout.addWidget(self.font_size_combo)
        
        font_layout.addLayout(font_family_layout)
        font_layout.addLayout(font_size_layout)
        actions_section.addLayout(font_layout)
        
        # Subtitle positioning button
        self.position_btn = QtWidgets.QPushButton("⚙ Reposition Subtitles")
        self.position_btn.setToolTip("Click to reposition subtitles on screen")
        self.position_btn.clicked.connect(self.toggle_positioning_mode)
        self.position_btn.setStyleSheet("""
            QPushButton {
                background-color: #0078d4;
                border: none;
                border-radius: 6px;
                color: white;
                font-weight: 600;
                padding: 8px 12px;
                font-size: 11px;
            }
            QPushButton:hover {
                background-color: #106ebe;
                transform: translateY(-1px);
            }
            QPushButton:pressed {
                background-color: #005a9e;
                transform: translateY(0px);
            }
        """)
        actions_section.addWidget(self.position_btn)
        
        main_layout.addWidget(actions_section_widget)
        
        # Add spacer to push start button to bottom
        main_layout.addStretch()
        
        # Main control button
        self.btn = QtWidgets.QPushButton("▶️ Start Translation")
        self.btn.setMinimumHeight(40)
        self.btn.setStyleSheet("""
            QPushButton {
                background-color: #0078d4;
                font-size: 12px;
                font-weight: 600;
                border-radius: 8px;
            }
            QPushButton:hover {
                background-color: #106ebe;
            }
            QPushButton:pressed {
                background-color: #005a9e;
            }
        """)
        main_layout.addWidget(self.btn)

        self.btn.clicked.connect(self.toggle)

        # Runtime fields
        self.overlay = Overlay()
        self.queue = queue.Queue()
        self.stop_evt = threading.Event()
        self.audio_th = None
        self.nlp_th = None
        
        # Initialize audio devices
        self.refresh_audio_devices()
        
        # Load saved font settings and update combo boxes
        self.load_font_settings()
        
        # Load saved language settings
        self.load_language_settings()
        
        # Load all other settings
        self.load_all_settings()
    
    def load_font_settings(self):
        """Load saved font settings and update the combo boxes"""
        try:
            with open("babel_settings.json", "r") as f:
                settings = json.load(f)
                font_family = settings.get("font_family", "Segoe UI")
                font_size = settings.get("font_size", 16)
                
                # Update combo boxes
                self.font_combo.setCurrentText(f"\u00A0\u00A0{font_family}")
                self.font_size_combo.setCurrentText(f"\u00A0\u00A0{font_size}")
        except (FileNotFoundError, json.JSONDecodeError, Exception):
            # Use defaults if file doesn't exist
            pass
    
    def load_language_settings(self):
        """Load saved language settings and update the combo boxes"""
        try:
            with open("babel_settings.json", "r") as f:
                settings = json.load(f)
                source_language = settings.get("source_language", "Auto-detect")
                target_language = settings.get("target_language", "English")
                
                # Update combo boxes
                source_index = self.source_combo.findText(f"\u00A0\u00A0{source_language}")
                if source_index >= 0:
                    self.source_combo.setCurrentIndex(source_index)
                
                target_index = self.combo.findText(f"\u00A0\u00A0{target_language}")
                if target_index >= 0:
                    self.combo.setCurrentIndex(target_index)
        except (FileNotFoundError, json.JSONDecodeError, Exception):
            # Use defaults if file doesn't exist
            pass
    
    def create_section(self, title):
        """Create a modern section widget with title"""
        section = QtWidgets.QWidget()
        section.setStyleSheet("""
            QWidget {
                background-color: #2d2d2d;
                border-radius: 10px;
                padding: 0px;
            }
        """)
        
        section_layout = QtWidgets.QVBoxLayout(section)
        section_layout.setContentsMargins(16, 8, 16, 12)
        section_layout.setSpacing(6)
        
        # Add title
        title_label = QtWidgets.QLabel(title)
        title_label.setStyleSheet("""
            QLabel {
                color: #ffffff;
                font-size: 12px;
                font-weight: 600;
                margin-bottom: 2px;
                background-color: transparent;
            }
        """)
        section_layout.addWidget(title_label)
        
        # Return both the widget and layout so we can add content to the layout
        return section, section_layout
    
    def refresh_audio_devices(self):
        """Refresh the list of available audio devices"""
        self.device_combo.clear()
        
        # Add auto-detection option
        self.device_combo.addItem("\u00A0\u00A0Auto (Recommended)", -1)
        
        try:
            devices = get_available_input_devices()
            
            # Separate devices by type for better organization
            virtual_cables = []
            system_audio = []
            regular_devices = []
            
            for device in devices:
                if device.get('is_virtual_cable', False):
                    virtual_cables.append(device)
                elif device['is_loopback']:
                    system_audio.append(device)
                else:
                    regular_devices.append(device)
            
            # Add virtual cables first (best for app-specific capture)
            if virtual_cables:
                for device in virtual_cables:
                    self.device_combo.addItem(
                        f"\u00A0\u00A0🎯 {device['name']} ({device['channels']} ch, {device['samplerate']} Hz)",
                        device['index']
                    )
            
            # Add system audio devices
            if system_audio:
                for device in system_audio:
                    self.device_combo.addItem(
                        f"\u00A0\u00A0🔊 {device['name']} ({device['channels']} ch, {device['samplerate']} Hz)",
                        device['index']
                    )
            
            # Add regular input devices
            for device in regular_devices:
                self.device_combo.addItem(
                    f"\u00A0\u00A0🎤 {device['name']} ({device['channels']} ch, {device['samplerate']} Hz)",
                    device['index']
                )
                
        except Exception as e:
            print(f"Error refreshing audio devices: {e}")
            # Add a fallback option
            self.device_combo.addItem("\u00A0\u00A0Default Device", DEVICE_INDEX or 0)
    
    def get_selected_device_index(self):
        """Get the currently selected device index"""
        return self.device_combo.currentData()
    
    def get_source_language(self):
        """Get the currently selected source language for Whisper"""
        # Remove invisible space characters when looking up the language
        selected_text = self.source_combo.currentText().lstrip("\u00A0")
        return WHISPER_SOURCE_LANGUAGES[selected_text]
    
    def update_threshold_label(self, value):
        """Update the threshold label when slider changes"""
        threshold = value / 1000.0  # Convert back from slider scale
        self.threshold_label.setText(f"{threshold:.3f}")
    
    def get_audio_threshold(self):
        """Get current audio threshold from slider"""
        return self.threshold_slider.value() / 1000.0
    
    def update_subtitle_font(self):
        """Update the overlay font when user changes font settings"""
        # Remove invisible space characters when getting font settings
        font_family = self.font_combo.currentText().lstrip("\u00A0")
        font_size = int(self.font_size_combo.currentText().lstrip("\u00A0"))
        self.overlay.update_font(font_family, font_size)
    
    def save_font_settings(self):
        """Save current font settings to babel_settings.json"""
        try:
            # Load existing settings first
            settings = {}
            try:
                with open("babel_settings.json", "r") as f:
                    settings = json.load(f)
            except (FileNotFoundError, json.JSONDecodeError):
                pass
            
            # Update font settings
            settings["font_family"] = self.font_combo.currentText().lstrip("\u00A0")
            settings["font_size"] = int(self.font_size_combo.currentText().lstrip("\u00A0"))
            
            # Save back to file
            with open("babel_settings.json", "w") as f:
                json.dump(settings, f)
        except Exception as e:
            if DEBUG_MODE:
                print(f"Could not save font settings: {e}")
    
    def save_language_settings(self):
        """Save current language settings to babel_settings.json"""
        try:
            # Load existing settings first
            settings = {}
            try:
                with open("babel_settings.json", "r") as f:
                    settings = json.load(f)
            except (FileNotFoundError, json.JSONDecodeError):
                pass
            
            # Update language settings
            settings["source_language"] = self.source_combo.currentText().lstrip("\u00A0")
            settings["target_language"] = self.combo.currentText().lstrip("\u00A0")
            
            # Save back to file
            with open("babel_settings.json", "w") as f:
                json.dump(settings, f)
        except Exception as e:
            if DEBUG_MODE:
                print(f"Could not save language settings: {e}")
    
    def save_all_settings(self):
        """Save all current settings to babel_settings.json"""
        try:
            # Load existing settings first
            settings = {}
            try:
                with open("babel_settings.json", "r") as f:
                    settings = json.load(f)
            except (FileNotFoundError, json.JSONDecodeError):
                pass
            
            # Update all settings
            settings["font_family"] = self.font_combo.currentText().lstrip("\u00A0")
            settings["font_size"] = int(self.font_size_combo.currentText().lstrip("\u00A0"))
            settings["source_language"] = self.source_combo.currentText().lstrip("\u00A0")
            settings["target_language"] = self.combo.currentText().lstrip("\u00A0")
            settings["audio_device"] = self.device_combo.currentText().lstrip("\u00A0")
            settings["audio_device_data"] = self.device_combo.currentData()
            settings["whisper_model"] = self.model_combo.currentData()
            settings["audio_threshold"] = self.threshold_slider.value() / 1000.0
            settings["performance_mode"] = self.performance_mode.isChecked()
            
            # Save back to file
            with open("babel_settings.json", "w") as f:
                json.dump(settings, f, indent=2)
        except Exception as e:
            if DEBUG_MODE:
                print(f"Could not save settings: {e}")
    
    def load_all_settings(self):
        """Load all saved settings and update the controls"""
        try:
            with open("babel_settings.json", "r") as f:
                settings = json.load(f)
                
                # Load audio device setting
                saved_device = settings.get("audio_device", "Auto (Recommended)")
                device_index = self.device_combo.findText(f"\u00A0\u00A0{saved_device}")
                if device_index >= 0:
                    self.device_combo.setCurrentIndex(device_index)
                
                # Load whisper model setting
                saved_model = settings.get("whisper_model", "turbo")
                model_index = self.model_combo.findData(saved_model)
                if model_index >= 0:
                    self.model_combo.setCurrentIndex(model_index)
                
                # Load audio threshold setting
                saved_threshold = settings.get("audio_threshold", DEFAULT_AUDIO_THRESHOLD)
                self.threshold_slider.setValue(int(saved_threshold * 1000))
                self.update_threshold_label(int(saved_threshold * 1000))
                
                # Load performance mode setting
                saved_performance_mode = settings.get("performance_mode", False)
                self.performance_mode.setChecked(saved_performance_mode)
                
        except (FileNotFoundError, json.JSONDecodeError, Exception):
            # Use defaults if file doesn't exist or has errors
            pass
    
    def get_selected_model(self):
        """Get the currently selected Whisper model"""
        return self.model_combo.currentData()
    
    def is_performance_mode(self):
        """Check if performance mode is enabled"""
        return self.performance_mode.isChecked()
    
    def toggle_positioning_mode(self):
        """Toggle subtitle positioning mode"""
        if not hasattr(self, '_positioning_active'):
            self._positioning_active = False
            
        self._positioning_active = not self._positioning_active
        
        if self._positioning_active:
            # Show example subtitle for positioning
            self.overlay.set_positioning_mode(True)
            self.overlay.showFullScreen()
            self.position_btn.setText("✓ Done Positioning")
            self.position_btn.setStyleSheet("""
                QPushButton {
                    background-color: #059669;
                    border: none;
                    border-radius: 6px;
                    color: white;
                    font-weight: 600;
                    padding: 8px 12px;
                    font-size: 11px;
                }
                QPushButton:hover {
                    background-color: #047857;
                }
                QPushButton:pressed {
                    background-color: #065F46;
                }
            """)
            
            # Show instructions
            msg = QtWidgets.QMessageBox()
            msg.setWindowTitle("Subtitle Positioning")
            msg.setText("Drag the gray example subtitle to your preferred position.\n" +
                       "You can move it both horizontally and vertically.\n" +
                       "Click 'Done Positioning' when finished.")
            msg.setIcon(QtWidgets.QMessageBox.Information)
            msg.setStyleSheet("""
                QMessageBox {
                    background-color: #2d2d2d;
                    color: #ffffff;
                }
                QMessageBox QPushButton {
                    background-color: #0078d4;
                    color: white;
                    border: none;
                    border-radius: 6px;
                    padding: 8px 16px;
                    min-width: 80px;
                }
                QMessageBox QPushButton:hover {
                    background-color: #106ebe;
                }
            """)
            msg.exec_()
        else:
            # Exit positioning mode
            self.overlay.set_positioning_mode(False)
            self.overlay.hide()
            self.position_btn.setText("⚙ Reposition Subtitles")
            self.position_btn.setStyleSheet("""
                QPushButton {
                    background-color: #0078d4;
                    border: none;
                    border-radius: 6px;
                    color: white;
                    font-weight: 600;
                    padding: 8px 12px;
                    font-size: 11px;
                }
                QPushButton:hover {
                    background-color: #106ebe;
                    transform: translateY(-1px);
                }
                QPushButton:pressed {
                    background-color: #005a9e;
                    transform: translateY(0px);
                }
            """)

    def toggle(self):
        if self.audio_th and self.audio_th.is_alive():
            self.stop()
        else:
            self.start()

    def start(self):
        self.stop_evt.clear()
        # Remove invisible space characters when getting language code
        lang_code = TARGETS[self.combo.currentText().lstrip("\u00A0")]
        audio_threshold = self.get_audio_threshold()
        device_index = self.get_selected_device_index()
        source_lang = self.get_source_language()
        model_name = self.get_selected_model()
        
        # Set global debug mode based on performance setting
        global DEBUG_MODE
        DEBUG_MODE = not self.is_performance_mode()

        # Spawn audio + NLP threads
        self.audio_th = AudioWorker(self.queue, self.stop_evt, device_index)
        self.nlp_th = NLPWorker(self.queue, self.stop_evt, lang_code, source_lang, audio_threshold, model_name)
        self.nlp_th.new_line.connect(self.overlay.push)
        self.nlp_th.clear_overlay.connect(self.overlay.clear)

        self.audio_th.start()
        self.nlp_th.start()
        self.overlay.showFullScreen()
        self.btn.setText("⏸ Stop Translation")
        self.btn.setStyleSheet("""
            QPushButton {
                background-color: #d13438;
                font-size: 12px;
                font-weight: 600;
                border-radius: 8px;
            }
            QPushButton:hover {
                background-color: #b02e32;
            }
            QPushButton:pressed {
                background-color: #9c282c;
            }
        """)

    def stop(self):
        self.stop_evt.set()
        if self.nlp_th:
            self.nlp_th.join()
        if self.audio_th:
            self.audio_th.join()
        self.overlay.hide()
        self.btn.setText("▶ Start Translation")
        self.btn.setStyleSheet("""
            QPushButton {
                background-color: #0078d4;
                font-size: 12px;
                font-weight: 600;
                border-radius: 8px;
            }
            QPushButton:hover {
                background-color: #106ebe;
            }
            QPushButton:pressed {
                background-color: #005a9e;
            }
        """)
        
        # Clear queue to free memory
        while not self.queue.empty():
            try:
                self.queue.get_nowait()
            except queue.Empty:
                break
        
        # Force garbage collection to free memory
        gc.collect()

# ─────────────────────────── entry-point ───────────────────────────── #
if __name__ == "__main__":
    # HiDPI tweak for Windows
    if platform.system() == "Windows":
        try:
            ctypes.windll.shcore.SetProcessDpiAwareness(1)
        except:
            pass

    app = QtWidgets.QApplication(sys.argv)
    panel = ControlPanel()
    panel.show()
    
    print("🎯 Babel Audio Translator - Modern Edition")
    print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
    print("✨ Features:")
    print("  • Sleek modern interface with dark theme")
    print("  • Smart audio device auto-detection")
    print("  • Multi-language transcription & translation")
    print("  • Optimized Whisper models for speed vs accuracy")
    print("  • Adjustable audio sensitivity controls")
    print("  • Drag-and-drop subtitle positioning")
    print("  • Performance mode for low CPU/memory usage")
    print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
    print("🚀 Ready to translate!")
    print("")
    
    sys.exit(app.exec_())
