from __future__ import annotations

import json
from typing import Any

from .analyzer import AnalysisResult
from .scorer import ScoreBreakdown


class SeoReporter:
    """분석 결과와 점수를 dict/JSON 형식으로 포맷한다."""

    def build_report(
        self,
        result: AnalysisResult,
        breakdown: ScoreBreakdown,
        url: str = "",
    ) -> dict[str, Any]:
        return {
            "url": url,
            "summary": {
                "total_score": breakdown.total,
                "grade": self._grade(breakdown.total),
                "word_count": result.word_count,
            },
            "scores": {
                "title": breakdown.title,
                "meta_description": breakdown.meta_description,
                "headings": breakdown.headings,
                "keyword_density": breakdown.keyword_density,
                "image_alts": breakdown.image_alts,
                "content_length": breakdown.content_length,
                "canonical": breakdown.canonical,
            },
            "meta": {
                "title": result.title,
                "meta_description": result.meta_description,
                "meta_keywords": result.meta_keywords,
                "canonical": result.canonical,
                "lang": result.lang,
            },
            "headings": {tag: texts for tag, texts in result.headings.items() if texts},
            "top_keywords": dict(list(result.keyword_density.items())[:10]),
            "images": {
                "total": len(result.image_alts),
                "missing_alt": sum(1 for a in result.image_alts if not a or not a.strip()),
            },
            "recommendations": self._recommendations(result, breakdown),
        }

    def to_json(
        self,
        result: AnalysisResult,
        breakdown: ScoreBreakdown,
        url: str = "",
        indent: int = 2,
    ) -> str:
        return json.dumps(self.build_report(result, breakdown, url), ensure_ascii=False, indent=indent)

    @staticmethod
    def _grade(total: int) -> str:
        if total >= 90:
            return "A+"
        if total >= 80:
            return "A"
        if total >= 70:
            return "B"
        if total >= 60:
            return "C"
        if total >= 50:
            return "D"
        return "F"

    @staticmethod
    def _recommendations(result: AnalysisResult, breakdown: ScoreBreakdown) -> list[str]:
        recs: list[str] = []
        if not result.title:
            recs.append("페이지 타이틀을 추가하세요.")
        elif breakdown.title < 15:
            recs.append("타이틀 길이를 10~60자로 맞추세요.")

        if not result.meta_description:
            recs.append("메타 설명을 추가하세요.")
        elif breakdown.meta_description < 15:
            recs.append("메타 설명 길이를 50~160자로 맞추세요.")

        if not result.headings.get("h1"):
            recs.append("H1 태그를 하나 추가하세요.")
        elif len(result.headings["h1"]) > 1:
            recs.append("H1 태그는 페이지당 하나만 사용하세요.")

        missing_alts = sum(1 for a in result.image_alts if not a or not a.strip())
        if missing_alts:
            recs.append(f"이미지 {missing_alts}개에 alt 속성을 추가하세요.")

        if result.word_count < 300:
            recs.append("콘텐츠 분량을 최소 300 단어 이상으로 늘리세요.")

        if not result.canonical:
            recs.append("canonical 링크 태그를 추가하세요.")

        return recs
