from __future__ import annotations

import re
from html.parser import HTMLParser
from collections import Counter
from dataclasses import dataclass, field
from typing import Optional


@dataclass
class AnalysisResult:
    title: Optional[str]
    meta_description: Optional[str]
    meta_keywords: Optional[str]
    headings: dict[str, list[str]]
    body_text: str
    word_count: int
    keyword_density: dict[str, float]
    image_alts: list[Optional[str]]
    canonical: Optional[str]
    lang: Optional[str]


class _HtmlExtractor(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.title: Optional[str] = None
        self.meta_description: Optional[str] = None
        self.meta_keywords: Optional[str] = None
        self.canonical: Optional[str] = None
        self.lang: Optional[str] = None
        self.headings: dict[str, list[str]] = {f"h{i}": [] for i in range(1, 7)}
        self.image_alts: list[Optional[str]] = []
        self._in_title = False
        self._in_heading: Optional[str] = None
        self._heading_buf: list[str] = []
        self._body_parts: list[str] = []
        self._ignore_tags = {"script", "style", "head"}
        self._current_ignore = 0

    def handle_starttag(self, tag: str, attrs: list[tuple[str, Optional[str]]]) -> None:
        attr_map = dict(attrs)

        if tag == "html":
            self.lang = attr_map.get("lang")

        if tag in self._ignore_tags:
            self._current_ignore += 1

        if tag == "title":
            self._in_title = True

        if tag == "meta":
            name = (attr_map.get("name") or "").lower()
            if name == "description":
                self.meta_description = attr_map.get("content")
            elif name == "keywords":
                self.meta_keywords = attr_map.get("content")

        if tag == "link" and attr_map.get("rel") == "canonical":
            self.canonical = attr_map.get("href")

        if tag in self.headings:
            self._in_heading = tag
            self._heading_buf = []

        if tag == "img":
            self.image_alts.append(attr_map.get("alt"))

    def handle_endtag(self, tag: str) -> None:
        if tag in self._ignore_tags:
            self._current_ignore -= 1

        if tag == "title":
            self._in_title = False

        if tag == self._in_heading:
            self.headings[tag].append("".join(self._heading_buf).strip())
            self._in_heading = None
            self._heading_buf = []

    def handle_data(self, data: str) -> None:
        if self._in_title:
            self.title = data.strip()

        if self._in_heading:
            self._heading_buf.append(data)

        if self._current_ignore == 0:
            self._body_parts.append(data)

    @property
    def body_text(self) -> str:
        return " ".join(self._body_parts)


class SeoAnalyzer:
    """HTML 텍스트를 파싱하여 SEO 관련 메타데이터와 콘텐츠를 추출한다."""

    _STOP_WORDS: frozenset[str] = frozenset(
        {
            "a", "an", "the", "and", "or", "but", "in", "on", "at",
            "to", "for", "of", "with", "is", "are", "was", "were", "be",
            "been", "being", "have", "has", "had", "do", "does", "did",
            "will", "would", "shall", "should", "may", "might", "can",
            "could", "this", "that", "these", "those", "i", "you", "he",
            "she", "it", "we", "they", "not",
        }
    )

    def analyze(self, html: str) -> AnalysisResult:
        parser = _HtmlExtractor()
        parser.feed(html)

        body_text = re.sub(r"\s+", " ", parser.body_text).strip()
        word_count, keyword_density = self._compute_keyword_density(body_text)

        return AnalysisResult(
            title=parser.title,
            meta_description=parser.meta_description,
            meta_keywords=parser.meta_keywords,
            headings=parser.headings,
            body_text=body_text,
            word_count=word_count,
            keyword_density=keyword_density,
            image_alts=parser.image_alts,
            canonical=parser.canonical,
            lang=parser.lang,
        )

    def _compute_keyword_density(
        self, text: str
    ) -> tuple[int, dict[str, float]]:
        words = re.findall(r"[a-zA-Z가-힣]+", text.lower())
        filtered = [w for w in words if w not in self._STOP_WORDS and len(w) > 2]
        total = len(words)
        if total == 0:
            return 0, {}
        counts = Counter(filtered)
        density = {word: round(count / total * 100, 2) for word, count in counts.most_common(20)}
        return total, density
