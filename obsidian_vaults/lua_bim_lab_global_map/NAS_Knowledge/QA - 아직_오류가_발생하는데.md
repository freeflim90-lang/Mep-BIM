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

# QA - 아직 오류가 발생하는데?

## 질문
> **카테고리:** Claude대화 | **날짜:** 2026-06-10
> **출처:** Claude Code 세션

아직 오류가 발생하는데?

## 답변

Google Cloud Console에서 `http://localhost:8085`가 아직 등록 안 된 상태입니다. 아래 절차대로 직접 추가해야 합니다.

---

**Google Cloud Console에서 등록하는 방법:**

1. 브라우저에서 이 주소로 이동:
   ```
   https://console.cloud.google.com/apis/credentials
   ```

2. `665916659329-8lmca52m4r3v6v5lam48nmljgf6v2c2i` 클라이언트 ID를 클릭

3. **"승인된 리디렉션 URI"** 섹션에서 **"+ URI 추가"** 클릭

4. 아래를 그대로 입력:
   ```
   http://localhost:8085
   ```

5. **저장** 클릭

6. 저장 후 다시 스크립트 실행

---

저장 완료되면 알려주세요, 바로 재실행하겠습니다.

## 관련 자료

- [[MOC - Q&A Knowledge Base]]

## 연결

- [[Global Knowledge Map]]

---

## 질문 (추가 2026-06-10)
> **카테고리:** Claude대화 | **날짜:** 2026-06-10
> **출처:** Claude Code 세션

아직 오류가 발생하는데?

## 답변

Google Cloud Console에서 `http://localhost:8085`가 아직 등록 안 된 상태입니다. 아래 절차대로 직접 추가해야 합니다.

---

**Google Cloud Console에서 등록하는 방법:**

1. 브라우저에서 이 주소로 이동:
   ```
   https://console.cloud.google.com/apis/credentials
   ```

2. `665916659329-8lmca52m4r3v6v5lam48nmljgf6v2c2i` 클라이언트 ID를 클릭

3. **"승인된 리디렉션 URI"** 섹션에서 **"+ URI 추가"** 클릭

4. 아래를 그대로 입력:
   ```
   http://localhost:8085
   ```

5. **저장** 클릭

6. 저장 후 다시 스크립트 실행

---

저장 완료되면 알려주세요, 바로 재실행하겠습니다.
