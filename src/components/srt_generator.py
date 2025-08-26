import os
import sys
from typing import List, Dict
from src.entity.artifacts import SRTGenerationArtifact
from src.entity.config_entity import SRTGeneratorConfig, ConfigEntity
from src.logger import logging
from src.exceptions import CustomException

class SRTGenerator:
    def __init__(self):
        self.config = SRTGeneratorConfig(config=ConfigEntity())
         
        logging.info("SRTGenerator initialized")

    def generate(self, word_timestamps: List[Dict[str, any]], task_id: str, language: str, video_name: str) -> SRTGenerationArtifact:
        try:
            if not word_timestamps:
                raise CustomException("No word timestamps provided", sys)

            subtitles = []
            current_subtitle = []
            current_chars = 0
            subtitle_index = 1

            for i, word_info in enumerate(word_timestamps):
                word = word_info.get("word", "").strip()
                start = word_info.get("start", 0.0)
                end = word_info.get("end", 0.0)
                if not word:
                    continue

                current_subtitle.append({"word": word, "start": start, "end": end})
                current_chars += len(word) + 1

                should_break = (
                    current_chars >= self.config.max_chars_per_line or
                    i == len(word_timestamps) - 1 or
                    (current_subtitle and end - current_subtitle[0]["start"] >= self.config.max_duration_sec)
                )

                if should_break and current_subtitle:
                    sub_start = current_subtitle[0]["start"]
                    sub_end = current_subtitle[-1]["end"]
                    sub_text = " ".join(w["word"] for w in current_subtitle)
                    start_srt = self._format_timestamp(sub_start)
                    end_srt = self._format_timestamp(sub_end)
                    subtitles.extend([str(subtitle_index), f"{start_srt} --> {end_srt}", sub_text.strip(), ""])
                    subtitle_index += 1
                    current_subtitle = []
                    current_chars = 0

            srt_content = "\n".join(subtitles)

            # Save to file with video name
            lang_name = self.config.indic_languages.get(language, language).lower() if language != "en" else "english"
            filename = f"{self.config.srt_filename_prefix}{video_name}_{lang_name}{self.config.srt_extension}"
            srt_path = os.path.join(self.config.output_dir, filename)
            os.makedirs(self.config.output_dir, exist_ok=True)
            with open(srt_path, "w", encoding="utf-8") as f:
                f.write(srt_content)

            logging.info(f"SRT generated and saved to {srt_path}")
            return SRTGenerationArtifact(srt_content=srt_content, srt_file_path=srt_path)

        except Exception as e:
            logging.error(f"Error in SRT generation: {str(e)}")
            raise CustomException(e, sys)

    def _format_timestamp(self, seconds: float) -> str:
        hours = int(seconds // 3600)
        minutes = int((seconds % 3600) // 60)
        secs = int(seconds % 60)
        milliseconds = int((seconds % 1) * 1000)
        return f"{hours:02d}:{minutes:02d}:{secs:02d},{milliseconds:03d}"



