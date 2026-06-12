---
type: index
project: Model Quality Auditor
status: active
node_type: concept
tags:
  - mqa
  - errors
  - fixes
created: 2026-05-20
---

# Error Fix Index

개발 중 발생한 오류와 수정 기록을 모으는 인덱스다. 이 영역은 단순 장애 기록이 아니라 `오답노트`로 운영하며, 같은 실수를 다시 줄이고 Revit API 가능 환경에서 이어서 검증할 수 있도록 만든다.

## 오류 기록

- [[ERR-2026-05-20-001 Revit API Boundary Risk]]

## 기록 기준

오류가 발생하면 다음 조건 중 하나라도 해당할 때 반드시 기록한다.

- 15분 이상 원인 파악이 필요한 오류
- Revit API, Addin Dashboard 병합, Store 패키징과 관련된 오류
- 같은 유형으로 반복될 가능성이 있는 오류
- Qwen 또는 AI 초안이 실제 개발 조건과 맞지 않았던 오류
- 임시 수정으로 해결했지만 추후 재검증이 필요한 오류

## 오답노트 필수 항목

| 항목 | 기준 |
|---|---|
| 한 줄 요약 | 다음에 검색할 사람이 바로 이해할 문장 |
| 증상 | 화면, 로그, 빌드 메시지, 동작 차이 |
| 재현 절차 | 같은 오류를 다시 만들 수 있는 순서 |
| 원인 | 추정이 아니라 확인된 원인 중심 |
| 수정 | 실제 변경한 코드, 설정, 문서 |
| 배운 점 | 다음 프로젝트에 재사용할 원칙 |
| 재발 방지 | 테스트, 체크리스트, 설계 기준 |
| 연결 | 관련 결정, 테스트, API 게이트, 문서 링크 |

## 분류 태그

- `#error/build`
- `#error/revit-api`
- `#error/report`
- `#error/packaging`
- `#error/store`
- `#fix/refactor`
- `#fix/test`
- `#fix/documentation`

## 연결

- [[Development Logging SOP]]
- [[Qwen Development Boundary]]
- [[Revit API Test Gate Index]]
- [[Build Test Index]]
- [[Knowledge Capture Rules]]
- [[Lessons Learned Matrix]]
