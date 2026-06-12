# 고객지원CS Q&A 지식

텔레그램 질문·자동 수집 응답 저장소 — 기준 가이드라인(고객지원CS.md)과 분리 운영.

## 2026-06-05 CS 실전 Q&A 추가 (KST 근거기반 응답 기준 반영)
- Source: LUA BIM LABS CS 운영 기준, KST 태그 체계
- Tags: cs,qa,evidence-response,kst,customer-support,2026

**Q: 고객이 "BIM 납품 기준이 무엇인가요?"라고 물을 때 어떻게 답변하나요?**
A: 먼저 공식 확정 기준과 프로젝트별 확인 사항을 구분하여 답변합니다. "국토부 건설산업 BIM 시행지침에서 LOD 기준, 납품 파일 형식, CDE 요건을 정의합니다(KST01). 다만 발주처 과업지시서·BEP에 따라 적용 기준이 달라지므로 프로젝트 별로 확인이 필요합니다(KST03)." 자동 수집된 수치는 KST04로 분리하여 확정 답변으로 제시하지 않습니다. *(운영 기준)*

**Q: 고객이 납품 파일 형식을 물을 때 답변은?**
A: "공공 BIM 프로젝트 기준으로 IFC 파일(IFC 2x3 또는 IFC 4), Revit 원본(.rvt), PDF 도면이 기본 납품 대상입니다(KST01). 단, 발주처 BEP 또는 과업지시서의 납품물 목록이 최우선 기준입니다. 조달청 기준과 LH 기준도 일부 다르므로 발주처 확인이 필요합니다(KST03)."

**Q: 고객이 BIM 서비스 가격을 물을 때 어떻게 답변하나요?**
A: 가격은 프로젝트 연면적·공종·LOD·일정에 따라 달라지므로 즉시 확정 답변은 어렵습니다. "BIM 설계 용역 가격은 연면적, 적용 LOD 단계, 공종 범위에 따라 산정합니다. 기본설계 BIM은 설계비의 약 10~15%, 실시설계 BIM은 약 15~25% 추가를 일반 기준으로 참고하시고, 구체적인 견적은 별도 상담으로 확인하겠습니다." *(KST03 적용주의)*

**Q: 고객이 "이번만 무료로 clash report 리뷰 2회를 추가해달라"고 요청하면 어떻게 답변하나요?**
A: CS는 무료 제공을 단독 확정하지 않습니다. "요청 주신 추가 리뷰가 계약 범위에 포함되는지와 예상 공수를 먼저 확인한 뒤, 유상 옵션 또는 1회성 예외 가능 여부를 검토하겠습니다."라고 답변합니다. 범위 외 추가 작업은 유상 견적 원칙이며, 고객 신뢰 회복 목적의 1회성 무상 예외는 CFO 승인과 공수 상한이 있을 때만 가능합니다. 관련 선례는 `AITEST_20260605_004`, `AITEST_20260605_008`입니다.

**Q: 고객이 BF 관련 BIM 검토를 요청할 때 CS 대응 기준은?**
A: CS는 BF 적합/불합격을 단독으로 확정하지 않습니다. "BF(Barrier-Free) 인증 대상 여부, 의무/권장 구분, 예비인증/본인증 단계, 지자체 조건을 확인해야 결론을 드릴 수 있습니다. 자동검수 결과는 참고 후보이며, 인증 통과 확정은 BF 인증기관·설계자·PM 확인이 필요합니다(KST03)." *(운영 기준)*


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
