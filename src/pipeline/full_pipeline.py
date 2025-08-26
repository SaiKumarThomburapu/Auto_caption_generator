import os
import sys
import uuid
import tempfile
from fastapi import UploadFile
from src.entity.config_entity import ConfigEntity
from src.components.audio_extractor import AudioExtractor
from src.components.language_detector import LanguageDetector
from src.components.transcriber import Transcriber
from src.components.srt_generator import SRTGenerator
from src.utils.io_utils import validate_uploaded_file
from src.logger import logging
from src.exceptions import CustomException

async def upload_service(video: UploadFile, task_data: dict):
    try:
        base_config = ConfigEntity()
        task_id = uuid.uuid4().hex
        video_name = os.path.splitext(video.filename)[0]  # Get video name without extension

        # Validate and read file
        file_content = await validate_uploaded_file(video, base_config)

        # Save temporarily
        with tempfile.NamedTemporaryFile(suffix=os.path.splitext(video.filename)[1], delete=False) as temp_file:
            temp_file.write(file_content)
            video_path = temp_file.name

        # Initialize task
        task_data[task_id] = {
            "status": "processing",
            "transcription": None,
            "language": None,
            "model_used": None,
            "srt_file_path": None,
            "error": None,
            "video_path": video_path
        }

        logging.info(f"Task {task_id} processing started for video: {video_name}")

        # Process synchronously
        process_task(task_id, task_data, video_name)

        result = task_data[task_id]
        if result["status"] == "failed":
            raise CustomException(result["error"], sys)

        logging.info(f"Task {task_id} completed")
        return {
            "task_id": task_id,
            "status": result["status"],
            "message": "Processing completed",
            "srt_file_path": result["srt_file_path"]
        }

    except Exception as e:
        if task_id in task_data:
            task_data[task_id]["status"] = "failed"
            task_data[task_id]["error"] = str(e)
        raise CustomException(e, sys)

def process_task(task_id: str, task_data: dict, video_name: str):
    try:
        if task_id not in task_data:
            raise CustomException(f"Task not found: {task_id}", sys)

        video_path = task_data[task_id]["video_path"]

        # Extract audio
        extractor = AudioExtractor()
        audio_artifact = extractor.extract(video_path)
        audio_path = audio_artifact.audio_path

        # Detect language
        detector = LanguageDetector()
        lang_artifact = detector.detect(audio_path)
        if lang_artifact.error:
            task_data[task_id]["status"] = "failed"
            task_data[task_id]["error"] = lang_artifact.error
            return
        language = lang_artifact.detected_language

        # Transcribe
        transcriber = Transcriber()
        trans_artifact = transcriber.transcribe(audio_path, language)
        if trans_artifact.error:
            task_data[task_id]["status"] = "failed"
            task_data[task_id]["error"] = trans_artifact.error
            return

        # Generate SRT
        generator = SRTGenerator()
        srt_artifact = generator.generate(trans_artifact.word_timestamps, task_id, language, video_name)

        # Update task data
        task_data[task_id].update({
            "status": "completed",
            "transcription": trans_artifact.transcription,
            "language": language,
            "model_used": trans_artifact.model_used,
            "srt_file_path": srt_artifact.srt_file_path
        })

        # Cleanup
        try:
            os.unlink(video_path)
            os.unlink(audio_path)
        except:
            pass

    except Exception as e:
        task_data[task_id]["status"] = "failed"
        task_data[task_id]["error"] = str(e)
        logging.error(f"Task {task_id} failed: {str(e)}")
        raise  # Re-raise to propagate to upload_service



