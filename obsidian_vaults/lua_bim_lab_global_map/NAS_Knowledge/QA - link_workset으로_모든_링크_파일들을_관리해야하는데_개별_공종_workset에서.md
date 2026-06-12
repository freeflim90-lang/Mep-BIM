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

# QA - link workset으로 모든 링크 파일들을 관리해야하는데 개별 공종 workset에서

## 질문
> **카테고리:** Claude대화 | **날짜:** 2026-06-06
> **출처:** Claude Code 세션

link workset으로 모든 링크 파일들을 관리해야하는데 개별 공종 workset에서 관리하다보면 공종 workset을 off 하는 경우 안보이게되

## 답변

정확히 이해했습니다. **링크 파일이 공종 워크셋에 있으면 해당 공종 워크셋을 off할 때 링크도 같이 사라지는 근본 문제**입니다. 시각적으로 찾기 어렵고, 발견하면 이미 협업이 틀어진 후.

바로 코드 작성하겠습니다.

**수정/생성 파일:**
1. `LinkHealthEngine.cs` — 워크셋 정보 추가
2. `Services/WorksetLinkHandlers.cs` (신규) — 스캔 + 일괄이동 ExternalEvent
3. `UI/WorksetTabViewModel.cs` (신규) — 탭 전용 VM
4. `DashboardView.xaml` — Tab 3 추가
5. `DashboardView.xaml.cs` — 탭 선택 연결
6. `App.cs` — 이벤트 초기화

## 관련 자료

- [[MOC - Q&A Knowledge Base]]

## 연결

- [[Global Knowledge Map]]

---

## 질문 (추가 2026-06-06)
> **카테고리:** Claude대화 | **날짜:** 2026-06-06
> **출처:** Claude Code 세션

link workset으로 모든 링크 파일들을 관리해야하는데 개별 공종 workset에서 관리하다보면 공종 workset을 off 하는 경우 안보이게되

## 답변

정확히 이해했습니다. **링크 파일이 공종 워크셋에 있으면 해당 공종 워크셋을 off할 때 링크도 같이 사라지는 근본 문제**입니다. 시각적으로 찾기 어렵고, 발견하면 이미 협업이 틀어진 후.

바로 코드 작성하겠습니다.

**수정/생성 파일:**
1. `LinkHealthEngine.cs` — 워크셋 정보 추가
2. `Services/WorksetLinkHandlers.cs` (신규) — 스캔 + 일괄이동 ExternalEvent
3. `UI/WorksetTabViewModel.cs` (신규) — 탭 전용 VM
4. `DashboardView.xaml` — Tab 3 추가
5. `DashboardView.xaml.cs` — 탭 선택 연결
6. `App.cs` — 이벤트 초기화
