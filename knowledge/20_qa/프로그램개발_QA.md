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


## 웹 보강: MSI 인스톨러 패키징 코드 서명 인증서 구성 (2026-06-14 16:18:31)
- Source: system-auto-quality-search
- Tags: auto-collect,needs-review

질문: MSI 인스톨러 패키징 코드 서명 인증서 구성

• [Naver] Setup.exe 서명하고 MySetup.msi - Win32 apps
  웹 서버에 Setup.exe 배치하고 MySetup.msi 전에 SignTool 유틸리티를 사용하여 디지털 인증서 및 프라이빗 키 Mycert.cer 및 Mycert.pvk로 파일에 서명해야 합니다. SignTool 유틸리티 사용에 대한 자세한 내용은 Microsoft SDK(Windows 소프트웨어 개발 키트)의 CryptoAPI Tools 참조 참조하세요.
  출처: https://learn.microsoft.com/ko-kr/windows/win32/msi/sign-setup-exe-and-mysetup-msi

• [DDG] 디지털 서명 및 Windows Installer - Win32 apps | Microsoft Learn
  Windows Installer는 디지털 서명을 사용하여 손상된 리소스를 검색할 수 있습니다. 서명자 인증서는 패키지에서 설치할 외부 리소스의 서명자 인증서와 비교할 수 있습니다. 디지털 서명, 디지털 인증서 및 WinVerifyTrust 사용에 대한 자세한 내용은 Microsoft Windows SDK (소프트웨어 개발 키트)의 보안 섹션을 ...
  출처: https://learn.microsoft.com/ko-kr/windows/win32/msi/digital-signatures-and-windows-installer

• [Naver] 드라이버 패키지 테스트 서명 방법 - Windows drivers
  테스트 서명은 테스트 인증서를 사용하여 테스트 컴퓨터에서 사용할 드라이버 패키지 시험판 버전에 서명하는 것을 의미합니다. 특히 이를 통해 개발자는 MakeCert 도구에서 생성하는 같은 자체 서명된 인증서를 사용하여 커널 모드 이진 파일에 서명할 수 있습니다. 이 기능을 사용하면 개발자가 드라이버 서명 확인을 사용하도록 설정된 Windows에서 커널 모드 이진 파일을 테스트...
  출처: https://learn.microsoft.com/ko-kr/windows-hardware/drivers/install/how-to-test-sign-a-driver-package

• [DDG] Visual Studio .msi의 설치 파일에 서명하는 방법 : 네이버 블로그
  다른 옵션 (내가 하고 있는 것)은 먼저 .msi를 만든 다음 pfx (인증서)를 사용하여 서명합니다. (globalsign.com에서 구매한 코드 서명 인증서를 사용하고 있습니다.) CMD 열기: 실행 -&gt; 파워쉘 인증서가 있는 위치에서 지문을 실행하고 저장합니다. PS C:&#92;Windows&#92;system32&gt; Get-PfxCertificate -FilePath .&#92;CompanyCertificate.pfx ...
  출처: https://blog.naver.com/PostView.naver?blogId=wetchop7437&amp;logNo=222677673231

• [Naver] 테스트 서명을 지원하도록 테스트 컴퓨터 구성 - Windows drivers
  테스트 컴퓨터에 테스트 서명된 드라이버 패키지를 설치하기 전에 테스트 서명을 지원하도록 컴퓨터를 구성해야 합니다. 이 섹션에서는 컴퓨터에서 테스트 서명 지원을 사용하도록 설정하는 데 관련된 절차를 설명하고 다음 항목을 포함합니다.
  출처: https://learn.microsoft.com/ko-kr/windows-hardware/drivers/install/configuring-the-test-computer-to-support-test-signing

• [DDG] 윈도우 응용 프로그램 코드 서명::::새로 쓰는 사용 설명서
  앞서 설명한 바와 같이, 코드 서명을 하기 위해서는 OV 또는 EV 인증서를 발급받아야 하며, 2023년 6월 이후부터는 개발자가 직접 개인 키를 생성하고, CA 기관에 CSR 파일을 제출하는 과정이 필요하다. 이번 글에서는 코드 서명 과정의 세부적인 단계를 설명하겠다. 1.
  출처: https://manualbook.tistory.com/118

• [Naver] 드라이버 패키지를 릴리스-서명하는 방법 - Windows drivers
  이 섹션에서는 드라이버 패키지를 릴리스 서명할 때 따라야 하는 기본 단계를 제공합니다. 여기에는 다음과 같은 사항이 포함됩니다. 이 섹션의 각 항목에서는 릴리스 서명 프로세스의 별도 프로시저에 대해 설명하고 프로시저에 대해 이해해야 하는 일반적인 정보를 제공합니다. 또한 각 항목은 절차에 대한 자세한 정보를 제공하는 다른 항목을 가리킵니다. 참고 이 섹션에서는...
  출처: https://learn.microsoft.com/ko-kr/windows-hardware/drivers/install/how-to-release-sign-a-driver-package

검토 기준: 공식 문서·최신성·적용성 확인 후 FAQ 승격.
