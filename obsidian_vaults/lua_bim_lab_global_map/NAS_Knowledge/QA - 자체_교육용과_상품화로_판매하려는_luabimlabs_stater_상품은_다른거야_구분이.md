---
type: qa-note
category: Claude대화
domain: 기타
date: 2026-06-03
status: verified
tags:
  - QA
  - 기타
---

# QA - 자체 교육용과 상품화로 판매하려는 luabimlabs stater 상품은 다른거야 구분이

## 질문
> **카테고리:** Claude대화 | **날짜:** 2026-06-03
> **출처:** Claude Code 세션

자체 교육용과 상품화로 판매하려는 luabimlabs stater 상품은 다른거야 구분이 필요해

## 답변

맞습니다. 현재 `send_daily.py`에 두 가지가 섞여 있습니다.

| | **내부 직원 교육** | **Starter Plan (상품)** |
|---|---|---|
| 대상 | 최정연·오수빈·김선정·허진석 | 유료 글로벌 클라이언트 |
| 언어 | KO 전용 | EN·JA·ZH·AR |
| 커리큘럼 | 1yr~10yr (365일×10년) | 90일 구조화 프로그램 |
| 가격 | 내부 | USD 39/월 |
| 성격 | 운영 | 수익 상품 |

**분리 방향 제안:**

1. **스크립트 분리** — `send_internal.py` / `send_starter.py` 로 완전히 분리
2. **LaunchAgent 분리** — 별도 plist로 독립 실행
3. **데이터 디렉토리** — 이미 분리됨 (`bim_education/` vs `starter_plan/`)

어떤 방식으로 분리할까요?

## 관련 자료

- [[MOC - Q&A Knowledge Base]]

## 연결

- [[Global Knowledge Map]]

---

## 질문 (추가 2026-06-03)
> **카테고리:** Claude대화 | **날짜:** 2026-06-03
> **출처:** Claude Code 세션

자체 교육용과 상품화로 판매하려는 luabimlabs stater 상품은 다른거야 구분이 필요해

## 답변

맞습니다. 현재 `send_daily.py`에 두 가지가 섞여 있습니다.

| | **내부 직원 교육** | **Starter Plan (상품)** |
|---|---|---|
| 대상 | 최정연·오수빈·김선정·허진석 | 유료 글로벌 클라이언트 |
| 언어 | KO 전용 | EN·JA·ZH·AR |
| 커리큘럼 | 1yr~10yr (365일×10년) | 90일 구조화 프로그램 |
| 가격 | 내부 | USD 39/월 |
| 성격 | 운영 | 수익 상품 |

**분리 방향 제안:**

1. **스크립트 분리** — `send_internal.py` / `send_starter.py` 로 완전히 분리
2. **LaunchAgent 분리** — 별도 plist로 독립 실행
3. **데이터 디렉토리** — 이미 분리됨 (`bim_education/` vs `starter_plan/`)

어떤 방식으로 분리할까요?

---

## 질문 (추가 2026-06-03)
> **카테고리:** Claude대화 | **날짜:** 2026-06-03
> **출처:** Claude Code 세션

자체 교육용과 상품화로 판매하려는 luabimlabs stater 상품은 다른거야 구분이 필요해

## 답변

맞습니다. 현재 `send_daily.py`에 두 가지가 섞여 있습니다.

| | **내부 직원 교육** | **Starter Plan (상품)** |
|---|---|---|
| 대상 | 최정연·오수빈·김선정·허진석 | 유료 글로벌 클라이언트 |
| 언어 | KO 전용 | EN·JA·ZH·AR |
| 커리큘럼 | 1yr~10yr (365일×10년) | 90일 구조화 프로그램 |
| 가격 | 내부 | USD 39/월 |
| 성격 | 운영 | 수익 상품 |

**분리 방향 제안:**

1. **스크립트 분리** — `send_internal.py` / `send_starter.py` 로 완전히 분리
2. **LaunchAgent 분리** — 별도 plist로 독립 실행
3. **데이터 디렉토리** — 이미 분리됨 (`bim_education/` vs `starter_plan/`)

어떤 방식으로 분리할까요?

---

## 질문 (추가 2026-06-03)
> **카테고리:** Claude대화 | **날짜:** 2026-06-03
> **출처:** Claude Code 세션

자체 교육용과 상품화로 판매하려는 luabimlabs stater 상품은 다른거야 구분이 필요해

## 답변

맞습니다. 현재 `send_daily.py`에 두 가지가 섞여 있습니다.

| | **내부 직원 교육** | **Starter Plan (상품)** |
|---|---|---|
| 대상 | 최정연·오수빈·김선정·허진석 | 유료 글로벌 클라이언트 |
| 언어 | KO 전용 | EN·JA·ZH·AR |
| 커리큘럼 | 1yr~10yr (365일×10년) | 90일 구조화 프로그램 |
| 가격 | 내부 | USD 39/월 |
| 성격 | 운영 | 수익 상품 |

**분리 방향 제안:**

1. **스크립트 분리** — `send_internal.py` / `send_starter.py` 로 완전히 분리
2. **LaunchAgent 분리** — 별도 plist로 독립 실행
3. **데이터 디렉토리** — 이미 분리됨 (`bim_education/` vs `starter_plan/`)

어떤 방식으로 분리할까요?

---

## 질문 (추가 2026-06-04)
> **카테고리:** Claude대화 | **날짜:** 2026-06-04
> **출처:** Claude Code 세션

자체 교육용과 상품화로 판매하려는 luabimlabs stater 상품은 다른거야 구분이 필요해

## 답변

맞습니다. 현재 `send_daily.py`에 두 가지가 섞여 있습니다.

| | **내부 직원 교육** | **Starter Plan (상품)** |
|---|---|---|
| 대상 | 최정연·오수빈·김선정·허진석 | 유료 글로벌 클라이언트 |
| 언어 | KO 전용 | EN·JA·ZH·AR |
| 커리큘럼 | 1yr~10yr (365일×10년) | 90일 구조화 프로그램 |
| 가격 | 내부 | USD 39/월 |
| 성격 | 운영 | 수익 상품 |

**분리 방향 제안:**

1. **스크립트 분리** — `send_internal.py` / `send_starter.py` 로 완전히 분리
2. **LaunchAgent 분리** — 별도 plist로 독립 실행
3. **데이터 디렉토리** — 이미 분리됨 (`bim_education/` vs `starter_plan/`)

어떤 방식으로 분리할까요?
