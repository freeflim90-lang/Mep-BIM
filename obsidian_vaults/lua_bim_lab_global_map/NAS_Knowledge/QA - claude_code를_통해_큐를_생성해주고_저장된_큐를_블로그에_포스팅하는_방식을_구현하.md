---
type: qa-note
category: Claude대화
domain: 기타
date: 2026-06-09
status: verified
tags:
  - QA
  - 기타
---

# QA - claude code를 통해 큐를 생성해주고 저장된 큐를 블로그에 포스팅하는 방식을 구현하

## 질문
> **카테고리:** Claude대화 | **날짜:** 2026-06-09
> **출처:** Claude Code 세션

claude code를 통해 큐를 생성해주고 저장된 큐를 블로그에 포스팅하는 방식을 구현하려고해

## 답변

이해했어요. 구조가 명확하네요:

- **큐 생성**: 사용자가 나(Claude Code)에게 주제 주면 → 내가 글 생성 + `knowledge/60_public/blogger_queue/` 에 JSON 저장
- **자동 발행**: 기존 LaunchAgent가 큐 파일 읽어서 Blogger에 올림

현재 `render_post()`는 템플릿만 사용하는데, 큐 JSON에 `content` 필드가 있으면 그걸 바로 쓰도록 한 줄만 수정하면 됩니다.

## 관련 자료

- [[MOC - Q&A Knowledge Base]]

## 연결

- [[Global Knowledge Map]]

---

## 질문 (추가 2026-06-09)
> **카테고리:** Claude대화 | **날짜:** 2026-06-09
> **출처:** Claude Code 세션

claude code를 통해 큐를 생성해주고 저장된 큐를 블로그에 포스팅하는 방식을 구현하려고해

## 답변

이해했어요. 구조가 명확하네요:

- **큐 생성**: 사용자가 나(Claude Code)에게 주제 주면 → 내가 글 생성 + `knowledge/60_public/blogger_queue/` 에 JSON 저장
- **자동 발행**: 기존 LaunchAgent가 큐 파일 읽어서 Blogger에 올림

현재 `render_post()`는 템플릿만 사용하는데, 큐 JSON에 `content` 필드가 있으면 그걸 바로 쓰도록 한 줄만 수정하면 됩니다.

---

## 질문 (추가 2026-06-09)
> **카테고리:** Claude대화 | **날짜:** 2026-06-09
> **출처:** Claude Code 세션

claude code를 통해 큐를 생성해주고 저장된 큐를 블로그에 포스팅하는 방식을 구현하려고해

## 답변

이해했어요. 구조가 명확하네요:

- **큐 생성**: 사용자가 나(Claude Code)에게 주제 주면 → 내가 글 생성 + `knowledge/60_public/blogger_queue/` 에 JSON 저장
- **자동 발행**: 기존 LaunchAgent가 큐 파일 읽어서 Blogger에 올림

현재 `render_post()`는 템플릿만 사용하는데, 큐 JSON에 `content` 필드가 있으면 그걸 바로 쓰도록 한 줄만 수정하면 됩니다.
