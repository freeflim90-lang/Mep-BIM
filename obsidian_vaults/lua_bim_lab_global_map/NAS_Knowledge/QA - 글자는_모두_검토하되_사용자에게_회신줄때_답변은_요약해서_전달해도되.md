---
type: qa-note
category: Claude대화
domain: 기타
date: 2026-06-06
status: verified
tags:
  - QA
  - 기타
---

# QA - 글자는 모두 검토하되 사용자에게 회신줄때 답변은 요약해서 전달해도되

## 질문
> **카테고리:** Claude대화 | **날짜:** 2026-06-06
> **출처:** Claude Code 세션

글자는 모두 검토하되 사용자에게 회신줄때 답변은 요약해서 전달해도되

## 답변

`simulate_qa_quality.py`의 `_search` 함수가 `content[:8000]`만 보는 게 버그입니다. 전체 파일을 검색하도록 수정하겠습니다.

## 관련 자료

- [[MOC - Q&A Knowledge Base]]

## 연결

- [[Global Knowledge Map]]

---

## 질문 (추가 2026-06-07)
> **카테고리:** Claude대화 | **날짜:** 2026-06-07
> **출처:** Claude Code 세션

글자는 모두 검토하되 사용자에게 회신줄때 답변은 요약해서 전달해도되

## 답변

`simulate_qa_quality.py`의 `_search` 함수가 `content[:8000]`만 보는 게 버그입니다. 전체 파일을 검색하도록 수정하겠습니다.
