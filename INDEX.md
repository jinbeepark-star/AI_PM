# INDEX.md — 지식 지도

> 본 레포에서 무엇이 어디에 있는지의 진입점.
> Claude Code는 작업 전 이 파일을 먼저 읽고 관련 파일만 펼친다.
>
> 형식: `경로` · owner · use · freshness

---

## 운영 (Root)

- `README.md` — owner: @kimsanguine — use: 첫 진입점, 학습 동선 — freshness: 2026-05
- `CLAUDE.md` — owner: @kimsanguine — use: Claude Code 행동 규칙 (8축) — freshness: 2026-05
- `INDEX.md` (본 파일) — owner: @kimsanguine — use: 지식 지도 — freshness: 2026-05
- `EXAMPLES.md` — owner: @kimsanguine — use: `260317_*` ↔ 챕터 매핑 — freshness: 2026-05
- `CHANGELOG.md` — owner: @kimsanguine — use: 버전 이력 — freshness: 2026-05
- `00-index.md` — owner: @kimsanguine — use: 챕터 목차(상세) — freshness: 2026-05

## Part 1 — Foundations

- `1.1-why-now.md` — use: AI 네이티브 PM의 명제
- `1.2-what-is-claude-code.md` — use: Claude Code 정의·비교
- `1.3-install-and-first-run.md` — use: 설치 + 첫 실행

## Part 2 — Basics

- `2.1-files-and-input.md` — use: 파일/이미지 입력, XML 태그 패턴
- `2.2-modes-and-depth.md` — use: effort · adaptive thinking
- `2.3-project-memory.md` — use: 메모리 계층 (global ↔ repo)
- `2.4-custom-subagents.md` — use: 서브에이전트 정의
- `2.5-agent-teams.md` — use: 멀티에이전트 + 병렬 세션
- `2.6-human-in-the-loop.md` — use: HITL · 검증 사다리

## Part 3 — Advanced

- `3.1-mcp-integration.md` — use: Notion / Linear / Slack / GitHub MCP
- `3.2-claude-md-deep-dive.md` — use: CLAUDE.md 8축 프레임워크
- `3.3-slash-commands.md` — use: 슬래시 커맨드 (4섹션 표준)
- `3.4-custom-skills.md` — use: SKILL.md 패키지
- `3.5-automation-n8n.md` — use: 외부 자동화

## Part 4 — Discovery

- `4.1-discovery-user-research.md`
- `4.2-discovery-competitive-analysis.md`

## Part 5 — Definition

- `5.1-definition-write-prd.md`
- `5.2-definition-product-strategy.md`

## Part 6 — Delivery

- `6.1-delivery-vibe-coding.md`
- `6.2-delivery-visual-assets.md`
- `6.3-delivery-github-deploy.md`

## Part 7 — Growth

- `7.1-growth-experiment-analysis.md`
- `7.2-growth-kpi-dashboard.md`
- `7.3-ai-observability.md`

## Part 8 — Strategy

- `8.1-ai-product-strategy.md`
- `8.2-growth-path.md`

## Appendix

- `A.1-running-scenario.md` — use: `260317_*` 프로젝트의 출처 시나리오
- `A.2-level3-exercises.md`
- `A.3-usecase-scenarios.md`
- `A.4-usecase-daily-briefing.md`
- `A.5-usecase-status-report.md`
- `A.6-usecase-battle-cards.md`
- `A.7-usecase-customer-personas.md`
- `A.8-usecase-investment-memo.md`
- `A.9-usecase-process-flowchart.md`
- `A.10-usecase-content-adaptation.md`

## 자산

- `templates/CLAUDE-md-starter.md` — use: 새 프로젝트용 CLAUDE.md 스타터
- `templates/commands/today.md` — `/today` 일일 브리핑
- `templates/commands/prd.md` — `/prd` PRD 생성
- `templates/commands/status.md` — `/status` 상태 보고서
- `skills/prd-generator/SKILL.md` — PRD 생성 스킬

## 샘플 데이터

- `samples/ab-test-results.csv` — use: 7.1 A/B 분석 실습
- `samples/competitor-data.json` — use: 4.2 경쟁사 분석 실습
- `samples/user-survey-results.csv` — use: 4.1 유저 리서치 실습

## 예제 프로젝트 (L0 → L1 스캐폴딩)

- `260317_community_manager/` — 자세한 매핑은 `EXAMPLES.md`
- `260317_seo_optimizer/`
- `260317_voice_clone_studio/`

## .github (메타)

- `.github/ISSUE_TEMPLATE/` — PRD / Discovery / RFC / UseCase / Bug
- `.github/PULL_REQUEST_TEMPLATE.md`
- `.github/labels.yml`
- `.github/CODEOWNERS`

## 외부 (참조)

- **Notion** — 자료 조사·인터뷰 원본·실험 로그 (SoT, 정책은 향후 명문화)
- **kimsanguine/hplan** — Product Build Gate (자매 PM 도구)
- **kimsanguine/AI_Human** — AI 입문 100일 (시리즈 1단계)
- **kimsanguine/AI_Engineer** — AI Agent 100개 직접 구현 (시리즈 2단계)
- **kimsanguine/ai-prompts-playbook** — 3-Layer 인지 프레임워크 (참조)

---

last_updated: 2026-05-19
