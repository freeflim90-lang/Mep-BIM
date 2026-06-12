---
type: qa-note
category: Claude대화
domain: 기타
date: 2026-06-10
status: verified
tags:
  - QA
  - 기타
---

# QA - 서버의존해서 보여야 옵시디언이 점차 성장하는걸 고객들이 확인이 가능할거 같아

## 질문
> **카테고리:** Claude대화 | **날짜:** 2026-06-10
> **출처:** Claude Code 세션

서버의존해서 보여야 옵시디언이 점차 성장하는걸 고객들이 확인이 가능할거 같아

## 답변

맞습니다. 서버 의존이 맞는 방향입니다. 그럼 **파일 크기와 lazy loading** 문제만 고치면 됩니다.

구체적으로 두 가지 수정:

**1. `loading="lazy"` 제거** — [website/index.html:1292](website/index.html#L1292)
모바일에서 lazy가 오작동하는 경우가 있어 제거합니다.

**2. 모바일용 경량 그래프 엔드포인트 추가** — 서버에서 User-Agent 감지 또는 `?embed=1` 요청 시 노드 수를 줄인 버전 응답
현재 3.6MB → 상위 카테고리 노드만 포함한 500KB 이하 버전

지금 바로 이 두 가지 수정 진행할까요? 아니면 먼저 핸드폰에서 실제로 어떻게 보이는지 확인해보고 싶으신가요?

## 관련 자료

- [[MOC - Q&A Knowledge Base]]

## 연결

- [[Global Knowledge Map]]
