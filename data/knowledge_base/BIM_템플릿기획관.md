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

## BIM 템플릿기획관 Claude Code 심화 업데이트 (2026-05-28)
- Source: claude-code-enhanced 2026-05-28
- Tags: Revit템플릿, 공유파라미터, 뷰템플릿, 패밀리표준화, BIM표준화, MEP

Revit 프로젝트 템플릿(.rte)은 회사·발주처 표준을 사전 설정하여 프로젝트 일관성을 확보하는 핵심 산출물이다. LUA BIM LABS 표준 템플릿은 국토교통부 BIM 지침과 buildingSMART Korea 지침을 반영하여 건축·구조·MEP 공종별로 분리 관리한다.
- 공유 파라미터(Shared Parameters) 표준: 공유 파라미터 파일(.txt)을 회사 표준으로 단일화하고, 파라미터 GUID를 변경하지 않는 원칙을 준수한다. MEP 필수 파라미터: 시스템 약어(System Abbreviation), 서비스 타입(Service Type), 도면 기호(Drawing Symbol), LOD 등급(LOD Grade). 파라미터 그룹은 PG_IDENTITY_DATA, PG_MECHANICAL, PG_ELECTRICAL, PG_PLUMBING으로 분류한다.
- 뷰 템플릿(View Template) 체계: 뷰 종류별(평면·입면·단면·3D) × 공종별(건축·구조·MEP) × 단계별(DD/CD/시공) 조합으로 뷰 템플릿을 사전 정의한다. MEP 평면도는 공조(HVAC)·위생(Plumbing)·전기(Electrical) 레이어를 별도 뷰 템플릿으로 분리한다.
- 패밀리 표준화: 자사 패밀리 라이브러리는 OmniClass 분류 기반으로 폴더 구조를 구성한다. 패밀리 파일명 규칙: [공종코드]_[장비명]_[크기]_LUA.rfa. Revit Add-in으로 패밀리 배치 시 공유 파라미터 자동 입력 기능을 적용한다.
- 템플릿 배포 관리: 연 1회 Revit 버전 업그레이드 시 템플릿 호환성 검증→수정→Git 버전 관리→전사 배포 프로세스를 수행한다.
- 관련: [[Revit_Addin]] · [[BIM_지침서]] · [[설비장비]]

## BIM 템플릿 기획 실전 심화 (2026-05-28)
- Source: claude-code-enhanced 2026-05-28
- Tags: revit-template,shared-parameter,view-template,family,bim-standard

**Revit 프로젝트 템플릿(.rte) 구성 체크리스트:**
- [ ] 공유 파라미터 파일(.txt) 연결 + 필수 파라미터 그룹 등록
- [ ] 뷰 템플릿 4종: 평면도(DD/CD 분리), 입면도, 단면도, 상세도
- [ ] 필터: 공종별 색상 (건축=파랑, 구조=회색, 소방=빨강, 공조=녹색)
- [ ] 레벨 명명: `1FL(+0)`, `2FL(+4000)` 형식 통일
- [ ] 그리드 명명: 수평 A/B/C..., 수직 1/2/3...
- [ ] 기본 패밀리 로드: 제목 블록·문·창·MEP 기본 기기 세트
- [ ] 시트 번호 체계: A(건축)/S(구조)/M(기계)/E(전기)/P(배관)/F(소방)

**공유 파라미터 관리 규칙:**
- GUID 불변 원칙: 한번 발행된 공유 파라미터 GUID 변경 금지 (모든 프로젝트 동일 GUID)
- 그룹 분류: `LUA_Identity`(식별), `LUA_BIM`(BIM기준), `LUA_FM`(자산관리), `LUA_COBie`
- 명명: `[그룹].[영문명]` — 예: `LUA_BIM.LOD_Level`, `LUA_FM.MaintenanceCycle`
- 버전 관리: Git으로 공유 파라미터 .txt 파일 이력 관리 (변경 시 PR 검토 필수)

**뷰 템플릿 단계별 분리 이유:**
- DD(기본설계) 뷰: 위치·크기 중심 표현, 치수선·태그 간략
- CD(실시설계) 뷰: 파라미터 완전 표기, 상세 치수, 마감 기호 포함
- 통일 효과: 모든 설계자가 같은 뷰 설정 → 도면 품질 균일화, 검토 시간 단축

**패밀리 파일명 규칙:**
`[공종코드]_[카테고리]_[제조사]_[규격].rfa`
- 예: `M_팬코일_LG_FCU-4P-0.8RT.rfa`, `F_스프링클러_세이프티_표준형75A.rfa`
- 공종코드: A(건축), S(구조), M(기계), E(전기), P(위생), F(소방), T(통신)
- 관련: [[Revit_Addin]] · [[Revit_Family제작]] · [[설계_지침서]] · [[BIM_지침서]]


## BIM 템플릿 기획 최신 동향 (2026-05-29)
- Source: auto-enrich via Naver+Tavily+Google+DDG+Ollama 2026-05-29
- Tags: BIM,template,planning,update

- Revit BIM 프로젝트 템플릿 기획 및 관리는 최신 기준과 팁을 고려해야 합니다.
- 공유 파라미터 사용: Revit 2025 템플릿은 Autodesk 포럼에서 제공되며, 이는 프로젝트 설정과 표준을 정의합니다. 공유 파라미터를 활용하여 프로젝트 내부에서 일관된 데이터 관리를 가능하게 합니다 (Revit 2025 templates for Korea on Autodesk forums).
- 뷰 템플릿: BIM 표준 및 인프라 구축 부록에서는 BIM 데이터 작성 수준을 통일하기 위해 뷰 템플릿 개발이 필요합니다. 이는 프로젝트 관리와 협업을 효율화하는 데 도움이 됩니다 (OTKCRK160122.pdf).
- 패밀리 표준화: 조경 BIM 라이브러리 표준화를 위한 연구에서는 KBIMS의 공통 속성 정책을 참고하여 추가 정보를 제공하며, 이는 패밀리 표준화 방향을 제시합니다 (jkila-51-2-103).
- 최신 기준: 한국 BIM 표준(KBIMS)과 Revit 2025 템플릿은 프로젝트 관리와 협업에 있어 중요한 기준이 됩니다. 이를 통해 데이터 작성 수준을 통일하고 일관성을 유지할 수 있습니다 (Revit 2025 templates for Korea on Autodesk forums, OTKCRK160122.pdf).
- 관련: [[건축]] · [[설계_지침서]] · [[시공_지침서]] · [[BIM_지침서]]


## BIM 템플릿 기획 최신 동향 (2026-05-30)
- Source: auto-enrich via Naver+Tavily+Google+DDG+Ollama 2026-05-30
- Tags: BIM,template,planning,update

- Revit BIM 프로젝트 템플릿 기획 및 관리에서 최신 기준을 따르는 것이 중요합니다. 2025년 버전의 Revit 템플릿은 한국에서는 공통된 가구 라이브러리와 템플릿을 통해 일관된 BIM 표준을 유지하고 있습니다.
- BIM Depot Revit Template은 프로젝트 시작 속도를 높이는 데 도움이 되며, 이는 Revit BIM 프로젝트 관리를 위한 효과적인 도구입니다. 
- 공유 파라미터 사용은 데이터의 일관성과 재사용성을 향상시킵니다. 각 요소에 대한 정보를 저장하고 공유할 수 있어, 프로젝트 내에서 효율적으로 협업할 수 있습니다.
- 뷰 템플릿을 통해 다양한 시각화 요구사항을 충족시키며, 이를 통해 프로젝트의 일관된 시각적 표준을 유지할 수 있습니다. 
- 패밀리 표준화는 BIM 모델링의 질을 높이는 데 중요하며, 이는 모든 설계 요소에 대한 일관된 정의와 규격을 제공합니다. 이를 통해 프로젝트 내에서 효율적인 협업과 통합이 가능해집니다.
- 최신 기준과 팁은 Autodesk 지원 문서를 참고하여 확인할 수 있으며, 이들은 Revit BIM 프로젝트 관리에 대한 실질적인 가이드라인을 제공합니다.
- 관련: [[건축]] · [[설계_지침서]] · [[시공_지침서]] · [[BIM_지침서]]
