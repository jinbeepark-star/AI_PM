import pytest
from src.seo_optimizer.analyzer import SeoAnalyzer
from src.seo_optimizer.scorer import SeoScorer

GOOD_HTML = """<!DOCTYPE html>
<html lang="en">
<head>
  <title>Best Python SEO Guide for Developers</title>
  <meta name="description" content="A detailed guide to python seo tools and techniques for modern web developers building search-optimized sites.">
  <link rel="canonical" href="https://example.com/seo-guide">
</head>
<body>
  <h1>Python SEO Guide</h1>
  <h2>Introduction</h2>
  <p>Python python python python python python python python python python python
  python python python python python python python python python python python
  python python python python python python python python python python python
  python python python python python python python python python python python
  python python python python python python python python python python python
  python python python python python python python python python python python
  python python python python python python python python python python python
  python python python python python python python python python python python
  python python python python python python python python python python python
  python python python python python python python python python python python
  python python python python python python python python python python python
  python python python python python python python python python python python
  python python python python python python python python python python python
  python python python python python python python python python python python
  python python python python python python python python python python python
  python python python python python python python python python python python
  python python python python python python python python python python python
  python python python python python python python python python python python
  python python python python python python python python python python python
  python python python python python python python python python python python
  python python python python python python python python python python python
  python python python python python python python python python python python
  python python python python python python python python python python python
  python python python python python python python python python python python
  python python python python python python python python python python python
  python python python python python python python python python python python
  python python python python python python python python python python python
  python python python python python python python python python python python
  python python python python python python python python python python python</p>
  <img src="x.png" alt="diagram">
</body>
</html>"""

EMPTY_HTML = "<html><head></head><body></body></html>"


@pytest.fixture
def scorer():
    return SeoScorer()


@pytest.fixture
def analyzer():
    return SeoAnalyzer()


def test_total_score_in_range(scorer, analyzer):
    result = analyzer.analyze(GOOD_HTML)
    breakdown = scorer.score(result)
    assert 0 <= breakdown.total <= 100


def test_good_html_has_positive_total(scorer, analyzer):
    result = analyzer.analyze(GOOD_HTML)
    breakdown = scorer.score(result)
    assert breakdown.total > 50


def test_empty_html_scores_zero(scorer, analyzer):
    result = analyzer.analyze(EMPTY_HTML)
    breakdown = scorer.score(result)
    assert breakdown.total <= 10  # empty HTML: only image_alts can score (no images = 10)


def test_canonical_score_present(scorer, analyzer):
    result = analyzer.analyze(GOOD_HTML)
    breakdown = scorer.score(result)
    assert breakdown.canonical == scorer.CANONICAL_MAX


def test_missing_canonical_scores_zero(scorer, analyzer):
    html = "<html><head><title>Hi there world</title></head><body></body></html>"
    result = analyzer.analyze(html)
    breakdown = scorer.score(result)
    assert breakdown.canonical == 0


def test_title_score_optimal_length(scorer, analyzer):
    html = "<html><head><title>Optimal length title for SEO check</title></head><body></body></html>"
    result = analyzer.analyze(html)
    breakdown = scorer.score(result)
    assert breakdown.title == scorer.TITLE_MAX


def test_no_title_scores_zero(scorer, analyzer):
    result = analyzer.analyze(EMPTY_HTML)
    breakdown = scorer.score(result)
    assert breakdown.title == 0


def test_image_alts_perfect_score_when_no_images(scorer, analyzer):
    html = "<html><head></head><body><p>Text only content</p></body></html>"
    result = analyzer.analyze(html)
    breakdown = scorer.score(result)
    assert breakdown.image_alts == scorer.IMAGE_ALTS_MAX
