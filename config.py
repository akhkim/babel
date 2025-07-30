"""
Configuration module for Enhanced Babel - Real-time Audio Translation

This module contains all configuration constants, language mappings,
translation utilities, and audio device management functions.
"""

import json, platform
from pathlib import Path
import sounddevice as sd


class Config:
    """Configuration class to hold mutable settings"""
    def __init__(self):
        # Audio configuration
        self.WASAPI_HOST_API = None
        self.WASAPI_SETTINGS = None
        
        # User settings
        self.DEVICE_INDEX = None
        self.SAMPLE_RATE = 48_000
        self.CHUNK_SECONDS = 3
        self.MODEL_NAME = "turbo"
        self.DEBUG_MODE = False
        self.DEFAULT_AUDIO_THRESHOLD = 0.001
        self.MAX_QUEUE_SIZE = 3
        
        # UI and translations
        self.CURRENT_UI_LANGUAGE = "English"
        self.TRANSLATIONS = {}

# Global configuration instance
config = Config()

# Initialize WASAPI on Windows
if platform.system() == "Windows":
    try:
        # Find WASAPI host API
        for i, api in enumerate(sd.query_hostapis()):
            if 'wasapi' in api['name'].lower():
                config.WASAPI_HOST_API = i
                break
        
        if config.WASAPI_HOST_API is not None:
            # Create shared mode settings
            config.WASAPI_SETTINGS = sd.WasapiSettings(exclusive=False)
            print(f"✅ WASAPI shared mode configured (Host API: {config.WASAPI_HOST_API}) - audio capture will work during calls")
        else:
            print("⚠️  WASAPI host API not found - using default audio settings")
    except Exception as e:
        print(f"⚠️  Could not configure WASAPI shared mode: {e}")
        print("   Audio capture may not work during calls or when other apps use audio")

# Backward compatibility - expose individual variables
WASAPI_HOST_API = config.WASAPI_HOST_API
WASAPI_SETTINGS = config.WASAPI_SETTINGS
DEVICE_INDEX = config.DEVICE_INDEX
SAMPLE_RATE = config.SAMPLE_RATE
CHUNK_SECONDS = config.CHUNK_SECONDS
MODEL_NAME = config.MODEL_NAME
DEBUG_MODE = config.DEBUG_MODE
DEFAULT_AUDIO_THRESHOLD = config.DEFAULT_AUDIO_THRESHOLD
MAX_QUEUE_SIZE = config.MAX_QUEUE_SIZE
CURRENT_UI_LANGUAGE = config.CURRENT_UI_LANGUAGE
TRANSLATIONS = config.TRANSLATIONS

# Available Whisper models (used as keys for translation lookup)
WHISPER_MODEL_KEYS = ["tiny", "turbo", "large-v3", "distil-large-v3"]

# ──────────────────────────── LANGUAGE MAPPINGS ─────────────────────── #

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

# ──────────────────────────── TRANSLATION SYSTEM ─────────────────────── #

def load_translations():
    """Load translation files from the translations directory"""
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
                    config.TRANSLATIONS[language] = json.load(f)
            else:
                print(f"Warning: Translation file {filename} not found")
        except Exception as e:
            print(f"Error loading translation {filename}: {e}")
    
    # Fallback to English if no translations loaded
    if not config.TRANSLATIONS:
        config.TRANSLATIONS["English"] = {
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
    if not config.TRANSLATIONS:
        load_translations()
    
    current_lang = config.TRANSLATIONS.get(config.CURRENT_UI_LANGUAGE)
    if not current_lang:
        current_lang = config.TRANSLATIONS.get("English", {})
    
    return current_lang.get(category, {}).get(key, key)

def get_whisper_model_description(model_key):
    """Get translated Whisper model description"""
    return get_ui_text(model_key, "whisper_models")

def get_available_ui_languages():
    """Get list of available UI languages"""
    if not config.TRANSLATIONS:
        load_translations()
    return list(config.TRANSLATIONS.keys())

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
    if config.TRANSLATIONS and config.CURRENT_UI_LANGUAGE in config.TRANSLATIONS:
        language_names = config.TRANSLATIONS[config.CURRENT_UI_LANGUAGE].get("language_names", {})
        for original, translated in language_names.items():
            if translated == translated_name:
                return original
    
    # Fallback - return as is if not found
    return translated_name

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
                                      for keyword in ['cable', 'vac', 'virtual']),
                'is_wasapi': (config.WASAPI_HOST_API is not None and device['hostapi'] == config.WASAPI_HOST_API)
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
    try:
        print("=== Initializing Audio Device ===")
        
        # Show available devices in debug mode
        if config.DEBUG_MODE:
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
        config.DEVICE_INDEX = best_device_index
        config.SAMPLE_RATE = best_sample_rate
        
        # Get device info for reporting
        device_info = sd.query_devices(best_device_index)
        device_name = device_info['name']
        
        print(f"✅ Selected audio device: {device_name} (Index: {best_device_index}, Rate: {best_sample_rate}Hz)")
        return True
        
    except Exception as e:
        print(f"❌ Failed to initialize audio device: {e}")
        print("Using default fallback settings...")
        config.DEVICE_INDEX = None
        return False

def get_loopback_device(device_index=None) -> tuple[int, int]:
    """
    Return (device_index, samplerate) of specified device or auto-detect.
    """
    if device_index is not None and device_index != -1:
        device_info = sd.query_devices(device_index)
        print(f"Using specified device {device_index}: {device_info['name']}")
        return device_index, int(device_info['default_samplerate'])
    
    # Auto-detection
    if config.DEBUG_MODE:
        print("=== Audio Device Auto-Detection ===")
        devices = sd.query_devices()
        print(f"Found {len(devices)} audio devices:")
        for idx, dev in enumerate(devices):
            if dev['max_input_channels'] > 0:
                print(f"  {idx}: {dev['name']} (inputs: {dev['max_input_channels']}, rate: {dev['default_samplerate']})")
    
    return auto_detect_loopback_device()
