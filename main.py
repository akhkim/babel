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
import warnings
# Suppress the ctranslate2 deprecation warning
warnings.filterwarnings("ignore", message=".*pkg_resources is deprecated.*")

import sys, queue, threading, platform, ctypes, time, gc, json, traceback
from pathlib import Path

import numpy as np
import sounddevice as sd
from faster_whisper import WhisperModel
from googletrans import Translator
from scipy import signal

from PyQt5 import QtCore, QtGui, QtWidgets
import torch

# ──────────────────────────── AUDIO CONFIGURATION ───────────────────── #
# Configure WASAPI for shared mode to fix audio capture during calls/meetings
WASAPI_HOST_API = None
WASAPI_SETTINGS = None

if platform.system() == "Windows":
    try:
        # Find WASAPI host API
        for i, api in enumerate(sd.query_hostapis()):
            if 'wasapi' in api['name'].lower():
                WASAPI_HOST_API = i
                break
        
        if WASAPI_HOST_API is not None:
            # Create shared mode settings
            WASAPI_SETTINGS = sd.WasapiSettings(exclusive=False)
            print(f"✅ WASAPI shared mode configured (Host API: {WASAPI_HOST_API}) - audio capture will work during calls")
        else:
            print("⚠️  WASAPI host API not found - using default audio settings")
    except Exception as e:
        print(f"⚠️  Could not configure WASAPI shared mode: {e}")
        print("   Audio capture may not work during calls or when other apps use audio")

# ──────────────────────────── USER SETTINGS ─────────────────────────── #
DEVICE_INDEX = None    # Will be auto-detected at startup
SAMPLE_RATE  = 48_000
CHUNK_SECONDS           = 3     # Reduced from 4 to 2 for lower latency
MODEL_NAME              = "turbo"    # Use turbo model by default
DEBUG_MODE              = False     # Disable debug output for performance
DEFAULT_AUDIO_THRESHOLD = 0.001     # Increased threshold to reduce processing
MAX_QUEUE_SIZE          = 3         # Limit queue size to reduce memory usage

# Available Whisper models (used as keys for translation lookup)
WHISPER_MODEL_KEYS = ["tiny", "turbo", "large-v3", "distil-large-v3"]

# Global UI language and translation system
CURRENT_UI_LANGUAGE = "English"
TRANSLATIONS = {}

def load_translations():
    """Load translation files from the translations directory"""
    global TRANSLATIONS
    translation_dir = Path(__file__).parent / "translations"
    
    # Language code mappings
    language_files = {
        "English": "en.json",
        "Spanish": "es.json", 
        "French": "fr.json",
        "German": "de.json",
        "Portuguese": "pt.json",
        "Korean": "ko.json"
    }
    
    for language, filename in language_files.items():
        try:
            file_path = translation_dir / filename
            if file_path.exists():
                with open(file_path, 'r', encoding='utf-8') as f:
                    TRANSLATIONS[language] = json.load(f)
            else:
                print(f"Warning: Translation file {filename} not found")
        except Exception as e:
            print(f"Error loading translation {filename}: {e}")
    
    # Fallback to English if no translations loaded
    if not TRANSLATIONS:
        TRANSLATIONS["English"] = {
            "ui": {"app_name": "Babel", "app_subtitle": "Live Translation"},
            "whisper_models": {
                "tiny": "Fast but basic accuracy",
                "turbo": "Balanced speed/accuracy", 
                "large-v3": "High accuracy but slower",
                "distil-large-v3": "Optimized large model"
            },
            "audio_devices": {}
        }

def get_ui_text(key, category="ui"):
    """Get translated text for the current language"""
    if not TRANSLATIONS:
        load_translations()
    
    current_lang = TRANSLATIONS.get(CURRENT_UI_LANGUAGE)
    if not current_lang:
        current_lang = TRANSLATIONS.get("English", {})
    
    return current_lang.get(category, {}).get(key, key)

def get_whisper_model_description(model_key):
    """Get translated Whisper model description"""
    return get_ui_text(model_key, "whisper_models")

def get_available_ui_languages():
    """Get list of available UI languages"""
    if not TRANSLATIONS:
        load_translations()
    return list(TRANSLATIONS.keys())

def get_native_language_names():
    """Get UI languages displayed in their native language names"""
    native_names = {
        "English": "English",
        "Spanish": "Español", 
        "French": "Français",
        "German": "Deutsch",
        "Portuguese": "Português",
        "Korean": "한국어"
    }
    
    available_languages = get_available_ui_languages()
    return [(native_names.get(lang, lang), lang) for lang in available_languages]

def get_language_by_native_name(native_name):
    """Get the internal language key by its native display name"""
    native_to_internal = {
        "English": "English",
        "Español": "Spanish", 
        "Français": "French",
        "Deutsch": "German",
        "Português": "Portuguese",
        "한국어": "Korean"
    }
    return native_to_internal.get(native_name, native_name)

def translate_language_name(language_name):
    """Translate specific language names that need localization"""
    # Use hardcoded translations to avoid recursion
    translated_name = get_ui_text(language_name, "language_names")
    # If not found in language_names, return original
    if translated_name == language_name:
        # Try the old auto-detect fallback
        if language_name == "Auto-detect":
            return get_ui_text("auto_detect")
        return language_name
    return translated_name

def translate_whisper_model_display(model_name, model_desc):
    """Create translated display text for Whisper model dropdown"""
    return f"{model_name} • {model_desc}"

def get_translated_whisper_models():
    """Get Whisper models with translated descriptions"""
    translated_models = []
    for model_name in WHISPER_MODEL_KEYS:
        model_desc = get_whisper_model_description(model_name)
        display_text = translate_whisper_model_display(model_name, model_desc)
        translated_models.append((display_text, model_name))
    return translated_models

def get_translated_source_languages():
    """Get source languages with translated names where appropriate"""
    translated_langs = []
    for lang in WHISPER_SOURCE_LANGUAGES.keys():
        translated_langs.append(translate_language_name(lang))
    return translated_langs

def get_translated_target_languages():
    """Get target languages with translated names where appropriate"""
    translated_langs = []
    for lang in TARGETS.keys():
        translated_langs.append(translate_language_name(lang))
    return translated_langs

def get_original_language_name(translated_name):
    """Convert translated language name back to original English name"""
    # Handle auto-detect special case
    if translated_name == get_ui_text("auto_detect"):
        return "Auto-detect"
    
    # Search through language_names to find original
    if TRANSLATIONS and CURRENT_UI_LANGUAGE in TRANSLATIONS:
        language_names = TRANSLATIONS[CURRENT_UI_LANGUAGE].get("language_names", {})
        for original, translated in language_names.items():
            if translated == translated_name:
                return original
    
    # Fallback - return as is if not found
    return translated_name

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
    "Azerbaijani": "az",
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

# Translation system (loaded when application starts)

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
                                      for keyword in ['cable', 'vac', 'virtual']),
                'is_wasapi': (WASAPI_HOST_API is not None and device['hostapi'] == WASAPI_HOST_API)
            })
    
    return input_devices

def auto_detect_loopback_device():
    """Auto-detect the best loopback device, preferring WASAPI devices for call compatibility"""
    devices = get_available_input_devices()
    
    # First priority: Stereo Mix with 2ch 48000Hz (ideal configuration)
    # Prefer WASAPI version if available
    ideal_devices = [d for d in devices if (d['is_loopback'] and 
                                          d['channels'] == 2 and 
                                          d['samplerate'] == 48000 and
                                          'stereo mix' in d['name'].lower())]
    if ideal_devices:
        # Prefer WASAPI device if available
        wasapi_ideal = [d for d in ideal_devices if d.get('is_wasapi', False)]
        if wasapi_ideal:
            device = wasapi_ideal[0]
            print(f"Found ideal WASAPI Stereo Mix device: {device['name']}")
            return device['index'], device['samplerate']
        else:
            device = ideal_devices[0]
            print(f"Found ideal Stereo Mix device: {device['name']}")
            return device['index'], device['samplerate']
    
    # Second priority: Virtual Audio Cables (best for app-specific capture)
    virtual_devices = [d for d in devices if d.get('is_virtual_cable', False)]
    if virtual_devices:
        # Prefer WASAPI version if available
        wasapi_virtual = [d for d in virtual_devices if d.get('is_wasapi', False)]
        if wasapi_virtual:
            device = wasapi_virtual[0]
            print(f"Found WASAPI Virtual Audio Cable: {device['name']}")
            return device['index'], device['samplerate']
        else:
            device = virtual_devices[0]
            print(f"Found Virtual Audio Cable: {device['name']}")
            return device['index'], device['samplerate']
    
    # Third priority: Any Stereo Mix device
    stereo_devices = [d for d in devices if (d['is_loopback'] and 'stereo mix' in d['name'].lower())]
    if stereo_devices:
        # Prefer WASAPI version if available
        wasapi_stereo = [d for d in stereo_devices if d.get('is_wasapi', False)]
        if wasapi_stereo:
            device = wasapi_stereo[0]
            print(f"Found WASAPI Stereo Mix device: {device['name']}")
            return device['index'], device['samplerate']
        else:
            device = stereo_devices[0]
            print(f"Found Stereo Mix device: {device['name']}")
            return device['index'], device['samplerate']
    
    # Fourth priority: Other loopback devices
    loopback_devices = [d for d in devices if d['is_loopback']]
    if loopback_devices:
        # Prefer WASAPI version if available
        wasapi_loopback = [d for d in loopback_devices if d.get('is_wasapi', False)]
        if wasapi_loopback:
            device = wasapi_loopback[0]
            print(f"Found WASAPI loopback device: {device['name']}")
            return device['index'], device['samplerate']
        else:
            device = loopback_devices[0]
            print(f"Found other loopback device: {device['name']}")
            return device['index'], device['samplerate']
    
    # Last resort: use any input device with 2+ channels
    fallback_devices = [d for d in devices if d['channels'] >= 2]
    if fallback_devices:
        # Prefer WASAPI version if available
        wasapi_fallback = [d for d in fallback_devices if d.get('is_wasapi', False)]
        if wasapi_fallback:
            device = wasapi_fallback[0]
            print(f"Using WASAPI fallback input device: {device['name']}")
            return device['index'], device['samplerate']
        else:
            device = fallback_devices[0]
            print(f"Using fallback input device: {device['name']}")
            return device['index'], device['samplerate']
    
    raise RuntimeError("No suitable audio input device found!")

def initialize_audio_device():
    """Initialize the global DEVICE_INDEX with the best available audio device"""
    global DEVICE_INDEX, SAMPLE_RATE
    
    try:
        print("=== Initializing Audio Device ===")
        
        # Show available devices in debug mode
        if DEBUG_MODE:
            devices = get_available_input_devices()
            print(f"Found {len(devices)} input devices:")
            for device in devices:
                device_type = []
                if device.get('is_loopback'):
                    device_type.append("Loopback")
                if device.get('is_virtual_cable'):
                    device_type.append("Virtual Cable")
                if not device_type:
                    device_type.append("Standard Input")
                
                type_str = " + ".join(device_type)
                print(f"  {device['index']:2d}: {device['name']} ({type_str}, {device['channels']}ch, {device['samplerate']}Hz)")
            print()
        
        best_device_index, best_sample_rate = auto_detect_loopback_device()
        
        # Update global settings
        DEVICE_INDEX = best_device_index
        SAMPLE_RATE = best_sample_rate
        
        # Get device info for reporting
        device_info = sd.query_devices(best_device_index)
        device_name = device_info['name']
        
        print(f"✅ Selected audio device: {device_name} (Index: {best_device_index}, Rate: {best_sample_rate}Hz)")
        return True
        
    except Exception as e:
        print(f"❌ Failed to initialize audio device: {e}")
        print("Using default fallback settings...")
        DEVICE_INDEX = None
        return False

# ──────────────────────────── LOOP-BACK DISCOVERY ───────────────────── #
def get_loopback_device(device_index=None) -> tuple[int, int]:
    """
    Return (device_index, samplerate) of specified device or auto-detect.
    """
    if device_index is not None and device_index != -1:
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
        self.font_family = "Inter"
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
                self.font_family = settings.get("font_family", "Inter")
                self.font_size = settings.get("font_size", 16)
                # Update font with loaded settings
                self.font = QtGui.QFont(self.font_family, self.font_size, QtGui.QFont.Bold)
                self._font_metrics = QtGui.QFontMetrics(self.font)
        except (FileNotFoundError, json.JSONDecodeError, Exception):
            # Use default values if file doesn't exist or is corrupted
            self.subtitle_y_offset = 50
            self.subtitle_x_offset = 0
            self.font_family = "Inter"
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
            painter.drawRoundedRect(rect, 8, 8)
            
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
                item_text = self.itemText(i)
                if item_text.upper().startswith(self._search_string):
                    self.setCurrentIndex(i)
                    break
        else:
            # For other keys, use default behavior
            super().keyPressEvent(event)

class FontItemDelegate(QtWidgets.QStyledItemDelegate):
    """Custom delegate to display font names in their respective fonts"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.default_font = QtGui.QFont("Segoe UI", 8)
    
    def paint(self, painter, option, index):
        """Custom paint method to render each font name in its own font"""
        # Get the font name from the model
        font_name = index.data(QtCore.Qt.DisplayRole)
        
        # Create a font object with the font family
        font = QtGui.QFont(font_name, 8)
        font.setStyleHint(QtGui.QFont.AnyStyle)
        
        # Set up the painter
        painter.save()
        
        # Draw background
        if option.state & QtWidgets.QStyle.State_Selected:
            painter.fillRect(option.rect, QtGui.QColor(88, 101, 242))  # #5865f2
            painter.setPen(QtGui.QColor(255, 255, 255))  # White text
        else:
            if option.state & QtWidgets.QStyle.State_MouseOver:
                hover_color = QtGui.QColor(64, 66, 73)  # #404249
                painter.fillRect(option.rect, hover_color)
            painter.setPen(QtGui.QColor(255, 255, 255))  # White text
        
        # Set the font and draw the text
        painter.setFont(font)
        text_rect = option.rect.adjusted(4, 0, -4, 0)  # Reduced padding to match other dropdowns
        painter.drawText(text_rect, QtCore.Qt.AlignLeft | QtCore.Qt.AlignVCenter, font_name)
        
        painter.restore()
    
    def sizeHint(self, option, index):
        """Return the size hint for the item"""
        return QtCore.QSize(200, 24)  # Match the exact dropdown item height from CSS

class ControlPanel(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle(f"{get_ui_text('app_name')} - {get_ui_text('app_subtitle')}")
        self.setMinimumWidth(900)
        self.setMinimumHeight(680)
        self.resize(900, 702)
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground, True)
        
        # Set ultra-modern slick styling with enhanced visual effects
        self.setStyleSheet("""
            /* Main window background with gradient and shadow effect */
            QWidget#mainWindow {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1, 
                    stop:0 #0f1116, stop:0.3 #1a1d23, stop:0.7 #1a1d23, stop:1 #0f1116);
                border: 2px solid qlineargradient(x1:0, y1:0, x2:1, y2:1, 
                    stop:0 #4c5ce8, stop:0.5 #5865f2, stop:1 #7289da);
                border-radius: 24px;
            }
            
            /* Sidebar styling with enhanced depth */
            QWidget#sidebar {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0, 
                    stop:0 #0a0c0f, stop:0.8 #141619, stop:1 #1a1d23);
                border-radius: 24px 0px 0px 24px;
                border-right: 2px solid qlineargradient(x1:0, y1:0, x2:0, y2:1, 
                    stop:0 #4c5ce8, stop:0.5 #5865f2, stop:1 #7289da);
            }
            
            /* Content area styling with subtle gradient */
            QWidget#contentArea {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1, 
                    stop:0 #1a1d23, stop:0.5 #22252a, stop:1 #1a1d23);
                border-radius: 0px 24px 24px 0px;
            }
            
            /* Header bar styling with glassmorphism effect */
            QWidget#headerBar {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1, 
                    stop:0 rgba(91, 101, 242, 0.12), 
                    stop:0.5 rgba(34, 37, 43, 0.9), 
                    stop:1 rgba(91, 101, 242, 0.08));
                border-radius: 0px 20px 0px 0px;
                border-bottom: 1px solid rgba(91, 101, 242, 0.25);
                min-height: 90px;
                max-height: 90px;
            }
            
            /* Enhanced title labels with better typography */
            QLabel#titleLabel {
                color: #ffffff;
                font-size: 18px;
                font-weight: 700;
                background: transparent;
                padding: 0px;
                margin: 0px;
            }
            
            QLabel#subtitleLabel {
                color: #c9cccf;
                font-size: 13px;
                background: transparent;
                padding: 0px;
                margin: 0px;
                font-weight: 400;
            }
            
            /* Enhanced section card styling with depth and glow */
            QWidget#sectionCard {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1, 
                    stop:0 rgba(91, 101, 242, 0.10), 
                    stop:0.2 rgba(34, 37, 43, 0.98), 
                    stop:0.8 rgba(34, 37, 43, 0.98),
                    stop:1 rgba(91, 101, 242, 0.06));
                border: 2px solid rgba(91, 101, 242, 0.2);
                border-radius: 16px;
                margin: 4px 2px;
                padding: 2px;
            }
            
            QWidget#sectionCard:hover {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1, 
                    stop:0 rgba(91, 101, 242, 0.15), 
                    stop:0.2 rgba(34, 37, 43, 1.0), 
                    stop:0.8 rgba(34, 37, 43, 1.0),
                    stop:1 rgba(91, 101, 242, 0.10));
                border: 2px solid rgba(91, 101, 242, 0.35);
            }
            
            /* Enhanced sidebar menu buttons with modern animations */
            QPushButton#menuBtn {
                background: transparent;
                border: none;
                color: #d1d4d8;
                font-size: 14px;
                font-weight: 600;
                padding: 16px 20px;
                text-align: left;
                border-radius: 10px;
                margin: 2px 8px;
                min-height: 18px;
            }
            
            QPushButton#menuBtn:hover {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0, 
                    stop:0 rgba(91, 101, 242, 0.15), 
                    stop:1 rgba(91, 101, 242, 0.08));
                color: #ffffff;
                border: 1px solid rgba(91, 101, 242, 0.3);
            }
            
            QPushButton#menuBtn:pressed {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0, 
                    stop:0 rgba(91, 101, 242, 0.25), 
                    stop:1 rgba(91, 101, 242, 0.15));
                color: #ffffff;
                border: 1px solid rgba(91, 101, 242, 0.5);
            }
            
            QPushButton#menuBtn[selected="true"] {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0, 
                    stop:0 #5b65f2, stop:1 #7289da);
                color: #ffffff;
                border: 1px solid rgba(255, 255, 255, 0.1);
                font-weight: 700;
            }
            
            /* Enhanced window control buttons with better hover effects */
            QPushButton#windowBtn {
                background: transparent;
                border: none;
                color: #c9cccf;
                font-size: 14px;
                font-weight: 600;
                padding: 6px;
                border-radius: 6px;
                min-width: 28px;
                max-width: 28px;
                min-height: 28px;
                max-height: 28px;
                margin: 2px;
            }
            
            QPushButton#windowBtn:hover {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1, 
                    stop:0 rgba(91, 101, 242, 0.2), 
                    stop:1 rgba(91, 101, 242, 0.1));
                color: #ffffff;
                border: 1px solid rgba(91, 101, 242, 0.3);
            }
            
            QPushButton#windowBtn:pressed {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1, 
                    stop:0 rgba(91, 101, 242, 0.3), 
                    stop:1 rgba(91, 101, 242, 0.2));
                color: #ffffff;
                border: 1px solid rgba(91, 101, 242, 0.5);
            }
            
            QPushButton#windowBtn:focus {
                outline: none;
            }
            
            QPushButton#closeBtn {
                background: transparent;
                border: none;
                color: #c9cccf;
                font-size: 14px;
                font-weight: 600;
                padding: 6px;
                border-radius: 6px;
                min-width: 28px;
                max-width: 28px;
                min-height: 28px;
                max-height: 28px;
                margin: 2px;
            }
            
            QPushButton#closeBtn:hover {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1, 
                    stop:0 #ff4757, stop:1 #ed4245);
                color: #ffffff;
                border: 1px solid rgba(255, 255, 255, 0.2);
            }
            
            QPushButton#closeBtn:pressed {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1, 
                    stop:0 #ed4245, stop:1 #dc3545);
                color: #ffffff;
                border: 1px solid rgba(255, 255, 255, 0.3);
            }
            
            QPushButton#closeBtn:focus {
                outline: none;
            }
            
            /* Enhanced default widget styling */
            QWidget {
                background-color: transparent;
                color: #ffffff;
                font-family: 'Inter', 'Segoe UI', 'Roboto', 'Arial', sans-serif;
                font-size: 12px;
                font-weight: 500;
            }
            
            /* Enhanced section labels with better typography */
            QLabel {
                color: #ffffff;
                font-weight: 600;
                margin: 3px 0px;
                background: transparent;
            }
            
            QLabel#sectionTitle {
                color: rgba(255, 255, 255, 0.95);
                font-size: 15px;
                font-weight: bold;
                font-family: 'Inter', 'Segoe UI', 'Roboto', sans-serif;
                padding: 8px 0px 4px 0px;
                margin-bottom: 6px;
                border-bottom: 2px solid rgba(91, 101, 242, 0.3);
                background: transparent;
            }
            
            /* Ultra-modern ComboBox styling with enhanced effects */
            QComboBox {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1, 
                    stop:0 rgba(44, 47, 54, 0.9), 
                    stop:1 rgba(34, 37, 43, 0.95));
                border: 2px solid rgba(91, 101, 242, 0.18);
                border-radius: 8px;
                padding: 10px 14px;
                color: #ffffff;
                min-height: 18px;
                font-size: 12px;
                font-weight: 600;
                selection-background-color: rgba(91, 101, 242, 0.3);
            }
            
            QComboBox:hover {
                border-color: rgba(91, 101, 242, 0.4);
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1, 
                    stop:0 rgba(44, 47, 54, 0.95), 
                    stop:1 rgba(34, 37, 43, 1.0));
            }
            
            QComboBox:focus {
                border-color: #5b65f2;
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1, 
                    stop:0 rgba(44, 47, 54, 1.0), 
                    stop:1 rgba(34, 37, 43, 1.0));
                outline: none;
            }
            
            QComboBox::drop-down {
                subcontrol-origin: padding;
                subcontrol-position: top right;
                width: 24px;
                border: none;
                background: transparent;
            }
            
            QComboBox::down-arrow {
                image: none;
                border-style: solid;
                border-width: 5px 4px 0px 4px;
                border-color: #c9cccf transparent transparent transparent;
            }
            
            QComboBox::down-arrow:hover {
                border-color: #5b65f2 transparent transparent transparent;
            }
            
            QComboBox QAbstractItemView {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1, 
                    stop:0 #1e2025, stop:1 #252831);
                border: 2px solid rgba(91, 101, 242, 0.25);
                border-radius: 8px;
                padding: 6px;
                selection-background-color: rgba(91, 101, 242, 0.4);
                outline: none;
            }
            
            QComboBox QAbstractItemView::item {
                padding: 8px 12px;
                border: none;
                border-radius: 6px;
                margin: 1px;
                min-height: 28px;
                color: #ffffff;
                font-size: 12px;
                font-weight: 500;
            }
            
            QComboBox QAbstractItemView::item:selected {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0, 
                    stop:0 #5b65f2, stop:1 #7289da);
                color: #ffffff;
                font-weight: 600;
            }
            
            QComboBox QAbstractItemView::item:hover {
                background: rgba(91, 101, 242, 0.2);
                color: #ffffff;
                border: 1px solid rgba(91, 101, 242, 0.3);
            }
            
            /* Ultra-modern button styling with enhanced gradients */
            QPushButton {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1, 
                    stop:0 #5b65f2, stop:0.5 #4c5ce8, stop:1 #3c4ae0);
                border: none;
                border-radius: 8px;
                color: #ffffff;
                font-weight: 700;
                padding: 12px 18px;
                font-size: 12px;
                min-height: 14px;
            }
            
            QPushButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1, 
                    stop:0 #6875f3, stop:0.5 #5865f2, stop:1 #4c5ce8);
                border: 1px solid rgba(255, 255, 255, 0.1);
            }
            
            QPushButton:pressed {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1, 
                    stop:0 #3c4ae0, stop:0.5 #2f3694, stop:1 #1e2875);
            }
            
            /* Enhanced slider styling with modern aesthetics */
            QSlider::groove:horizontal {
                border: none;
                height: 6px;
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0, 
                    stop:0 #2a2d32, stop:1 #34373c);
                border-radius: 3px;
            }
            
            QSlider::handle:horizontal {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1, 
                    stop:0 #6875f3, stop:1 #5b65f2);
                border: 2px solid rgba(255, 255, 255, 0.2);
                width: 20px;
                height: 20px;
                border-radius: 12px;
                margin: -8px 0;
            }
            
            QSlider::handle:horizontal:hover {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1, 
                    stop:0 #7985f4, stop:1 #6875f3);
                border: 2px solid rgba(255, 255, 255, 0.3);
            }
            
            QSlider::sub-page:horizontal {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0, 
                    stop:0 #5b65f2, stop:1 #7289da);
                border-radius: 3px;
            }
            
            /* Enhanced checkbox styling with modern animations */
            QCheckBox {
                spacing: 8px;
                color: #ffffff;
                font-weight: 600;
                font-size: 12px;
            }
            
            QCheckBox::indicator {
                width: 20px;
                height: 20px;
                border-radius: 6px;
                border: 2px solid rgba(91, 101, 242, 0.25);
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1, 
                    stop:0 rgba(44, 47, 54, 0.8), 
                    stop:1 rgba(34, 37, 43, 0.9));
            }
            
            QCheckBox::indicator:checked {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1, 
                    stop:0 #6875f3, stop:1 #5b65f2);
                border: 2px solid rgba(255, 255, 255, 0.2);
                image: url(data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iMTQiIGhlaWdodD0iMTEiIHZpZXdCb3g9IjAgMCAxNCAxMSIgZmlsbD0ibm9uZSIgeG1sbnM9Imh0dHA6Ly93d3cudzMub3JnLzIwMDAvc3ZnIj4KPHBhdGggZD0iTTEuNSA1LjVMNS41IDkuNUwxMi41IDEuNSIgc3Ryb2tlPSJ3aGl0ZSIgc3Ryb2tlLXdpZHRoPSIyLjUiIHN0cm9rZS1saW5lY2FwPSJyb3VuZCIgc3Ryb2tlLWxpbmVqb2luPSJyb3VuZCIvPgo8L3N2Zz4K);
            }
            
            QCheckBox::indicator:hover {
                border-color: rgba(91, 101, 242, 0.5);
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1, 
                    stop:0 rgba(44, 47, 54, 0.9), 
                    stop:1 rgba(34, 37, 43, 1.0));
            }
            
            QCheckBox::indicator:checked:hover {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1, 
                    stop:0 #7985f4, stop:1 #6875f3);
                border: 2px solid rgba(255, 255, 255, 0.3);
            }
            
            /* Enhanced scrollbar styling with modern aesthetics */
            QScrollBar:vertical {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0, 
                    stop:0 #1e2025, stop:1 #252831);
                width: 14px;
                border-radius: 7px;
                margin: 0;
                border: 1px solid rgba(91, 101, 242, 0.08);
            }
            
            QScrollBar::handle:vertical {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0, 
                    stop:0 rgba(91, 101, 242, 0.4), 
                    stop:1 rgba(91, 101, 242, 0.6));
                border-radius: 6px;
                min-height: 24px;
                margin: 2px;
                border: 1px solid rgba(255, 255, 255, 0.1);
            }
            
            QScrollBar::handle:vertical:hover {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0, 
                    stop:0 rgba(91, 101, 242, 0.6), 
                    stop:1 rgba(91, 101, 242, 0.8));
                border: 1px solid rgba(255, 255, 255, 0.2);
            }
            
            QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
                height: 0px;
            }
        """)

        # Set object name for main window styling
        self.setObjectName("mainWindow")
        
        # Create main horizontal layout for sidebar + content
        main_horizontal_layout = QtWidgets.QHBoxLayout(self)
        main_horizontal_layout.setContentsMargins(0, 0, 0, 0)
        main_horizontal_layout.setSpacing(0)
        
        # Create sidebar
        sidebar = QtWidgets.QWidget()
        sidebar.setObjectName("sidebar")
        sidebar.setFixedWidth(250)
        sidebar_layout = QtWidgets.QVBoxLayout(sidebar)
        sidebar_layout.setContentsMargins(0, 20, 0, 20)
        sidebar_layout.setSpacing(5)
        
        # Sidebar logo/title area
        logo_container = QtWidgets.QWidget()
        logo_layout = QtWidgets.QVBoxLayout(logo_container)
        logo_layout.setContentsMargins(20, 10, 20, 10)
        
        # App logo/icon
        logo_label = QtWidgets.QLabel()
        logo_label.setAlignment(QtCore.Qt.AlignCenter)
        
        pixmap = QtGui.QPixmap("logo.png")
        if not pixmap.isNull():
            # Scale the image to a reasonable size
            scaled_pixmap = pixmap.scaled(48, 48, QtCore.Qt.KeepAspectRatio, QtCore.Qt.SmoothTransformation)
            logo_label.setPixmap(scaled_pixmap)
            logo_label.setStyleSheet("margin-bottom: 8px; margin-top: 5px;")
        
        logo_layout.addWidget(logo_label)
        
        # App name
        self.app_name_label = QtWidgets.QLabel(get_ui_text("app_name"))
        self.app_name_label.setAlignment(QtCore.Qt.AlignCenter)
        self.app_name_label.setStyleSheet("""
            color: #ffffff;
            font-size: 16px;
            font-weight: 600;
            margin-bottom: 3px;
        """)
        logo_layout.addWidget(self.app_name_label)
        
        # App subtitle
        self.app_subtitle_label = QtWidgets.QLabel(get_ui_text("app_subtitle"))
        self.app_subtitle_label.setAlignment(QtCore.Qt.AlignCenter)
        self.app_subtitle_label.setStyleSheet("""
            color: #b9bbbe;
            font-size: 10px;
            margin-bottom: 10px;
        """)
        logo_layout.addWidget(self.app_subtitle_label)
        
        sidebar_layout.addWidget(logo_container)
        
        # Add separator line
        separator = QtWidgets.QFrame()
        separator.setFrameShape(QtWidgets.QFrame.HLine)
        separator.setStyleSheet("background-color: #3f4147; margin: 0 12px;")
        separator.setFixedHeight(1)
        sidebar_layout.addWidget(separator)
        
        # Menu buttons
        menu_buttons = [
            (get_ui_text("audio_input"), "audio"),
            (get_ui_text("languages"), "languages"), 
            (get_ui_text("ai_model"), "model"),
            (get_ui_text("settings"), "settings"),
            (get_ui_text("subtitles"), "subtitles")
        ]
        
        self.menu_btns = {}
        for btn_text, btn_id in menu_buttons:
            btn = QtWidgets.QPushButton(btn_text)
            btn.setObjectName("menuBtn")
            btn.clicked.connect(lambda checked, id=btn_id: self.switch_to_page(id))
            self.menu_btns[btn_id] = btn
            sidebar_layout.addWidget(btn)
        
        # Set first button as selected
        self.menu_btns["audio"].setProperty("selected", True)
        self.current_page = "audio"
        
        sidebar_layout.addStretch()
        
        # Add version info at bottom
        self.version_label = QtWidgets.QLabel(get_ui_text("version"))
        self.version_label.setAlignment(QtCore.Qt.AlignCenter)
        self.version_label.setStyleSheet("""
            color: #72767d;
            font-size: 9px;
            margin-top: 8px;
            margin-bottom: 8px;
        """)
        sidebar_layout.addWidget(self.version_label)
        
        main_horizontal_layout.addWidget(sidebar)
        
        # Create content area
        content_area = QtWidgets.QWidget()
        content_area.setObjectName("contentArea")
        content_layout = QtWidgets.QVBoxLayout(content_area)
        content_layout.setContentsMargins(0, 0, 0, 0)
        content_layout.setSpacing(0)
        
        # Create header bar
        header_bar = QtWidgets.QWidget()
        header_bar.setObjectName("headerBar")
        header_layout = QtWidgets.QHBoxLayout(header_bar)
        header_layout.setContentsMargins(25, 0, 5, 0)  # Reduced right margin to give more space for buttons
        header_layout.setSpacing(15)
        
        # Header title section
        title_container = QtWidgets.QWidget()
        title_layout = QtWidgets.QVBoxLayout(title_container)
        title_layout.setContentsMargins(0, 18, 0, 18)
        title_layout.setSpacing(4)
        
        self.page_title = QtWidgets.QLabel(get_ui_text("audio_input"))
        self.page_title.setObjectName("titleLabel")
        self.page_title.setWordWrap(True)
        self.page_title.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Preferred)
        title_layout.addWidget(self.page_title)
        
        self.page_subtitle = QtWidgets.QLabel(get_ui_text("audio_input_desc"))
        self.page_subtitle.setObjectName("subtitleLabel")
        self.page_subtitle.setWordWrap(False)
        self.page_subtitle.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Preferred)
        title_layout.addWidget(self.page_subtitle)
        
        header_layout.addWidget(title_container, 1)  # Give title container priority
        
        # Add some spacing but less stretch
        spacer = QtWidgets.QSpacerItem(20, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        header_layout.addItem(spacer)
        
        # Window control buttons
        window_controls = QtWidgets.QWidget()
        window_controls.setFixedWidth(120)  # Increased width to accommodate proper spacing
        controls_layout = QtWidgets.QHBoxLayout(window_controls)
        controls_layout.setContentsMargins(5, 15, 15, 15)  # Added margins for better positioning
        controls_layout.setSpacing(6)  # Increased spacing between buttons
        
        # Minimize button
        min_btn = QtWidgets.QPushButton("−")
        min_btn.setObjectName("windowBtn")
        min_btn.clicked.connect(self.showMinimized)
        controls_layout.addWidget(min_btn)
        
        # Maximize button  
        max_btn = QtWidgets.QPushButton("⬜")
        max_btn.setObjectName("windowBtn")
        max_btn.clicked.connect(self.toggle_maximize)
        controls_layout.addWidget(max_btn)
        
        # Close button
        close_btn = QtWidgets.QPushButton("✕")
        close_btn.setObjectName("closeBtn")
        close_btn.clicked.connect(self.close)
        controls_layout.addWidget(close_btn)
        
        header_layout.addWidget(window_controls)
        content_layout.addWidget(header_bar)
        
        # Create main content area without scroll (fixed height)
        content_widget = QtWidgets.QWidget()
        content_widget.setStyleSheet("background: transparent;")
        main_content_layout = QtWidgets.QVBoxLayout(content_widget)
        main_content_layout.setContentsMargins(25, 20, 25, 20)
        main_content_layout.setSpacing(14)
        
        # Create stacked widget for different pages
        self.stacked_widget = QtWidgets.QStackedWidget()
        self.stacked_widget.setStyleSheet("background: transparent;")
        
        # Create all pages
        self.create_audio_page()
        self.create_languages_page() 
        self.create_model_page()
        self.create_settings_page()
        self.create_subtitles_page()
        
        main_content_layout.addWidget(self.stacked_widget, 1)  # Give it most of the space
        
        # Add main control button at bottom with enhanced styling
        self.btn = QtWidgets.QPushButton(get_ui_text("start_translation"))
        self.btn.setMinimumHeight(56)
        self.btn.setStyleSheet("""
            QPushButton {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1, 
                    stop:0 #6875f3, stop:0.2 #5b65f2, stop:0.8 #4c5ce8, stop:1 #3c4ae0);
                font-size: 14px;
                font-weight: 700;
                border-radius: 8px;
                color: #ffffff;
                margin: 8px 0 12px 0;
                border: 2px solid rgba(255, 255, 255, 0.1);
                padding: 16px 24px;
            }
            QPushButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1, 
                    stop:0 #7985f4, stop:0.2 #6875f3, stop:0.8 #5b65f2, stop:1 #4c5ce8);
                border: 2px solid rgba(255, 255, 255, 0.2);
            }
            QPushButton:pressed {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1, 
                    stop:0 #4c5ce8, stop:0.2 #3c4ae0, stop:0.8 #2f3694, stop:1 #1e2875);
                border: 2px solid rgba(255, 255, 255, 0.05);
            }
        """)
        main_content_layout.addWidget(self.btn)
        self.btn.clicked.connect(self.toggle)
        
        content_layout.addWidget(content_widget)
        main_horizontal_layout.addWidget(content_area)
        
        # Enable window dragging
        self.old_pos = self.pos()
        
        # Runtime fields
        self.overlay = Overlay()
        self.queue = queue.Queue()
        self.stop_evt = threading.Event()
        self.audio_th = None
        self.nlp_th = None
        
        # Initialize audio devices
        self.refresh_audio_devices()
        
        # Load all saved settings BEFORE connecting save signals
        # This prevents defaults from overwriting loaded settings
        self.load_all_settings()
        
        # Now connect save signals after settings are loaded
        self.connect_save_signals()
        
        # Set the initial window mask for rounded corners
        QtCore.QTimer.singleShot(0, self.update_window_mask)
    
    def create_audio_page(self):
        """Create the audio input configuration page"""
        page = QtWidgets.QWidget()
        layout = QtWidgets.QVBoxLayout(page)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(20)
        
        # Audio device selection card
        device_card = self.create_section_card(get_ui_text("audio_device"), get_ui_text("audio_device_desc"))
        device_layout = QtWidgets.QVBoxLayout()
        device_layout.setSpacing(10)
        
        self.device_combo = AlphabetComboBox()
        self.device_combo.setToolTip(get_ui_text("select_audio_device"))
        device_layout.addWidget(self.device_combo)
        
        device_card.layout().addLayout(device_layout)
        layout.addWidget(device_card)
        layout.addStretch()
        
        self.stacked_widget.addWidget(page)
    
    def create_languages_page(self):
        """Create the language configuration page"""
        page = QtWidgets.QWidget()
        layout = QtWidgets.QVBoxLayout(page)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(20)
        
        # Source language card
        source_card = self.create_section_card(get_ui_text("source_language"), get_ui_text("source_language_desc"))
        source_layout = QtWidgets.QVBoxLayout()
        source_layout.setSpacing(10)
        
        self.source_combo = AlphabetComboBox()
        source_items = get_translated_source_languages()
        self.source_combo.addItems(source_items)
        self.source_combo.setToolTip(get_ui_text("select_source_language"))
        source_layout.addWidget(self.source_combo)
        
        source_card.layout().addLayout(source_layout)
        layout.addWidget(source_card)
        
        # Target language card
        target_card = self.create_section_card(get_ui_text("target_language"), get_ui_text("target_language_desc"))
        target_layout = QtWidgets.QVBoxLayout()
        target_layout.setSpacing(10)
        
        self.combo = AlphabetComboBox()
        target_items = get_translated_target_languages()
        self.combo.addItems(target_items)
        # Set English as default
        english_index = self.combo.findText("English")
        if english_index >= 0:
            self.combo.setCurrentIndex(english_index)
        self.combo.setToolTip(get_ui_text("select_target_language"))
        target_layout.addWidget(self.combo)
        
        target_card.layout().addLayout(target_layout)
        layout.addWidget(target_card)
        layout.addStretch()
        
        self.stacked_widget.addWidget(page)
    
    def create_model_page(self):
        """Create the AI model configuration page"""
        page = QtWidgets.QWidget()
        layout = QtWidgets.QVBoxLayout(page)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(20)
        
        # Model selection card
        model_card = self.create_section_card(get_ui_text("whisper_model"), get_ui_text("whisper_model_desc"))
        model_layout = QtWidgets.QVBoxLayout()
        model_layout.setSpacing(10)
        
        self.model_combo = AlphabetComboBox()
        for model_name in WHISPER_MODEL_KEYS:
            model_desc = get_whisper_model_description(model_name)
            self.model_combo.addItem(f"{model_name} • {model_desc}", model_name)
        # Set turbo as default
        turbo_index = self.model_combo.findData("turbo")
        if turbo_index >= 0:
            self.model_combo.setCurrentIndex(turbo_index)
        self.model_combo.setToolTip(get_ui_text("select_whisper_model"))
        model_layout.addWidget(self.model_combo)
        
        model_card.layout().addLayout(model_layout)
        layout.addWidget(model_card)
        layout.addStretch()
        
        self.stacked_widget.addWidget(page)
    
    def create_settings_page(self):
        """Create the settings configuration page"""
        page = QtWidgets.QWidget()
        layout = QtWidgets.QVBoxLayout(page)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(20)
        
        # Audio sensitivity card
        sensitivity_card = self.create_section_card(get_ui_text("audio_sensitivity"), get_ui_text("audio_sensitivity_desc"))
        sensitivity_layout = QtWidgets.QVBoxLayout()
        sensitivity_layout.setSpacing(15)
        
        # Threshold control
        threshold_header = QtWidgets.QHBoxLayout()
        self.sensitivity_level_label = QtWidgets.QLabel(get_ui_text("sensitivity_level"))
        threshold_header.addWidget(self.sensitivity_level_label)
        self.threshold_label = QtWidgets.QLabel(f"{DEFAULT_AUDIO_THRESHOLD:.3f}")
        self.threshold_label.setAlignment(QtCore.Qt.AlignRight)
        self.threshold_label.setStyleSheet("color: #5865f2; font-weight: 600; min-width: 70px; font-size: 12px;")
        threshold_header.addWidget(self.threshold_label)
        sensitivity_layout.addLayout(threshold_header)
        
        self.threshold_slider = QtWidgets.QSlider(QtCore.Qt.Horizontal)
        self.threshold_slider.setMinimum(1)
        self.threshold_slider.setMaximum(100)
        self.threshold_slider.setValue(int(DEFAULT_AUDIO_THRESHOLD * 1000))
        self.threshold_slider.setToolTip(get_ui_text("adjust_sensitivity"))
        self.threshold_slider.valueChanged.connect(self.update_threshold_label)
        sensitivity_layout.addWidget(self.threshold_slider)
        
        sensitivity_card.layout().addLayout(sensitivity_layout)
        layout.addWidget(sensitivity_card)
        
        # Performance mode card
        performance_card = self.create_section_card(get_ui_text("performance"), get_ui_text("performance_desc"))
        performance_layout = QtWidgets.QVBoxLayout()
        performance_layout.setSpacing(10)
        
        self.performance_mode = QtWidgets.QCheckBox(get_ui_text("enable_performance_mode"))
        self.performance_mode.setChecked(False)
        self.performance_mode.setToolTip(get_ui_text("optimize_performance"))
        performance_layout.addWidget(self.performance_mode)
        
        performance_card.layout().addLayout(performance_layout)
        layout.addWidget(performance_card)
        
        # UI Language card
        language_card = self.create_section_card(get_ui_text("ui_language"), get_ui_text("ui_language_desc"))
        language_layout = QtWidgets.QVBoxLayout()
        language_layout.setSpacing(10)
        
        self.ui_language_combo = AlphabetComboBox()
        # Populate with native language names
        native_languages = get_native_language_names()
        for native_name, internal_name in native_languages:
            self.ui_language_combo.addItem(native_name, internal_name)
        
        # Set current selection based on CURRENT_UI_LANGUAGE
        current_index = self.ui_language_combo.findData(CURRENT_UI_LANGUAGE)
        if current_index >= 0:
            self.ui_language_combo.setCurrentIndex(current_index)
        
        self.ui_language_combo.setToolTip(get_ui_text("select_ui_language"))
        self.ui_language_combo.currentTextChanged.connect(self.change_ui_language)
        language_layout.addWidget(self.ui_language_combo)
        
        language_card.layout().addLayout(language_layout)
        layout.addWidget(language_card)
        layout.addStretch()
        
        self.stacked_widget.addWidget(page)
    
    def create_subtitles_page(self):
        """Create the subtitle customization page"""
        page = QtWidgets.QWidget()
        layout = QtWidgets.QVBoxLayout(page)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(20)
        
        # Font selection card
        font_card = self.create_section_card(get_ui_text("font_settings"), get_ui_text("font_settings_desc"))
        font_layout = QtWidgets.QVBoxLayout()
        font_layout.setSpacing(15)
        
        # Font family
        family_layout = QtWidgets.QVBoxLayout()
        family_layout.setSpacing(5)
        self.family_label = QtWidgets.QLabel(get_ui_text("font_family"))
        self.family_label.setStyleSheet("color: #ffffff; font-weight: 600;")
        family_layout.addWidget(self.family_label)
        
        self.font_combo = AlphabetComboBox()
        fonts = ["Inter", "Segoe UI", "Roboto", "Arial", "Helvetica", "Calibri", 
                "Trebuchet MS", "Verdana", "Georgia", "Times New Roman"]
        font_items = [f"{font}" for font in fonts]
        self.font_combo.addItems(font_items)
        self.font_combo.setCurrentText("Inter")
        
        # Set custom delegate to show fonts in their own typeface
        font_delegate = FontItemDelegate(self.font_combo)
        self.font_combo.setItemDelegate(font_delegate)
        self.font_combo.setToolTip(get_ui_text("choose_font_family"))
        self.font_combo.currentTextChanged.connect(self.update_subtitle_font)
        family_layout.addWidget(self.font_combo)
        font_layout.addLayout(family_layout)
        
        # Font size
        size_layout = QtWidgets.QVBoxLayout()
        size_layout.setSpacing(5)
        self.size_label = QtWidgets.QLabel(get_ui_text("font_size"))
        self.size_label.setStyleSheet("color: #ffffff; font-weight: 600;")
        size_layout.addWidget(self.size_label)
        
        self.font_size_combo = AlphabetComboBox()
        sizes = ["10", "12", "14", "16", "18", "20", "22", "24", "28", "32", "36", "40", "48"]
        size_items = [f"{size}" for size in sizes]
        self.font_size_combo.addItems(size_items)
        self.font_size_combo.setCurrentText("16")
        self.font_size_combo.setToolTip(get_ui_text("choose_font_size"))
        self.font_size_combo.currentTextChanged.connect(self.update_subtitle_font)
        size_layout.addWidget(self.font_size_combo)
        font_layout.addLayout(size_layout)
        
        font_card.layout().addLayout(font_layout)
        layout.addWidget(font_card)
        
        # Position control card
        position_card = self.create_section_card(get_ui_text("position_control"), get_ui_text("position_control_desc"))
        position_layout = QtWidgets.QVBoxLayout()
        position_layout.setSpacing(10)
        
        self.position_btn = QtWidgets.QPushButton(get_ui_text("reposition_subtitles"))
        self.position_btn.setToolTip(get_ui_text("click_reposition_subtitles"))
        self.position_btn.setStyleSheet("""
            QPushButton {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1, 
                    stop:0 #6875f3, stop:0.5 #5b65f2, stop:1 #4c5ce8);
                border: 2px solid rgba(255, 255, 255, 0.1);
                border-radius: 10px;
                color: #ffffff;
                font-weight: 700;
                padding: 16px 24px;
                font-size: 13px;
                min-height: 18px;
                text-align: center;
            }
            QPushButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1, 
                    stop:0 #7985f4, stop:0.5 #6875f3, stop:1 #5b65f2);
                border: 2px solid rgba(255, 255, 255, 0.2);
            }
            QPushButton:pressed {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1, 
                    stop:0 #4c5ce8, stop:0.5 #3c4ae0, stop:1 #2f3694);
                border: 2px solid rgba(255, 255, 255, 0.05);
            }
            QPushButton:focus {
                outline: none;
                border: 2px solid rgba(121, 133, 244, 0.6);
            }
        """)
        self.position_btn.clicked.connect(self.toggle_positioning_mode)
        position_layout.addWidget(self.position_btn)
        
        position_card.layout().addLayout(position_layout)
        layout.addWidget(position_card)
        layout.addStretch()
        
        self.stacked_widget.addWidget(page)
    
    def create_section_card(self, title, description):
        """Create a modern card section"""
        card = QtWidgets.QWidget()
        card.setObjectName("sectionCard")
        card_layout = QtWidgets.QVBoxLayout(card)
        card_layout.setContentsMargins(16, 12, 16, 16)
        card_layout.setSpacing(8)
        
        # Title
        title_label = QtWidgets.QLabel(title)
        title_label.setObjectName("sectionTitle")
        card_layout.addWidget(title_label)
        
        # Description
        desc_label = QtWidgets.QLabel(description)
        desc_label.setStyleSheet("color: rgba(185, 187, 190, 0.8); font-size: 10px; margin-bottom: 3px;")
        card_layout.addWidget(desc_label)
        
        return card
    
    def switch_to_page(self, page_id):
        """Switch to the specified page"""
        # Update menu button states
        for btn_id, btn in self.menu_btns.items():
            btn.setProperty("selected", btn_id == page_id)
            btn.style().unpolish(btn)
            btn.style().polish(btn)
        
        # Update page content
        page_info = {
            "audio": (0, get_ui_text("audio_input"), get_ui_text("audio_input_desc")),
            "languages": (1, get_ui_text("languages"), get_ui_text("languages_desc")),
            "model": (2, get_ui_text("ai_model"), get_ui_text("ai_model_desc")),
            "settings": (3, get_ui_text("settings"), get_ui_text("settings_desc")),
            "subtitles": (4, get_ui_text("subtitles"), get_ui_text("subtitles_desc"))
        }
        
        if page_id in page_info:
            page_index, title, subtitle = page_info[page_id]
            self.stacked_widget.setCurrentIndex(page_index)
            self.page_title.setText(title)
            self.page_subtitle.setText(subtitle)
            self.current_page = page_id
    
    def toggle_maximize(self):
        """Toggle between maximized and normal window state"""
        if self.isMaximized():
            self.showNormal()
        else:
            self.showMaximized()
    
    def paintEvent(self, event):
        """Custom paint event to draw rounded corners"""
        painter = QtGui.QPainter(self)
        painter.setRenderHint(QtGui.QPainter.Antialiasing)
        
        # Get the widget rect
        rect = self.rect()
        
        # Draw the main window background with rounded corners and enhanced styling
        painter.setBrush(QtGui.QBrush(QtGui.QColor(26, 29, 35)))  # #1a1d23 - darker background
        painter.setPen(QtGui.QPen(QtGui.QColor(91, 101, 242), 2))   # Enhanced border color
        painter.drawRoundedRect(rect, 24, 24)
    
    def resizeEvent(self, event):
        """Handle resize events to update the window mask"""
        super().resizeEvent(event)
        self.update_window_mask()
    
    def update_window_mask(self):
        """Update the window mask to create rounded corners"""
        # Create a region with rounded corners
        region = QtGui.QRegion(self.rect(), QtGui.QRegion.Rectangle)
        
        # Create a path for the rounded rectangle with enhanced radius
        path = QtGui.QPainterPath()
        path.addRoundedRect(QtCore.QRectF(self.rect()), 24, 24)
        
        # Convert path to region
        region = QtGui.QRegion(path.toFillPolygon().toPolygon())
        
        # Apply the mask
        self.setMask(region)
    
    def mousePressEvent(self, event):
        """Handle mouse press for window dragging"""
        if event.button() == QtCore.Qt.LeftButton:
            self.old_pos = event.globalPos()
    
    def mouseMoveEvent(self, event):
        """Handle mouse move for window dragging"""
        if event.buttons() == QtCore.Qt.LeftButton and self.old_pos:
            delta = QtCore.QPoint(event.globalPos() - self.old_pos)
            self.move(self.x() + delta.x(), self.y() + delta.y())
            self.old_pos = event.globalPos()
    
    def refresh_audio_devices(self):
        """Refresh the list of available audio devices"""
        # Store current selection before clearing
        current_device_index = None
        if self.device_combo.count() > 0:
            current_device_index = self.device_combo.currentData()
        
        self.device_combo.clear()
        
        # Add auto-detection option
        self.device_combo.addItem(get_ui_text("auto_recommended"), -1)
        
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
                        f"[Virtual] {device['name']} ({device['channels']} ch, {device['samplerate']} Hz)",
                        device['index']
                    )
            
            # Add system audio devices
            if system_audio:
                for device in system_audio:
                    self.device_combo.addItem(
                        f"[System] {device['name']} ({device['channels']} ch, {device['samplerate']} Hz)",
                        device['index']
                    )
            
            # Add regular input devices
            for device in regular_devices:
                self.device_combo.addItem(
                    f"[Input] {device['name']} ({device['channels']} ch, {device['samplerate']} Hz)",
                    device['index']
                )
            
            # Restore previous selection if it was stored
            if current_device_index is not None:
                # Find the item with matching device index
                for i in range(self.device_combo.count()):
                    if self.device_combo.itemData(i) == current_device_index:
                        self.device_combo.setCurrentIndex(i)
                        break
                
        except Exception as e:
            print(f"Error refreshing audio devices: {e}")
            # Add a fallback option
            self.device_combo.addItem(get_ui_text("default_device", "audio_devices"), DEVICE_INDEX or 0)
    
    def get_selected_device_index(self):
        """Get the currently selected device index"""
        return self.device_combo.currentData()
    
    def get_source_language(self):
        """Get the currently selected source language for Whisper"""
        # Get the selected text and convert back to original name if translated
        selected_text = self.source_combo.currentText()
        original_name = get_original_language_name(selected_text)
        return WHISPER_SOURCE_LANGUAGES[original_name]
    
    def update_threshold_label(self, value):
        """Update the threshold label when slider changes"""
        threshold = value / 1000.0  # Convert back from slider scale
        self.threshold_label.setText(f"{threshold:.3f}")
    
    def get_audio_threshold(self):
        """Get current audio threshold from slider"""
        return self.threshold_slider.value() / 1000.0
    
    def update_subtitle_font(self):
        """Update the overlay font when user changes font settings"""
        # Get font settings directly
        font_family = self.font_combo.currentText()
        font_size = int(self.font_size_combo.currentText())
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
            settings["font_family"] = self.font_combo.currentText()
            settings["font_size"] = int(self.font_size_combo.currentText())
            
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
            settings["source_language"] = self.source_combo.currentText()
            settings["target_language"] = self.combo.currentText()
            
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
            
            # Update all settings (convert translated names back to original for consistency)
            if hasattr(self, 'font_combo'):
                settings["font_family"] = self.font_combo.currentText()
            if hasattr(self, 'font_size_combo'):
                settings["font_size"] = int(self.font_size_combo.currentText())
            if hasattr(self, 'source_combo'):
                settings["source_language"] = get_original_language_name(self.source_combo.currentText())
            if hasattr(self, 'combo'):
                settings["target_language"] = get_original_language_name(self.combo.currentText())
            if hasattr(self, 'device_combo'):
                settings["audio_device"] = self.device_combo.currentText()
                settings["audio_device_data"] = self.device_combo.currentData()
            if hasattr(self, 'model_combo'):
                settings["whisper_model"] = self.model_combo.currentData()
            if hasattr(self, 'threshold_slider'):
                settings["audio_threshold"] = self.threshold_slider.value() / 1000.0
            if hasattr(self, 'performance_mode'):
                settings["performance_mode"] = self.performance_mode.isChecked()
            settings["ui_language"] = CURRENT_UI_LANGUAGE
            
            # Save back to file
            with open("babel_settings.json", "w") as f:
                json.dump(settings, f, indent=2)
        except Exception as e:
            if DEBUG_MODE:
                print(f"Could not save settings: {e}")
    
    def connect_save_signals(self):
        """Connect all save signals after settings are loaded"""
        # Connect font save signals
        if hasattr(self, 'font_combo'):
            self.font_combo.currentTextChanged.connect(self.save_all_settings)
        if hasattr(self, 'font_size_combo'):
            self.font_size_combo.currentTextChanged.connect(self.save_all_settings)
        
        # Connect language save signals
        if hasattr(self, 'source_combo'):
            self.source_combo.currentTextChanged.connect(self.save_all_settings)
        if hasattr(self, 'combo'):
            self.combo.currentTextChanged.connect(self.save_all_settings)
        
        # Connect audio device save signal
        if hasattr(self, 'device_combo'):
            self.device_combo.currentTextChanged.connect(self.save_all_settings)
        
        # Connect model save signal
        if hasattr(self, 'model_combo'):
            self.model_combo.currentTextChanged.connect(self.save_all_settings)
        
        # Connect threshold save signal
        if hasattr(self, 'threshold_slider'):
            self.threshold_slider.valueChanged.connect(self.save_all_settings)
        
        # Connect performance mode save signal
        if hasattr(self, 'performance_mode'):
            self.performance_mode.toggled.connect(self.save_all_settings)
        
        # Note: UI language change is handled by change_ui_language method which calls save_all_settings

    def load_all_settings(self):
        """Load all saved settings and update the controls"""
        try:
            with open("babel_settings.json", "r") as f:
                settings = json.load(f)
                
                # Load UI language setting FIRST (affects other translations)
                global CURRENT_UI_LANGUAGE
                saved_ui_language = settings.get("ui_language", "English")
                if saved_ui_language in get_available_ui_languages():
                    CURRENT_UI_LANGUAGE = saved_ui_language
                    if hasattr(self, 'ui_language_combo'):
                        # Find the index by internal language name (stored as data)
                        language_index = self.ui_language_combo.findData(saved_ui_language)
                        if language_index >= 0:
                            self.ui_language_combo.setCurrentIndex(language_index)
                    self.update_ui_text()
                
                # Load font settings
                font_family = settings.get("font_family", "Inter")
                font_size = settings.get("font_size", 16)
                
                if hasattr(self, 'font_combo'):
                    font_index = self.font_combo.findText(str(font_family))
                    if font_index >= 0:
                        self.font_combo.setCurrentIndex(font_index)
                if hasattr(self, 'font_size_combo'):
                    size_index = self.font_size_combo.findText(str(font_size))
                    if size_index >= 0:
                        self.font_size_combo.setCurrentIndex(size_index)
                
                # Load language settings
                source_language = settings.get("source_language", "Auto-detect")
                target_language = settings.get("target_language", "English")
                
                if hasattr(self, 'source_combo'):
                    # Convert original names to translated names for display
                    translated_source = translate_language_name(source_language)
                    source_index = self.source_combo.findText(translated_source)
                    if source_index >= 0:
                        self.source_combo.setCurrentIndex(source_index)
                
                if hasattr(self, 'combo'):
                    translated_target = translate_language_name(target_language)
                    target_index = self.combo.findText(translated_target)
                    if target_index >= 0:
                        self.combo.setCurrentIndex(target_index)
                
                # Load audio device setting with improved matching
                saved_device_text = settings.get("audio_device", "")
                saved_device_data = settings.get("audio_device_data", -1)
                
                if hasattr(self, 'device_combo'):
                    # Try to match by data first (more reliable)
                    if saved_device_data is not None:
                        device_index = self.device_combo.findData(saved_device_data)
                        if device_index >= 0:
                            self.device_combo.setCurrentIndex(device_index)
                        else:
                            # Fallback to text matching
                            device_index = -1
                            for i in range(self.device_combo.count()):
                                item_text = self.device_combo.itemText(i)
                                if saved_device_text in item_text or item_text in saved_device_text:
                                    device_index = i
                                    break
                            if device_index >= 0:
                                self.device_combo.setCurrentIndex(device_index)
                
                # Load whisper model setting
                saved_model = settings.get("whisper_model", "turbo")
                if hasattr(self, 'model_combo'):
                    model_index = self.model_combo.findData(saved_model)
                    if model_index >= 0:
                        self.model_combo.setCurrentIndex(model_index)
                
                # Load audio threshold setting
                saved_threshold = settings.get("audio_threshold", DEFAULT_AUDIO_THRESHOLD)
                if hasattr(self, 'threshold_slider'):
                    self.threshold_slider.setValue(int(saved_threshold * 1000))
                    self.update_threshold_label(int(saved_threshold * 1000))
                
                # Load performance mode setting
                saved_performance_mode = settings.get("performance_mode", False)
                if hasattr(self, 'performance_mode'):
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
            self.position_btn.setText("✓ " + get_ui_text("done_positioning"))
            self.position_btn.setStyleSheet("""
                QPushButton {
                    background: qlineargradient(x1:0, y1:0, x2:0, y2:1, 
                        stop:0 #00d68f, stop:0.5 #00b894, stop:1 #00a085);
                    border: 2px solid rgba(255, 255, 255, 0.1);
                    border-radius: 10px;
                    color: #ffffff;
                    font-weight: 700;
                    padding: 14px 20px;
                    font-size: 12px;
                }
                QPushButton:hover {
                    background: qlineargradient(x1:0, y1:0, x2:0, y2:1, 
                        stop:0 #0ae298, stop:0.5 #00d68f, stop:1 #00b894);
                    border: 2px solid rgba(255, 255, 255, 0.2);
                }
                QPushButton:pressed {
                    background: qlineargradient(x1:0, y1:0, x2:0, y2:1, 
                        stop:0 #00a085, stop:0.5 #008f76, stop:1 #007d67);
                }
            """)
            
            # Show instructions
            msg = QtWidgets.QMessageBox()
            msg.setWindowTitle(get_ui_text("subtitle_positioning"))
            msg.setText(get_ui_text("positioning_instructions"))
            msg.setIcon(QtWidgets.QMessageBox.Information)
            msg.setStyleSheet("""
                QMessageBox {
                    background: #36393f;
                    color: #ffffff;
                    border: 1px solid #3f4147;
                    border-radius: 8px;
                }
                QMessageBox QPushButton {
                    background: #5865f2;
                    color: #ffffff;
                    border: none;
                    border-radius: 4px;
                    padding: 8px 16px;
                    min-width: 80px;
                    font-weight: 600;
                }
                QMessageBox QPushButton:hover {
                    background: #4752c4;
                }
            """)
            msg.exec_()
        else:
            # Exit positioning mode
            self.overlay.set_positioning_mode(False)
            self.overlay.hide()
            self.position_btn.setText(get_ui_text("reposition_subtitles"))
            # The button styling is already set by the default CSS, no need to override
    
    def change_ui_language(self, native_language_name):
        """Change the UI language and update all text elements"""
        global CURRENT_UI_LANGUAGE
        # Convert native name to internal language key
        internal_language = get_language_by_native_name(native_language_name)
        CURRENT_UI_LANGUAGE = internal_language
        
        # Update all UI text elements
        self.update_ui_text()
        
        # Save the language setting
        self.save_all_settings()
    
    def update_ui_text(self):
        """Update all UI text elements with current language"""
        # Update sidebar elements
        if hasattr(self, 'app_name_label'):
            self.app_name_label.setText(get_ui_text("app_name"))
        if hasattr(self, 'app_subtitle_label'):
            self.app_subtitle_label.setText(get_ui_text("app_subtitle"))
        if hasattr(self, 'version_label'):
            self.version_label.setText(get_ui_text("version"))
        
        # Update menu buttons
        menu_buttons_text = [
            (get_ui_text("audio_input"), "audio"),
            (get_ui_text("languages"), "languages"), 
            (get_ui_text("ai_model"), "model"),
            (get_ui_text("settings"), "settings"),
            (get_ui_text("subtitles"), "subtitles")
        ]
        
        for i, (text, btn_id) in enumerate(menu_buttons_text):
            if btn_id in self.menu_btns:
                self.menu_btns[btn_id].setText(text)
        
        # Update page titles and descriptions based on current page
        self.update_current_page_text()
        
        # Refresh all page content with new translations
        self.refresh_page_content()
        
        # Update main button
        if hasattr(self, 'btn'):
            if self.btn.text().startswith("▶") or "start" in self.btn.text().lower():
                self.btn.setText(get_ui_text("start_translation"))
            else:
                self.btn.setText(get_ui_text("stop_translation"))
        
        # Update position button
        if hasattr(self, 'position_btn'):
            self.position_btn.setText(get_ui_text("reposition_subtitles"))
    
    def refresh_page_content(self):
        """Refresh all page content with current language translations"""
        if not hasattr(self, 'stacked_widget'):
            return
        
        # Refresh dropdown options with new translations
        self.refresh_language_dropdowns()
        
        # Refresh audio device dropdown with new translations
        if hasattr(self, 'device_combo'):
            self.refresh_audio_devices()
        
        # Refresh UI element texts
        self.refresh_ui_element_texts()
        
        # Instead of recreating pages, update existing text elements directly
        # This is more efficient and preserves state
        
        # Update all section cards in all pages
        for page_index in range(self.stacked_widget.count()):
            page_widget = self.stacked_widget.widget(page_index)
            if page_widget:
                self.update_page_cards_text(page_widget, page_index)
    
    def refresh_ui_element_texts(self):
        """Refresh text of UI elements like checkboxes, labels, etc."""
        # Update performance mode checkbox
        if hasattr(self, 'performance_mode'):
            self.performance_mode.setText(get_ui_text("enable_performance_mode"))
        
        # Update sensitivity level label
        if hasattr(self, 'sensitivity_level_label'):
            self.sensitivity_level_label.setText(get_ui_text("sensitivity_level"))
        
        # Update font labels
        if hasattr(self, 'family_label'):
            self.family_label.setText(get_ui_text("font_family"))
        
        if hasattr(self, 'size_label'):
            self.size_label.setText(get_ui_text("font_size"))
        
        # Update any other UI elements that need text refresh
        # Add more elements here as needed
    
    def refresh_language_dropdowns(self):
        """Refresh language dropdown options with current translations"""
        if not hasattr(self, 'source_combo') or not hasattr(self, 'combo'):
            return
        
        # Save current selections (in original language names)
        current_source = get_original_language_name(self.source_combo.currentText())
        current_target = get_original_language_name(self.combo.currentText())
        
        # Clear and repopulate source language dropdown
        self.source_combo.clear()
        source_items = get_translated_source_languages()
        self.source_combo.addItems(source_items)
        
        # Clear and repopulate target language dropdown
        self.combo.clear()
        target_items = get_translated_target_languages()
        self.combo.addItems(target_items)
        
        # Refresh model dropdown if it exists
        if hasattr(self, 'model_combo'):
            current_model = self.model_combo.currentData()
            self.model_combo.clear()
            for model_name in WHISPER_MODEL_KEYS:
                model_desc = get_whisper_model_description(model_name)
                self.model_combo.addItem(f"{model_name} • {model_desc}", model_name)
            # Restore selection
            if current_model:
                model_index = self.model_combo.findData(current_model)
                if model_index >= 0:
                    self.model_combo.setCurrentIndex(model_index)
        
        # Restore selections using translated names
        translated_source = translate_language_name(current_source)
        translated_target = translate_language_name(current_target)
        
        source_index = self.source_combo.findText(translated_source)
        if source_index >= 0:
            self.source_combo.setCurrentIndex(source_index)
        
        target_index = self.combo.findText(translated_target)
        if target_index >= 0:
            self.combo.setCurrentIndex(target_index)
        else:
            # Default to English if not found
            english_index = self.combo.findText("English")
            if english_index >= 0:
                self.combo.setCurrentIndex(english_index)
    
    def update_page_cards_text(self, page_widget, page_index):
        """Update text content of cards in a specific page"""
        # Find all section cards in the page and update their text
        cards = page_widget.findChildren(QtWidgets.QWidget, "sectionCard")
        
        # Define the text mappings for each page
        page_text_mappings = {
            0: [  # Audio page
                ("🎵 " + get_ui_text("audio_device"), get_ui_text("audio_device_desc"))
            ],
            1: [  # Languages page
                ("🎙️ " + get_ui_text("source_language"), get_ui_text("source_language_desc")),
                ("🌍 " + get_ui_text("target_language"), get_ui_text("target_language_desc"))
            ],
            2: [  # Model page
                ("🤖 " + get_ui_text("whisper_model"), get_ui_text("whisper_model_desc"))
            ],
            3: [  # Settings page
                ("🔊 " + get_ui_text("audio_sensitivity"), get_ui_text("audio_sensitivity_desc")),
                ("⚡ " + get_ui_text("performance"), get_ui_text("performance_desc")),
                ("🌐 " + get_ui_text("ui_language"), get_ui_text("ui_language_desc"))
            ],
            4: [  # Subtitles page
                ("🎨 " + get_ui_text("font_settings"), get_ui_text("font_settings_desc")),
                ("📍 " + get_ui_text("position_control"), get_ui_text("position_control_desc"))
            ]
        }
        
        if page_index in page_text_mappings:
            text_mappings = page_text_mappings[page_index]
            
            # Update each card's title and description
            for i, card in enumerate(cards):
                if i < len(text_mappings):
                    title, description = text_mappings[i]
                    
                    # Find title and description labels in the card
                    title_labels = card.findChildren(QtWidgets.QLabel, "sectionTitle")
                    desc_labels = card.findChildren(QtWidgets.QLabel)
                    
                    # Update title
                    if title_labels:
                        title_labels[0].setText(title)
                    
                    # Update description (find the label with description styling)
                    for label in desc_labels:
                        if label.objectName() != "sectionTitle":
                            style = label.styleSheet()
                            if "color: #b9bbbe" in style or "font-size: 10px" in style:
                                label.setText(description)
                                break
        
        # Update tooltips
        self.update_tooltips_for_page(page_widget, page_index)
    
    def update_tooltips_for_page(self, page_widget, page_index):
        """Update tooltips for controls in a specific page"""
        tooltip_mappings = {
            0: {  # Audio page
                'AlphabetComboBox': get_ui_text("select_audio_device")
            },
            1: {  # Languages page
                'AlphabetComboBox': [get_ui_text("select_source_language"), get_ui_text("select_target_language")]
            },
            2: {  # Model page
                'AlphabetComboBox': get_ui_text("select_whisper_model")
            },
            3: {  # Settings page
                'QSlider': get_ui_text("adjust_sensitivity"),
                'QCheckBox': get_ui_text("optimize_performance"),
                'AlphabetComboBox': get_ui_text("select_ui_language")
            },
            4: {  # Subtitles page
                'AlphabetComboBox': [get_ui_text("choose_font_family"), get_ui_text("choose_font_size")],
                'QPushButton': get_ui_text("click_reposition_subtitles")
            }
        }
        
        if page_index in tooltip_mappings:
            mappings = tooltip_mappings[page_index]
            
            for widget_type, tooltip_text in mappings.items():
                # Find widgets by type more safely
                if widget_type == 'AlphabetComboBox':
                    widgets = page_widget.findChildren(AlphabetComboBox)
                elif widget_type == 'QSlider':
                    widgets = page_widget.findChildren(QtWidgets.QSlider)
                elif widget_type == 'QCheckBox':
                    widgets = page_widget.findChildren(QtWidgets.QCheckBox)
                elif widget_type == 'QPushButton':
                    widgets = page_widget.findChildren(QtWidgets.QPushButton)
                else:
                    continue
                
                if isinstance(tooltip_text, list):
                    # Multiple widgets of the same type
                    for i, widget in enumerate(widgets):
                        if i < len(tooltip_text):
                            widget.setToolTip(tooltip_text[i])
                else:
                    # Single tooltip for all widgets of this type
                    for widget in widgets:
                        widget.setToolTip(tooltip_text)
    
    def update_current_page_text(self):
        """Update the current page title and subtitle"""
        page_info = {
            "audio": (get_ui_text("audio_input"), get_ui_text("audio_input_desc")),
            "languages": (get_ui_text("languages"), get_ui_text("languages_desc")),
            "model": (get_ui_text("ai_model"), get_ui_text("ai_model_desc")),
            "settings": (get_ui_text("settings"), get_ui_text("settings_desc")),
            "subtitles": (get_ui_text("subtitles"), get_ui_text("subtitles_desc"))
        }
        
        if hasattr(self, 'current_page') and self.current_page in page_info:
            title, subtitle = page_info[self.current_page]
            self.page_title.setText(title)
            self.page_subtitle.setText(subtitle)

    def toggle(self):
        if self.audio_th and self.audio_th.is_alive():
            self.stop()
        else:
            self.start()

    def start(self):
        self.stop_evt.clear()
        # Get language code directly
        original_target_name = get_original_language_name(self.combo.currentText())
        lang_code = TARGETS[original_target_name]
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
        self.btn.setText(get_ui_text("stop_translation"))
        self.btn.setStyleSheet("""
            QPushButton {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1, 
                    stop:0 #dc3545, stop:0.5 #c82333, stop:1 #b21e2f);
                font-size: 14px;
                font-weight: 700;
                border-radius: 8px;
                color: #ffffff;
                margin: 8px 0 12px 0;
                border: 2px solid rgba(255, 255, 255, 0.1);
                padding: 16px 24px;
            }
            QPushButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1, 
                    stop:0 #e85663, stop:0.5 #dc3545, stop:1 #c82333);
                border: 2px solid rgba(255, 255, 255, 0.2);
            }
            QPushButton:pressed {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1, 
                    stop:0 #bd2130, stop:0.5 #a71e2a, stop:1 #941b25);
                border: 2px solid rgba(255, 255, 255, 0.05);
            }
        """)

    def stop(self):
        self.stop_evt.set()
        if self.nlp_th:
            self.nlp_th.join()
        if self.audio_th:
            self.audio_th.join()
        self.overlay.hide()
        self.btn.setText(get_ui_text("start_translation"))
        # Reset button styling back to the default blue
        self.btn.setStyleSheet("""
            QPushButton {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1, 
                    stop:0 #6875f3, stop:0.2 #5b65f2, stop:0.8 #4c5ce8, stop:1 #3c4ae0);
                font-size: 14px;
                font-weight: 700;
                border-radius: 8px;
                color: #ffffff;
                margin: 8px 0 12px 0;
                border: 2px solid rgba(255, 255, 255, 0.1);
                padding: 16px 24px;
            }
            QPushButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1, 
                    stop:0 #7985f4, stop:0.2 #6875f3, stop:0.8 #5b65f2, stop:1 #4c5ce8);
                border: 2px solid rgba(255, 255, 255, 0.2);
            }
            QPushButton:pressed {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1, 
                    stop:0 #4c5ce8, stop:0.2 #3c4ae0, stop:0.8 #2f3694, stop:1 #1e2875);
                border: 2px solid rgba(255, 255, 255, 0.05);
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
    
    # Load translations before creating the UI
    load_translations()
    
    # Initialize audio device detection
    initialize_audio_device()
    
    panel = ControlPanel()
    panel.show()
    
    print("Babel Audio Translator")
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
