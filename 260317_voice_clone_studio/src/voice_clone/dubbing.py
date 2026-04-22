from __future__ import annotations

from .cloner import VoiceCloner


class DubbingPipeline:
    """Mock 더빙 파이프라인 — 스크립트 라인과 프로필로 더빙 결과를 생성합니다."""

    def __init__(self, cloner: VoiceCloner | None = None) -> None:
        self._cloner = cloner if cloner is not None else VoiceCloner()

    # ------------------------------------------------------------------
    def dub(self, script_lines: list[str], profile_id: str) -> list[dict]:
        """스크립트 라인 목록을 더빙하여 결과 list를 반환합니다.

        Args:
            script_lines: 더빙할 텍스트 라인 목록
            profile_id: 사용할 음성 복제 프로필 ID

        Returns:
            각 라인에 대한 dict 목록:
            {
                "index": int,
                "text": str,
                "profile_id": str,
                "duration_ms": int,
                "format": str,
                "status": str,
            }
        """
        if not isinstance(script_lines, list):
            raise TypeError("script_lines must be a list")
        if not script_lines:
            raise ValueError("script_lines must not be empty")

        results: list[dict] = []
        offset_ms = 0

        for idx, line in enumerate(script_lines):
            if not isinstance(line, str):
                raise TypeError(f"script_lines[{idx}] must be a string")

            text = line.strip()
            if not text:
                results.append(
                    {
                        "index": idx,
                        "text": "",
                        "profile_id": profile_id,
                        "duration_ms": 0,
                        "offset_ms": offset_ms,
                        "format": "wav",
                        "status": "skipped",
                    }
                )
                continue

            cloned = self._cloner.clone(text, profile_id)
            entry = {
                "index": idx,
                "text": text,
                "profile_id": profile_id,
                "duration_ms": cloned["duration_ms"],
                "offset_ms": offset_ms,
                "format": cloned["format"],
                "status": "success",
            }
            results.append(entry)
            offset_ms += cloned["duration_ms"]

        return results

    def total_duration_ms(self, dub_results: list[dict]) -> int:
        """더빙 결과 목록의 총 길이(ms)를 반환합니다."""
        if not dub_results:
            return 0
        last = dub_results[-1]
        return last["offset_ms"] + last["duration_ms"]
