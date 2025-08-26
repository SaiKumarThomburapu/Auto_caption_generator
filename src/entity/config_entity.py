from src.constants import *
import os

class ConfigEntity:
    def __init__(self):
        self.output_dir = OUTPUT_DIR
        self.temp_audio_filename = TEMP_AUDIO_FILENAME
        self.srt_filename_prefix = SRT_FILENAME_PREFIX
        self.srt_extension = SRT_EXTENSION
        self.max_file_size_mb = MAX_FILE_SIZE_MB
        self.allowed_video_extensions = ALLOWED_VIDEO_EXTENSIONS
        self.indic_model_name = INDIC_MODEL_NAME
        self.whisper_model_name = WHISPER_MODEL_NAME
        self.target_sample_rate = TARGET_SAMPLE_RATE
        self.segment_length_sec = SEGMENT_LENGTH_SEC
        self.strong_indian_threshold = STRONG_INDIAN_THRESHOLD
        self.weak_indian_threshold = WEAK_INDIAN_THRESHOLD
        self.english_threshold = ENGLISH_THRESHOLD
        self.max_chars_per_line = MAX_CHARS_PER_LINE
        self.max_duration_sec = MAX_DURATION_SEC
        self.indic_languages = INDIC_LANGUAGES
        self.test_languages = TEST_LANGUAGES

class AudioExtractorConfig:
    def __init__(self, config: ConfigEntity):
        self.target_sample_rate = config.target_sample_rate
        self.temp_audio_filename = config.temp_audio_filename

class LanguageDetectorConfig:
    def __init__(self, config: ConfigEntity):
        self.indic_languages = config.indic_languages
        self.test_languages = config.test_languages
        self.target_sample_rate = config.target_sample_rate
        self.segment_length_sec = config.segment_length_sec
        self.strong_indian_threshold = config.strong_indian_threshold
        self.weak_indian_threshold = config.weak_indian_threshold
        self.english_threshold = config.english_threshold
        self.indic_model_name = config.indic_model_name
        self.whisper_model_name = config.whisper_model_name

class TranscriberConfig:
    def __init__(self, config: ConfigEntity):
        self.indic_model_name = config.indic_model_name
        self.whisper_model_name = config.whisper_model_name
        self.target_sample_rate = config.target_sample_rate

class SRTGeneratorConfig:
    def __init__(self, config: ConfigEntity):
        self.output_dir = config.output_dir
        self.srt_filename_prefix = config.srt_filename_prefix
        self.srt_extension = config.srt_extension
        self.max_chars_per_line = config.max_chars_per_line
        self.max_duration_sec = config.max_duration_sec
        self.indic_languages = config.indic_languages


