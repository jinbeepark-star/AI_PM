import json
import pytest
from src.seo_optimizer.analyzer import SeoAnalyzer
from src.seo_optimizer.scorer import SeoScorer
from src.seo_optimizer.reporter import SeoReporter

SAMPLE_HTML = """<!DOCTYPE html>
<html lang="ko">
<head>
  <title>파이썬 SEO 분석 가이드</title>
  <meta name="description" content="파이썬으로 SEO를 분석하는 방법을 상세히 설명합니다. 초보자도 쉽게 따라할 수 있는 단계별 안내입니다.">
  <link rel="canonical" href="https://example.com/guide">
</head>
<body>
  <h1>SEO 분석 소개</h1>
  <p>SEO 분석 내용입니다.</p>
  <img src="img.png">
</body>
</html>"""


@pytest.fixture
def report_data():
    analyzer = SeoAnalyzer()
    scorer = SeoScorer()
    reporter = SeoReporter()
    result = analyzer.analyze(SAMPLE_HTML)
    breakdown = scorer.score(result)
    report = reporter.build_report(result, breakdown, url="https://example.com/guide")
    return report, result, breakdown, reporter


def test_report_has_required_keys(report_data):
    report, *_ = report_data
    assert "url" in report
    assert "summary" in report
    assert "scores" in report
    assert "meta" in report
    assert "recommendations" in report


def test_report_url_set_correctly(report_data):
    report, *_ = report_data
    assert report["url"] == "https://example.com/guide"


def test_report_total_score_matches_breakdown(report_data):
    report, result, breakdown, _ = report_data
    assert report["summary"]["total_score"] == breakdown.total


def test_report_grade_is_string(report_data):
    report, *_ = report_data
    assert isinstance(report["summary"]["grade"], str)
    assert report["summary"]["grade"] in {"A+", "A", "B", "C", "D", "F"}


def test_to_json_valid_json(report_data):
    _, result, breakdown, reporter = report_data
    json_str = reporter.to_json(result, breakdown, url="https://example.com")
    parsed = json.loads(json_str)
    assert "summary" in parsed


def test_missing_image_alt_in_recommendations(report_data):
    report, *_ = report_data
    recs = report["recommendations"]
    assert any("alt" in r for r in recs)


def test_image_missing_alt_count(report_data):
    report, *_ = report_data
    assert report["images"]["missing_alt"] >= 1


def test_top_keywords_is_dict(report_data):
    report, *_ = report_data
    assert isinstance(report["top_keywords"], dict)


def test_grade_f_for_zero_score():
    reporter = SeoReporter()
    assert reporter._grade(0) == "F"
    assert reporter._grade(49) == "F"


def test_grade_a_plus_for_high_score():
    reporter = SeoReporter()
    assert reporter._grade(90) == "A+"
    assert reporter._grade(100) == "A+"
