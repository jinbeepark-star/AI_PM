import pytest
from src.seo_optimizer.analyzer import SeoAnalyzer

FULL_HTML = """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>Best Python SEO Tools in 2024</title>
  <meta name="description" content="A comprehensive guide to Python-based SEO analysis tools for developers and marketers in 2024.">
  <meta name="keywords" content="python, seo, tools, analysis">
  <link rel="canonical" href="https://example.com/python-seo">
</head>
<body>
  <h1>Python SEO Tools Overview</h1>
  <p>Python is widely used for seo analysis and automation. Many python developers rely on
  python libraries for seo tasks. Python makes it easy to parse html, extract keywords,
  and generate seo reports. This python guide covers the best seo tools available.</p>
  <h2>Why Use Python for SEO?</h2>
  <p>Python provides excellent libraries for web scraping, data processing, and automation,
  making it ideal for seo workflows.</p>
  <img src="chart.png" alt="SEO performance chart">
  <img src="logo.png" alt="Python logo">
</body>
</html>"""

MINIMAL_HTML = "<html><head></head><body><p>Hello world</p></body></html>"

MISSING_ALT_HTML = """<html><body>
<img src="a.png" alt="described">
<img src="b.png">
<img src="c.png" alt="">
</body></html>"""


@pytest.fixture
def analyzer():
    return SeoAnalyzer()


def test_extracts_title(analyzer):
    result = analyzer.analyze(FULL_HTML)
    assert result.title == "Best Python SEO Tools in 2024"


def test_extracts_meta_description(analyzer):
    result = analyzer.analyze(FULL_HTML)
    assert result.meta_description is not None
    assert "comprehensive" in result.meta_description


def test_extracts_h1(analyzer):
    result = analyzer.analyze(FULL_HTML)
    assert result.headings["h1"] == ["Python SEO Tools Overview"]


def test_extracts_h2(analyzer):
    result = analyzer.analyze(FULL_HTML)
    assert len(result.headings["h2"]) == 1
    assert "Python" in result.headings["h2"][0]


def test_keyword_density_positive(analyzer):
    result = analyzer.analyze(FULL_HTML)
    assert "python" in result.keyword_density
    assert result.keyword_density["python"] > 0


def test_word_count_positive(analyzer):
    result = analyzer.analyze(FULL_HTML)
    assert result.word_count > 0


def test_canonical_extracted(analyzer):
    result = analyzer.analyze(FULL_HTML)
    assert result.canonical == "https://example.com/python-seo"


def test_lang_extracted(analyzer):
    result = analyzer.analyze(FULL_HTML)
    assert result.lang == "en"


def test_image_alts_count(analyzer):
    result = analyzer.analyze(FULL_HTML)
    assert len(result.image_alts) == 2
    assert all(alt for alt in result.image_alts)


def test_missing_alt_detected(analyzer):
    result = analyzer.analyze(MISSING_ALT_HTML)
    assert len(result.image_alts) == 3
    missing = sum(1 for a in result.image_alts if not a or not a.strip())
    assert missing == 2


def test_minimal_html_no_title(analyzer):
    result = analyzer.analyze(MINIMAL_HTML)
    assert result.title is None
    assert result.meta_description is None
    assert result.canonical is None
