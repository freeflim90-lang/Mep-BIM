# BIM 지침서 지식 베이스

## 초기 기준
LOD 기준, 명명규칙, 좌표계, 모델 분리, 협업 환경, IFC 내보내기, BIM 데이터 품질 기준을 통합 관리한다. 국토교통부 BIM 지침 및 buildingSMART 국제 표준을 기반으로 한다.


## LOD(Level of Development) 기준표 — LOD 100~500 (2026-05-26)
- Source: LUA BIM LABS curated baseline, BIMForum LOD Specification, 국토교통부 건축BIM 활성화 로드맵 2026-05-26
- Tags: bim,lod,level-of-development,model-progression

LOD는 BIM 요소의 기하학적 정밀도(Geometry)와 정보 완성도(Information)를 함께 정의한다.

LOD 100 — 개념 수준 (Conceptual):
- 기하학: 매스, 볼륨, 면적 표현. 실제 형상 불필요, 심볼·아이콘 대체 가능.
- 정보: 유형, 대략적 면적·부피, 개략 사업비.
- 적용 단계: 기획설계.
- 활용: 용적률·건폐율 검토, 개산 사업비 산출, 일조·조망 시뮬레이션.

LOD 200 — 개략 수준 (Approximate Geometry):
- 기하학: 일반적인 크기·형상·위치·방향 표현. 치수 불확정 허용.
- 정보: 주요 재료, 시스템 종류, 개략 물량.
- 적용 단계: 계획설계.
- 활용: 공간 배치 검토, 주요 공종 시스템 결정, 인허가 도서 작성.

LOD 300 — 정밀 수준 (Precise Geometry):
- 기하학: 실제 크기·형상·위치·방향 정밀 표현. 도면 추출 가능 수준.
- 정보: 재료 사양, 제조사 계열, 성능 파라미터(강도, 열관류율 등).
- 적용 단계: 기본설계.
- 활용: 공종 간 BIM 간섭 검토, 물량 산출, 비용 견적.

LOD 350 — 시공 연계 수준 (Construction Coordination):
- 기하학: LOD 300 수준 + 인접 요소와의 연계 정보(슬리브, 인서트, 행거 위치).
- 정보: 접합 상세, 시공 방법, 시공 순서, 공정 코드(Activity ID).
- 적용 단계: 실시설계 ~ 시공 착수.
- 활용: Shop Drawing 추출, 공종 간 최종 간섭 해소, 4D 시뮬레이션.

LOD 400 — 제작·시공 수준 (Fabrication):
- 기하학: 실제 제작·시공에 쓰이는 완전한 상세 형상.
- 정보: 제조사, 모델번호, 설치 지침, 시공 접합부 완전 정의.
- 적용 단계: 시공 중.
- 활용: 공장 제작 도면(Fabrication Drawing), 프리팹(Prefab) 제작, 현장 설치 검증.

LOD 500 — 준공·유지관리 수준 (As-Built / FM):
- 기하학: 실제 시공 결과(As-Built) 반영 형상. 측량 실측값 기반.
- 정보: 설치 완료 장비 상세 (시리얼번호, 보증일, 유지관리 주기, 관련 문서 링크).
- 적용 단계: 준공 ~ 유지관리.
- 활용: 시설물 유지관리(FM BIM), CAFM/CMMS 시스템 연동.

LOD 적용 시 주의 사항:
- LOD는 요소별로 다르게 적용할 수 있다. 단계별 LOD 기준표에서 요소별 LOD를 명시한다.
- LOD 300 이상부터 BIM 모델에서 도면 직접 추출을 원칙으로 한다.
- LOD 500 달성을 위해 준공 BIM 업데이트는 시공 완료 후 30일 이내 수행한다.


## BIM 모델 명명규칙 — 파일명, 요소명, 파라미터명 (2026-05-26)
- Source: LUA BIM LABS internal BIM naming standard, BS EN ISO 19650 Part 2 기준 2026-05-26
- Tags: bim,naming,file-naming,element-naming,parameter,convention

BIM 파일 명명규칙:
- 형식: [프로젝트코드]_[조직코드]_[공종코드]_[단계코드]_[구역코드]_Rev[번호]
- 예시: LUA-PROJ01_LUA_A_CD_ZN-ALL_Rev03.rvt
  - 프로젝트코드: 발주처 지정 또는 LUA 내부 코드 (4~8자리)
  - 조직코드: LUA(루아), DS(설계사), CM(CM사), SC(시공사)
  - 공종코드: A(건축), S(구조), M(기계), P(배관), E(전기), FA(소방), C(토목)
  - 단계코드: SD(기본설계), DD(실시설계), CD(시공도), AB(준공)
  - 구역코드: ZN-ALL(전체), ZN-A(A구역), ZN-B1(지하1층)
  - Rev번호: 01부터 시작, 승인본은 짝수 권장(01=초안, 02=승인)
- 파일명에 한글, 특수문자(!@#$%^&*), 공백 사용 금지.
- 날짜를 파일명에 포함할 경우: YYYYMMDD 형식만 허용.

패밀리 파일 명명규칙:
- 형식: [공종코드]_[요소유형]_[세부사양]_[제조사옵션]
- 예시: M_AHU_수평형_A사.rfa, E_패널_분전반_300A.rfa, FA_스프링클러_습식_표준형.rfa
- 공용 패밀리: LUA_공종코드_요소명.rfa (예: LUA_S_보-H형강.rfa)

BIM 요소 명칭(Type Name) 기준:
- 형식: [재질/계통]-[규격]-[기타사양]
- 구조 보: RC-보-600x300, H형강-H300x150x6.5x9
- 배관: 급수관-DN50-SGP, 냉수관-DN100-STPG370
- 덕트: SA-덕트-400x300-아연도강판, RA-덕트-600x400
- 케이블 트레이: CT-강전-W400-H100, CT-약전-W200-H75

파라미터 명명규칙:
- 공유 파라미터 파일명: [프로젝트코드]_SharedParameters_[버전].txt
- 파라미터명: [공종접두사]_[내용]_[단위옵션]
  - 예: S_구조부재유형, M_설계유량_CMH, E_회로번호, FA_헤드종류
- 파라미터 그룹: 공종별 탭으로 분류 (건축, 구조, 기계, 전기, 소방, 공통)
- 공통 필수 파라미터 (전 공종): 공종코드, LOD, 승인상태, 담당자, 최종수정일


## 좌표계 설정 기준 — 프로젝트 원점, 측량 좌표, 공유 좌표 (2026-05-26)
- Source: LUA BIM LABS internal coordinate standard, Autodesk Revit 좌표계 운영 기준 2026-05-26
- Tags: bim,coordinate,survey-point,project-basepoint,shared-coordinates,origin

Revit 좌표계 3요소 정의:
1. Internal Origin(내부 원점): Revit 내부 수학적 계산 기준점. 절대 이동 금지.
2. Project Base Point(프로젝트 기준점, PBP): 프로젝트 상대 좌표 원점. 건물 주요 그리드 교점 또는 건물 모서리 지정.
3. Survey Point(측량 기준점, SP): 실제 현장 측량 절대 좌표(국가 좌표계 또는 현장 임시 좌표) 연결점.

좌표계 설정 절차 (프로젝트 시작 시 1회):
1. 측량 성과 확인: 측량 회사로부터 SP 좌표(N, E, Z), 방위각(North Angle) 수령.
2. Survey Point 이동: Revit에서 SP를 측량 성과 좌표로 이동 (Clip 상태에서 이동).
3. Project Base Point 설정: PBP를 건물 그리드 원점(1번 그리드 교점)에 배치 (Unclip 상태에서 이동).
4. 진북(True North) 설정: 프로젝트 북(Project North)과 진북(True North) 각도 차이 설정 → Site Plan 뷰에 True North 적용.
5. 좌표 발행: 기준 BIM 파일(일반적으로 건축 모델)에서 "Publish Coordinates to Linked Files" 실행.
6. 좌표 수신: 구조·MEP 등 모든 공종 파일에서 "Acquire Coordinates from Linked Files" 실행.
7. 검증: 전 공종 모델 링크 후 그리드 및 레벨 일치 육안 확인.

국가 좌표계 적용 기준 (한국):
- 사용 좌표계: TM(Transverse Mercator) 중부원점 기준 (대부분의 국내 현장).
  - 중부원점: N 500,000m / E 200,000m (WGS84 기준 위도 38°N, 경도 127°E).
- 높이 기준: 인천 인하공전 수준원점(기준 해발 26.6871m) 기준 EL(Elevation Level).
- BIM 레벨 0.0m = 건물 설계 기준 FL(1층 바닥) 또는 GL 기준 — 프로젝트 초기에 확정 필수.

좌표계 오류 방지 체크리스트:
- [ ] Internal Origin에서 PBP까지 거리: 20km 이내 권장 (초과 시 Revit 정밀도 저하).
- [ ] 모든 링크 모델 삽입: "Auto - By Shared Coordinates" 방식.
- [ ] IFC 내보내기: "Shared Coordinates" 옵션 선택.
- [ ] 좌표 변경 금지: 모델 완성 후 PBP, SP 이동 금지 — 위반 시 전 공종 재조정 필요.


## 모델 분리 기준 — 공종별, 구역별, 레벨별 (2026-05-26)
- Source: LUA BIM LABS internal model split standard, Revit Workset 운영 기준 2026-05-26
- Tags: bim,model-split,workset,discipline,zone,level,link

모델 분리 원칙:
- 단일 Revit 파일은 300MB 이하 유지 권장, 500MB 초과 시 반드시 분리.
- 공종별 분리: 건축(A), 구조(S), 기계(M), 전기(E), 소방(FA), 위생(P), 토목(C) 각각 별도 파일.
- 구역별 분리: 연면적 30,000㎡ 이상 또는 동이 2개 이상인 경우 구역(Zone) 분리.
- 레벨별 분리: 지하와 지상을 분리하거나, 기준 레벨 설정 후 레벨별 워크셋 관리.

Workset 구성 기준 (공종 내 분리):
- 공통 Workset:
  - WS_GRID: 그리드, 레벨 (건축 모델에만 존재, 다른 공종 링크)
  - WS_LINK_[공종]: 링크 모델 컨테이너 (예: WS_LINK_구조, WS_LINK_기계)
- 건축 Workset 예시:
  - WS_A_SHELL: 외벽, 지붕, 바닥 구조체
  - WS_A_INTERIOR: 내벽, 문, 바닥 마감
  - WS_A_CEILING: 천장
  - WS_A_FURNITURE: 가구, 비치물 (협의용)
- 구조 Workset 예시:
  - WS_S_FOUNDATION: 기초
  - WS_S_FRAME_B1F~RF: 층별 골조 (층수에 따라 분리)
- MEP Workset 예시:
  - WS_M_HVAC: 공조
  - WS_M_PLUMBING: 위생
  - WS_E_STRONG: 강전
  - WS_E_WEAK: 약전
  - WS_FA_FIRE: 소방

링크 모델 관리 기준:
- 링크 방식: "Overlay" 방식 사용 (Attachment 방식은 중첩 링크 문제 발생 가능).
- 링크 경로: 상대 경로(Relative Path) 설정 필수.
- 링크 모델 업데이트: 주요 변경 후 링크 파일 최신화 및 협업 팀에 공지.
- 링크 모델 공유: ACC(Autodesk Construction Cloud) 또는 공용 서버 폴더 지정.

구역 분리 기준 (대형 프로젝트):
- 구역 코드: ZN-A, ZN-B, ZN-C 또는 동 코드(BLDG-01, BLDG-02) 사용.
- 구역 경계: 구조 그리드 기준 분리 (그리드 사이 구역 경계 지정).
- 공용 구역: COMMON 또는 ZN-COMMON으로 별도 파일 관리.
- 구역 간 간섭 검토: Navisworks에서 전 구역 모델 취합 후 간섭 검토 수행.


## BIM 협업 환경 — ACC, Revit Workset, 링크 모델 관리 (2026-05-26)
- Source: LUA BIM LABS internal BIM collaboration standard, Autodesk Construction Cloud 운영 기준 2026-05-26
- Tags: bim,collaboration,acc,workset,cloud,revit,link-model

ACC(Autodesk Construction Cloud) 운영 기준:
- 프로젝트 폴더 구조:
  ```
  [프로젝트명]/
  ├── 01_BIM모델/
  │   ├── 건축/
  │   ├── 구조/
  │   ├── 기계/
  │   ├── 전기/
  │   ├── 소방/
  │   └── 통합모델(Navisworks)/
  ├── 02_도면/
  │   ├── 설계도면/
  │   └── 시공도면/
  ├── 03_문서/
  │   ├── BEP/
  │   ├── RFI/
  │   ├── NCR/
  │   └── 회의록/
  └── 04_준공/
      ├── As-Built BIM/
      └── 준공도면/
  ```
- 파일 권한 설정: 공종별 팀은 자기 공종 폴더 편집 권한, 타 공종 폴더 열람 권한.
- 모델 업로드 주기: 주 1회 이상 정기 업로드, 주요 변경 시 즉시 업로드.
- BIM 360 Design (Revit Cloud Collaboration): 동시 편집 가능, Workset 기반 작업 범위 분리.

Revit Workset 협업 운영 규칙:
- 작업 시작: 사용할 Workset을 "Editable(편집 가능)"로 설정 후 작업.
- 작업 완료: 반드시 "Relinquish All Mine(내 것 모두 반환)"으로 Workset 반환.
- 동기화 주기: 하루 최소 2회(오전 업무 시작 전, 퇴근 전) "Synchronize with Central" 실행.
- 중앙 파일(Central File): 서버 또는 ACC에 보관, 로컬 파일은 "Local Copy"로만 사용.
- 충돌 방지: 동일 Workset에 2명 이상 동시 편집 금지.

BIM 협업 회의 체계:
- BIM 킥오프 회의: 프로젝트 시작 시 1회 — BEP 합의, 파일 구조 확정, 좌표계 확인.
- 주간 BIM 조율 회의: 매주 1회 — 공종 간 간섭 검토 결과 공유, RFI/NCR 현황.
- 월간 BIM 품질 검토: 매월 1회 — LOD 진척도, 파라미터 입력 완성도, 납품 기준 점검.
- BIM 납품 검토: 단계 완료 시 — 납품물 목록 대비 완성도 확인.

ACC Issues 및 BIM 360 Coordination 활용:
- 간섭 검토 결과는 Autodesk Build Issues로 자동 연동.
- 이슈 담당자: 간섭 발생 공종의 담당 BIM 코디네이터 자동 지정.
- 이슈 기한: 일반 이슈 14일, 중요 이슈 7일, 치명 이슈 72시간.


## IFC 내보내기 표준 — IFC2x3, IFC4, MVD 기준 (2026-05-26)
- Source: LUA BIM LABS internal IFC export standard, buildingSMART IFC 표준, 국토교통부 IFC 납품 기준 2026-05-26
- Tags: bim,ifc,export,ifc2x3,ifc4,mvd,open-bim

IFC 버전 선택 기준:
- IFC2x3 (IFC2x3 TC1): 현재 가장 범용적으로 사용. 구형 소프트웨어 호환.
  - 사용 권장: 발주처 지정 소프트웨어가 IFC4 미지원인 경우, 국내 인허가 제출.
- IFC4 (IFC4 ADD2 TC1): 최신 표준, 더 풍부한 정보 표현 가능.
  - 사용 권장: FM BIM 납품, 국제 프로젝트, buildingSMART 인증 요구 프로젝트.
- IFC4.3: 인프라(토목) 특화 — 도로, 철도, 교량 프로젝트에 적용.

MVD(Model View Definition) 기준:
- CoordinationView 2.0 (IFC2x3): 간섭 검토 목적 — 기하학 중심, 정보 최소화.
- ReferenceView (IFC4): 참조·시각화 목적 — 경량 기하학.
- DesignTransferView (IFC4): 설계 데이터 완전 전달 목적 — 편집 가능 데이터.
- 국토교통부 BIM 납품 기준: CoordinationView 2.0 기본 요구, 발주처 별도 지정 시 준수.

Revit에서 IFC 내보내기 설정:
- 내보내기 좌표: "Shared Coordinates" 선택 (Project Internal 선택 금지).
- 공간(Space) 내보내기: "Export Rooms and Areas" 체크 — FM 용도 시 필수.
- 레벨 기준: "All Levels" 또는 "Visible Levels" 선택.
- IFC 프로젝트 정보: 프로젝트명, 발주처, 주소, 작성자 입력 필수.
- 설정 파일(.ifcxml): IFC 내보내기 설정을 파일로 저장하여 전 공종 동일 설정 적용.
- 매핑 파일: Revit 카테고리 → IFC 엔티티 매핑 확인 (주요 매핑 예시):
  - Structural Framing → IfcBeam
  - Walls → IfcWall
  - Floors → IfcSlab
  - Duct → IfcDuctSegment
  - Pipe → IfcPipeSegment
  - Cable Tray → IfcCableCarrierSegment

IFC 납품 품질 기준:
- IFC 파일 검증 도구: Solibri Model Checker, BIMCollab ZOOM, FZKViewer.
- 필수 확인 항목:
  - IfcProject, IfcSite, IfcBuilding, IfcBuildingStorey 계층 구조 정상 여부.
  - 모든 요소에 GlobalId(GUID) 고유 부여 여부.
  - 좌표계(IfcGeometricRepresentationContext) 설계 기준과 일치 여부.
  - 공간(IfcSpace) 정보 포함 여부 (FM 납품 시 필수).
  - 재료(IfcMaterial) 및 속성집합(IfcPropertySet) 정상 연결 여부.
- 허용 오류: 검증 도구 Critical 오류 0건 (Warning은 목록화 후 발주처 협의).


## BIM 데이터 품질 기준 — 간섭, 미완성 요소, 파라미터 오류 (2026-05-26)
- Source: LUA BIM LABS internal BIM data quality standard, ISO 19650 Part 2, Autodesk BIM 360 품질 기준 2026-05-26
- Tags: bim,quality,clash,incomplete-element,parameter-error,data-quality

BIM 데이터 품질 관리 3대 영역:

1. 간섭(Clash) 관리 기준:
- 간섭 검토 도구: Navisworks Manage, Solibri Model Checker, BIMCollab.
- 간섭 유형:
  - Hard Clash(실물 충돌): 두 요소가 물리적으로 겹침 → 반드시 해소.
  - Soft Clash(간격 부족): 설치·유지관리 공간 미확보 (예: MEP 이격 100mm 부족) → 기준 미달 시 해소.
  - Workflow Clash(작업 간섭): 동시 시공 불가 상황 → 4D 시뮬레이션으로 확인.
- 허용 간섭 기준:
  - 같은 요소 중복(Duplicate): 허용 0건.
  - 배관 행거 vs 덕트 행거: Soft Clash 허용 (행거 간격 50mm 이상이면 허용).
  - 장식적 요소(가구, 비치물)와의 간섭: 협의 검토 대상.
- 간섭 해소 기한: 설계 단계 Critical 7일, Major 14일 / 시공 단계 Critical 48시간, Major 7일.
- 간섭 보고 형식: 공종, 위치(X/Y/Z), 관련 요소 ID, 간섭 거리, 해소 방법, 담당자, 기한.

2. 미완성 요소(Incomplete Element) 기준:
- 미완성 요소 정의: LOD 기준 이하 정밀도 또는 필수 파라미터 미입력 요소.
- 자동 감지 방법: Dynamo 또는 Revit 스케줄로 파라미터 빈값(Empty) 필터링.
- 허용 기준:
  - 납품 시점 필수 파라미터 미입력: 0건 (납품 거부 사유).
  - 선택 파라미터 미입력: 목록화 후 사유 기재.
- 주요 감지 항목:
  - 룸(Room) 미배치 공간: 모든 공간에 룸 요소 배치 필수.
  - 레벨 미연결 요소: 허공에 떠 있는 요소 (Unassociated to Level) 0건.
  - 패밀리 타입 미지정: Generic Model 등 기본 패밀리 그대로 사용 0건.
  - 그룹(Group) 미폭발: 수정 불가 상태 그룹 요소 0건.

3. 파라미터 오류 관리 기준:
- 오류 유형:
  - 값 오류: 수치 단위 불일치 (예: mm 입력란에 m 값 입력), 음수 입력.
  - 형식 오류: 날짜 형식 불일치(YYYYMMDD 아닌 형식), 코드 오타.
  - 중복 파라미터: 같은 정보를 다른 파라미터에 중복 입력 (정합성 오류).
  - 미사용 파라미터: 정의는 됐으나 전혀 입력되지 않은 파라미터 → 프로젝트 적합성 검토.
- 파라미터 검증 방법:
  - Revit 스케줄: 필수 파라미터 열 추가 후 빈값 필터링.
  - Dynamo 스크립트: 파라미터 값 범위 자동 검증 (예: fck 값이 18~80MPa 범위 벗어나면 경고).
  - 외부 검토 도구: Solibri의 규칙 기반 검사(Rule-Based Checking) 활용.
- 정기 검증 주기: 주간 BIM 조율 회의 전 자동 검증 실행, 결과 보고서 공유.

BIM 데이터 품질 지표 (KPI):
- 간섭 해소율: (해소 건수 / 전체 발견 건수) × 100 → 목표 납품 시 100%.
- 파라미터 완성도: (입력 완료 요소 수 / 전체 요소 수) × 100 → 목표 납품 시 95% 이상.
- 경고(Warning) 건수: Revit 경고 창 Critical 경고 0건 목표.
- IFC 검증 오류: Critical 오류 0건, Warning 건수 공종별 추적.
- NCR 재발율: 동일 유형 NCR 재발 → 0건 목표 (재발 시 프로세스 개선 트리거).


## BIM 지침서 최신 동향 및 표준 업데이트 (2026-05-28)
- Source: auto-enrich via Naver+Tavily+Google+DDG+Ollama 2026-05-28
- Tags: BIM,guideline,IFC,openBIM,update

- 국제 BIM 표준 ISO 19650와 IFC4, IDS가 최신 동향을 이끌고 있으며, 특히 한국에서는 BuildingSMART Korea BIM 지침의 업데이트에 따라 IDS 적용 실무가 활발히 진행되고 있다.
- IDS는 IFC 모델에서 정보 요구사항을 정의하는 표준으로, 2025년 버전은 아직 검토 중이다.
- openBIM은 buildingSMART가 주도하며, Revit→IFC 내보내기는 BIM 데이터의 개방성과 상호운용성을 높이는 중요한 기술로 자리 잡고 있다. 최신 기준에 따르면 Revit에서 IFC4 형식으로 파일을 내보내는 것이 권장된다.

## BIM 지침서 Claude Code 심화 업데이트 (2026-05-28)
- Source: claude-code-enhanced 2026-05-28
- Tags: openBIM, ISO19650, IFC4, IDS, buildingSMART, 국제표준

ISO 19650(BIM 정보 관리 국제표준) 시리즈는 Part 1(개념), Part 2(납품 단계), Part 3(운영 단계), Part 5(보안)로 구성되며, 한국은 2022년 KS X ISO 19650-1/2를 국가표준으로 채택하였다. IFC(Industry Foundation Classes) 4.3 버전은 토목 인프라까지 확장되어 교량·도로·철도 BIM에도 적용된다.
- IDS(Information Delivery Specification): ISO 21597과 연계하여 BIM 모델의 정보 요구사항을 XML 기반으로 정의한다. 발주처가 IDS 파일을 제공하면 수행사는 buildingSMART IDS Tool로 IFC 모델의 준수 여부를 자동 검증할 수 있다.
- openBIM 워크플로: Revit → IFC4 내보내기 시 「Open BIM Object Parametrics」플러그인 또는 Revit 기본 내보내기(IFC 4 Design Transfer View) 사용을 권장한다. 내보내기 전 Project Information의 필수 파라미터(ProjectName, SiteAddress, BuildingType) 입력을 체크리스트로 관리한다.
- CDE(Common Data Environment) 운영: ISO 19650-2의 4가지 상태(WIP→Shared→Published→Archived)를 ACC(Autodesk Construction Cloud) 또는 BIMcollab Zoom에서 폴더 구조로 구현한다.
- buildingSMART Korea는 2024년 「한국형 IFC 적용 가이드」를 발표하였으며, MEP 시스템 분류를 위해 OmniClass Table 23(Products)과 UniFormat을 병행 사용하도록 권고한다.
- 관련: [[설계_지침서]] · [[시공_지침서]] · [[BIM_시방서]] · [[BEP_수행계획서]]

## ISO 19650 실무 적용 마스터급 경험 지식 (2026-05-28)
- Source: claude-code-enhanced 2026-05-28
- Tags: ISO19650, CDE, 공유파라미터, 납품포맷, 실패패턴, 사전예방

ISO 19650-2 실무 적용에서 가장 많이 실패하는 3가지 패턴과 사전 예방 체크포인트를 정리한다.

**실패 패턴 1 — CDE 폴더 구조 공종별 합의 실패**: 프로젝트 시작 전 "ACC에 폴더 만들면 된다"는 안일한 접근이 가장 흔한 실패 원인이다. 건축사는 WIP 폴더를 설계안 버전으로 쓰고, MEP 시공사는 같은 폴더를 시공 모델 작업 공간으로 쓰면서 Shared 폴더 내 파일 기준이 공종마다 달라진다. 사전 예방: 착수 BIM 킥오프 회의에서 "WIP→Shared→Published" 상태 전환 기준을 공종별로 문서화하고 BEP에 명시. 체크포인트: BEP Section 6(협업 플랫폼) 작성 시 각 폴더 상태에서 어떤 행위가 허용/금지되는지 표로 서명 합의.

**실패 패턴 2 — 공유 파라미터 GUID 프로젝트 간 불일치**: 동일 파라미터명(예: `BIM_장비번호`)이라도 프로젝트마다 다른 SharedParameter.txt 파일에서 생성되면 GUID가 달라 IFC PSet 매핑, Solibri 검증, FM 시스템 연동이 모두 깨진다. 실제 사례: 시공사 BIM 팀이 자체 파라미터 파일로 모델을 받아 파라미터를 재정의하면서 발주처 FM 시스템 COBie 연동이 중단. 사전 예방: 프로젝트 착수 시 LUA BIM LABS 표준 SharedParameters.txt를 발주처·시공사에 배포하고, 공유 파라미터 파일을 ACC Docs `03_문서/BIM표준/` 폴더에 잠금 게시. 파라미터 변경 요청 시 GUID 유지 원칙(파라미터 삭제 후 재생성 금지).

**실패 패턴 3 — 납품 파일 포맷 프로젝트 중간 변경**: 실시설계 납품 직전에 발주처가 "IFC2x3 대신 IFC4로 납품해달라"거나 "COBie 스프레드시트도 추가해달라"고 요구하는 케이스가 빈번하다. 중간 포맷 변경은 수행사 추가 공수 발생뿐 아니라 파라미터 매핑 재점검, IFC Export 설정 재구성, 검수 재수행이 필요해 납기 2~4주 지연으로 직결된다. 사전 예방: BEP 작성 시 `납품 파일 형식 변경은 변경 계약 대상`임을 명문화하고 발주처 서명을 받는다. 체크포인트: BEP Section 7(납품 계획) 납품 형식란에 버전 고정 문구 포함.

- 관련: [[설계_지침서]] · [[시공_지침서]] · [[BIM_시방서]] · [[BEP_수행계획서]]


## BIM 지침서 최신 동향 및 표준 업데이트 (2026-05-29)
- Source: auto-enrich via Naver+Tavily+Google+DDG+Ollama 2026-05-29
- Tags: BIM,guideline,IFC,openBIM,update

- 최신 국제 BIM 표준 ISO 19650와 IFC4가 한국의 BIM 지침에 반영되고 있으며, openBIM과 IDS 적용 실무가 강조되고 있습니다.
- 한국에서는 2025년 기준으로 BuildingSMART Korea BIM 지침이 업데이트되어, openBIM 및 IDS를 통해 데이터 공유와 협업을 높이는 방향으로 진행됩니다.
- IFC4는 인프라 프로젝트에서의 상호운용성을 향상시키기 위한 최신 표준입니다.
- Revit에서 IFC4 형식으로 내보내기는 BIM 데이터의 중립성과 상호 운용성을 높이는 중요한 과정이며, 최신 기준은 이 방향을 따르고 있습니다.
- 관련: [[설계_지침서]] · [[시공_지침서]] · [[건축]] · [[BIM_시방서]]


## BIM 지침서 최신 동향 및 표준 업데이트 (2026-05-30)
- Source: auto-enrich via Naver+Tavily+Google+DDG+Ollama 2026-05-30
- Tags: BIM,guideline,IFC,openBIM,update

- 최신 국제 BIM 표준으로 ISO 19650과 IFC4가 채택되어 데이터 교류와 협업을 개선하고 있습니다.
- IDS(Integrated Delivery Standard) 도입으로 한국의 BIM 지침이 업데이트되었습니다. 이는 openBIM 프레임워크를 강화하여 중립적인 BIM 작업 환경을 구축하는 데 기여합니다.
- Revit에서 IFC로의 내보내기는 최신 기준으로, BuildingSMART Korea 2025 BIM 표준 업데이트에 따라 지원됩니다.
- 관련: [[설계_지침서]] · [[시공_지침서]] · [[건축]] · [[BIM_시방서]]


## BIM 지침서 최신 동향 및 표준 업데이트 (2026-05-31)
- Source: auto-enrich via Naver+Tavily+Google+DDG+Ollama 2026-05-31
- Tags: BIM,guideline,IFC,openBIM,update

- 국제 BIM 표준인 ISO 19650와 IFC4는 openBIM을 기반으로 하며, 정보 전달 지침 IDS(Intformation Delivery Specification)를 통해 건설 산업 간의 협력을 지원한다.
- 한국에서는 2025 BIM 지침이 최신 동향을 반영하고 있으며, 이는 국제 openBIM 프레임워크와 일치한다.
- Revit에서 IFC4로 내보내기의 최신 기준은 IFC4.3을 따르고 있어, BIM 데이터의 호환성을 높일 수 있다.
- IDS 적용 실무에서는 BCF(BIM Collaboration Format)와 IDM(Information Delivery Manual)이 주요하게 활용되고 있으며, 이는 BIM 프로젝트에서 정보 공유를 용이하게 한다.
- 관련: [[설계_지침서]] · [[시공_지침서]] · [[건축]] · [[BIM_시방서]]
