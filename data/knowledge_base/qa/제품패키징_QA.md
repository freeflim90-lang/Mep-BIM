# 제품패키징 Q&A 지식

텔레그램 질문·자동 수집 응답 저장소 — 기준 가이드라인(제품패키징.md)과 분리 운영.

## 2026-06-09 제품패키징 실전 Q&A
- Source: LUA BIM LABS 패키징/설치 운영 기준, Autodesk 배포 가이드
- Tags: packaging,installer,manifest,deployment,qa,2026

**Q: Revit Add-in 배포 패키지 구조는?**
A: 기본 패키지 구조:
```
BIMCommandCenter/
  ├── BIMCommandCenter.addin       # 매니페스트
  ├── BIMCommandCenter.dll         # 메인 어셈블리
  ├── BIMCommandCenter.dll.config  # 설정 (옵션)
  └── Resources/                   # 아이콘, 번역 리소스
```
.addin 파일은 버전별 폴더(`C:\ProgramData\Autodesk\Revit\Addins\20xx\`)에 배치하고 DLL은 해당 경로의 `BIMCommandCenter\` 서브폴더에 배치한다. *(KST01)*

**Q: MSI 인스톨러 vs. 수동 배포 중 어떤 방식을 선택하나요?**
A: Autodesk App Store 제출 기준: MSI 인스톨러 방식 권장. 이유: ① 제거(Uninstall)가 표준화됨 ② Windows 이벤트 로그에 설치 기록 남음 ③ 업데이트 시 이전 버전 자동 제거. 수동 배포(ZIP)는 내부 테스트 또는 엔터프라이즈 직접 배포에만 사용. Autodesk Bundle 폴더(.bundle) 방식도 지원한다.

**Q: 설치 오류 1603은 어떻게 해결하나요?**
A: 오류 1603은 Windows Installer 일반 실패다. 해결 순서: ① 이전 버전 완전 제거(Add/Remove Programs + 수동 폴더 정리) ② `%AppData%\Autodesk\Revit\Addins\`에서 잔여 .addin 파일 삭제 ③ 재설치 시도 ④ 관리자 권한으로 재설치 ⑤ Windows Installer 서비스 재시작. 해결 안 되면 고객지원 CS에 설치 로그 파일 요청.

**Q: 여러 Revit 버전을 동시에 지원하는 패키지는 어떻게 만드나요?**
A: 방법 1 (Bundle): `.bundle` 폴더에 각 버전별 PackageContents.xml을 작성해 Revit이 해당 버전 DLL을 자동 선택. 방법 2 (MSI 조건부): 설치 시 감지된 Revit 버전에 맞는 .addin 파일만 복사. Bundle 방식이 Autodesk App Store 권장 방식이다. 패키지 구조가 확정되면 빌드검증이 버전별 smoke test를 수행한다.

**Q: 코드 서명(Code Signing)은 필수인가요?**
A: Autodesk App Store 제출 시 코드 서명 강력 권장. 미서명 DLL은 Windows SmartScreen이 차단하거나 고객 보안 정책에서 걸림. 라이선스_보안관이 서명 인증서 관리를 담당한다. 서명 인증서 만료 전 갱신 알림을 설정해야 한다.
