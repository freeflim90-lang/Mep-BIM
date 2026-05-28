# BIM_템플릿기획관 지식 베이스


## BIM 템플릿 기획 기준 (2026-05-19 09:16:50)
- Source: LUA BIM LABS curated baseline, Autodesk official docs checked 2026-05-19
- Tags: bim-template,parameters,standards

BIM 템플릿기획관은 공유 파라미터, 카테고리, 뷰/필터, 패밀리 명명 규칙, 보고서 필드 표준을 정리해 Add-in이 일관된 데이터 구조를 쓰도록 한다.


## 공유 파라미터 표준 설계 기준 (2026-05-19 17:26:40)
- Source: LUA BIM LABS domain knowledge baseline 2026-05-19
- Tags: bim-template,shared-parameter,revit

공유 파라미터 파일 관리: 프로젝트 서버 또는 BIM 360/ACC에 단일 파일 버전 관리.
파라미터 명명: [공종]_[항목명]_[단위] (예: MEP_관경_mm, STR_보강필요여부)
카테고리 배정: 해당 패밀리 카테고리에만 배정 (전체 카테고리 배정 금지)
데이터 타입: 수치는 Length/Area/Volume 타입 사용 (텍스트 수치 금지)
Add-in이 읽는 파라미터는 모두 공유 파라미터로 표준화하여 프로젝트 간 이식성 확보.


## 뷰 템플릿 및 필터 기준 (2026-05-19 17:26:40)
- Source: LUA BIM LABS domain knowledge baseline 2026-05-19
- Tags: bim-template,view-template,filter

공종별 협의도 뷰 템플릿: 구조 협의(구조+건축 가시), MEP 협의(MEP+구조 가시).
필터 규칙: 계통별 색상 코드 고정 (공조배관=파랑, 소방=빨강, 전기=노랑, 통신=초록).
Add-in 보고서 뷰: 별도 3D 뷰 자동 생성 → 충돌 마커만 표시.
패밀리 명명: [공종]_[기능]_[규격] (예: MEP_배관_DN100, STR_보_H300×150).


## BIM 템플릿 기획 최신 동향 (2026-05-28)
- Source: auto-enrich via Naver+Tavily+Google+DDG+Ollama 2026-05-28
- Tags: BIM,template,planning,update

- 최신 Revit BIM 프로젝트 템플릿 기획 및 관리 실무에서는 공유 파라미터의 표준화가 중요하다. 2025년 Korea Revit template BIM 표준에 따르면, 공유 파라미터는 다양한 프로젝트에서 일관된 데이터를 생성하기 위해 필수적이다.
- 뷰 템플릿도 중요한 구성 요소다. Autodesk의 BIM-MEP AUS 템플릿은 효율적인 BIM 전달을 위한 일관성을 제공한다. 이를 활용하여 뷰 설정을 통일화하고, 프로젝트 관리의 효율성을 높일 수 있다.
- 패밀리 표준화는 BIM 프로젝트에서 필수적이다. 한국 BIM 표준(KBIMS)에 따르면, 공통 속성 정의를 기반으로 하여 조경 객체 및 속성 정보 분류 체계를 구축해야 한다.
- BIM 데이터 작성 수준을 명시하고 통일된 데이터 관리를 위해 BIM 실행 계획서 템플릿을 개발하는 것이 중요하다. 이를 통해 프로젝트 진행 시 일관된 데이터 작성 스탠다드를 유지할 수 있다.
