# EXAMPLES.md — 예제 프로젝트 매핑

> `260317_*` 프로젝트가 가이드의 어느 챕터·어느 단계 산출물인지의 매핑.
> 챕터 A.1 러닝 시나리오의 일부로 단계적으로 만들어지는 예시입니다.

---

## 매핑 표

| 프로젝트 | 챕터 출처 | Tier | 단계 | 한 줄 설명 |
|---|---|---|---|---|
| `260317_community_manager/` | A.1 · A.4 | L1 | Definition → Delivery | Discord/Slack 활동 모니터링 + 자동 응답 에이전트 |
| `260317_seo_optimizer/` | A.1 · A.10 | L1 | Definition → Delivery | SEO 키워드/메타 최적화 에이전트 |
| `260317_voice_clone_studio/` | A.1 · 6.2 | L1 | Discovery → Definition | 보이스 클론 + 음성 합성 워크플로우 |

## 각 프로젝트의 산출물 구조

```
260317_<name>/
├── project.yaml         # 메타: chapter, tier, stage, owner
├── requirements.txt
├── src/<package>/       # 구현
└── tests/               # 검증 (검증 사다리 2단)
```

## 단계별 의미 — A.1 러닝 시나리오

| 단계 | 산출물 |
|---|---|
| Discovery | 유저 인터뷰 합성 (Notion) + `samples/user-survey-results.csv` 활용 |
| Definition | PRD 이슈 (`.github/ISSUE_TEMPLATE/prd.yml`) + `project.yaml` `tier: L0` |
| Delivery  | `src/` 스캐폴딩 → `tier: L1` 업그레이드 |
| Growth    | KPI 정의 카드 + A/B 테스트 (`samples/ab-test-results.csv`) |

## Tier 정의

| Tier | 의미 | 결과물 |
|---|---|---|
| L0 | Concept | PRD 이슈 1건, `project.yaml` 메타만 |
| L1 | Prototype | `src/` 스캐폴딩 + 단위 테스트 |
| L2 | Production | 배포 + 모니터링 + KPI 추적 (미래) |

---

last_updated: 2026-05-19
