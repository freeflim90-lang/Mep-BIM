---
type: qa-note
category: Claude대화
domain: 기타
date: 2026-05-31
status: verified
tags:
  - QA
  - 기타
---

# QA - website 폴더와 헷갈리는데 불필요한 폴더야?

## 질문
> **카테고리:** Claude대화 | **날짜:** 2026-05-31
> **출처:** Claude Code 세션

website 폴더와 헷갈리는데 불필요한 폴더야?

## 답변

두 폴더는 완전히 다른 목적입니다. **불필요하지 않습니다.**

| 폴더 | 역할 | 서빙 위치 |
|------|------|-----------|
| `website/` | 공개 회사 홈페이지 (luabimlabs.com) | Cloudflare Pages |
| `frontend/` | 내부 엔터프라이즈 대시보드 | FastAPI 백엔드 (`api.luabimlabs.com`) |

`website/`는 Cloudflare Pages가 배포하는 소스 폴더이고, `frontend/`는 백엔드 서버가 직접 서빙하는 별개의 앱입니다. 이름 때문에 헷갈릴 수 있으니 `website/` → `public_site/` 같은 이름으로 변경하면 명확해지는데, 그러면 Cloudflare Pages 설정도 같이 바꿔야 합니다. 현재대로 유지하는 게 무난합니다.

## 관련 자료

- [[MOC - Q&A Knowledge Base]]

## 연결

- [[Global Knowledge Map]]

---

## 질문 (추가 2026-05-31)
> **카테고리:** Claude대화 | **날짜:** 2026-05-31
> **출처:** Claude Code 세션

website 폴더와 헷갈리는데 불필요한 폴더야?

## 답변

두 폴더는 완전히 다른 목적입니다. **불필요하지 않습니다.**

| 폴더 | 역할 | 서빙 위치 |
|------|------|-----------|
| `website/` | 공개 회사 홈페이지 (luabimlabs.com) | Cloudflare Pages |
| `frontend/` | 내부 엔터프라이즈 대시보드 | FastAPI 백엔드 (`api.luabimlabs.com`) |

`website/`는 Cloudflare Pages가 배포하는 소스 폴더이고, `frontend/`는 백엔드 서버가 직접 서빙하는 별개의 앱입니다. 이름 때문에 헷갈릴 수 있으니 `website/` → `public_site/` 같은 이름으로 변경하면 명확해지는데, 그러면 Cloudflare Pages 설정도 같이 바꿔야 합니다. 현재대로 유지하는 게 무난합니다.

---

## 질문 (추가 2026-05-31)
> **카테고리:** Claude대화 | **날짜:** 2026-05-31
> **출처:** Claude Code 세션

website 폴더와 헷갈리는데 불필요한 폴더야?

## 답변

두 폴더는 완전히 다른 목적입니다. **불필요하지 않습니다.**

| 폴더 | 역할 | 서빙 위치 |
|------|------|-----------|
| `website/` | 공개 회사 홈페이지 (luabimlabs.com) | Cloudflare Pages |
| `frontend/` | 내부 엔터프라이즈 대시보드 | FastAPI 백엔드 (`api.luabimlabs.com`) |

`website/`는 Cloudflare Pages가 배포하는 소스 폴더이고, `frontend/`는 백엔드 서버가 직접 서빙하는 별개의 앱입니다. 이름 때문에 헷갈릴 수 있으니 `website/` → `public_site/` 같은 이름으로 변경하면 명확해지는데, 그러면 Cloudflare Pages 설정도 같이 바꿔야 합니다. 현재대로 유지하는 게 무난합니다.

---

## 질문 (추가 2026-05-31)
> **카테고리:** Claude대화 | **날짜:** 2026-05-31
> **출처:** Claude Code 세션

website 폴더와 헷갈리는데 불필요한 폴더야?

## 답변

두 폴더는 완전히 다른 목적입니다. **불필요하지 않습니다.**

| 폴더 | 역할 | 서빙 위치 |
|------|------|-----------|
| `website/` | 공개 회사 홈페이지 (luabimlabs.com) | Cloudflare Pages |
| `frontend/` | 내부 엔터프라이즈 대시보드 | FastAPI 백엔드 (`api.luabimlabs.com`) |

`website/`는 Cloudflare Pages가 배포하는 소스 폴더이고, `frontend/`는 백엔드 서버가 직접 서빙하는 별개의 앱입니다. 이름 때문에 헷갈릴 수 있으니 `website/` → `public_site/` 같은 이름으로 변경하면 명확해지는데, 그러면 Cloudflare Pages 설정도 같이 바꿔야 합니다. 현재대로 유지하는 게 무난합니다.
