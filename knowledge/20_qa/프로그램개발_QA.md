# 프로그램개발 Q&A 지식

텔레그램 질문·자동 수집 응답 저장소 — 기준 가이드라인(프로그램개발.md)과 분리 운영.

## 2026-06-09 프로그램개발 실전 Q&A
- Source: LUA BIM LABS 개발 운영 기준, Revit/Navisworks API 경험
- Tags: development,revit-api,csharp,code-review,qa,2026

**Q: Revit API에서 Transaction은 어떻게 사용하나요?**
A: 트랜잭션 사용 기본 규칙: ① `[Transaction(TransactionMode.Manual)]` 속성을 IExternalCommand 클래스에 붙인다 ② 모든 모델 수정은 `using (Transaction tx = new Transaction(doc, "작업명")) { tx.Start(); ... tx.Commit(); }` 블록 안에서만 수행한다 ③ 예외 발생 시 `tx.RollBack()`으로 복구한다 ④ 트랜잭션 중첩은 금지된다(SubTransaction 별도 사용). *(KST01 — Autodesk API 공식 문서)*

**Q: Revit Add-in에서 설정값을 저장하는 방법은?**
A: 권장 방법: `ExtensibleStorage` API 사용 (Revit 문서 내 저장). 대안: 사용자 AppData 폴더에 JSON/XML 파일로 저장. 절대 금지: Registry에 민감 데이터 저장, 프로젝트 파일 외부 경로에 의존하는 하드코딩. 라이선스 정보는 별도 Entitlement API를 통해 관리하고 DLL에 임베드하지 않는다.

**Q: 코드 리뷰 시 주요 확인 항목은?**
A: 프로그램개발 에이전트의 코드 리뷰 체크리스트: ① 트랜잭션 경계 명확성 ② 예외 처리 완비 (null 체크, API 버전 분기) ③ 민감 데이터 노출 없음 (API Key, 고객 정보 하드코딩 금지) ④ 메모리 해제 (Dispose 패턴 적용 여부) ⑤ 로깅 적절성 (디버그 로그가 릴리스 빌드에 과다하게 남지 않음) ⑥ Qwen 초안에서 Autodesk API 의존 코드가 확정 코드로 잘못 승격됐는지.

**Q: Revit 버전별 API 차이는 어떻게 처리하나요?**
A: `#if REVIT2025` 등 조건부 컴파일 또는 런타임 버전 체크 방식을 사용한다. 버전 분기가 많아지면 어댑터 패턴으로 분리한다. Autodesk는 매년 API 변경 사항을 "What's New" 문서로 제공하므로, 프로그램개발 에이전트는 신규 버전 지원 시 이 문서를 먼저 검토한다.

**Q: Qwen_Coder_8B 초안과 실제 구현의 차이는 어떻게 관리하나요?**
A: 프로그램개발이 Qwen 초안을 받으면: ① Autodesk API 의존 부분을 식별하고 실제 API 호출로 교체 ② 트랜잭션 경계를 추가 ③ 보안 취약점 제거 ④ 성능 이슈 수정. 수정 내용은 PR 설명에 명시한다. Qwen 초안은 검토용이며 직접 프로덕션 배포하지 않는다.
