# 🎙️ Smart Audio Transcriber

- [![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
- [![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
- [![Streamlit](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://share.streamlit.io/)
- [![Faster-Whisper](https://img.shields.io/badge/Faster--Whisper-Enabled-orange.svg)](https://github.com/SYSTRAN/faster-whisper)
- [![Docker](https://img.shields.io/badge/Docker-Ready-2496ED.svg)](https://www.docker.com/)

> 🚀 **Local AI-powered audio transcription with full Persian and English support, built with Faster-Whisper**

![Demo](https://img.shields.io/badge/Demo-Live-brightgreen)
![100+ Languages](https://img.shields.io/badge/Languages-100+-purple)
![Privacy](https://img.shields.io/badge/Privacy-100%25%20Local-success)

---

## 🌟 Overview

**Smart Audio Transcriber** is a privacy-first, fully local audio-to-text application that converts speech in 100+ languages into accurate transcriptions with timestamps. Unlike cloud-based services, **your audio files never leave your device**.

## ✨ Key Features

- 🎤 **Local AI Processing** — Powered by Faster-Whisper (4x faster than OpenAI Whisper)
- 🌐 **100+ Languages** — Full support for Persian, English, Arabic, and more
- ⏱️ **Timestamped Output** — Word-level timing for subtitles and analytics
- 🎵 **Multiple Formats** — MP3, WAV, M4A, FLAC, MP4, OGG support
- 🎯 **Voice Activity Detection** — Smart filtering of non-speech audio
- 🌍 **Bilingual UI** — Toggle between English and Persian interface
- 🐳 **Docker Ready** — One-command deployment anywhere
- 🔒 **100% Private** — No data ever leaves your machine
- ☁️ **Cloud Deployable** — Works on Streamlit Cloud

## 🛠️ Tech Stack

| Component                 | Technology                            |
|---------------------------|---------------------------------------|
| **Transcription Engine**  | Faster-Whisper (CTranslate2 optimized)|
| **Web Interface**         | Streamlit                             |
| **Audio Processing**      | SoundFile, Librosa                    |
| **Containerization**      | Docker                                |
| **Deployment**            | Streamlit Cloud                       |

## 🚀 Quick Start

### 1. Clone the repository

```bash
git clone https://github.com/YOUR_USERNAME/smart-audio-transcriber.git
cd smart-audio-transcriber
```

### 2. Set up environment

```bash
python -m venv venv
source venv/Scripts/activate  # Windows Git Bash
# or: source venv/bin/activate  # Linux/Mac
pip install -r requirements.txt
```

### 3. Install FFmpeg (required)

**Windows:**

```bash
winget install Gyan.FFmpeg
```

**macOS:**

```bash
brew install ffmpeg
```

**Linux:**

```bash
sudo apt-get install ffmpeg
```

### 4. Run the application

```bash
streamlit run app/main.py
```

The app will open automatically at `http://localhost:8501`

## 🐳 Docker Deployment

### Build and run locally

```bash
# Build the image
docker build -t smart-audio-transcriber .

# Run the container
docker run -d -p 8501:8501 --name transcriber-app smart-audio-transcriber
```

### Access the app

Open `http://localhost:8501` in your browser.

### Stop and remove

```bash
docker stop transcriber-app
docker rm transcriber-app
```

## 📁 Project Structure

```tree
smart-audio-transcriber/
├── app/
│   └── main.py              # Streamlit UI (bilingual)
├── src/
│   └── transcriber.py       # Faster-Whisper engine
├── data/
│   └── temp/                # Temporary audio files
├── Dockerfile               # Container configuration
├── .dockerignore
├── requirements.txt         # Python dependencies
├── .gitignore
└── README.md
```

## 🎯 Available Models

| Model        | Size   | Speed    | Accuracy    | Best For               |
|--------------|--------|----------|-------------|------------------------|
| **Tiny**     | 39 MB  |⚡⚡⚡⚡  |★★           | Quick tests            |
| **Base**     | 74 MB  |⚡⚡⚡    |★★★          | English audio          |
| **Small**    | 244 MB |⚡⚡      |★★★★         | General use            |
| **Medium**   | 769 MB |⚡        |★★★★★        | Persian audio          |
| **Large-v3** | 1.5 GB |🐌        |★★★★★        | Maximum accuracy       |

> 💡 **Tip:** For Persian transcription, use `Medium` or `Large-v3` for best results.

## 💡 Use Cases

- 🎙️ **Meeting Transcription** — Auto-transcribe interviews and meetings
- 🎬 **Video Subtitles** — Generate SRT/TXT subtitles for videos
- 🇮🇷 **Persian Content** — Excellent support for Farsi speech
- 🎵 **Lyrics Extraction** — Extract song lyrics (disable VAD)
- 📝 **Podcast Notes** — Convert podcasts to searchable text
- 🎓 **Lecture Notes** — Auto-generate notes from lectures

## ⚙️ Configuration

### Voice Activity Detection (VAD)

- **Enabled (default):** Filters out music, silence, and non-speech audio
- **Disabled:** Processes all audio (useful for songs with vocals)

### Language Selection

- **Auto-detect:** Model identifies language automatically
- **Force Persian/English:** Lock language for higher accuracy

### Model Selection

Choose based on your needs:

- **Speed:** Tiny or Base
- **Balance:** Small or Medium
- **Accuracy:** Large-v3

## ⚠️ Cloud Deployment Notes

When deploying to Streamlit Cloud:

- **Model downloads:** Models are downloaded once on the server
- **Memory limits:** Use `Base` or `Small` models (Large-v3 may crash)
- **File size:** Default 200MB limit (configurable to 500MB)
- **Privacy:** Audio files are processed on Streamlit servers (not local)

For **100% privacy**, run locally with Docker.

## 🧪 Testing

### Test with Persian audio

1. Upload a Persian audio file
2. Select model: **Medium** or **Large-v3**
3. Select language: **Persian**
4. Click "Start Transcription"

### Test with songs

1. Upload an audio file with music
2. **Disable VAD** in sidebar
3. Select model: **Large-v3**
4. Click "Start Transcription"

## 📝 License

This project is licensed under the MIT License — see the [LICENSE](LICENSE) file for details.

## 🤝 Contributing

Contributions, issues, and feature requests are welcome!

1. Fork the project
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 🙏 Acknowledgments

- [OpenAI Whisper](https://github.com/openai/whisper) — Original model
- [Faster-Whisper](https://github.com/SYSTRAN/faster-whisper) — CTranslate2 optimization
- [Streamlit](https://streamlit.io/) — Web framework
- [Hugging Face](https://huggingface.co/) — Model hosting

## 📧 Contact

**Saleh Bakhtyiari** — [Gmail](javascriptsali@gmail.com)

Project Link: [https://github.com/javascriptsali/smart-audio-transcriber](https://github.com/YOUR_USERNAME/smart-audio-transcriber)

---

## ⭐ Support

**If you find this project useful, consider giving it a star!**

Your support helps motivate me to create more open-source projects. 🚀
