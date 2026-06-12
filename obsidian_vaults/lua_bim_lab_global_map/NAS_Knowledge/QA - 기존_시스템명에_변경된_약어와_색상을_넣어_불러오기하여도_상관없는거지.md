---
type: qa-note
category: Claude대화
domain: 기타
date: 2026-05-27
status: verified
tags:
  - QA
  - 기타
---

# QA - 기존 시스템명에 변경된 약어와 색상을 넣어 불러오기하여도 상관없는거지?

## 질문
> **카테고리:** Claude대화 | **날짜:** 2026-05-27
> **출처:** Claude Code 세션

기존 시스템명에 변경된 약어와 색상을 넣어 불러오기하여도 상관없는거지?

## 답변

네, 전혀 문제없습니다.

내보낸 CSV에서 약어와 RGB만 수정한 후 가져오면, 시스템명으로 매칭해서 변경된 값만 덮어씁니다. 시스템명은 매칭 키로만 사용되고 값 자체는 바뀌지 않습니다.

## 관련 자료

- [[MOC - Q&A Knowledge Base]]

## 연결

- [[Global Knowledge Map]]
