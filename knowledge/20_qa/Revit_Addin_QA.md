

## Telegram 팀원 보강 요청 (2026-06-06 15:09:03)
- Source: telegram:@FreeFilmer (7899169126)
- Tags: telegram,team-request,knowledge-gap,needs-review

팀원이 기존 Obsidian 답변이 부족하다고 회신했다.

원 질문: revit 간섭 검토시 고려해야 하는 공종간 회피해야하는 공종에 대한 우선순위 알고 싶어
추가 요청: 추가 설명 없음

처리 기준:
1. 내부 지식에서 누락된 기준을 우선 보강한다.
2. 외부 검색 또는 공식 문서 확인이 필요한 항목은 자동 수집 후 지식 업데이트 후보로 표시한다.
3. 고객명, 프로젝트명, 개인정보는 수집하지 않는다.


## Telegram 더 찾아줘 자동 수집 결과 (2026-06-06 15:09:07)
- Source: telegram-auto-search:@FreeFilmer (7899169126)
- Tags: telegram,team-request,auto-collect,needs-review

원 질문: revit 간섭 검토시 고려해야 하는 공종간 회피해야하는 공종에 대한 우선순위 알고 싶어
추가 요청: 추가 설명 없음

자동 수집 결과:

• [Tavily] Tavily AI 요약
  To avoid interference in Revit, focus on avoiding conflicts between structural and electrical components. Use Revit's built-in interference check tool to identify and resolve overlaps. Ensure your add-in manifest correctly references necessary DLLs for API integration.
  출처: 

• [Tavily] building revit plug-ins with visual studio: part two | archi-lab
  So there it is. We have the structure of our plug-in in place. We defined the sequence of how we will create our plug-in using pseudo code, we implemented IExternalCommand with Transaction Attribute and prepared ourselves for potential errors and how to handle them. Now, we just need to add a \.addi
  출처: https://archi-lab.net/building-revit-plug-ins-with-visual-studio-part-two

• [Tavily] [PDF] Preparing Apps for the Store: Guidelines
  Revit goes through the common install folder and parse for Revit apps for the appropriate environments (RuntimeRequirements) 2.
Revit picks up the location of addin manifest (ModuleName) 3.
Read .addin manifest and load the app. Revit App Auto Load Flow <?xml version="1.0" encoding="utf-8"?> <Applic
  출처: https://damassets.autodesk.net/content/dam/autodesk/www/developer-network/app-store/revit/pdf/3%20Autodesk%20Exchange%20Publish%20Revit%20Apps%20-%20Preparing%20Apps%20for%20the%20Store_Guidelines.pdf

• [Tavily] Revit API Docs
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
  출처: https://www.revitapidocs.com

• [Tavily] Practice Revit MEP / 전기 BIM / 간섭 확인하기 및 해결하기 - YouTube
  Practice Revit MEP / 전기 BIM / 간섭 확인하기 및 해결하기 1. 간섭 확인하기 2. 간섭 해결하기 Music from YouTube Audio Library [Aka YAL] Music
  출처: https://www.youtube.com/watch?v=Gks4Yw9jXSc

• [Tavily] Revit(기초) 12. 간섭 보고
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
  출처: https://hwang-ya.tistory.com/entry/Revit%EA%B8%B0%EC%B4%88-12-%EA%B0%84%EC%84%AD-%EB%B3%B4%EA%B3%A0

검토 기준: 공식 문서 여부, 최신성, 프로젝트 적용 가능성, 보안/개인정보 포함 여부를 확인한 뒤 표준/교육/FAQ 후보로 승격한다.


## 웹 보강: Revit 뷰템플릿 일괄 적용 방법 (2026-06-16 07:53:05)
- Source: system-auto-quality-search
- Tags: auto-collect,needs-review

질문: Revit 뷰템플릿 일괄 적용 방법

• [DDG] External Commands - Autodesk Knowledge Network
  External Applications that can be invoked. External Tools that can be added to the Revit External Tools menu-button. External Application session adds panels and content to the Add-ins tab. IExternalCommand You create an external command by creating an object that implements the IExternalCommand int
  출처: https://help.autodesk.com/cloudhelp/2024/ENU/Revit-API/files/Revit_API_Developers_Guide/Introduction/Add_In_Integration/Revit_API_Revit_API_Developers_Guide_Introduction_Add_In_Integration_External_Commands_html.html

• [DDG] Creating C# Plugins for Revit: A Complete Developer Guide
  Step-by-step guide to building custom C# plugins for Autodesk Revit. Covers project setup, Revit API, external commands, ribbon UI, transactions, and deployment.
  출처: https://archgyan.com/creating-csharp-plugins-for-revit/

• [DDG] IExternalCommand Interface - revitapidocs.com
  To add an external command to Autodesk Revit the developer should implement an object that supports the IExternalCommand interface.
  출처: https://www.revitapidocs.com/2025/ad99887e-db50-bf8f-e4e6-2fb86082b5fb.htm

• [DDG] Building Your First Structural Plugin for Revit: A C# Crash Course
  Learn to build a Revit structural plugin in C# from scratch. Covers IExternalCommand, FilteredElementCollector, Transactions, .addin manifest setup, and a real beam span-to-depth ratio checker you can run today.
  출처: https://civilmat.com/revit-plugin-csharp-crash-course/

• [DDG] Create a Plugin in Revit 2026 with .NET8 — AYDrafting
  1. Context / Introduction Overview: Revit Plugin Types External Commands - Commands invoked from Add-in Tab and implements - IExternalCommand interface External Applications - programmatically add or modify the UI (for instance, create custom ribbon tabs, panels, and buttons) and implements the IExt
  출처: https://www.aydrafting.com/case/starting-a-project-in-revit-2026-net8-api

검토: 공식문서·최신성·적용성 확인 후 FAQ 승격.
