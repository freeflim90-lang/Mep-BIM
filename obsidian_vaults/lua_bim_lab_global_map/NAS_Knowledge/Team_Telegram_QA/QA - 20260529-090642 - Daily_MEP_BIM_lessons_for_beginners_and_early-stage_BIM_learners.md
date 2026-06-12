---
type: team-telegram-qa
category: 팀원간질문
domain: BIM실무
agent: 지식업데이트
date: 2026-05-29
status: answered-pending-feedback
tags:
  - QA
  - team-telegram
  - knowledge-loop
  - BIM실무
---

# QA - Daily MEP BIM lessons for beginners and early-stage BIM learners.

## 질문

> 요청자: @FreeFilmer ([LONG_ID_MASKED])
> 수집일: 2026-05-29 09:06:42
> 담당 지식: [[지식업데이트]]

Daily MEP BIM lessons for beginners and early-stage BIM learners.

## 답변

[📚 지식 베이스 (score 40)]

Daily MEP BIM 교육에서 초보자와 초기 단계 BIM 학습자를 위한 주제로는 'Dynamo 스크립트를 활용한 자동 객실 배치'가 좋습니다. 이 주제에서는 층과 호수 번호 부여 로직을 정확하게 설정하여 중복된 호수가 발생하지 않도록 하는 방법을 다룹니다.

예를 들어, Dynamo 스크립트로 호텔 객실을 자동 배치할 때 1101호가 두 개 생성되는 오류를 해결하는 방법을 배울 수 있습니다. 이를 위해 다음과 같은 단계를 따르면 됩니다:

1. **Revit API 사용**: `Autodesk.Revit.DB` 모듈을 통해 Revit 문서와 요소에 접근합니다.
2. **DocumentManager 사용**: 현재 작업 중인 Revit 문서를 가져옵니다.
3. **호텔 객실 Family Symbol, 층 리스트, 객실 수 설정**: 입력으로 받은 값들을 정의합니다.
4. **TransactionManager 사용**: Dynamo 스크립트 내에서 트랜잭션을 관리하여 변경 사항을 적용하고 롤백할 수 있습니다.

이러한 과정을 통해 MEP BIM 초보자들이 실무에서 자주 발생하는 문제를 해결할 수 있는 실용적인 기술을 익힐 수 있습니다.

## 근거 문서

- `data/knowledge_base/시설유형/호텔_숙박시설_BIM.md` · score `40`
- `data/knowledge_base/시설유형/오피스_업무시설_BIM.md` · score `40`
- `data/knowledge_base/시설유형/아파트_공동주택_BIM.md` · score `40`
- `docs/starter_plan_application_form_spec.md` · score `40`

## 지식화 판단

- [ ] 반복 질문 여부 확인
- [ ] 표준문서/교육자료/FAQ 승격 필요 여부 확인
- [ ] 답변 부족 시 지식 공백으로 전환
- [ ] 개인정보, 고객명, 프로젝트명, 계약정보 제거 확인

## 연결

- [[MOC - Team Telegram QA]]
- [[MOC - QA Index]]
- [[24_TEAM_TELEGRAM_KNOWLEDGE_REQUEST_LOOP]]
- [[21_KNOWLEDGE_CURATION_INTELLIGENCE_CELL]]
- [[Global Knowledge Map]]
