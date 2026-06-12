---
type: index
project: Model Quality Auditor
status: active
node_type: concept
tags:
  - mqa
  - knowledge-map
  - semantic-index
created: 2026-05-30
---

# Semantic Knowledge Index

`node_type`이 붙은 노트를 모아 보는 색인이다. Dataview가 켜져 있으면 아래 표가 자동으로 갱신된다.

```dataview
TABLE node_type, status, tags
FROM ""
WHERE node_type
SORT node_type ASC, file.name ASC
```

## 운영 체크

- `claim`은 근거, 반박, 전제 중 하나와 연결한다.
- `procedure`는 실제 실행 기록인 `event`와 연결한다.
- `concept`는 정의가 흐려질 때 `similar_to`나 `specifies`로 정리한다.
- `actor`는 주장 자체가 아니라 주장 노트와 `asserts`로 연결한다.

## 연결

- [[Semantic Node Edge Taxonomy]]
- [[Model Quality Auditor - Knowledge Map]]
