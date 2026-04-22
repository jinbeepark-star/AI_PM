from __future__ import annotations

from dataclasses import dataclass
from typing import Optional

from .analyzer import AnalysisResult


@dataclass
class ScoreBreakdown:
    title: int
    meta_description: int
    headings: int
    keyword_density: int
    image_alts: int
    content_length: int
    canonical: int
    total: int


class SeoScorer:
    """AnalysisResult를 받아 항목별 SEO 점수(0~100)를 산출한다."""

    TITLE_MAX = 20
    META_DESC_MAX = 20
    HEADINGS_MAX = 15
    KEYWORD_DENSITY_MAX = 15
    IMAGE_ALTS_MAX = 10
    CONTENT_LENGTH_MAX = 15
    CANONICAL_MAX = 5

    TITLE_MIN_LEN = 10
    TITLE_MAX_LEN = 60
    META_MIN_LEN = 50
    META_MAX_LEN = 160
    MIN_WORD_COUNT = 300
    GOOD_WORD_COUNT = 800

    def score(self, result: AnalysisResult) -> ScoreBreakdown:
        title_score = self._score_title(result.title)
        meta_score = self._score_meta_description(result.meta_description)
        headings_score = self._score_headings(result.headings)
        keyword_score = self._score_keyword_density(result.keyword_density)
        image_score = self._score_image_alts(result.image_alts)
        content_score = self._score_content_length(result.word_count)
        canonical_score = self._score_canonical(result.canonical)

        total = (
            title_score
            + meta_score
            + headings_score
            + keyword_score
            + image_score
            + content_score
            + canonical_score
        )
        return ScoreBreakdown(
            title=title_score,
            meta_description=meta_score,
            headings=headings_score,
            keyword_density=keyword_score,
            image_alts=image_score,
            content_length=content_score,
            canonical=canonical_score,
            total=total,
        )

    def _score_title(self, title: Optional[str]) -> int:
        if not title:
            return 0
        length = len(title)
        if self.TITLE_MIN_LEN <= length <= self.TITLE_MAX_LEN:
            return self.TITLE_MAX
        if length < self.TITLE_MIN_LEN:
            return int(self.TITLE_MAX * length / self.TITLE_MIN_LEN)
        excess = length - self.TITLE_MAX_LEN
        penalty = min(excess, self.TITLE_MAX_LEN)
        return max(0, self.TITLE_MAX - int(self.TITLE_MAX * penalty / self.TITLE_MAX_LEN))

    def _score_meta_description(self, meta: Optional[str]) -> int:
        if not meta:
            return 0
        length = len(meta)
        if self.META_MIN_LEN <= length <= self.META_MAX_LEN:
            return self.META_DESC_MAX
        if length < self.META_MIN_LEN:
            return int(self.META_DESC_MAX * length / self.META_MIN_LEN)
        excess = length - self.META_MAX_LEN
        penalty = min(excess, self.META_MAX_LEN)
        return max(0, self.META_DESC_MAX - int(self.META_DESC_MAX * penalty / self.META_MAX_LEN))

    def _score_headings(self, headings: dict[str, list[str]]) -> int:
        score = 0
        if headings.get("h1"):
            if len(headings["h1"]) == 1:
                score += 8
            else:
                score += 4
        if any(headings.get(f"h{i}") for i in range(2, 7)):
            score += 7
        return min(score, self.HEADINGS_MAX)

    def _score_keyword_density(self, density: dict[str, float]) -> int:
        if not density:
            return 0
        top_density = list(density.values())[0] if density else 0
        if 1.0 <= top_density <= 3.0:
            return self.KEYWORD_DENSITY_MAX
        if top_density < 1.0:
            return int(self.KEYWORD_DENSITY_MAX * top_density)
        if top_density > 3.0:
            over = top_density - 3.0
            penalty = min(over / 3.0, 1.0)
            return max(0, int(self.KEYWORD_DENSITY_MAX * (1 - penalty)))
        return 0

    def _score_image_alts(self, image_alts: list[Optional[str]]) -> int:
        if not image_alts:
            return self.IMAGE_ALTS_MAX
        filled = sum(1 for alt in image_alts if alt and alt.strip())
        ratio = filled / len(image_alts)
        return int(self.IMAGE_ALTS_MAX * ratio)

    def _score_content_length(self, word_count: int) -> int:
        if word_count >= self.GOOD_WORD_COUNT:
            return self.CONTENT_LENGTH_MAX
        if word_count >= self.MIN_WORD_COUNT:
            progress = (word_count - self.MIN_WORD_COUNT) / (self.GOOD_WORD_COUNT - self.MIN_WORD_COUNT)
            return int(self.CONTENT_LENGTH_MAX * (0.5 + 0.5 * progress))
        ratio = word_count / self.MIN_WORD_COUNT
        return int(self.CONTENT_LENGTH_MAX * 0.5 * ratio)

    def _score_canonical(self, canonical: Optional[str]) -> int:
        return self.CANONICAL_MAX if canonical else 0
