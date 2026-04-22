from __future__ import annotations

import math
from typing import Literal


SUPPORTED_FORMATS: tuple[str, ...] = ("mp3", "wav", "ogg")
DEFAULT_SAMPLE_RATE = 22050
CHARS_PER_SECOND = 15.0  # rough estimate for Korean/English mixed text


class TtsSynthesizer:
    """Mock TTS 합성기 — 실제 API 호출 없이 메타데이터를 반환합니다."""

    def __init__(
        self,
        default_voice_id: str = "default",
        default_format: Literal["mp3", "wav", "ogg"] = "mp3",
        sample_rate: int = DEFAULT_SAMPLE_RATE,
    ) -> None:
        self.default_voice_id = default_voice_id
        self.default_format = default_format
        self.sample_rate = sample_rate

    # ------------------------------------------------------------------
    def synthesize(
        self,
        text: str,
        voice_id: str | None = None,
        speed: float = 1.0,
        format: Literal["mp3", "wav", "ogg"] | None = None,
    ) -> dict:
        """텍스트를 음성 메타데이터 dict로 변환합니다.

        Returns:
            {
                "text": str,
                "voice_id": str,
                "speed": float,
                "format": str,
                "sample_rate": int,
                "duration_ms": int,
                "char_count": int,
            }
        """
        if not isinstance(text, str):
            raise TypeError("text must be a string")
        if not text.strip():
            raise ValueError("text must not be empty")
        if speed <= 0:
            raise ValueError("speed must be positive")
        if format is not None and format not in SUPPORTED_FORMATS:
            raise ValueError(f"format must be one of {SUPPORTED_FORMATS}")

        effective_voice = voice_id if voice_id is not None else self.default_voice_id
        effective_format = format if format is not None else self.default_format

        raw_duration_s = len(text) / CHARS_PER_SECOND
        duration_ms = math.ceil((raw_duration_s / speed) * 1000)

        return {
            "text": text,
            "voice_id": effective_voice,
            "speed": speed,
            "format": effective_format,
            "sample_rate": self.sample_rate,
            "duration_ms": duration_ms,
            "char_count": len(text),
        }

    def list_voices(self) -> list[dict]:
        """사용 가능한 mock 음성 목록을 반환합니다."""
        return [
            {"voice_id": "default", "name": "Default", "language": "ko"},
            {"voice_id": "male_warm", "name": "Male Warm", "language": "ko"},
            {"voice_id": "female_clear", "name": "Female Clear", "language": "ko"},
        ]
