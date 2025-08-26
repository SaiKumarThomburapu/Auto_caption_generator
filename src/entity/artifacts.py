from dataclasses import dataclass
from typing import List, Dict, Any, Optional
      
@dataclass
class AudioExtractionArtifact:
    audio_path: str
    
@dataclass
class LanguageDetectionArtifact:
    detected_language: str
    confidence: float
    error: Optional[str] = None

@dataclass
class TranscriptionArtifact:
    transcription: Optional[str]
    word_timestamps: Optional[List[Dict[str, Any]]]
    model_used: str
    error: Optional[str] = None

@dataclass
class SRTGenerationArtifact:
    srt_content: str
    srt_file_path: Optional[str] = None


