import torch
import torchaudio
import whisper
import sys
from src.entity.artifacts import LanguageDetectionArtifact
from src.entity.config_entity import LanguageDetectorConfig, ConfigEntity
from src.logger import logging
from src.exceptions import CustomException
from transformers import AutoModel

# Global models (loaded in app.py)
indic_model = None
whisper_model = None

class LanguageDetector:
    def __init__(self):
        self.config = LanguageDetectorConfig(config=ConfigEntity()) 
        logging.info("LanguageDetector initialized")

    def detect(self, audio_path: str) -> LanguageDetectionArtifact:
        global indic_model, whisper_model
        try:
            if not indic_model or not whisper_model:
                raise CustomException("Models not loaded", sys)

            # Load audio
            wav, sr = torchaudio.load(audio_path)
            if wav.shape[0] > 1:
                wav = torch.mean(wav, dim=0, keepdim=True)
            if sr != self.config.target_sample_rate:
                resampler = torchaudio.transforms.Resample(sr, self.config.target_sample_rate)
                wav = resampler(wav)

            segment_length = min(self.config.segment_length_sec * self.config.target_sample_rate, wav.shape[1])
            test_wav = wav[:, :segment_length]

            # Test Indian languages
            language_scores = {}
            for lang in self.config.test_languages:
                try:
                    transcription = indic_model(test_wav, lang, "rnnt") or indic_model(test_wav, lang, "ctc")
                    if transcription and len(transcription.strip()) > 3:
                        text = transcription.strip()
                        char_count = len(text)
                        word_count = len(text.split())
                        unique_chars = len(set(text.replace(' ', '')))
                        if word_count >= 2 and char_count >= 8:
                            score = (word_count * 15) + (unique_chars * 8) + min(char_count * 2, 100)
                            language_scores[lang] = score
                        else:
                            language_scores[lang] = 0
                    else:
                        language_scores[lang] = 0
                except:
                    language_scores[lang] = 0

            best_indian_lang = max(language_scores, key=language_scores.get) if language_scores else None
            best_indian_score = language_scores.get(best_indian_lang, 0)

            # Test English if needed
            english_prob = 0.0
            if best_indian_score < 80:
                result = whisper_model.transcribe(audio_path, language=None, verbose=False)
                detected_lang = result.get('language', 'unknown')
                text = result.get('text', '').strip()
                if detected_lang == 'en' and len(text) > 10:
                    english_prob = 0.8
                elif detected_lang == 'en':
                    english_prob = 0.3
                else:
                    english_prob = 0.2

            # Decision logic
            if best_indian_score >= self.config.strong_indian_threshold:
                detected = best_indian_lang
                confidence = min(1.0, best_indian_score / 150)
            elif english_prob >= self.config.english_threshold and best_indian_score < self.config.weak_indian_threshold:
                detected = "en"
                confidence = english_prob
            elif best_indian_score >= self.config.weak_indian_threshold:
                detected = best_indian_lang
                confidence = min(1.0, best_indian_score / 150)
            elif english_prob > 0.3:
                detected = "en"
                confidence = english_prob
            else:
                detected = "hi"
                confidence = 0.3

            logging.info(f"Language detected: {detected} with confidence {confidence}")
            return LanguageDetectionArtifact(detected_language=detected, confidence=confidence)

        except Exception as e:
            logging.error(f"Error in language detection: {str(e)}")
            return LanguageDetectionArtifact(detected_language="hi", confidence=0.0, error=str(e))


