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

# QA - dashboard는 뭐야?

## 질문
> **카테고리:** Claude대화 | **날짜:** 2026-05-31
> **출처:** Claude Code 세션

dashboard는 뭐야?

## 답변

프로젝트 안에 두 개의 "대시보드"가 있어서 먼저 정확히 짚겠습니다.

---

## 현재 존재하는 대시보드 2개

### 1. LUA BIM LABS 기업 지휘 통제 대시보드
**경로:** [frontend/index.html](frontend/index.html)
- FastAPI 백엔드(`server_total.py`)와 WebSocket으로 연결된 **HTML 단일 파일**
- Command 뷰 / BIM LAND 뷰 전환 구조
- CEO 에이전트, AI 파이프라인, Telegram 수신, Qwen 개발 현황 등 **전사 운영 모니터링** 용도
- 브라우저에서 `http://localhost:PORT` 로 접속하는 웹 앱

### 2. Revit 애드인 내장 Model Health Dashboard
**경로:** [260519 소스 폴더/01_Revit_Addins/Model Health Dashboard/](260519\ 소스\ 폴더/01_Revit_Addins/Model\ Health\ Dashboard/)
- Revit 애드인 내부에서 열리는 **React 앱 (웹뷰)**
- Revit 모델 상태 데이터를 받아 시각화하는 BIM Command Center UI
- 별도 Windows 개발 PC에서 빌드·통합 필요

---

어느 쪽을 말씀하신 건가요?

- **A: 기업 대시보드 (frontend)** → FastAPI API 엔드포인트 추가, Python 모듈 개발, 지금 즉시 가능
- **B: Revit 애드인 내 웹뷰 (Model Health Dashboard)** → React 컴포넌트 추가, Windows PC 없이 UI 코드는 가능하지만 Revit 연동 테스트는 별도 PC 필요

## 관련 자료

- [[MOC - Q&A Knowledge Base]]

## 연결

- [[Global Knowledge Map]]

---

## 질문 (추가 2026-05-31)
> **카테고리:** Claude대화 | **날짜:** 2026-05-31
> **출처:** Claude Code 세션

dashboard는 뭐야?

## 답변

프로젝트 안에 두 개의 "대시보드"가 있어서 먼저 정확히 짚겠습니다.

---

## 현재 존재하는 대시보드 2개

### 1. LUA BIM LABS 기업 지휘 통제 대시보드
**경로:** [frontend/index.html](frontend/index.html)
- FastAPI 백엔드(`server_total.py`)와 WebSocket으로 연결된 **HTML 단일 파일**
- Command 뷰 / BIM LAND 뷰 전환 구조
- CEO 에이전트, AI 파이프라인, Telegram 수신, Qwen 개발 현황 등 **전사 운영 모니터링** 용도
- 브라우저에서 `http://localhost:PORT` 로 접속하는 웹 앱

### 2. Revit 애드인 내장 Model Health Dashboard
**경로:** [260519 소스 폴더/01_Revit_Addins/Model Health Dashboard/](260519\ 소스\ 폴더/01_Revit_Addins/Model\ Health\ Dashboard/)
- Revit 애드인 내부에서 열리는 **React 앱 (웹뷰)**
- Revit 모델 상태 데이터를 받아 시각화하는 BIM Command Center UI
- 별도 Windows 개발 PC에서 빌드·통합 필요

---

어느 쪽을 말씀하신 건가요?

- **A: 기업 대시보드 (frontend)** → FastAPI API 엔드포인트 추가, Python 모듈 개발, 지금 즉시 가능
- **B: Revit 애드인 내 웹뷰 (Model Health Dashboard)** → React 컴포넌트 추가, Windows PC 없이 UI 코드는 가능하지만 Revit 연동 테스트는 별도 PC 필요

---

## 질문 (추가 2026-05-31)
> **카테고리:** Claude대화 | **날짜:** 2026-05-31
> **출처:** Claude Code 세션

dashboard는 뭐야?

## 답변

프로젝트 안에 두 개의 "대시보드"가 있어서 먼저 정확히 짚겠습니다.

---

## 현재 존재하는 대시보드 2개

### 1. LUA BIM LABS 기업 지휘 통제 대시보드
**경로:** [frontend/index.html](frontend/index.html)
- FastAPI 백엔드(`server_total.py`)와 WebSocket으로 연결된 **HTML 단일 파일**
- Command 뷰 / BIM LAND 뷰 전환 구조
- CEO 에이전트, AI 파이프라인, Telegram 수신, Qwen 개발 현황 등 **전사 운영 모니터링** 용도
- 브라우저에서 `http://localhost:PORT` 로 접속하는 웹 앱

### 2. Revit 애드인 내장 Model Health Dashboard
**경로:** [260519 소스 폴더/01_Revit_Addins/Model Health Dashboard/](260519\ 소스\ 폴더/01_Revit_Addins/Model\ Health\ Dashboard/)
- Revit 애드인 내부에서 열리는 **React 앱 (웹뷰)**
- Revit 모델 상태 데이터를 받아 시각화하는 BIM Command Center UI
- 별도 Windows 개발 PC에서 빌드·통합 필요

---

어느 쪽을 말씀하신 건가요?

- **A: 기업 대시보드 (frontend)** → FastAPI API 엔드포인트 추가, Python 모듈 개발, 지금 즉시 가능
- **B: Revit 애드인 내 웹뷰 (Model Health Dashboard)** → React 컴포넌트 추가, Windows PC 없이 UI 코드는 가능하지만 Revit 연동 테스트는 별도 PC 필요

---

## 질문 (추가 2026-05-31)
> **카테고리:** Claude대화 | **날짜:** 2026-05-31
> **출처:** Claude Code 세션

dashboard는 뭐야?

## 답변

프로젝트 안에 두 개의 "대시보드"가 있어서 먼저 정확히 짚겠습니다.

---

## 현재 존재하는 대시보드 2개

### 1. LUA BIM LABS 기업 지휘 통제 대시보드
**경로:** [frontend/index.html](frontend/index.html)
- FastAPI 백엔드(`server_total.py`)와 WebSocket으로 연결된 **HTML 단일 파일**
- Command 뷰 / BIM LAND 뷰 전환 구조
- CEO 에이전트, AI 파이프라인, Telegram 수신, Qwen 개발 현황 등 **전사 운영 모니터링** 용도
- 브라우저에서 `http://localhost:PORT` 로 접속하는 웹 앱

### 2. Revit 애드인 내장 Model Health Dashboard
**경로:** [260519 소스 폴더/01_Revit_Addins/Model Health Dashboard/](260519\ 소스\ 폴더/01_Revit_Addins/Model\ Health\ Dashboard/)
- Revit 애드인 내부에서 열리는 **React 앱 (웹뷰)**
- Revit 모델 상태 데이터를 받아 시각화하는 BIM Command Center UI
- 별도 Windows 개발 PC에서 빌드·통합 필요

---

어느 쪽을 말씀하신 건가요?

- **A: 기업 대시보드 (frontend)** → FastAPI API 엔드포인트 추가, Python 모듈 개발, 지금 즉시 가능
- **B: Revit 애드인 내 웹뷰 (Model Health Dashboard)** → React 컴포넌트 추가, Windows PC 없이 UI 코드는 가능하지만 Revit 연동 테스트는 별도 PC 필요

---

## 질문 (추가 2026-05-31)
> **카테고리:** Claude대화 | **날짜:** 2026-05-31
> **출처:** Claude Code 세션

dashboard는 뭐야?

## 답변

프로젝트 안에 두 개의 "대시보드"가 있어서 먼저 정확히 짚겠습니다.

---

## 현재 존재하는 대시보드 2개

### 1. LUA BIM LABS 기업 지휘 통제 대시보드
**경로:** [frontend/index.html](frontend/index.html)
- FastAPI 백엔드(`server_total.py`)와 WebSocket으로 연결된 **HTML 단일 파일**
- Command 뷰 / BIM LAND 뷰 전환 구조
- CEO 에이전트, AI 파이프라인, Telegram 수신, Qwen 개발 현황 등 **전사 운영 모니터링** 용도
- 브라우저에서 `http://localhost:PORT` 로 접속하는 웹 앱

### 2. Revit 애드인 내장 Model Health Dashboard
**경로:** [260519 소스 폴더/01_Revit_Addins/Model Health Dashboard/](260519\ 소스\ 폴더/01_Revit_Addins/Model\ Health\ Dashboard/)
- Revit 애드인 내부에서 열리는 **React 앱 (웹뷰)**
- Revit 모델 상태 데이터를 받아 시각화하는 BIM Command Center UI
- 별도 Windows 개발 PC에서 빌드·통합 필요

---

어느 쪽을 말씀하신 건가요?

- **A: 기업 대시보드 (frontend)** → FastAPI API 엔드포인트 추가, Python 모듈 개발, 지금 즉시 가능
- **B: Revit 애드인 내 웹뷰 (Model Health Dashboard)** → React 컴포넌트 추가, Windows PC 없이 UI 코드는 가능하지만 Revit 연동 테스트는 별도 PC 필요

---

## 질문 (추가 2026-05-31)
> **카테고리:** Claude대화 | **날짜:** 2026-05-31
> **출처:** Claude Code 세션

dashboard는 뭐야?

## 답변

프로젝트 안에 두 개의 "대시보드"가 있어서 먼저 정확히 짚겠습니다.

---

## 현재 존재하는 대시보드 2개

### 1. LUA BIM LABS 기업 지휘 통제 대시보드
**경로:** [frontend/index.html](frontend/index.html)
- FastAPI 백엔드(`server_total.py`)와 WebSocket으로 연결된 **HTML 단일 파일**
- Command 뷰 / BIM LAND 뷰 전환 구조
- CEO 에이전트, AI 파이프라인, Telegram 수신, Qwen 개발 현황 등 **전사 운영 모니터링** 용도
- 브라우저에서 `http://localhost:PORT` 로 접속하는 웹 앱

### 2. Revit 애드인 내장 Model Health Dashboard
**경로:** [260519 소스 폴더/01_Revit_Addins/Model Health Dashboard/](260519\ 소스\ 폴더/01_Revit_Addins/Model\ Health\ Dashboard/)
- Revit 애드인 내부에서 열리는 **React 앱 (웹뷰)**
- Revit 모델 상태 데이터를 받아 시각화하는 BIM Command Center UI
- 별도 Windows 개발 PC에서 빌드·통합 필요

---

어느 쪽을 말씀하신 건가요?

- **A: 기업 대시보드 (frontend)** → FastAPI API 엔드포인트 추가, Python 모듈 개발, 지금 즉시 가능
- **B: Revit 애드인 내 웹뷰 (Model Health Dashboard)** → React 컴포넌트 추가, Windows PC 없이 UI 코드는 가능하지만 Revit 연동 테스트는 별도 PC 필요

---

## 질문 (추가 2026-05-31)
> **카테고리:** Claude대화 | **날짜:** 2026-05-31
> **출처:** Claude Code 세션

dashboard는 뭐야?

## 답변

프로젝트 안에 두 개의 "대시보드"가 있어서 먼저 정확히 짚겠습니다.

---

## 현재 존재하는 대시보드 2개

### 1. LUA BIM LABS 기업 지휘 통제 대시보드
**경로:** [frontend/index.html](frontend/index.html)
- FastAPI 백엔드(`server_total.py`)와 WebSocket으로 연결된 **HTML 단일 파일**
- Command 뷰 / BIM LAND 뷰 전환 구조
- CEO 에이전트, AI 파이프라인, Telegram 수신, Qwen 개발 현황 등 **전사 운영 모니터링** 용도
- 브라우저에서 `http://localhost:PORT` 로 접속하는 웹 앱

### 2. Revit 애드인 내장 Model Health Dashboard
**경로:** [260519 소스 폴더/01_Revit_Addins/Model Health Dashboard/](260519\ 소스\ 폴더/01_Revit_Addins/Model\ Health\ Dashboard/)
- Revit 애드인 내부에서 열리는 **React 앱 (웹뷰)**
- Revit 모델 상태 데이터를 받아 시각화하는 BIM Command Center UI
- 별도 Windows 개발 PC에서 빌드·통합 필요

---

어느 쪽을 말씀하신 건가요?

- **A: 기업 대시보드 (frontend)** → FastAPI API 엔드포인트 추가, Python 모듈 개발, 지금 즉시 가능
- **B: Revit 애드인 내 웹뷰 (Model Health Dashboard)** → React 컴포넌트 추가, Windows PC 없이 UI 코드는 가능하지만 Revit 연동 테스트는 별도 PC 필요

---

## 질문 (추가 2026-05-31)
> **카테고리:** Claude대화 | **날짜:** 2026-05-31
> **출처:** Claude Code 세션

dashboard는 뭐야?

## 답변

프로젝트 안에 두 개의 "대시보드"가 있어서 먼저 정확히 짚겠습니다.

---

## 현재 존재하는 대시보드 2개

### 1. LUA BIM LABS 기업 지휘 통제 대시보드
**경로:** [frontend/index.html](frontend/index.html)
- FastAPI 백엔드(`server_total.py`)와 WebSocket으로 연결된 **HTML 단일 파일**
- Command 뷰 / BIM LAND 뷰 전환 구조
- CEO 에이전트, AI 파이프라인, Telegram 수신, Qwen 개발 현황 등 **전사 운영 모니터링** 용도
- 브라우저에서 `http://localhost:PORT` 로 접속하는 웹 앱

### 2. Revit 애드인 내장 Model Health Dashboard
**경로:** [260519 소스 폴더/01_Revit_Addins/Model Health Dashboard/](260519\ 소스\ 폴더/01_Revit_Addins/Model\ Health\ Dashboard/)
- Revit 애드인 내부에서 열리는 **React 앱 (웹뷰)**
- Revit 모델 상태 데이터를 받아 시각화하는 BIM Command Center UI
- 별도 Windows 개발 PC에서 빌드·통합 필요

---

어느 쪽을 말씀하신 건가요?

- **A: 기업 대시보드 (frontend)** → FastAPI API 엔드포인트 추가, Python 모듈 개발, 지금 즉시 가능
- **B: Revit 애드인 내 웹뷰 (Model Health Dashboard)** → React 컴포넌트 추가, Windows PC 없이 UI 코드는 가능하지만 Revit 연동 테스트는 별도 PC 필요

---

## 질문 (추가 2026-05-31)
> **카테고리:** Claude대화 | **날짜:** 2026-05-31
> **출처:** Claude Code 세션

dashboard는 뭐야?

## 답변

프로젝트 안에 두 개의 "대시보드"가 있어서 먼저 정확히 짚겠습니다.

---

## 현재 존재하는 대시보드 2개

### 1. LUA BIM LABS 기업 지휘 통제 대시보드
**경로:** [frontend/index.html](frontend/index.html)
- FastAPI 백엔드(`server_total.py`)와 WebSocket으로 연결된 **HTML 단일 파일**
- Command 뷰 / BIM LAND 뷰 전환 구조
- CEO 에이전트, AI 파이프라인, Telegram 수신, Qwen 개발 현황 등 **전사 운영 모니터링** 용도
- 브라우저에서 `http://localhost:PORT` 로 접속하는 웹 앱

### 2. Revit 애드인 내장 Model Health Dashboard
**경로:** [260519 소스 폴더/01_Revit_Addins/Model Health Dashboard/](260519\ 소스\ 폴더/01_Revit_Addins/Model\ Health\ Dashboard/)
- Revit 애드인 내부에서 열리는 **React 앱 (웹뷰)**
- Revit 모델 상태 데이터를 받아 시각화하는 BIM Command Center UI
- 별도 Windows 개발 PC에서 빌드·통합 필요

---

어느 쪽을 말씀하신 건가요?

- **A: 기업 대시보드 (frontend)** → FastAPI API 엔드포인트 추가, Python 모듈 개발, 지금 즉시 가능
- **B: Revit 애드인 내 웹뷰 (Model Health Dashboard)** → React 컴포넌트 추가, Windows PC 없이 UI 코드는 가능하지만 Revit 연동 테스트는 별도 PC 필요
