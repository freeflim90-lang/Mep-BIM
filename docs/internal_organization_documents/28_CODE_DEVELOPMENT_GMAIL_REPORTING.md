# LUA BIM LAB
# 코드 개발 Gmail 보고 운영 기준

━━━━━━━━━━━━━━━━━━━━

문서번호: LBL-ORG-028  
문서상태: 내부 기준 초안  
작성일: 2026-05-28  
배포등급: Internal Only

## 1. 목적

본 문서는 LUA BIM LABS에서 코드 개발이 발생했을 때 Gmail로 개발 요약을 발송하는 기준을 정의한다.

Mac mini는 지식 수집, 큐레이션, 기획, 운영 자동화 장비로 사용하고, 코드 개발 본문은 별도 개발 컴퓨터에서 처리한다. 따라서 Mac mini에는 코드 개발 본문을 저장하지 않고 Gmail로 외부 개발 컴퓨터에 전달한다.

## 2. 적용 범위

- Qwen 개발 초안 생성
- Revit/Navisworks/Add-in 관련 코드 변경
- backend, frontend, scripts, tests 변경
- git commit 이후 코드 변경 보고

## 3. 발송 방식

| 트리거 | 방식 | 도구 |
|---|---|---|
| Qwen 개발 초안 | 초안 생성 후 Gmail 발송 시도 | `backend/qwen_product_drafts.py` |
| 일반 코드 변경 | 수동 실행 또는 git post-commit 훅으로 요약 발송 | `scripts/send_code_development_gmail.py` |
| git commit | commit 직후 자동 실행 | `.git/hooks/post-commit` |

## 4. Gmail 설정

`.env`에 아래 값을 설정해야 실제 발송된다.

```bash
GMAIL_ADDRESS=your-gmail-address@gmail.com
GMAIL_APP_PASSWORD=your-gmail-app-password
GMAIL_TO=receiver@gmail.com
```

대체 변수명:

```bash
CODE_DEV_GMAIL_FROM=your-gmail-address@gmail.com
CODE_DEV_GMAIL_APP_PASSWORD=your-gmail-app-password
CODE_DEV_GMAIL_TO=receiver@gmail.com
```

Gmail은 일반 계정 비밀번호 대신 앱 비밀번호를 사용한다. 앱 비밀번호가 없으면 발송은 스킵되고 `logs/code_development_gmail.log`에 설정 필요 상태를 남긴다.

코드 본문 로컬 저장 방지 기본값:

```bash
CODE_DEV_EXTERNAL_ONLY=true
```

이 값이 기본 정책이다. 특별한 검증 목적이 아니면 `false`로 바꾸지 않는다.

## 5. 수동 실행

```bash
source .dev-venv/bin/activate
python scripts/send_code_development_gmail.py --reason "manual-code-development-report"
```

별도 개발 컴퓨터로 코드 diff 일부를 보내려면:

```bash
python scripts/send_code_development_gmail.py --reason "manual-code-development-report" --include-diff
```

## 6. 보안 기준

- 토큰, API 키, Gmail 앱 비밀번호, 고객 모델 경로, 개인정보는 메일 본문에 포함하지 않는다.
- 코드 diff 포함은 내부 검토용으로만 사용한다.
- 외부 고객에게 직접 발송하지 않고 내부 수신 주소로 발송한다.
- 실제 Revit API write 작업은 검증 게이트 전 확정하지 않는다.
- Mac mini에는 코드 개발 본문을 저장하지 않는다. Obsidian에는 메타데이터와 발송 기록만 남긴다.

## 7. 연결

- [[LUA BIM LABS AX BIM 선도기업 성장 비전]]
- [[AX 전환을 위한 건설 BIM AI 지식 축적 전략]]
- [[지식업데이트]]
- [[Global Knowledge Map]]
