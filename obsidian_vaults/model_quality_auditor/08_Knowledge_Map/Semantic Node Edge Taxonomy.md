---
type: rule
project: Model Quality Auditor
status: active
node_type: concept
tags:
  - mqa
  - knowledge-map
  - semantic-taxonomy
created: 2026-05-30
---

# Semantic Node Edge Taxonomy

이 문서는 옵시디언 링크를 단순한 참조가 아니라 성장하는 사고 구조로 쓰기 위한 최소 분류 규칙이다.

## 노드 유형

| node_type | 색상 | 쓸 때 | 예시 |
|---|---|---|---|
| concept | `#2563eb` | 정의, 개념, 기준, 프레임을 설명할 때 | IFC, dry-run, 모델 품질 점수 |
| procedure | `#059669` | 반복 가능한 절차, 체크리스트, 워크플로를 남길 때 | Store 제출 절차, QA smoke test |
| event | `#f59e0b` | 특정 시점의 사건, 테스트 결과, 회의, 배포 기록을 남길 때 | 2026-05-30 빌드 검증 |
| claim | `#dc2626` | 판단, 가설, 결론, 제품/전략 주장을 남길 때 | dry-run은 MVP 신뢰도를 높인다 |
| actor | `#6b7280` | 사람, 조직, 시스템, 소프트웨어, 역할을 다룰 때 | Autodesk Store, Qwen, Addin Dashboard |

## 엣지 유형

| 관계 | 색상 | 방향 | 의미 |
|---|---|---|---|
| supports | `#16a34a` | A -> B | A가 B의 근거가 된다. |
| refutes | `#dc2626` | A -> B | A가 B를 반박하거나 약화한다. |
| premise_of | `#7c3aed` | A -> B | A가 B가 성립하기 위한 전제다. |
| specifies | `#2563eb` | A -> B | A가 B를 더 구체적인 사례/요건으로 만든다. |
| expands | `#0891b2` | A -> B | A가 B의 범위나 가능성을 넓힌다. |
| refines | `#d97706` | A -> B | A가 B를 더 정확한 형태로 수정한다. |
| similar_to | `#64748b` | A -- B | A와 B가 의미, 구조, 용도가 유사하다. |
| triggers | `#db2777` | A -> B | A가 B를 발생시키거나 검토하게 만든다. |
| about | `#6b7280` | A -> B | A가 B를 주제로 다룬다. |
| asserts | `#4f46e5` | A -> B | 주체 A가 주장 B를 제기한다. |

## 색상 적용 우선순위

1. Canvas에서 관계 의미가 명확한 선은 엣지 유형 색상을 우선한다.
2. MOC나 인덱스에서 노드를 분류해 보여주는 선은 대상 `node_type` 색상을 쓴다.
3. Obsidian 기본 Graph View는 엣지 색상을 직접 구분하지 못하므로, 노드는 Graph color group으로, 선은 Canvas와 본 문서 범례로 관리한다.

## 작성 규칙

1. 오래 살아남을 노트에만 `node_type`을 붙인다.
2. 임시 메모는 억지로 분류하지 않고, 승격할 때만 분류한다.
3. `claim` 노트는 최소 하나의 `supports`, `refutes`, `premise_of` 중 하나를 갖도록 노력한다.
4. `procedure` 노트는 관련 `event`와 연결해 실제 실행 기록을 남긴다.
5. `actor` 노트는 `asserts`, `triggers`, `about` 관계로 행동과 주장을 분리한다.
6. `similar_to`는 의미 동질, 동의어, 표현 차이를 묶는 용도로 쓴다.

## 본문 관계 섹션 표준

```markdown
## 관계

### Supports
- [[...]]

### Refutes
- [[...]]

### Premise Of
- [[...]]

### Specifies
- [[...]]

### Expands
- [[...]]

### Refines
- [[...]]

### Similar To
- [[...]]

### Triggers
- [[...]]

### About
- [[...]]

### Asserts
- [[...]]
```

## YAML 선택 필드

Dataview로 조회할 노트는 아래 필드를 선택적으로 사용한다. 본문 관계 섹션이 더 읽기 쉬우면 본문만 써도 된다.

```yaml
node_type: concept
supports: []
refutes: []
premise_of: []
specifies: []
expands: []
refines: []
similar_to: []
triggers: []
about: []
asserts: []
```

## 연결

- [[Knowledge Capture Rules]]
- [[Semantic Knowledge Index]]
- [[Organizational Knowledge Hierarchy]]
- [[Lessons Learned Matrix]]
