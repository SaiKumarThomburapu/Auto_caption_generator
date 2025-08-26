import os
import subprocess
import sys
import tempfile
from src.entity.artifacts import AudioExtractionArtifact
from src.entity.config_entity import AudioExtractorConfig, ConfigEntity
from src.logger import logging
from src.exceptions import CustomException

class AudioExtractor:
    def __init__(self):
        self.config = AudioExtractorConfig(config=ConfigEntity()) 
        logging.info("AudioExtractor initialized")

    def extract(self, video_path: str) -> AudioExtractionArtifact:
        try:
            with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as temp_audio:
                audio_path = temp_audio.name

            cmd = [
                "ffmpeg", "-y", "-i", video_path,
                "-ac", "1", "-ar", str(self.config.target_sample_rate),
                "-acodec", "pcm_s16le", audio_path
            ]
            result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, check=True)

            if result.returncode != 0:
                raise CustomException(f"FFmpeg error: {result.stderr}", sys)

            logging.info(f"Audio extracted successfully to {audio_path}")
            return AudioExtractionArtifact(audio_path=audio_path)

        except Exception as e:
            logging.error(f"Error in audio extraction: {str(e)}")
            raise CustomException(e, sys)


