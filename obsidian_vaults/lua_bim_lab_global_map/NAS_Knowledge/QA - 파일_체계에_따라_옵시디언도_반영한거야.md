---
type: qa-note
category: Claude대화
domain: 기타
date: 2026-06-13
status: verified
tags:
  - QA
  - 기타
---

# QA - 파일 체계에 따라 옵시디언도 반영한거야?

## 질문
> **카테고리:** Claude대화 | **날짜:** 2026-06-13
> **출처:** Claude Code 세션

파일 체계에 따라 옵시디언도 반영한거야?

## 답변

좋은 지적입니다. 볼트 폴더 자체는 의도적으로 이동하지 않았고(Obsidian 앱이 경로를 저장), 인덱스 볼트를 만드는 [build_global_obsidian_map.py](scripts/build_global_obsidian_map.py)는 새 경로 기준으로 수정해뒀지만 **볼트 재생성은 아직 안 돌렸습니다**. 즉 지금 Obsidian 글로벌 맵의 인덱스 노트들은 옛 경로(data/knowledge_base/...)를 가리키고 있습니다. 지금 반영하겠습니다 — 새 지식 층(30_intake~60_public, products)의 카테고리도 추가해서 재생성합니다.

## 관련 자료

- [[MOC - Q&A Knowledge Base]]

## 연결

- [[Global Knowledge Map]]

---

## 질문 (추가 2026-06-13)
> **카테고리:** Claude대화 | **날짜:** 2026-06-13
> **출처:** Claude Code 세션

파일 체계에 따라 옵시디언도 반영한거야?

## 답변

좋은 지적입니다. 볼트 폴더 자체는 의도적으로 이동하지 않았고(Obsidian 앱이 경로를 저장), 인덱스 볼트를 만드는 [build_global_obsidian_map.py](scripts/build_global_obsidian_map.py)는 새 경로 기준으로 수정해뒀지만 **볼트 재생성은 아직 안 돌렸습니다**. 즉 지금 Obsidian 글로벌 맵의 인덱스 노트들은 옛 경로(data/knowledge_base/...)를 가리키고 있습니다. 지금 반영하겠습니다 — 새 지식 층(30_intake~60_public, products)의 카테고리도 추가해서 재생성합니다.
