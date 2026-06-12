---
type: rule
project: Model Quality Auditor
status: active
node_type: procedure
tags:
  - mqa
  - knowledge-capture
created: 2026-05-20
---

# Knowledge Capture Rules

## 기록해야 하는 순간

- 오류를 해결했을 때
- Revit API 사용 여부가 바뀌었을 때
- Store 문구와 실제 기능이 달라졌을 때
- Addin Dashboard 병합 판단에 영향을 주는 결과가 나왔을 때
- Qwen 초안이 실제 테스트에서 틀렸을 때
- 반복 가능한 테스트 절차를 발견했을 때

## 좋은 기록의 조건

1. 무엇이 문제였는지 한 문장으로 설명한다.
2. 원인과 수정 방법을 분리한다.
3. 다음에 같은 문제를 막는 기준을 남긴다.
4. 관련 결정, 테스트, 오류 노드를 링크한다.
5. 오래 살아남을 노트라면 [[Semantic Node Edge Taxonomy]]에 따라 `node_type`과 관계를 붙인다.

## 오류 오답노트 기준

오류 기록은 해결 여부보다 재사용 가능성을 기준으로 작성한다.

| 구분 | 기록 기준 |
|---|---|
| 증상 | 로그, 화면, 빌드 메시지, 모델 조건을 구체적으로 남긴다. |
| 원인 | 추정과 확정을 구분하고, 확정되지 않은 내용은 `가설`로 표시한다. |
| 수정 | 실제 변경한 파일, 설정, 명령, 판단 기준을 남긴다. |
| 검증 | 로컬 검증과 Revit API 가능 환경 검증을 구분한다. |
| 배운 점 | 다음 개발자가 바로 적용할 수 있는 문장으로 남긴다. |
| 재발 방지 | 테스트, 체크리스트, 문서 개정, 제품 정책 중 하나로 연결한다. |

반복되는 오류는 [[Lessons Learned Matrix]]에 승격하고, 제품 정책이나 판매 문구에 영향을 주면 [[Decision Log Index]]에도 연결한다.

## 연결

- [[Semantic Node Edge Taxonomy]]
- [[Development Logging SOP]]
- [[Error Fix Index]]
- [[Decision Log Index]]
- [[Lessons Learned Matrix]]
