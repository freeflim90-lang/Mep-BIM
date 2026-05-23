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
