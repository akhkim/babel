# Real-time Internal Audio Translate & Transcriber

**Babel** is a Real-time internal audio translate & transcriber that uses [SYSTRAN/faster-whisper](https://github.com/SYSTRAN/faster-whisper), a reimplementation of OpenAI's Whisper model.

This script can recognize the volume of the recording, allowing the user to leave out the background noise and focus on louder sound if desired.
It also can automatically detect **57** different languages that Whisper model supports, and translate them into **134** different languages that Google Translate supports.

## Requirements
- Python 3.8 or greater

### GPU
GPU execution requires the following NVIDIA libraries to be installed:

- [cuBLAS for CUDA 12](https://developer.nvidia.com/cublas)
- [cuDNN 8 for CUDA 12](https://developer.nvidia.com/cudnn)

## Installation
```
git clone https://github.com/akhkim/babel.git
cd babel
pip install -r requirements.txt
```

## Command-line Usage
```
python3 main.py --model large --translation-lang English --threshold 0.0005
```

## To be Implemented
- Overlay of Transcribed Text
- Speech to Translated Speech Function
- Simple GUI
- Optimizing Memory Usage
- Increased Translation Accuracy
- Faster Translation / Transcription
