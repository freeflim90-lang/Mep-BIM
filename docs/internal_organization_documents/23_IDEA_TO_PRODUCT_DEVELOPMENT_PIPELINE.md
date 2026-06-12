# LUA BIM LAB
# 아이디어 발굴-상품화-개발 큐 전환 운영 기준

━━━━━━━━━━━━━━━━━━━━

문서번호: LBL-ORG-023  
문서상태: 내부 기준 초안  
작성일: 2026-05-21  
배포등급: Internal Only  
적용범위: 아이디어발굴, 전략기획, 견적심사원, CFO, CEO, 브랜드마케팅, 요구사항분석, 프로그램개발, Qwen_Coder_8B, QA_테스터, 빌드검증, 제품패키징

## 1. 목적

본 문서는 현재 개발 큐의 기능 내재화가 종료된 후, LUA BIM LAB 조직이 자체적으로 다음 제품 아이디어를 발굴하고 상품화 우선순위를 선정한 뒤 개발 순서를 확정하는 절차를 정의한다.

핵심 원칙은 `멈추지 않는 상품화 파이프라인`이다. 하나의 기능 내재화가 끝나면 아이디어발굴 조직이 다음 후보를 제안하고, 전략/견적/재무/브랜드/개발 조직이 검토하여 Qwen 개발 큐로 넘긴다.

## 2. 트리거

| 트리거 | 판단 기준 | 후속 조치 |
|---|---|---|
| 현재 Qwen 큐 완료 | `config/qwen_product_draft_queue.json`의 모든 task가 완료 | 아이디어 발굴 회의 자동 실행 |
| 제품 기능 내재화 완료 | Phase 1 기능의 백엔드 계약, 테스트, 문서화 완료 | 다음 상품 후보 우선순위 평가 |
| 산업 브리핑 반복 신호 | 동일 주제 3회 이상 반복 | 아이디어 후보 등록 |
| 고객/현장 반복 요청 | 동일 수작업/오류/보고 요구 반복 | MVP 후보 등록 |
| Store/경쟁 제품 공백 발견 | 고객 문제는 있으나 기존 해결책이 약함 | 상품화 후보 등록 |

## 3. 조직 협업 흐름

| 단계 | 주관 | 협업 | 산출물 |
|---:|---|---|---|
| 1 | 아이디어발굴 | 지식 큐레이션, 고객지원 CS | 아이디어 후보 목록 |
| 2 | 전략기획 | CEO, 브랜드마케팅 | MVP/Pro 범위, Store 포지션 |
| 3 | 견적심사원 | 프로그램개발, QA_테스터 | 개발 시간, 검증 시간, 비용 추정 |
| 4 | CFO | 글로벌_매출관리원 | MRR, 가격, 회수 기간 |
| 5 | CEO | 조율차장 | 개발 우선순위 승인 |
| 6 | 요구사항분석 | 프로그램개발, Qwen_Coder_8B | 개발 큐 task 분해 |
| 7 | Qwen_Coder_8B | QA_테스터, 빌드검증 | 초안 개발, Telegram 중간보고 |
| 8 | 제품패키징 | 배포문서, 스토어심사 | Store 패키징 준비 |

## 4. 상품화 우선순위 산식

| 항목 | 점수 기준 |
|---|---|
| 반복 빈도 | 고객/현장/내부에서 반복되는가 |
| 시간 절감 | 1회당 30분 이상 절감 가능한가 |
| 오류 감소 | 납품, 시공, 보고 오류를 줄이는가 |
| Store 적합성 | Autodesk Store 검색/판매 키워드와 맞는가 |
| 구현 가능성 | Revit/Navisworks API 위험이 낮거나 순수 로직으로 시작 가능한가 |
| 지원 부담 | 고객지원과 유지보수 부담이 낮은가 |
| 수익성 | 월 순매출과 회수 기간이 합리적인가 |

우선순위 점수는 `수익성 + Store 적합성 + 시간 절감 + 구현 가능성 - 리스크 - 지원 부담` 기준으로 계산한다.

## 5. Qwen 개발 큐 전환 기준

선정된 아이디어는 바로 구현하지 않고 다음 형태로 `config/qwen_product_draft_queue.json`에 전환한다.

| 큐 항목 | 기준 |
|---|---|
| product | 제품명 |
| selected_item | 선정된 상품화 아이템 |
| source_documents | 관련 표준문서, 지식베이스, 제품문서 |
| tasks | 도메인 모델, 설정/스키마, dry-run, 리포트, 테스트, Revit API 게이트, 패키징 계약 순서 |

Qwen은 초안 작성 후 `obsidian_vaults/model_quality_auditor/06_Qwen_Drafts/`에 기록하고 Telegram으로 중간보고한다.

## 6. 승인 규칙

- Revit API write 작업은 실제 Revit 환경 검증 전 확정하지 않는다.
- 개인정보, 외부 통신, 라이선스, 결제, Store 제출 문구는 보안/법무/스토어심사 검토 전 확정하지 않는다.
- 경쟁 제품에서 확인한 기능은 범위 참고로만 사용하고 명칭, UI, 아이콘, 문구, 구현은 복제하지 않는다.
- 최고지배자의 명시 지시가 없는 경우, 아이디어발굴은 상위 3개 후보만 보고한다.

## 7. 실행 도구

```bash
source .dev-venv/bin/activate && python scripts/idea_to_product_pipeline.py
```

현재 개발 큐가 완료되지 않았더라도 후보 보고서를 강제로 생성:

```bash
source .dev-venv/bin/activate && python scripts/idea_to_product_pipeline.py --force
```

선정된 1순위 후보를 다음 Qwen 큐 초안 파일로 생성:

```bash
source .dev-venv/bin/activate && python scripts/idea_to_product_pipeline.py --force --promote
```

## 8. 관련 문서

- `knowledge/10_agents/90_확장에이전트/아이디어발굴.md`
- `knowledge/10_agents/90_확장에이전트/전략기획.md`
- `knowledge/10_agents/90_확장에이전트/프로그램개발.md`
- `knowledge/10_agents/06_스토어상용화팀/제품패키징.md`
- `config/qwen_product_draft_queue.json`
- `scripts/qwen_product_draft_runner.py`
