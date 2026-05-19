# Changelog

본 가이드의 변경 이력. [Keep a Changelog](https://keepachangelog.com/) 형식.

---

## [v1.1] — 2026-05-19 (P0: Dogfood)

### Added
- 루트 `CLAUDE.md` — 본 레포의 dogfood. 8축 프레임워크 (Project / Conventions / Workflows / Tools / Voice / Examples / Escalation / Knowledge-Map).
- 루트 `INDEX.md` — 주석 달린 지식 지도 (경로 · 소유자 · 용도 · 신선도).
- 루트 `EXAMPLES.md` — `260317_*` 예제 프로젝트와 챕터 매핑.
- `.github/` — ISSUE_TEMPLATE (PRD / Discovery / RFC / UseCase / Bug), PR 템플릿, `labels.yml`, `CODEOWNERS`.
- 관련 프로젝트에 `kimsanguine/hplan` 추가.

### Changed
- README — `claude-opus-4-7` 기준 배지 + 부제 추가, "컨텍스트 인프라 4요소" 박스로 인트로 교체, "권장 시작 트랙(레벨별)" 표로 교체, 프로젝트 구조 박스 갱신, 빠른 시작에 `INDEX.md` / `CLAUDE.md` 진입점 추가.
- README 인코딩 깨짐 일괄 수정 (`ǭ�지`, `보여:니다`, `Part 18`, `방법론,��니다`, `학슰`, `(중급))`, `기벘`, `학습`, `학습`).
- 관련 프로젝트의 단계 라벨을 상단 학습 경로(AI_Human → AI_Engineer → AI_PM)와 정합화.

### Planned (v1.2 / v1.3)
- 폴더 재편 (`docs/partN/...`)
- 신규 챕터: **2.7 Hooks** · **3.2.1 패턴 카탈로그** · **3.2.2 4.7 시대 CLAUDE.md** · **3.6 Claude Code on the web**
- 자산 보강: `templates/claude-home/`, `templates/hooks/`, `.claude/agents/`, 슬래시 커맨드 6개, 스킬 4개
- 운영 문서: `docs/operations/sot-policy.md`, `docs/operations/closed-loop.md`
- CI: lint / links / frontmatter

---

## [v1.0] — 2026-04 (기존)

### Added
- Part 1–8 본문 + Appendix A.1–A.10
- `templates/commands/today.md`, `prd.md`, `status.md`
- `skills/prd-generator/`
- `samples/` 3종 + `260317_*` 예제 프로젝트 3개
