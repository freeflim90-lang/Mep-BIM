# LUA BIM LAB
# Model Quality Auditor Obsidian 지식관리 기준

문서번호: LBL-REV-MQA-014  
문서상태: 내부 운영 기준  
작성일: 2026-05-20  
배포등급: Internal Only

---

## 1. 목적

본 문서는 `Model Quality Auditor` 별도 프로젝트 개발 과정에서 발생하는 오류, 수정, 의사결정, Revit API 테스트 결과를 Obsidian 지식 그래프로 관리하기 위한 기준이다.

---

## 2. Vault 위치

`obsidian_vaults/model_quality_auditor`

Obsidian에서 `Open folder as vault`로 위 폴더를 열면 된다.

---

## 3. 핵심 운영 방식

| 기록 유형 | 위치 | 목적 |
|---|---|---|
| 개발 로그 | `02_Development_Log/` | 일일 작업과 변경 파일 기록 |
| 오류/수정 | `03_Errors_Fixes/` | 증상, 원인, 수정, 재발 방지 기록 |
| 의사결정 | `04_Decisions/` | 제품/기술/패키징 결정 기록 |
| Revit API 게이트 | `05_Revit_API_Gates/` | 실제 Revit 환경에서 검증할 항목 관리 |
| Qwen 초안 | `06_Qwen_Drafts/` | 로컬 초안과 검증 상태 관리 |
| 빌드/테스트 | `07_Build_Test/` | 빌드, 설치, smoke test 증빙 관리 |

Qwen 초안은 조직에서 선정한 수익형 아이템인 `Model Quality Auditor`를 기준으로 순차 큐 방식으로 운영한다.

| 항목 | 기준 |
|---|---|
| 큐 설정 | `config/qwen_product_draft_queue.json` |
| 실행 스크립트 | `scripts/qwen_product_draft_runner.py` |
| 상태 파일 | `obsidian_vaults/model_quality_auditor/06_Qwen_Drafts/qwen_product_draft_state.json` |
| 백엔드 API | `GET /api/qwen-product-drafts/status`, `POST /api/qwen-product-drafts/next` |
| 중간보고 | 초안 완료 후 Telegram으로 완료 작업, 기록 위치, 다음 작업 전송 |

실제 실행은 로컬 Qwen이 활성화된 상태에서 수행한다.

```bash
source .dev-venv/bin/activate && LOCAL_CODER_ENABLED=true python scripts/qwen_product_draft_runner.py
```

---

## 4. 시각화

| 방식 | 파일 |
|---|---|
| 계층형 MOC | `08_Knowledge_Map/Organizational Knowledge Hierarchy.md` |
| Obsidian Graph View | Vault 기본 Graph 설정 |
| Obsidian Canvas | `09_Canvas/Model Quality Auditor Knowledge Canvas.canvas` |
| 브라우저 HTML 그래프 | `Assets/mqa_knowledge_graph.html` |

HTML 그래프는 다음 명령으로 재생성한다.

```bash
source .dev-venv/bin/activate && python scripts/mqa_obsidian_tools.py graph
```

HTML 그래프는 관계망만 보여주는 화면이 아니라 좌측 계층 패널을 함께 제공한다. 사용자는 폴더별 하위 지식, 검색, 선택 노드의 경로를 확인하고, Obsidian 내부에서는 계층형 MOC를 기준으로 필요한 자료를 찾는다.

---

## 5. 새 기록 생성

```bash
source .dev-venv/bin/activate && python scripts/mqa_obsidian_tools.py new error "오류 제목"
source .dev-venv/bin/activate && python scripts/mqa_obsidian_tools.py new decision "결정 제목"
source .dev-venv/bin/activate && python scripts/mqa_obsidian_tools.py new devlog "오늘 작업 요약"
source .dev-venv/bin/activate && python scripts/mqa_obsidian_tools.py new gate "Revit API 검증 항목"
```

---

## 6. 운영 원칙

1. Qwen이 작성한 내용은 검증 상태를 표시한다.
2. Revit API가 필요한 내용은 실제 Revit 환경 테스트 전 확정하지 않는다.
3. 오류 기록은 원인과 재발 방지를 반드시 포함한다.
4. Addin Dashboard 병합에 영향을 주는 기록은 `Addin Dashboard Merge Plan`과 연결한다.
5. Store 문구와 실제 기능이 달라지는 경우 의사결정 로그를 남긴다.

---

## 7. 오류 오답노트 운영 기준

오류 기록은 단순 장애 처리 로그가 아니라 제품 개발의 오답노트로 운영한다. 목적은 같은 오류를 다시 줄이고, Revit API 가능 환경에서 이어서 검증할 때 판단 근거를 빠르게 찾게 하는 것이다.

| 항목 | 작성 기준 |
|---|---|
| 한 줄 요약 | 검색 가능한 문제 문장 |
| 증상 | 빌드 메시지, 실행 화면, 로그, 모델 조건 |
| 재현 절차 | 같은 오류를 다시 만들 수 있는 순서 |
| 원인 | 추정과 확정을 구분 |
| 수정 | 실제 변경한 파일, 설정, 명령 |
| 검증 | 로컬 검증과 Revit API 환경 검증 분리 |
| 배운 점 | 다음 개발에 적용할 원칙 |
| 재발 방지 | 테스트, 체크리스트, 문서 개정, 정책 변경 |

반복되는 오류 패턴은 `08_Knowledge_Map/Lessons Learned Matrix.md`에 승격한다. 제품 기능 범위, Store 문구, Addin Dashboard 병합 방향에 영향을 주면 `04_Decisions`에도 기록한다.

오류 노트 생성 명령:

```bash
source .dev-venv/bin/activate && python scripts/mqa_obsidian_tools.py new error "오류 제목"
```
