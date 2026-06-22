

## Telegram 팀원 보강 요청 (2026-06-06 15:09:03)
- Source: telegram:@FreeFilmer (7899169126)
- Tags: telegram,team-request,knowledge-gap,kst02-review

팀원이 기존 Obsidian 답변이 부족하다고 회신했다.

원 질문: revit 간섭 검토시 고려해야 하는 공종간 회피해야하는 공종에 대한 우선순위 알고 싶어
추가 요청: 추가 설명 없음

처리 기준:
1. 내부 지식에서 누락된 기준을 우선 보강한다.
2. 외부 검색 또는 공식 문서 확인이 필요한 항목은 자동 수집 후 지식 업데이트 후보로 표시한다.
3. 고객명, 프로젝트명, 개인정보는 수집하지 않는다.


## Telegram 더 찾아줘 수집 후보 결과 (2026-06-06 15:09:07)
- Source: telegram-search-candidate:@FreeFilmer (7899169126)
- Tags: telegram,team-request,kst04-collected-review,kst02-review

원 질문: revit 간섭 검토시 고려해야 하는 공종간 회피해야하는 공종에 대한 우선순위 알고 싶어
추가 요청: 추가 설명 없음

수집 후보 결과:

• Tavily evidence Tavily AI 요약
  To avoid interference in Revit, focus on avoiding conflicts between structural and electrical components. Use Revit's built-in interference check tool to identify and resolve overlaps. Ensure your add-in manifest correctly references necessary DLLs for API integration.
  출처: 

• Tavily evidence building revit plug-ins with visual studio: part two | archi-lab
  So there it is. We have the structure of our plug-in in place. We defined the sequence of how we will create our plug-in using pseudo code, we implemented IExternalCommand with Transaction Attribute and prepared ourselves for potential errors and how to handle them. Now, we just need to add a \.addi
  source-url: https://archi-lab.net/building-revit-plug-ins-with-visual-studio-part-two

• Tavily evidence [PDF] Preparing Apps for the Store: Guidelines
  Revit goes through the common install folder and parse for Revit apps for the appropriate environments (RuntimeRequirements) 2.
Revit picks up the location of addin manifest (ModuleName) 3.
Read .addin manifest and load the app. Revit App Auto Load Flow <?xml version="1.0" encoding="utf-8"?> <Applic
  source-url: https://damassets.autodesk.net/content/dam/autodesk/www/developer-network/app-store/revit/pdf/3%20Autodesk%20Exchange%20Publish%20Revit%20Apps%20-%20Preparing%20Apps%20for%20the%20Store_Guidelines.pdf

• Tavily evidence Revit API Docs
  #### Other Resources

##### Autodesk

 Autodesk Developer Network
 2017: Developer's Guide
 2016: Developer's Guide
 2015: Developer's Guide
 2014: Developer's Guide
 Dynamo Primer - Python

##### Blogs + Resources

 ArchiLabs
 ArchiLabs Blog
 ArchiLabs Free Revit Tools
 Building Coder Blog
 Python-
  source-url: https://www.revitapidocs.com

• Tavily evidence Practice Revit MEP / 전기 BIM / 간섭 확인하기 및 해결하기 - YouTube
  Practice Revit MEP / 전기 BIM / 간섭 확인하기 및 해결하기 1. 간섭 확인하기 2. 간섭 해결하기 Music from YouTube Audio Library [Aka YAL] Music
  source-url: https://www.youtube.com/watch?v=Gks4Yw9jXSc

• Tavily evidence Revit(기초) 12. 간섭 보고
  ### Tag

BIM, REVIT, Revit 2022, 레빗, 레빗 2022

### '황 야의 Revit 2022'의 다른글

 이전글Revit(기초) 11. 룸 및 색상 범례
 현재글Revit(기초) 12. 간섭 보고
 다음글Revit(기초) 13. 일조 연구 및 보행 시선

### 관련글

 Revit(기초) 13. 일조 연구 및 보행 시선 2023.08.28
 Revit(기초) 11. 룸 및 색상 범례 2023.08.20
 Revit(기초) 10. 일람표 작성하기 2023.07.03
 Revit(기초) 09. 치수 및 지
  source-url: https://hwang-ya.tistory.com/entry/Revit%EA%B8%B0%EC%B4%88-12-%EA%B0%84%EC%84%AD-%EB%B3%B4%EA%B3%A0

검토 기준: 공식 문서 여부, 최신성, 프로젝트 적용 가능성, 보안/개인정보 포함 여부를 확인한 뒤 표준/교육/FAQ 후보로 승격한다.


## 웹 보강: Revit 뷰템플릿 일괄 적용 방법 (2026-06-16 07:53:05)
- Source: system-auto-quality-search
- Tags: kst04-collected-review,kst02-review

질문: Revit 뷰템플릿 일괄 적용 방법

• DDG evidence External Commands - Autodesk Knowledge Network
  External Applications that can be invoked. External Tools that can be added to the Revit External Tools menu-button. External Application session adds panels and content to the Add-ins tab. IExternalCommand You create an external command by creating an object that implements the IExternalCommand int
  source-url: https://help.autodesk.com/cloudhelp/2024/ENU/Revit-API/files/Revit_API_Developers_Guide/Introduction/Add_In_Integration/Revit_API_Revit_API_Developers_Guide_Introduction_Add_In_Integration_External_Commands_html.html

• DDG evidence Creating C# Plugins for Revit: A Complete Developer Guide
  Step-by-step guide to building custom C# plugins for Autodesk Revit. Covers project setup, Revit API, external commands, ribbon UI, transactions, and deployment.
  source-url: https://archgyan.com/creating-csharp-plugins-for-revit/

• DDG evidence IExternalCommand Interface - revitapidocs.com
  To add an external command to Autodesk Revit the developer should implement an object that supports the IExternalCommand interface.
  source-url: https://www.revitapidocs.com/2025/ad99887e-db50-bf8f-e4e6-2fb86082b5fb.htm

• DDG evidence Building Your First Structural Plugin for Revit: A C# Crash Course
  Learn to build a Revit structural plugin in C# from scratch. Covers IExternalCommand, FilteredElementCollector, Transactions, .addin manifest setup, and a real beam span-to-depth ratio checker you can run today.
  source-url: https://civilmat.com/revit-plugin-csharp-crash-course/

• DDG evidence Create a Plugin in Revit 2026 with .NET8 — AYDrafting
  1. Context / Introduction Overview: Revit Plugin Types External Commands - Commands invoked from Add-in Tab and implements - IExternalCommand interface External Applications - programmatically add or modify the UI (for instance, create custom ribbon tabs, panels, and buttons) and implements the IExt
  source-url: https://www.aydrafting.com/case/starting-a-project-in-revit-2026-net8-api

검토: 공식문서·최신성·적용성 확인 후 FAQ 승격.

## 2026-06-20 Revit Add-in 재현/환경차 실무 케이스 Q&A
- Source: `knowledge/40_curation/quality/2026-06-20_ALL_AGENTS_PRACTICAL_CASE_LIBRARY.md`
- Tags: revit,addin,field-case,debugging,journal,api,qa,2026

**Q: 고객 모델에서만 오류가 나고 샘플 모델에서는 재현되지 않으면 어떻게 하나요?**
A: 재현 실패로 종료하지 않는다. 고객 환경 차이를 줄이기 위해 Revit 버전, Add-in 버전, Journal 파일, LUA 로그, 오류 직전 명령 순서, 링크 모델 사용 여부를 요청한다. 실제 프로젝트 모델은 마지막 수단이며, 민감정보 제거와 고객 동의가 필요하다.


실무 보강 (2026-06-20 답변 품질 보강):
1. 기준 확인: `Revit_Addin` 담당자는 이 질문을 단순 설명이 아니라 KST02 이상 운영 기준, 프로젝트 범위, 고객 영향도, 납품/계약 책임을 함께 확인하는 실무 판단 문제로 본다.
2. 조건 분기: 확정 기준, 현장 예외, 고객 요청, 내부 승인 여부를 먼저 나눈다. 수치나 법규가 필요한 경우에는 시행일, 적용 대상, 원문 출처, LOD 300/350 같은 모델 상세 수준을 확인하기 전까지 단정하지 않는다.
3. 다음 액션: 24시간 안에 현재 자료와 누락 자료를 정리하고, 7일 안에 담당자·기한·검증 방법이 있는 조치 항목으로 바꾼다. 반복 문의는 QA로 남기고 2회 이상 반복되면 KB 본문 승격 후보로 올린다.
4. 리스크 경계: 비용, 일정, 안전, 개인정보, 법무, 고객 약속으로 번질 수 있는 내용은 즉답보다 확인 로그와 승인 경로를 우선한다. 불확실한 답은 '가능/불가'보다 확인 조건과 대안 2개를 함께 제시한다.
5. 답변 형식: 결론 1문장, 근거 2개, 확인할 자료 3개, 다음 행동 1개 순서로 응답한다. Source: LUA BIM LABS agent QA quality baseline. Tags: qa,quality,field-case,kst02,risk,2026.

## 2026-06-21 Revit Add-in 배포/장애 추가 Q&A
- Source: LUA BIM LABS coverage expansion
- Tags: revit,addin,api,deployment,journal,2026

**Q: Add-in 설치 후 버튼이 보이지 않으면 코드 오류로 봐야 하나요?**
A: 결론: 코드 오류로 단정하지 말고 .addin manifest, 설치 경로, Revit 버전, DLL 차단 여부를 먼저 확인한다. 1. Revit 2024/2025 버전, Add-in manifest 경로, Assembly 경로, RuntimeRequirements, Windows 보안 차단, Source/Tags를 기록한다. 2. 조건상 manifest가 누락된 경우 설치 패키지 이슈로 보고, 반면 버튼은 보이지만 실행 실패하면 IExternalCommand와 로그를 검토한다. 오판하면 고객 대응 지연, 배포 오류, 비용, 책임 리스크가 생긴다. 24시간 내 Add-in 담당자가 설치 로그를 요청·기록하고 7일 내 승인자, 기한, 수정 배포 로그를 공유한다.

**Q: Revit Add-in이 모델을 수정하다가 중간에 실패하면 어떻게 복구하나요?**
A: 결론: 실패 후 수동 복구를 지시하기 전에 Transaction 범위, 백업, 변경 로그, 실패 요소를 확인한다. 1. TransactionGroup, ElementId, Journal, LUA 로그, 모델 Revision, LOD 300/350 영향, Source/Tags를 확인한다. 2. 조건상 Transaction rollback이 정상 동작하면 재실행 조건을 안내하고, 반면 일부 요소가 변경된 경우 백업 모델 또는 변경 목록으로 복구한다. 복구 기준이 없으면 모델 손상, 납품 지연, 고객 데이터 책임, 법무 리스크가 생긴다. 24시간 내 담당자가 실패 재현 파일을 기록·공유하고 7일 내 승인권자, 기한, 패치/롤백 로그를 보고한다.
**Q: 파라미터 값을 바꾸는 기능이 일부 요소에서만 실패하면 무엇을 의심하나요?**
A: Instance/Type 파라미터 구분, 읽기 전용 파라미터, 공유 파라미터 누락, 링크 모델 요소, 그룹/옵션/패밀리 문서 여부를 확인한다. 고객에게는 "기능 오류"로 단정하지 않고 실패 요소 3개와 정상 요소 3개의 ElementId 또는 샘플을 요청한다.


실무 보강 (2026-06-20 답변 품질 보강):
1. 기준 확인: `Revit_Addin` 담당자는 이 질문을 단순 설명이 아니라 KST02 이상 운영 기준, 프로젝트 범위, 고객 영향도, 납품/계약 책임을 함께 확인하는 실무 판단 문제로 본다.
2. 조건 분기: 확정 기준, 현장 예외, 고객 요청, 내부 승인 여부를 먼저 나눈다. 수치나 법규가 필요한 경우에는 시행일, 적용 대상, 원문 출처, LOD 300/350 같은 모델 상세 수준을 확인하기 전까지 단정하지 않는다.
3. 다음 액션: 24시간 안에 현재 자료와 누락 자료를 정리하고, 7일 안에 담당자·기한·검증 방법이 있는 조치 항목으로 바꾼다. 반복 문의는 QA로 남기고 2회 이상 반복되면 KB 본문 승격 후보로 올린다.
4. 리스크 경계: 비용, 일정, 안전, 개인정보, 법무, 고객 약속으로 번질 수 있는 내용은 즉답보다 확인 로그와 승인 경로를 우선한다. 불확실한 답은 '가능/불가'보다 확인 조건과 대안 2개를 함께 제시한다.
5. 답변 형식: 결론 1문장, 근거 2개, 확인할 자료 3개, 다음 행동 1개 순서로 응답한다. Source: LUA BIM LABS agent QA quality baseline. Tags: qa,quality,field-case,kst02,risk,2026.
**Q: Revit 버전 업데이트 후 기능이 갑자기 안 된다는 문의에는 어떻게 답하나요?**
A: 먼저 지원 버전과 현재 설치 버전을 확인한다. Revit API 변경, .NET 런타임, ElementId/ForgeTypeId 변경, manifest 경로 차이가 원인일 수 있다. 임시 답변에는 지원 버전, 호환 업데이트 예정, 우회 방법, 로그 요청을 함께 포함한다.

실무 보강 (2026-06-20 답변 품질 보강):
1. 기준 확인: `Revit_Addin` 담당자는 이 질문을 단순 설명이 아니라 KST02 이상 운영 기준, 프로젝트 범위, 고객 영향도, 납품/계약 책임을 함께 확인하는 실무 판단 문제로 본다.
2. 조건 분기: 확정 기준, 현장 예외, 고객 요청, 내부 승인 여부를 먼저 나눈다. 수치나 법규가 필요한 경우에는 시행일, 적용 대상, 원문 출처, LOD 300/350 같은 모델 상세 수준을 확인하기 전까지 단정하지 않는다.
3. 다음 액션: 24시간 안에 현재 자료와 누락 자료를 정리하고, 7일 안에 담당자·기한·검증 방법이 있는 조치 항목으로 바꾼다. 반복 문의는 QA로 남기고 2회 이상 반복되면 KB 본문 승격 후보로 올린다.
4. 리스크 경계: 비용, 일정, 안전, 개인정보, 법무, 고객 약속으로 번질 수 있는 내용은 즉답보다 확인 로그와 승인 경로를 우선한다. 불확실한 답은 '가능/불가'보다 확인 조건과 대안 2개를 함께 제시한다.
5. 답변 형식: 결론 1문장, 근거 2개, 확인할 자료 3개, 다음 행동 1개 순서로 응답한다. Source: LUA BIM LABS agent QA quality baseline. Tags: qa,quality,field-case,kst02,risk,2026.

## 2026-06-21 Revit Add-in 보안배포 추가 Q&A
- Source: LUA BIM LABS coverage expansion
- Tags: revit,addin,deployment,security,manifest,2026

**Q: 고객 PC에서 Add-in DLL이 보안 차단되면 설치 파일을 다시 보내면 되나요?**
A: 결론: 재전송보다 차단 원인, 서명 상태, 배포 경로, Revit 버전 호환성을 먼저 확인한다. 1. DLL 서명, Windows SmartScreen, .addin manifest 경로, Revit 2024/2025/2026, .NET 런타임, 설치 로그, Source/Tags를 확인한다. 2. 조건상 다운로드 차단이면 신뢰 배포 채널과 해시 값을 안내하고, 반면 DLL 변조나 출처 불명확 경고이면 우선 배포를 중단한다. 다만 고객 관리자 권한으로 강제 해제해야 하는 경우 예외 없이 보안 승인과 책임 범위를 구분한다. 성급한 재배포는 보안 누수, 설치 오류, 고객 장애, 법무 책임 리스크를 만든다. 24시간 내 Add-in 담당자가 차단 로그를 기록·공유하고 7일 내 승인권자, 기한, 재배포/롤백 로그를 보고한다.
