# Auto Caption Generator 🎙️  

A production-ready **video to caption** pipeline built with **FastAPI**, leveraging **IndicConformer** for multilingual speech recognition and **Whisper** as a fallback for English.  

This project makes it easy to upload videos and automatically generate subtitles/captions in multiple Indic languages + English.  

---

## 🚀 Features  
- Multilingual speech-to-text using **IndicConformer (ai4bharat/indic-conformer-600m-multilingual)**  
- Fallback **Whisper** model for English audio  
- REST API powered by **FastAPI**  
- Automatic subtitle (`.srt`) generation support  
- Configurable constants for model management  
- Optimized for Python **3.10**  

---

## 📦 Requirements  
Python 3.10 with the following packages (from `requirements.txt`):  

```txt
fastapi==0.104.1
uvicorn[standard]==0.24.0
python-multipart==0.0.6
torch>=2.0.0
torchaudio>=2.0.0
transformers>=4.30.0
pydantic==2.5.0
librosa>=0.10.0
numpy>=1.21.0
aiofiles==23.2.0
onnxruntime
openai-whisper>=20231117
```

---

## ⚙️ Installation  

1. Clone the repo:  
   ```bash
   git clone https://github.com/<your-username>/auto_caption_generator.git
   cd auto_caption_generator
   ```

2. Create & activate a virtual environment:  
   ```bash
   python3.10 -m venv venv
   source venv/bin/activate
   ```

3. Install dependencies:  
   ```bash
   pip install -r requirements.txt
   ```

---

## ▶️ Running the API  

Start the FastAPI server with **Uvicorn**:  

```bash
uvicorn app:app --host 0.0.0.0 --port 8000 --reload
```

API will be available at:  
```
http://localhost:8000
```

Interactive API docs:  
```
http://localhost:8000/docs
```

---

## 📂 Project Structure  

```
auto_caption_generator/
│── app.py                          # Main FastAPI app
│── requirements.txt
│── src/
│   ├── components/
│   │   ├── audio_extractor.py      # Extracts audio from uploaded videos
│   │   ├── language_detector.py    # Language detection logic
│   │   ├── transcriber.py          # Transcription pipeline
│   │   ├── srt_generator.py        # Generates .srt subtitle files
│   ├── pipeline/
│   │   ├── full_pipeline.py        # Upload & processing service
│   ├── entity/
│   │   ├── config_entity.py        # Config and supported language setup
│   ├── constants/
│   │   ├── model_constants.py      # Model IDs & constants
│   ├── logger.py                   # Logging utility
│── artifacts/                      # Generated captions and outputs
```

---

## 📡 API Endpoints  

### `GET /`  
Health check + shows loaded models and supported languages.  

### `POST /upload-video/`  
Upload a video and receive transcription/captions.  
- Input: `multipart/form-data` video file  
- Output: JSON with transcription + generated caption file path  

---

## 🌐 Supported Languages  
Indic languages via **IndicConformer**, plus **English** with Whisper fallback.  

---

## 🔮 Roadmap  
- [ ] Add speaker diarization support  
- [ ] Provide direct `.srt` file download via API  
- [ ] Dockerize the deployment  
- [ ] Add Streamlit UI for non-tech users  

---

## 🤝 Contributing  
Pull requests are welcome! Please open an issue first to discuss major changes.  

---

## 📜 License  
MIT License © 2025  
