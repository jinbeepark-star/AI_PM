from __future__ import annotations

import argparse
import sys

from .analyzer import SeoAnalyzer
from .scorer import SeoScorer
from .reporter import SeoReporter

_SAMPLE_HTML = """<!DOCTYPE html>
<html lang="ko">
<head>
  <meta charset="UTF-8">
  <title>SEO Optimizer 데모 페이지</title>
  <meta name="description" content="SEO Optimizer는 웹 페이지의 SEO 점수를 자동으로 분석하고 최적화 방안을 제안합니다.">
  <link rel="canonical" href="https://example.com/demo">
</head>
<body>
  <h1>SEO 자동 분석 도구 소개</h1>
  <p>이 도구는 HTML 문서를 분석하여 검색 최적화 점수를 산출합니다.
  키워드 밀도, 메타태그 존재 여부, 헤딩 구조 등을 검사합니다.</p>
  <h2>주요 기능</h2>
  <p>키워드 분석, 메타태그 최적화, 콘텐츠 SEO 점수 산출 기능을 제공합니다.</p>
  <img src="demo.png" alt="SEO 분석 결과 화면">
</body>
</html>"""


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        prog="seo_optimizer",
        description="HTML SEO 자동 분석 도구",
    )
    parser.add_argument("--html", help="분석할 HTML 파일 경로")
    parser.add_argument("--url", default="", help="출력 리포트에 표시할 URL")
    parser.add_argument("--json", action="store_true", help="JSON 형식으로 출력")
    args = parser.parse_args(argv)

    if args.html:
        try:
            with open(args.html, encoding="utf-8") as f:
                html = f.read()
        except OSError as exc:
            print(f"오류: {exc}", file=sys.stderr)
            return 1
    else:
        html = _SAMPLE_HTML

    analyzer = SeoAnalyzer()
    scorer = SeoScorer()
    reporter = SeoReporter()

    result = analyzer.analyze(html)
    breakdown = scorer.score(result)

    if args.json:
        print(reporter.to_json(result, breakdown, url=args.url))
    else:
        report = reporter.build_report(result, breakdown, url=args.url)
        print(f"[SEO Optimizer]")
        print(f"URL       : {report['url'] or '(없음)'}")
        print(f"총점      : {report['summary']['total_score']} / 100  ({report['summary']['grade']})")
        print(f"단어 수   : {report['summary']['word_count']}")
        print()
        print("항목별 점수:")
        for key, val in report["scores"].items():
            print(f"  {key:<20}: {val}")
        print()
        if report["recommendations"]:
            print("개선 권고사항:")
            for rec in report["recommendations"]:
                print(f"  - {rec}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
