# Babel - Real-time Audio Translation with Subtitle Overlay

**English | [Español](docs/translations/README_ES.md) | [Français](docs/translations/README_FR.md) | [Deutsch](docs/translations/README_DE.md) | [日本語](docs/translations/README_JA.md) | [한국어](docs/translations/README_KO.md) | [中文](docs/translations/README_ZH.md)**

A Python application that captures your PC's internal audio, translates it in real-time using Faster-Whisper and Google Translate, and displays translated subtitles as an overlay on your screen.

## Features

### 🎵 **Audio Capture**
- **Auto-detection**: Automatically finds the best loopback device (Stereo Mix, Virtual Audio Cable)
- **Manual selection**: Choose from available input devices with device details
- **App-specific capture**: Support for Virtual Audio Cable to capture individual applications
- **System audio**: Capture all PC audio or specific application audio

### 🧠 **AI-Powered Translation**
- **Speech Recognition**: Uses Faster-Whisper models (tiny, turbo, large-v3, distil-large-v3)
- **Auto-language detection**: Let Whisper detect the source language automatically
- **90+ source languages**: Support for all major languages that Whisper can transcribe
- **100+ target languages**: Translate to any language supported by Google Translate
- **Real-time processing**: Optimized for low latency and memory usage

### 📺 **Professional Subtitles**
- **Overlay display**: Transparent, always-on-top subtitle overlay
- **Customizable fonts**: Choose from 10 popular fonts and multiple sizes
- **Repositionable**: Drag subtitles to any position on screen
- **Auto-clearing**: Subtitles disappear automatically during silence
- **Modern design**: Semi-transparent background with text outlines for readability

### ⚙️ **Smart Settings**
- **Persistent configuration**: All settings automatically saved to `babel_settings.json`
- **Performance mode**: Toggle between speed and accuracy
- **Audio sensitivity**: Adjustable threshold to filter background noise
- **Alphabetical navigation**: Type letters in dropdowns to quickly find options

## Requirements

- **Python**: 3.9 or higher
- **Operating System**: Windows (for WASAPI loopback audio capture)
- **Memory**: At least 4GB RAM (8GB recommended for large models)
- **Storage**: 1-5GB for Whisper models (downloaded automatically)

## Installation

1. **Clone or download** this repository
2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```
3. **Run the application**:
   ```bash
   python main.py
   ```

## Quick Start Guide

### Basic Setup
1. **Launch** the application: `python main.py`
2. **Audio Input**: Select "Auto (Recommended)" or choose a specific device
3. **Languages**: 
   - **From**: Choose source language or "Auto-detect"
   - **To**: Choose target language (defaults to English)
4. **Click** "▶️ Start Translation"

### First-Time Setup Tips
- **Test audio**: Speak or play audio to verify the microphone/system audio is working
- **Adjust sensitivity**: Lower values = more sensitive to quiet audio
- **Position subtitles**: Use "⚙ Reposition Subtitles" to place them where you want
- **Choose model**: "turbo" is recommended for balanced speed/accuracy
- **Quick language selection**: Type letters in language dropdowns to jump to options (e.g., type "E" for English)
- **All settings saved**: Your preferences are automatically remembered between sessions

## Supported Languages

### Source Languages (Whisper Recognition)
**Auto-detect**, Afrikaans, Albanian, Amharic, Arabic, Armenian, Assamese, Azerbaijani, Bashkir, Basque, Belarusian, Bengali, Bosnian, Breton, Bulgarian, Burmese, Catalan, Chinese, Croatian, Czech, Danish, Dutch, English, Estonian, Faroese, Finnish, French, Galician, Georgian, German, Greek, Gujarati, Haitian, Hausa, Hawaiian, Hebrew, Hindi, Hungarian, Icelandic, Indonesian, Italian, Japanese, Javanese, Kannada, Kazakh, Khmer, Korean, Lao, Latin, Latvian, Lithuanian, Luxembourgish, Macedonian, Malagasy, Malay, Malayalam, Maltese, Maori, Marathi, Mongolian, Nepali, Norwegian, Occitan, Pashto, Persian, Polish, Portuguese, Punjabi, Romanian, Russian, Sanskrit, Serbian, Shona, Sindhi, Sinhala, Slovak, Slovenian, Somali, Spanish, Sundanese, Swahili, Swedish, Tagalog, Tajik, Tamil, Tatar, Telugu, Thai, Tibetan, Turkish, Turkmen, Ukrainian, Urdu, Uzbek, Vietnamese, Welsh, Yiddish, Yoruba

### Target Languages (Google Translate)
**English** (default), Afrikaans, Albanian, Amharic, Arabic, Armenian, Azerbaijani, Basque, Belarusian, Bengali, Bosnian, Bulgarian, Catalan, Cebuano, Chinese (Simplified), Chinese (Traditional), Corsican, Croatian, Czech, Danish, Dutch, Esperanto, Estonian, Finnish, French, Frisian, Galician, Georgian, German, Greek, Gujarati, Haitian Creole, Hausa, Hawaiian, Hebrew, Hindi, Hmong, Hungarian, Icelandic, Igbo, Indonesian, Irish, Italian, Japanese, Javanese, Kannada, Kazakh, Khmer, Korean, Kurdish, Kyrgyz, Lao, Latin, Latvian, Lithuanian, Luxembourgish, Macedonian, Malagasy, Malay, Malayalam, Maltese, Maori, Marathi, Mongolian, Myanmar (Burmese), Nepali, Norwegian, Odia (Oriya), Pashto, Persian, Polish, Portuguese, Punjabi, Romanian, Russian, Samoan, Scots Gaelic, Serbian, Sesotho, Shona, Sindhi, Sinhala, Slovak, Slovenian, Somali, Spanish, Sundanese, Swahili, Swedish, Tagalog, Tajik, Tamil, Tatar, Telugu, Thai, Turkish, Turkmen, Ukrainian, Urdu, Uyghur, Uzbek, Vietnamese, Welsh, Xhosa, Yiddish, Yoruba, Zulu

## Configuration Options

### Audio Settings
- **Device Selection**: Auto-detection or manual device selection
- **Audio Sensitivity**: 0.001-0.100 threshold for noise filtering
- **Performance Mode**: Toggle for optimized speed vs. accuracy

### AI Models
- **tiny**: Fastest, basic accuracy (~40MB)
- **turbo**: Balanced speed/accuracy (~810MB) - **Recommended**
- **large-v3**: Highest accuracy, slower (~3GB)
- **distil-large-v3**: Optimized large model (~1.5GB)

### Subtitle Appearance
- **Font Family**: Segoe UI, Arial, Helvetica, Times New Roman, Calibri, Trebuchet MS, Verdana, Georgia, Comic Sans MS, Impact
- **Font Size**: 10px to 48px
- **Position**: Drag to reposition anywhere on screen
- **Auto-clear**: Subtitles disappear after 2 seconds of silence

## App-Specific Audio Capture Guide

### For Individual Applications
1. **Install Virtual Audio Cable** (VB-Cable or similar)
2. **Set application audio output** to Virtual Cable
3. **In Babel**: Select the Virtual Cable device (marked with 🎯)
4. **Start translation** - now only that app's audio will be translated

### For System Audio
1. **Enable Stereo Mix** in Windows Sound settings:
   - Right-click speaker icon → Sounds → Recording tab
   - Right-click empty space → Show Disabled Devices
   - Enable "Stereo Mix"
2. **In Babel**: Select Stereo Mix device (marked with 🔊) or use Auto-detection

### Virtual Audio Cable Setup
1. **Download** VB-Audio Virtual Cable (free)
2. **Install** and restart your computer
3. **Set target application** to output to "CABLE Input"
4. **In Babel**: Select "🎯 CABLE Output" device
5. **Optional**: Set "CABLE Input" as your default playback device to hear audio

## Troubleshooting

### No Audio Detected
- **Check device selection**: Try "Auto (Recommended)" first
- **Verify audio source**: Make sure audio is actually playing
- **Adjust sensitivity**: Lower the audio sensitivity threshold
- **Enable Stereo Mix**: Follow the system audio setup guide above

### Translation Not Working
- **Check internet connection**: Google Translate requires internet
- **Verify languages**: Ensure source language matches the actual audio
- **Try auto-detect**: Let Whisper automatically detect the source language
- **Switch models**: Try "turbo" model for better accuracy

### Performance Issues
- **Enable Performance Mode**: Reduces memory usage and improves speed
- **Use smaller model**: Switch from "large-v3" to "turbo" or "tiny"
- **Close other applications**: Free up RAM for better performance
- **Check internet speed**: Slow connection affects translation speed

### Subtitle Issues
- **Subtitles not visible**: Check if overlay is behind other windows
- **Wrong position**: Use "⚙ Reposition Subtitles" to move them
- **Font too small/large**: Adjust font size in settings
- **Not clearing**: Check audio sensitivity - may be detecting background noise

## How It Works

### Audio Pipeline
1. **Capture**: Records audio from selected device (system audio or app-specific)
2. **Processing**: Converts stereo to mono, applies noise filtering
3. **Transcription**: Uses Faster-Whisper to convert speech to text
4. **Translation**: Google Translate API translates to target language
5. **Display**: Shows subtitles as overlay with auto-clearing

### Technical Details
- **Audio Format**: 48kHz stereo, converted to 16kHz mono for Whisper
- **Chunk Size**: 3-second audio segments for real-time processing
- **Memory Management**: Queue size limits (max 3 chunks) and garbage collection for efficiency
- **Latency Optimization**: Beam size 1, VAD filtering, optimized resampling
- **UI Framework**: PyQt5 with custom AlphabetComboBox widgets for enhanced navigation
- **Settings Storage**: JSON-based persistent configuration with automatic saving

### Settings Persistence
All settings are automatically saved to `babel_settings.json`:
```json
{
  "subtitle_y_offset": 184,
  "subtitle_x_offset": -5,
  "font_family": "Segoe UI",
  "font_size": 16,
  "source_language": "Korean",
  "target_language": "English",
  "audio_device": "Auto (Recommended)",
  "audio_device_data": -1,
  "whisper_model": "turbo",
  "audio_threshold": 0.001,
  "performance_mode": false
}
```

## Files Structure

```
babel/
├── main.py              # Main application file
├── requirements.txt     # Python dependencies
├── babel_settings.json  # Auto-saved user settings
├── run.bat             # Windows batch file to run the app
└── README.md           # This documentation
```

## Advanced Usage

### Command Line Options
Currently, all configuration is done through the GUI. Future versions may include CLI options.

### Custom Audio Devices
The application automatically detects:
- **🎯 Virtual Audio Cables**: For app-specific capture
- **🔊 System Audio Devices**: For full system audio capture  
- **🎤 Microphone Inputs**: For external audio sources

### Performance Tuning
- **For Speed**: Use "tiny" model + Performance Mode enabled
- **For Accuracy**: Use "large-v3" model + Performance Mode disabled
- **Balanced**: Use "turbo" model (recommended default)

### Memory Usage
- **tiny model**: ~200MB RAM
- **turbo model**: ~1GB RAM  
- **large-v3 model**: ~4GB RAM
- **distil-large-v3**: ~2GB RAM

## Support & Contributing

### Getting Help
1. **Check this README** for common solutions
2. **Verify requirements**: Python 3.9+, Windows OS
3. **Test with simple audio**: Try with clear speech first
4. **Check the console**: Run from command line to see error messages

### Known Limitations
- **Windows only**: WASAPI loopback audio capture requires Windows
- **Internet required**: Google Translate API needs internet connection
- **Model downloads**: First run downloads Whisper models (can be large)
- **Real-time processing**: Some delay is normal (1-3 seconds)

### Future Enhancements
- Linux/macOS support
- Offline translation options
- Custom subtitle themes
- Batch file processing
- API for external integrations

## Latest Features & Updates

### 🆕 **Enhanced User Experience** 
- **All settings auto-saved**: Every configuration automatically saved to `babel_settings.json`
- **Alphabetical navigation**: Type letters in dropdowns to quickly jump to languages
- **Improved UI**: Modern dark theme with better spacing and visual feedback
- **Smart defaults**: English target language, turbo model pre-selected

### 🎨 **Advanced Subtitle Customization**
- **10 font options**: Segoe UI, Arial, Helvetica, Times New Roman, and more
- **13 font sizes**: From 10px to 48px for perfect visibility
- **Drag positioning**: Click "⚙ Reposition Subtitles" and drag to any screen position
- **Auto-clearing**: Subtitles disappear after 2 seconds of silence
- **Modern design**: Semi-transparent backgrounds with text outlines

### 🔧 **Complete Settings Persistence**
All settings are automatically saved and restored:
- Audio device selection and sensitivity
- Source and target languages  
- Whisper model choice
- Performance mode preference
- Font family and size
- Subtitle position coordinates

### 🎯 **Smart Audio Device Detection**
- **Auto-categorization**: Devices marked with 🎯 (Virtual Cable), 🔊 (System Audio), 🎤 (Microphone)
- **Intelligent priority**: Automatically selects best available loopback device
- **Device details**: Shows channels and sample rate for each device
- **Refresh capability**: Update device list without restarting

### ⚡ **Performance Optimizations**
- **Performance Mode**: Toggle for speed vs accuracy optimization
- **Memory management**: Automatic garbage collection and queue size limits
- **Optimized models**: Support for distil-large-v3 (optimized large model)
- **VAD filtering**: Voice Activity Detection to reduce processing of silence

---

**Babel** - Making real-time translation accessible for everyone. Perfect for international gaming, watching foreign content, or learning new languages!
