# Navisworks_Addin Q&A 지식

텔레그램 질문·자동 수집 응답 저장소 — 기준 가이드라인(Navisworks_Addin.md)과 분리 운영.

## 2026-06-09 Navisworks Add-in 개발 실전 Q&A
- Source: LUA BIM LABS Navisworks 개발 기준, Autodesk Navisworks API 문서
- Tags: navisworks,addin,clash,api,development,qa,2026

**Q: Navisworks API로 Clash 결과를 읽으려면 어떻게 하나요?**
A: `Autodesk.Navisworks.Api.Clash.ClashTest` 네임스페이스를 사용한다. 핵심 클래스: `DocumentClash`, `ClashTest`, `ClashResult`. ClashResult에서 읽을 수 있는 필드: `Status` (Active/Approved/Resolved), `FoundDate`, `ApprovedDate`, `ClashPoint` (XYZ 좌표). Navisworks_Addin 에이전트는 API 접근 범위를 먼저 확인하고 프로그램개발에 구현을 위임한다. *(KST01 — Navisworks API 공식 문서 기준)*

**Q: Clash Detective 결과를 Excel로 내보낼 때 필드 설계는?**
A: 기본 Excel 내보내기 필드 설계: ① 간섭 ID (Clash Name) ② 상태 (Active/Approved/Resolved) ③ 우선순위 (Critical/Major/Minor) ④ 발생일 ⑤ 공종1 (Element 1 Layer) ⑥ 공종2 (Element 2 Layer) ⑦ 위치 (ClashPoint X, Y, Z) ⑧ 담당자 ⑨ 해소 기한 ⑩ 비고. 필드는 클라이언트 요구사항에 맞게 조정하되 이 기본 필드는 항상 포함한다.

**Q: Navisworks Add-in 설치 경로는 어떻게 되나요?**
A: Navisworks Add-in 매니페스트 파일(.addin 또는 registry 등록)은 버전별 경로에 배치한다. Navisworks Manage 2023~2026 경로: `C:\Program Files\Autodesk\Navisworks Manage [버전]\` 또는 per-user 경로. 정확한 경로는 Autodesk Developer Network 공식 문서를 참고하며, 버전별 차이가 있으므로 제품패키징 에이전트와 협력해 설치 패키지를 구성한다.

**Q: 대용량 모델(50,000개 이상 객체)에서 Clash 처리 성능 이슈는?**
A: 대용량 모델 처리 시 고려사항: ① 전체 모델 로드 대신 NWC/NWD 캐시 활용 ② ClashResult 목록을 페이지네이션 방식으로 처리 ③ GUI 업데이트를 백그라운드 스레드와 분리 ④ 처리 진행률 표시(Progress callback 사용). 성능 임계치 초과가 예상되면 요구사항분석에 범위 제한(LOD 400 대신 LOD 300, 특정 공종만 선택)을 검토 요청한다.

**Q: Navisworks 버전 호환성은 어떻게 관리하나요?**
A: 지원 버전 기준: Navisworks Manage 2023, 2024, 2025, 2026 (Simulate·Freedom은 Clash Detective API 제한). 버전별 API 차이가 있으므로 조건부 컴파일 또는 런타임 버전 체크를 사용한다. 빌드검증 에이전트가 각 버전별 smoke test를 수행한다.
