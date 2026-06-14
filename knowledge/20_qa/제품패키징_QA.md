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


## 웹 보강: Windows MSI 인스톨러 코드 서명 인증서 패키징 구성 기준 (2026-06-14 08:50:22)
- Source: system-auto-quality-search
- Tags: auto-collect,needs-review

질문: Windows MSI 인스톨러 코드 서명 인증서 패키징 구성 기준

• [Naver] 업데이트 패키지 인증 및 서명 - Windows drivers
  다음 다이어그램은 이 문서의 나머지 부분에 설명된 다양한 구성 요소의 서명자를 나타냅니다. 서명된 경우 업데이트된 펌웨어의 서명은 부팅 중에 시스템의 펌웨어 로더에서 유효성을 검사할 수 있어야 합니다. 최소한 다시 부팅 시 자동으로 발생하지만 안정성 및 사용자 환경상의 이유로 사전 유효성 검사가 권장됩니다. Arm 시스템에서는 허용되는 UEFI PE/COFF 이미지만 Microsoft...
  출처: https://learn.microsoft.com/ko-kr/windows-hardware/drivers/bringup/certifying-and-signing-the-update-package

• [Naver] 테스트 서명을 지원하도록 테스트 컴퓨터 구성 - Windows drivers
  테스트 컴퓨터에 테스트 서명된 드라이버 패키지를 설치하기 전에 테스트 서명을 지원하도록 컴퓨터를 구성해야 합니다. 이 섹션에서는 컴퓨터에서 테스트 서명 지원을 사용하도록 설정하는 데 관련된 절차를 설명하고 다음 항목을 포함합니다.
  출처: https://learn.microsoft.com/ko-kr/windows-hardware/drivers/install/configuring-the-test-computer-to-support-test-signing

• [Naver] 드라이버 패키지 테스트 서명 방법 - Windows drivers
  테스트 서명은 테스트 인증서를 사용하여 테스트 컴퓨터에서 사용할 드라이버 패키지 시험판 버전에 서명하는 것을 의미합니다. 특히 이를 통해 개발자는 MakeCert 도구에서 생성하는 같은 자체 서명된 인증서를 사용하여 커널 모드 이진 파일에 서명할 수 있습니다. 이 기능을 사용하면 개발자가 드라이버 서명 확인을 사용하도록 설정된 Windows에서 커널 모드 이진 파일을 테스트...
  출처: https://learn.microsoft.com/ko-kr/windows-hardware/drivers/install/how-to-test-sign-a-driver-package

• [Naver] 테스트 서명 드라이버 패키지 설치 - Windows drivers
  Windows Vista부터 테스트 서명된 드라이버 패키지 는 다음 조건이 충족되는 경우 사용자 상호 작용 없이 설치 및 로드해야 합니다. 테스트 서명된 드라이버 패키지를 설치하는 방법에 대한 개요는 테스트 컴퓨터에 Test-Signed 드라이버 패키지 설치를 참조하세요. 설치 문제를 해결하는 방법에 대한 자세한 내용은 서명된 드라이버 패키지의 설치 및 로드 문제 해결을 참조하세요.
  출처: https://learn.microsoft.com/ko-kr/windows-hardware/drivers/install/installing-test-signed-driver-packages

검토 기준: 공식 문서·최신성·프로젝트 적용성 확인 후 FAQ 승격.
