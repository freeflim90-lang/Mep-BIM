# Model Quality Auditor Obsidian Vault

이 vault는 `Model Quality Auditor` 별도 프로젝트 개발 과정에서 발생하는 오류, 수정, 의사결정, Revit API 테스트 게이트, Qwen 초안 결과를 연결 지식으로 남기기 위한 공간이다.

시작 문서:

- [[Model Quality Auditor - Knowledge Map]]
- [[Organizational Knowledge Hierarchy]]
- [[Development Logging SOP]]
- [[Error Fix Index]]
- [[Decision Log Index]]
- [[Revit API Test Gate Index]]
- [[Qwen Development Boundary]]

시각화:

- 계층형 MOC: [[Organizational Knowledge Hierarchy]]
- Obsidian Graph View에서 `path:03_Errors_Fixes`, `path:04_Decisions`, `path:05_Revit_API_Gates`를 켜서 확인한다.
- Canvas 보기: [[Model Quality Auditor Knowledge Canvas.canvas]]
- 브라우저 그래프: `Assets/mqa_knowledge_graph.html`

그래프 재생성:

```bash
source .dev-venv/bin/activate && python scripts/mqa_obsidian_tools.py graph
```
