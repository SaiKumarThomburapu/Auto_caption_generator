import torch
import torchaudio
import whisper
import sys
from typing import List, Dict
from src.entity.artifacts import TranscriptionArtifact
from src.entity.config_entity import TranscriberConfig, ConfigEntity
from src.logger import logging
from src.exceptions import CustomException

# Global models
indic_model = None
whisper_model = None

class Transcriber:
    def __init__(self):
        self.config = TranscriberConfig(config=ConfigEntity()) 
        logging.info("Transcriber initialized")

    def transcribe(self, audio_path: str, language: str) -> TranscriptionArtifact:
        global indic_model, whisper_model
        try:
            if not indic_model or not whisper_model:
                raise CustomException("Models not loaded", sys)

            if language == "en":
                result = whisper_model.transcribe(audio_path, language="en", word_timestamps=True, verbose=False)
                transcription = result["text"]
                word_timestamps = []
                for segment in result.get("segments", []):
                    word_timestamps.extend(segment.get("words", []))
                model_used = "Whisper"
            else:
                wav, sr = torchaudio.load(audio_path)
                if wav.shape[0] > 1:
                    wav = torch.mean(wav, dim=0, keepdim=True)
                if sr != self.config.target_sample_rate:
                    resampler = torchaudio.transforms.Resample(sr, self.config.target_sample_rate)
                    wav = resampler(wav)
                transcription = indic_model(wav, language, "rnnt")
                audio_duration = wav.shape[1] / self.config.target_sample_rate
                words = transcription.split() if transcription else []
                word_timestamps: List[Dict[str, any]] = []
                if words:
                    time_per_word = audio_duration / len(words)
                    current_time = 0.0
                    for word in words:
                        start = current_time
                        end = current_time + time_per_word
                        word_timestamps.append({"word": word, "start": start, "end": end})
                        current_time = end
                model_used = "IndicConformer"

            logging.info(f"Transcription completed using {model_used}")
            return TranscriptionArtifact(transcription=transcription, word_timestamps=word_timestamps, model_used=model_used)

        except Exception as e:
            logging.error(f"Error in transcription: {str(e)}")
            return TranscriptionArtifact(transcription=None, word_timestamps=None, model_used="", error=str(e))


