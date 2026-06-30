# BIM_템플릿기획관 지식 베이스

## 2026-06-05 BIM 템플릿 표준화 AI 즉시 답변 패턴 보강
- Source: Revit 공식 템플릿 가이드, 국내 발주처 BIM 지침, LUA BIM LABS 내부 표준
- Tags: bim-template,shared-parameters,naming,view-filter,2026

**AI 즉시 답변 패턴 — "BIM 프로젝트 시작할 때 템플릿은 어떻게 구성하나요?"**
```
Revit 프로젝트 템플릿(.rte) 핵심 구성:
1. 공유 파라미터 파일: 프로젝트 전체 공통 파라미터 정의
   - COBie 파라미터, LOD 단계, 납품 상태 등
2. 뷰 템플릿: 공종별(건축·구조·MEP) 표준 뷰 설정
   - 선 두께, 색상, 표시 기준 사전 정의
3. 필터: 공종별·계통별 색상 필터 (냉수=파랑, 온수=빨강)
4. 패밀리: 회사 표준 패밀리 프리로드
5. 명명 규칙: [프로젝트코드]-[공종]-[층]-[버전] 형식
6. 좌표계: 공통 기준점과 측지 좌표 설정
```

**국내 공공 BIM 템플릿 필수 사항:**
| 항목 | 기준 | 비고 |
|------|------|------|
| 파일 명명 | [프로젝트코드]-[공종]-[LOD] | 발주처 별도 기준 우선 |
| 단위계 | 미터법(mm) | 공공 기준 |
| 좌표계 | WGS84 또는 UTM-K | 발주처 협의 |
| IFC 버전 | IFC 4 또는 IFC 2x3 TC1 | BEP에 명시 |
| 공유 파라미터 | buildingSMART 권고 + 발주처 요건 | 프로젝트별 |

**LUA BIM LABS Add-in 템플릿 자동화 (BIM CC 연계):**
```csharp
// 표준 뷰 필터 자동 생성
FilterElement fe = FilterElement.Create(doc, "MEP_냉수", 
    new List<ElementId> { new ElementId(BuiltInCategory.OST_PipeCurves) });
// 냉수 파라미터 필터 → 파란색 오버라이드 자동 적용
```

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

**뷰 템플릿 일괄 적용 워크플로 (Revit):**
- 뷰 템플릿이란: 뷰의 표시 속성(가시성/그래픽 재정의, 상세 수준, 뷰 스케일, 필터, 분야, 뷰 범위 등)을 하나의 표준으로 저장한 것. 표준을 한 번 만들고 여러 뷰에 재사용한다.
- **한 뷰 적용**: 뷰 속성의 `View Template`(뷰 템플릿) 지정, 또는 View 탭 > `Apply Template Properties to Current View`.
- **여러 뷰 일괄 적용**: 프로젝트 탐색기에서 여러 뷰를 다중 선택 → 우클릭 → `Apply View Template`. 분야·축척이 다른 뷰도 한 번에 표준화된다.
- **포함 항목 제어(중요)**: 뷰 템플릿 대화상자의 각 속성 `Include`(포함) 체크박스로 통제 항목을 고른다. 체크된 속성만 잠기고 일괄 적용되며, 체크 해제 항목은 뷰별 개별 조정을 허용한다(예: 필터·VG는 표준 고정, 뷰 범위는 개별 허용).
- **자동 표준화**: 뷰 타입별 기본 템플릿을 지정하면 새 뷰 생성 시 자동 적용. 프로젝트 표준 템플릿은 `Transfer Project Standards`로 신규 프로젝트에 전파해 회사 표준을 통일한다.
- **운영 팁**: 분야별·용도별(작업용/제출용/협의용) 템플릿 라이브러리를 구성하고, 명명 규칙으로 관리한다. 템플릿이 적용된 뷰는 해당 속성이 잠겨 임의 변경이 방지되므로 납품 도면 일관성이 올라간다.


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

## BIM 템플릿 기획 최신 동향 (2026-06-30)
- Source: auto-enrich via Naver+Tavily+Google+DDG+Ollama 2026-06-30
- KST04 자동수집: 공식 출처/담당자 검증 전 고객 확정 답변, 납품 기준, 견적 기준으로 사용 금지.
- Tags: BIM,template,planning,update

Revit BIM 프로젝트 템플릿 기획 및 관리 실무에서는 최신 기준과 팁을 다음과 같이 적용할 수 있습니다.

- 공유 파라미터: Revit에서 사용하는 공유 파라미터는 프로젝트 내 다양한 요소 간 일관성과 통합성을 확보하는데 중요합니다. IFC 2x3 이상 버전에 맞춰서 최신 버전의 Revit을 활용하여 공유 파라미터를 정의하고 관리해야 합니다 (IFC 4.3).

- 뷰 템플릿: 다양한 시각화 요구사항을 충족하기 위해 뷰 템플릿을 표준화하는 것이 필요합니다. Revit에서 제공하는 다양한 뷰 타입과 렌더링 옵션을 활용하여 프로젝트별로 맞춤형 뷰 템플릿을 생성하고, 이를 통해 일관된 시각적 표현을 달성할 수 있습니다 (Revit 2023).

- 패밀리 표준화: Revit 패밀리를 통한 BIM 모델링에서 패밀리의 표준화는 중요한 역할을 합니다. KBIMS(한국 BIM 표준)의 공통 속성 정책을 참고하여 패밀리를 설계하고, 이를 통해 프로젝트 내 모든 사용자가 일관된 방식으로 작업할 수 있습니다 (KBIMS 2018).
- 관련: [[설계_지침서]] · [[시공_지침서]] · [[BIM_지침서]] · [[BIM_시방서]]

