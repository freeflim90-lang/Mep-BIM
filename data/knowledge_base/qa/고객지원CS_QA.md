# 고객지원CS Q&A 지식

텔레그램 질문·자동 수집 응답 저장소 — 기준 가이드라인(고객지원CS.md)과 분리 운영.


## 고객지원 FAQ (2026-05-24)
- Source: LUA BIM LABS internal CS knowledge baseline
- Tags: cs,faq,support,revit,addin

Add-in이 Revit에 표시되지 않을 때:
- `.addin` 파일과 DLL이 `C:\ProgramData\Autodesk\Revit\Addins\[버전]\` 폴더에 있는지 확인
- Revit 버전 폴더(2023/2024/2025/2026)가 맞는지 확인
- Revit 재시작 후 확인
- Windows 이벤트 뷰어 → 응용 프로그램 로그에서 DLL 로드 오류 확인

라이선스 인증 실패 시:
- Autodesk 계정 로그인 상태 확인 (Autodesk Desktop App)
- Entitlement API 연결을 위해 인터넷 연결 필요
- 오프라인 환경: 마지막 인증 후 7일 이내 캐시 허용
- 라이선스 만료 여부를 Autodesk App Store > 내 계정에서 확인

구독 결제 후 기능이 활성화되지 않을 때:
- Autodesk App Store 구독 반영에 최대 24시간 소요 가능
- Revit 재시작 또는 Add-in 재로그인 시도
- 구독 계정 이메일과 Revit 로그인 계정이 동일한지 확인
- 24시간 후에도 미해결 시 Autodesk 고객센터 문의 안내

설치 중 오류코드 1603 발생 시:
- Windows Installer 오류 — 이전 버전 잔여 파일 충돌
- 프로그램 제거 후 `%AppData%\Autodesk\Revit\Addins\` 폴더 수동 정리
- 재설치 시도


## Q: 고객이 환불을 요청하면 어떻게 처리해? (2026-05-24)
- Source: LUA BIM LABS internal CS knowledge baseline
- Tags: cs,qa,refund,autodesk-store

Autodesk App Store 환불 정책:
- 결제 후 14일 이내, 미사용 조건에서 Autodesk를 통해 환불 요청 가능
- LUA BIM LABS가 직접 환불 처리하지 않음 — Autodesk 고객센터로 안내
- 고객에게 안내할 링크: https://www.autodesk.com/support
- 환불 정책 예외: 구독 기간 중 사용 이력이 있는 경우 Autodesk 재량

내부 처리:
- 환불 요청 내역을 CFO/경영지원에 공유
- 반복 환불 패턴 발생 시 제품 품질 이슈 여부 라이선스_보안관과 확인


## Q: 같은 문의가 반복되면 어떻게 해? (2026-05-24)
- Source: LUA BIM LABS internal CS knowledge baseline
- Tags: cs,qa,faq,knowledge-update

반복 문의 처리 프로세스:
1. 동일 문의 3회 이상 → 지식업데이트 에이전트에 FAQ 보강 요청
2. 제품 UI/UX 개선으로 해결 가능한 문의 → 요구사항분석 에이전트에 이슈 등록
3. 설치 가이드 부족으로 발생하는 문의 → 배포문서 에이전트에 가이드 보강 요청
4. FAQ 문서(`27_CS_RESPONSE_SCRIPT.md`)에 신규 스크립트 추가

목표: 반복 문의 30% 감소 (FAQ 자동 응대 전환).
