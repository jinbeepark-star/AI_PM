from __future__ import annotations

import uuid
from pathlib import Path


_PROFILES: dict[str, dict] = {}


class VoiceCloner:
    """Mock 음성 복제기 — 실제 모델 없이 프로필 메타데이터를 관리합니다."""

    def __init__(self) -> None:
        self._profiles: dict[str, dict] = _PROFILES

    # ------------------------------------------------------------------
    def create_profile(self, sample_path: str, name: str = "unnamed") -> dict:
        """음성 샘플 파일로부터 복제 프로필을 생성합니다.

        Returns:
            {
                "profile_id": str,
                "name": str,
                "sample_path": str,
                "sample_format": str,
                "status": "ready",
            }
        """
        if not sample_path:
            raise ValueError("sample_path must not be empty")
        if not name or not name.strip():
            raise ValueError("name must not be empty")

        ext = Path(sample_path).suffix.lstrip(".").lower() or "unknown"
        profile_id = str(uuid.uuid4())

        profile = {
            "profile_id": profile_id,
            "name": name.strip(),
            "sample_path": sample_path,
            "sample_format": ext,
            "status": "ready",
        }
        self._profiles[profile_id] = profile
        return profile

    def clone(self, text: str, profile_id: str) -> dict:
        """등록된 프로필로 텍스트를 복제 음성 메타데이터로 변환합니다.

        Returns:
            {
                "text": str,
                "profile_id": str,
                "voice_name": str,
                "duration_ms": int,
                "format": str,
                "status": "success",
            }
        """
        if not text or not text.strip():
            raise ValueError("text must not be empty")
        if profile_id not in self._profiles:
            raise KeyError(f"profile_id '{profile_id}' not found")

        profile = self._profiles[profile_id]
        duration_ms = max(1, len(text) * 65)  # mock: ~65 ms per char

        return {
            "text": text,
            "profile_id": profile_id,
            "voice_name": profile["name"],
            "duration_ms": duration_ms,
            "format": "wav",
            "status": "success",
        }

    def get_profile(self, profile_id: str) -> dict:
        """프로필을 조회합니다."""
        if profile_id not in self._profiles:
            raise KeyError(f"profile_id '{profile_id}' not found")
        return self._profiles[profile_id]

    def list_profiles(self) -> list[dict]:
        """등록된 모든 프로필 목록을 반환합니다."""
        return list(self._profiles.values())
