---
type: qa-note
category: 팀원간질문
domain: 개발기술
date: 2026-05-21
status: verified
tags:
  - QA
  - 개발기술
---

# QA - 엑셀 자동화 추천 라이브러리와 방식

## 질문
> **카테고리:** 팀원간질문 | **날짜:** 2026-05-21
> **출처:** 조서희 (관리팀, Telegram)

엑셀 자동화 추천해줘. 어떤 방식이 좋아?

## 답변

LUA BIM LABS 기준 우선순위:

1. **Python csv + openpyxl** (기본값) — BIM 리포트, 관리팀 업무 전반. 의존성 최소, 파일 손상 위험 낮음
2. **pandas + openpyxl** — 집계(pivot, groupby) 필요 시에만. `engine='openpyxl'` 명시 필수
3. **C# OpenXML SDK** — Revit Add-in 내부에서 직접 생성 시 한정

**VBA/매크로는 전면 금지** — 보안 리스크(악성코드 경로), 크로스플랫폼 비호환, 유지보수 불가

결과물은 Telegram으로 질문자에게 직접 회신 (Mac 로컬 저장 금지 / DeepSeek API 금지)

자세한 패턴과 체크리스트 → [[지식맵 - 엑셀 자동화]]

## 관련 자료

- [[지식맵 - 엑셀 자동화]]
- [[MOC - QA Index]]

## 연결

- [[Global Knowledge Map]]
