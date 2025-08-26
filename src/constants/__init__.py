# Directory for outputs
OUTPUT_DIR = "artifacts"

# File names and extensions
TEMP_AUDIO_FILENAME = "temp_audio.wav"
SRT_FILENAME_PREFIX = "subtitles_"
SRT_EXTENSION = ".srt"

# Validation constants
MAX_FILE_SIZE_MB = 100
ALLOWED_VIDEO_EXTENSIONS = (".mp4", ".avi", ".mov", ".mkv", ".webm", ".flv", ".m4v")

# Model configuration
INDIC_MODEL_NAME = "ai4bharat/indic-conformer-600m-multilingual"
WHISPER_MODEL_NAME = "small"

# Audio processing parameters
TARGET_SAMPLE_RATE = 16000
SEGMENT_LENGTH_SEC = 20

# Language detection parameters
STRONG_INDIAN_THRESHOLD = 60
WEAK_INDIAN_THRESHOLD = 25
ENGLISH_THRESHOLD = 0.6

# SRT generation parameters
MAX_CHARS_PER_LINE = 50
MAX_DURATION_SEC = 5.0

# Supported languages
INDIC_LANGUAGES = {
    'as': 'Assamese',
    'bn': 'Bengali', 
    'brx': 'Bodo',
    'doi': 'Dogri',
    'gu': 'Gujarati',
    'hi': 'Hindi',
    'kn': 'Kannada',
    'kok': 'Konkani', 
    'ks': 'Kashmiri',
    'mai': 'Maithili',
    'ml': 'Malayalam',
    'mni': 'Manipuri',
    'mr': 'Marathi',
    'ne': 'Nepali',
    'or': 'Odia',
    'pa': 'Punjabi',
    'sa': 'Sanskrit',
    'sat': 'Santali',
    'sd': 'Sindhi',
    'ta': 'Tamil',
    'te': 'Telugu',
    'ur': 'Urdu'
}
TEST_LANGUAGES = ['te', 'hi', 'ta', 'ml', 'kn', 'mr', 'gu', 'bn', 'ur', 'pa']


