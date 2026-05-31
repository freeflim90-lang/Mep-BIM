# BIM 시방서 지식 베이스

## 초기 기준
BIM 시방서는 발주처의 정보 요구(EIR)를 기반으로 작성되며, 모델 품질·납품물·검수 기준을 단계별로 규정한다.


## BIM 시방서 정의 및 적용 범위 (2026-05-26)
- Source: 국토교통부 건축 BIM 시방서(2023), 조달청 BIM 적용 기본 지침(v2.0), LUA BIM LABS curated baseline 2026-05-26
- Tags: bim,specification,definition,scope,EIR,BEP

BIM 시방서 정의:
BIM 시방서는 건설 프로젝트에서 생성·납품·관리해야 하는 BIM 정보의 품질, 형식, 절차, 검수 기준을 규정한 문서다. 국토교통부 BIM 적용 지침과 조달청 BIM 시방서를 기반으로 하되, 프로젝트 특성에 따라 발주처가 특기 사항을 추가한다.

적용 주체별 역할:

| 주체 | 역할 | 주요 의무 |
|------|------|-----------|
| 발주처 | EIR(Exchange Information Requirements) 발행 | 정보 요구 수준, 납품 형식, 검수 기준 정의 |
| 설계사 | BEP(BIM Execution Plan) 수립 | 모델 구성 계획, 소프트웨어, 납품 일정 확정 |
| 시공사 | 시공 BIM 수행 및 관리 | 시공 상세 모델 작성, 간섭 조정, 시공 조율 |
| 유지관리자 | FM BIM 활용 | COBie 데이터 수신, 자산 관리 시스템 연동 |

BIM 시방서 적용 단계:
- 기획: 발주처 EIR 작성, BIM 목표 및 활용 시나리오 정의
- 설계: LOD 200~350, 설계 조율, 간섭 검토, 법규 검토 모델
- 시공: LOD 350~400, 4D 공정, 5D 물량, 시공 상세 모델
- 준공: LOD 400(As-Built), 준공 BIM 납품
- 유지관리: LOD 500, FM 시스템 연동, COBie 납품


## BIM 모델 품질 기준 (2026-05-26)
- Source: 국토교통부 BIM 품질 기준(2023), buildingSMART Korea, LUA BIM LABS curated baseline 2026-05-26
- Tags: bim,quality,LOD,parameter,completeness

LOD(Level of Development) 기준:

| LOD | 단계 | 형상 정밀도 | 정보 요구 수준 |
|-----|------|-------------|----------------|
| LOD 100 | 기획 | 매스 모형 | 면적, 층수, 용도 |
| LOD 200 | 기본 설계 | 개략 크기·위치 | 재료, 공종 분류, 개략 사양 |
| LOD 300 | 실시 설계 | 정확한 크기·위치·수량 | 규격, 재료 코드, 성능값 |
| LOD 350 | 시공 조율 | 접속부·연결 포함 | 인터페이스 정보, 공종 조율 |
| LOD 400 | 시공/준공 | 시공 상세 | 제조사, 모델 번호, 설치 정보 |
| LOD 500 | 유지관리 | 실측 검증 | FM 데이터, 유지보수 이력 |

모델 완성도 기준(LOD 300 이상 설계 BIM 기준):
- 형상 완성도: 전체 부재 중 모델링 완료 비율 95% 이상
- 파라미터 충족률: 필수 파라미터 입력 비율 90% 이상, 공종별 핵심 항목 100%
- 정합성: 공종 간 모델 중복·누락 없음, 레벨 일치율 100%
- 파일 용량: 단일 Revit 파일 200MB 이하(연동 파일 포함 전체 1GB 권고 상한)

파라미터 충족률 측정 방법:
- 모델 품질 검토 소프트웨어(Solibri, BIM Collab) 활용
- Revit API 또는 Dynamo로 파라미터 공백값(Null, 0, 미입력) 자동 집계
- 공종별 필수 파라미터 체크리스트(아래 공종별 항목 참조)와 대조
- 품질 검토 보고서: 납품 7일 전 내부 검토, 납품 3일 전 감리자 사전 검토


## 공종별 BIM 모델 요구사항 (2026-05-26)
- Source: 국토교통부 건축 BIM 시방서(2023), LUA BIM LABS curated baseline 2026-05-26
- Tags: bim,architecture,structure,mep,requirement,parameter

### 건축 BIM 모델 요구사항 (LOD 300 기준)

필수 모델링 항목:
- 벽체: 외벽·내벽 모든 구획 벽, 두께·재료 레이어 구분 표현
- 바닥·천장: 마감층 포함, 실 경계 확정
- 창호: 개폐 방식, 크기, 단열 성능, 프레임 재료 표현
- 계단·경사로: 경사도, 폭, 챌면 높이, 디딤면 깊이 표현
- 실(Room/Space): 전체 실 명칭·번호 입력, 방화구획 구분

필수 파라미터 (공유 파라미터):
- Room_Name, Room_No, Room_Use (실명, 번호, 용도)
- Fire_Compartment_ID (방화구획 번호)
- Wall_Finish_Material (마감 재료)
- Floor_Finish_Thickness (마감 두께, mm)
- Net_CeilingHeight (순 천장고, mm)
- Thermal_Transmittance (열관류율, W/m²K)
- Fire_Rating (내화 등급, h)

### 구조 BIM 모델 요구사항 (LOD 300 기준)

필수 모델링 항목:
- 기둥·보: 전체 부재, 단면 정확히 표현(RC 철근 배근은 LOD 350 이상)
- 슬래브: 두께, 개구부 위치·크기
- 전이보·전이 슬래브: 별도 태그 표시(TRANSFER_BEAM 파라미터)
- 기초: 기초판 크기, 말뚝 위치·길이·직경
- 구조 벽: 두께, 내력벽 여부 구분

필수 파라미터:
- Structural_Material (재료 종류: RC, 철골, SRC)
- fck 또는 Steel_Grade (설계 강도, MPa 또는 등급)
- Member_Type (부재 유형: 보/기둥/슬래브/기초/벽)
- Transfer_Element (전이 부재 여부: Yes/No)
- Penetration_Allowed (관통 허용 여부: Yes/No/Review)
- Fire_Protection_Type (내화피복 공법: 뿜칠/보드/도료)
- Fire_Rating (내화 시간, h)

### MEP BIM 모델 요구사항 (LOD 300 기준)

공조(HVAC) 필수 항목:
- 덕트 전 계통(급기·환기·배기·외기), 크기·형상 표현
- 공조기(AHU/FCU) 장비 위치, 크기, 점검 공간
- 방화댐퍼 위치: 방화구획 관통 전수 표현
- 필수 파라미터: Duct_Width, Duct_Height, Airflow_CMH, System_Type, Fire_Damper(Yes/No)

위생(Plumbing) 필수 항목:
- 급수·급탕·배수·오수·통기 전 계통
- 배관 구배 방향 표현(수직 배수 계통 명확히)
- 위생 기구 위치 및 연결 배관
- 필수 파라미터: Pipe_Diameter, Pipe_Material, Flow_Rate_LPM, System_Type, Slope(%)

전기 필수 항목:
- 강전: 케이블 트레이, 전선관, 분전반·배전반 위치
- 약전: 통신 트레이, MDF·IDF 위치
- 조명기구 위치, 콘센트·스위치 위치(LOD 300 이상)
- 필수 파라미터: Circuit_No, Panel_Name, Cable_Type, Tray_Width, Voltage_V

소방 필수 항목:
- 스프링클러 헤드 전수, 소화 배관 계통
- 소방 감지기 위치, 비상조명·유도등
- 소방 배관 밸브류 위치
- 필수 파라미터: Sprinkler_Type, Coverage_M2, Fire_System_Type, Response_Temp_C


## BIM 납품물 체크리스트 (2026-05-26)
- Source: 국토교통부 BIM 납품 기준(2023), 조달청 BIM 발주 기준, LUA BIM LABS curated baseline 2026-05-26
- Tags: bim,deliverable,checklist,stage

기본 설계 단계 납품물:
- [ ] BEP(BIM Execution Plan) — 초안
- [ ] 건축 LOD 200 Revit 모델 (.rvt)
- [ ] 구조 LOD 200 Revit 모델 (.rvt)
- [ ] MEP LOD 200 Revit 모델 (.rvt)
- [ ] 공종 통합 NWD/NWC 파일 (Navisworks)
- [ ] 간섭 검토 보고서 (1차)
- [ ] IFC 파일 — 공종별 (.ifc)
- [ ] BIM 모델 뷰(도면) 추출 PDF

실시 설계 단계 납품물:
- [ ] BEP(BIM Execution Plan) — 확정판
- [ ] 건축 LOD 300 Revit 모델 (.rvt)
- [ ] 구조 LOD 300 Revit 모델 (.rvt)
- [ ] MEP 공종별 LOD 300 Revit 모델 (.rvt) — 기계, 전기, 소방, 통신 각각
- [ ] 공종 통합 조율 NWD 파일
- [ ] 간섭 검토 보고서 (최종) — 미해결 간섭 목록 포함
- [ ] 물량 산출 BIM 보고서 (5D)
- [ ] IFC 파일 공종별 최신판
- [ ] BIM 기반 도면(평면·입면·단면·상세) 추출 DWG/PDF
- [ ] 파라미터 충족률 품질 검토 보고서

시공 단계 납품물 (중간):
- [ ] LOD 350 시공 조율 모델 (공종별)
- [ ] 4D 공정 시뮬레이션 파일 (Navisworks 또는 Synchro)
- [ ] 공종 조율 회의 기록 + 간섭 해결 이력

준공 단계 납품물:
- [ ] LOD 400 As-Built 모델 (공종별)
- [ ] 준공 IFC 파일 (공종별)
- [ ] COBie 데이터 파일 (.xlsx 또는 .csv)
- [ ] BIM 모델 품질 최종 검수 보고서
- [ ] 장비 유지관리 정보 BIM 연동 확인서


## EIR(Exchange Information Requirements) 작성 기준 (2026-05-26)
- Source: ISO 19650-2, 국토교통부 EIR 가이드(2022), LUA BIM LABS curated baseline 2026-05-26
- Tags: bim,EIR,information-requirement,ISO19650

EIR 필수 구성 항목:
1. 프로젝트 정보 기본값 (발주처, 위치, 용도, 규모, 예산)
2. BIM 활용 목적 및 유스케이스 (설계 검토, 물량 산출, 시공 조율, FM 연동)
3. 정보 납품 이정표 (단계별 납품 시점, 형식)
4. 소프트웨어 및 파일 형식 요구사항 (Revit 버전, IFC 스키마 버전)
5. LOD 요구 수준 (단계별, 공종별)
6. 필수 파라미터 목록 (발주처 공유 파라미터 파일 첨부)
7. 모델 구조 기준 (파일 분할 기준, 링크 구조, 좌표계)
8. 명명 규칙 (파일명, 레벨명, 뷰명, 패밀리명)
9. 품질 검수 기준 및 검수 도구 (Solibri, BIM Collab, 자체 체크리스트)
10. 보안 및 정보 관리 (CDE 플랫폼, 접근 권한, 버전 관리)

명명 규칙 기준 (파일명):
```
[프로젝트코드]-[공종코드]-[단계코드]-[구역코드]-[버전]
예: LUA-ARCH-DD-Z01-R01.rvt
    LUA-MEP_HVAC-CD-Z01-R03.rvt
```

공종 코드:
- ARCH: 건축, STR: 구조, MEP_HVAC: 기계, MEP_PLMB: 위생, MEP_ELEC: 전기, MEP_FIRE: 소방, MEP_COMM: 통신

단계 코드:
- SD: 기본 설계(Schematic Design), DD: 기본 설계 확정(Design Development), CD: 실시 설계(Construction Documents), CN: 시공(Construction), AS: 준공(As-Built)

좌표계 기준:
- 프로젝트 기준점: 대지 경계선 또는 1층 기준 모서리에서 통일
- 측량 좌표계: UTM-K 또는 GRS80 TM 기준 (발주처 지정)
- 모든 공종 모델 동일 기준점 적용 — 시작 전 좌표 일치 확인 필수


## BIM 검수 기준 및 절차 (2026-05-26)
- Source: 국토교통부 BIM 품질 검수 가이드(2023), Solibri 검수 기준, LUA BIM LABS curated baseline 2026-05-26
- Tags: bim,review,clash,coordination,quality-check

공종 조율(Coordination) 검수 기준:

간섭(Clash) 허용 기준:
| 간섭 유형 | 허용 여부 | 기준 |
|-----------|-----------|------|
| 하드 클래시(Hard Clash) | 원칙 불허 | 물리적 충돌, 중복 — 전수 해결 |
| 소프트 클래시(Soft Clash) | 조건부 허용 | 이격 거리 부족 — 공종별 허용 이격 미달 시 해결 |
| 시공 공간 부족 | 불허 | 유지보수 접근 공간 미확보 — 해결 필수 |
| 의도적 교차 | 허용 | 설계 의도 확인, 문서화 필수 |

공종별 최소 이격 기준:
- 강전 케이블 트레이 ↔ 배수관: 300mm 이상 (누수 위험)
- 강전 트레이 ↔ 약전 트레이: 300mm 이상 (EMI 방지, 격벽 시 150mm)
- 덕트 ↔ 구조 보: 100mm 이상 (단열재 포함)
- 소방 배관 ↔ 기타 배관: 100mm 이상
- 천장 내 유지보수 공간: 최소 600mm(설비 밀집 구간 800mm 이상)

BIM 검수 절차:
1. 납품 전 자체 품질 검토 (시공사 또는 설계사 — Solibri/BIM Collab)
2. 감리자 BIM 사전 검토 (납품 7일 전)
3. 공종 통합 간섭 보고서 제출 (미해결 항목, 해결 방안 포함)
4. 발주처 BIM 검수 (기술 검토 위원회 또는 PM 지정 검수자)
5. 검수 통과 — 승인 서명 후 CDE(공통 데이터 환경)에 최종 등록
6. 검수 불합격 — 재작업 요청서 발행 → 14일 이내 재납품

간섭 보고서 필수 포함 항목:
- 간섭 번호(Clash ID), 간섭 유형(Hard/Soft)
- 공종 A vs 공종 B (충돌 주체)
- 위치 (레벨, 구역, 좌표)
- 현황 스크린샷(3D 뷰)
- 해결 방안 및 담당자
- 해결 상태(Open/In Progress/Resolved/Accepted)

검수 도구 및 파일 형식:
- 간섭 검수: Navisworks Manage(.nwd), Solibri Model Checker(.smc)
- 품질 규칙 파일: Solibri SMC 규칙 파일(발주처 제공 또는 LUA 표준 규칙)
- 검수 보고서: PDF + Excel(간섭 목록), BIM Collab BCF 파일(.bcf)


## 유지관리 BIM 연계 (2026-05-26)
- Source: 국토교통부 유지관리 BIM 가이드(2022), BuildingSMART COBie 표준, ISO 19650-3, LUA BIM LABS curated baseline 2026-05-26
- Tags: bim,FM,maintenance,COBie,asset-management

FM(Facility Management) 데이터 요구사항:

자산 분류 체계:
- 시설물 → 층 → 공간 → 시스템 → 구성 요소(Component) 체계로 계층화
- OmniClass Table 23(제품) 또는 UniClass 기준 분류 코드 사용
- 각 자산에 고유 Asset_ID 부여(바코드·QR 코드 연동 가능)

장비 필수 FM 데이터:
- 제조사(Manufacturer), 모델명(Model_No), 시리얼 번호(Serial_No)
- 설치 날짜(Install_Date), 보증 만료일(Warranty_Expiry)
- 유지보수 주기(Maintenance_Cycle: 월 단위)
- 담당 업체(Service_Contractor), 긴급 연락처(Emergency_Contact)
- 설계 수명(Design_Life: 년)
- 관련 문서 링크(Manual_URL, Drawing_URL)

COBie(Construction Operations Building information exchange) 기준:

COBie 주요 시트 구조:
| 시트명 | 내용 | 비고 |
|--------|------|------|
| Facility | 시설물 기본 정보 | 1행 (프로젝트 전체) |
| Floor | 층별 정보 | 층 + 지하층 |
| Space | 실별 정보 | 면적, 용도 |
| Zone | 구역(방화·공조·구역) | 공간 그룹 |
| Type | 자산 유형(장비 종류) | 공통 사양 |
| Component | 개별 자산(장비 1대) | Asset_ID |
| System | 계통(급수계통 등) | 컴포넌트 그룹 |
| Spare | 예비 부품 목록 | 재고 연동 |
| Resource | 유지보수 자원 | 인력·도구 |
| Job | 유지보수 작업 | PM 주기 |
| Document | 관련 문서 | 설명서·도면 |
| Attribute | 추가 속성 | 프로젝트 맞춤 |

COBie 납품 방식:
- 파일 형식: .xlsx(표준), .csv, IFC-COBie 스키마(.ifc) 중 발주처 선택
- 납품 시점: 준공 BIM 모델 납품과 동시 (LOD 400 기준)
- Revit COBie 자동 추출: Autodesk COBie Extension 또는 COBie DB 플러그인 활용
- 검증: COBie Validation Tool(buildingSMART 공식) 0 오류 달성 후 납품

FM 시스템 연동 기준:
- CAFM/CMMS 연동: REST API 또는 파일 Import/Export
- 지원 시스템: Archibus, Maximo, SAP PM, FM:Systems
- 실시간 연동(IoT 센서 데이터): BACnet/IP 또는 MQTT → Digital Twin 플랫폼
- 연동 후 데이터 정합성 검증: Asset_ID 매핑 100% 일치 확인 필수


## BIM 시방서 최신 기준 업데이트 (2026-05-28)
- Source: auto-enrich via Naver+Tavily+Google+DDG+Ollama 2026-05-28
- Tags: BIM,specification,EIR,COBie,update

한국의 BIM 시방서(EIR 기반)는 발주처별로 다양한 요구 수준을 보이고 있으며, 2025년까지 BIM 통합이 더욱 강화될 예정입니다. 발주처가 제시하는 정보요구사항(EIR; Employer’s Information Requirement)은 BIM 데이터의 적합성을 판단하는 방법론으로 활용됩니다.

- **발주처별 요구 수준**: 2025년까지 발주처는 EIR을 통해 구체적인 정보 요구사항을 명시, 이를 기반으로 설계 및 건설 공정에서 BIM을 적용합니다. 이는 발주자와 설계사 간의 데이터 통합과 협업을 강화하는 데 중점을 두고 있습니다.

- **COBie**: COBie(Costruction Operations Building Information Exchange)는 건물의 구조, 시설 및 서비스 정보를 포함한 디지털 데이터 스키마입니다. 항만 등의 특수 건설 프로젝트에서는 항만용 COBie 스키마가 개발되어 활용되고 있습니다.

- **FM 연동**: BIM과 FM( Facility Management)의 연동은 건물의 유지보수와 운영 효율성을 높이는 중요한 요소입니다. 이를 위해 국제표준화 기구인 BuildingSMART International의 가이드라인을 따르는 것이 권장됩니다.

- **데이터 상호운용성**: BIM 시방서에서는 공통 데이터 환경(CDE; Common Data Environment)을 통해 다양한 이해관계자가 서로 정보를 공유하고 통합할 수 있도록 하는 것을 목표로 합니다. 이를 통해 프로젝트의 전반적인 효율성을 향상시키는 데 도움이 됩니다.

- **프로젝트별 요구사항**: 각 프로젝트에 따라 특정한 요구사항이 제시되며, 이는 발주자의 특수성과 건설 공정을 고려하여 정의됩니다. 이를 통해 프로젝트 지속期间，我将继续用中文回答您的问题。韩国BIM实施指南（EIR为基础）的最新趋势和实际应用技巧包括：- 发包方根据特定信息需求(EIR)来判断提交的BIM数据的适用性；- 2025年前，BIM集成将在合同中进一步加强；- COBie标准在港口等特殊建设项目中被开发并使用；- BIM与设施管理（FM）的联动是提高建筑维护和运营效率的关键因素；- 公共数据环境(CDE)旨在促进多方信息共享和整合。对于每个项目，特定要求会根据发包方的特点和建设过程进行定义，以提升项目的整体效率。

## BIM 시방서 Claude Code 심화 업데이트 (2026-05-28)
- Source: claude-code-enhanced 2026-05-28
- Tags: BIM시방서, EIR, COBie, FM연동, CDE, 발주처요구사항

BIM 시방서는 발주처의 EIR(Employer's Information Requirements)을 구체화한 계약 문서로, ISO 19650-2의 정보 요구사항 체계를 기반으로 작성한다. 국내 공공발주 시 LH·LX·조달청·국방부 등 발주처별 BIM 시방서 표준 템플릿이 상이하므로 사전 확인이 필수다.
- EIR 핵심 항목: ① 목적(Purpose): 설계검토·시공조율·FM 연동 중 명시, ② LOD 기준표(단계별·공종별), ③ IFC 내보내기 버전(IFC 2x3 또는 IFC4), ④ CDE 플랫폼 지정(ACC/ProCore/Aconex), ⑤ 모델 파일 명명 규칙(ISO 19650 준거: 프로젝트코드-발신자-볼륨-레벨-타입-역할-분류-번호)
- COBie(Construction Operations Building Information Exchange): NBIMS-US v3 기반 스프레드시트 포맷으로, 기기(Component), 공간(Space), 시스템(System), 구역(Zone) 정보를 FM 인계 데이터로 구조화한다. Revit에서 COBie Extension 플러그인으로 직접 내보내기 가능하다.
- FM 연동 검토: COBie 데이터를 CAFM(Computer-Aided Facility Management) 시스템(ArchiBUS, IBM Maximo)에 임포트 시 공간 코드와 기기 태그번호 일치 여부를 사전 검증한다.
- BIM 시방서 품질 기준: 모델 오류율 0%(Clash 0건), IFC 검증 도구(Solibri/BIMcollab)로 EIR 준수율 95% 이상, 파일 용량 단계별 최대 500MB(구조 모델) 기준 관리.
- 관련: [[BIM_지침서]] · [[BEP_수행계획서]] · [[설계_시방서]]


## BIM 시방서 마스터급 경험 지식 (2026-05-29)
- Source: claude-code-enhanced 2026-05-29
- Tags: BIM시방서, EIR, 발주처협상, COBie, 납품검수, 실무실패패턴

### 현장에서 반복되는 BIM 시방서 실패 패턴 5가지

**1. LOD 기준 미정의 → 납품 분쟁**
- 원인: EIR에 "LOD 300 이상"만 명기, 세부 공종별 LOD 미분류
- 증상: 설비 배관 LOD 200(위치만 표현) 납품 → 발주처 LOD 350 요구 → 재모델링 클레임
- 해결: EIR 작성 시 공종×단계 LOD 매트릭스 필수 첨부 (건축/구조/MEP×설계/시공/준공 → 9셀 이상)

**2. IFC 버전 불일치 → 데이터 손실**
- 원인: 시방서에 IFC 버전 미명시 → 설계사 IFC 4, 발주처 뷰어 IFC 2x3만 지원
- 증상: 공간(IfcSpace) 정보 유실, 속성(Pset) 미표시
- 해결: IFC 2x3이 아직 표준; 4 사용 시 발주처 호환성 사전 테스트 명기 필수

**3. CDE 플랫폼 지정 없음 → 파일 버전 충돌**
- 원인: 이메일로 NWC/RVT 파일 교환 → 버전 혼재
- 해결: EIR에 ACC(Autodesk Construction Cloud) 또는 동급 CDE 지정, 파일 명명규칙 ISO 19650 준거 명기

**4. COBie 제출 시점 미정 → 준공 직전 대량 작업**
- 원인: "준공 시 COBie 납품"만 명기 → 시공 중 데이터 축적 없이 준공 전 일괄 입력
- 증상: 데이터 오류율 30%+, FM 연동 실패
- 해결: 시방서에 COBie 중간 제출 마일스톤 설정 (골조완료, MEP 설치완료 시점)

**5. 검수 기준 정량화 부재 → 납품 무한 반복**
- 원인: "모델 품질 우수" 등 주관적 기준만 명기
- 해결: Solibri/BIMcollab 검증 기준 정량 명기: IFC 스키마 오류 0건, 필수 파라미터 누락률 < 1%, 클래시 Zero 기준 공종별 명시

### 발주처별 BIM 시방서 특이사항 (국내 주요 기관)

| 발주처 | 주요 특이사항 |
|--------|-------------|
| LH (한국토지주택공사) | 자체 BIM 가이드라인(LH BIM 지침) 준수 필수, 공동주택 LOD 기준 별도 |
| LX (한국국토정보공사) | 지적 측량 데이터 연계, 좌표계 TM 기준 명시 필수 |
| 조달청 | 나라장터 BIM 데이터 연동, 설계VE 단계 BIM 제출 의무 |
| 국방부 | 보안 CDE 별도 운영(외부망 ACC 불가), 철저한 반출 통제 |
| 서울시 | S-BIM 플랫폼 연계, IFC 업로드 자동 검증 지원 |

### BIM 시방서 작성 체크리스트 (CS 지원 기준)

```
□ EIR 필수 항목
  - [ ] 프로젝트 목적 (설계검토/시공조율/FM/인허가)
  - [ ] 단계별 LOD 매트릭스 (공종×단계 표)
  - [ ] IFC 버전 명시 (2x3/4 및 MVD)
  - [ ] CDE 플랫폼 및 파일 명명규칙
  - [ ] 중간 제출 마일스톤

□ 검수 기준 정량화
  - [ ] IFC 스키마 검증 도구 지정
  - [ ] 허용 오류율 수치 명기
  - [ ] 클래시 Zero 기준 공종별 명기
  - [ ] COBie 데이터 완성도 기준 (필드별 필수/선택 구분)
```

### Revit API — EIR 준수율 자동 검증

```csharp
// 필수 파라미터 누락 감지
var requiredParams = new[] { "건물_구분", "층_번호", "공종_코드", "LOD_단계" };
var collector = new FilteredElementCollector(doc).OfClass(typeof(FamilyInstance));
int missingCount = 0, totalChecks = 0;
foreach (var elem in collector)
{
    foreach (var paramName in requiredParams)
    {
        totalChecks++;
        var param = elem.LookupParameter(paramName);
        if (param == null || string.IsNullOrEmpty(param.AsString()))
            missingCount++;
    }
}
// missingCount / totalChecks < 0.01 → EIR 준수율 99% 이상
```


## BIM 시방서 최신 기준 업데이트 (2026-05-29)
- Source: auto-enrich via Naver+Tavily+Google+DDG+Ollama 2026-05-29
- Tags: BIM,specification,EIR,COBie,update

- 2025년 한국 BIM 규격에서 발주처의 정보 요구사항(EIR)이 반영될 예정이며, COBie와 FM 표준을 적용하여 데이터 상호운용성을 강화할 계획이다.
- EIR은 프로젝트 특정 요구사항을 명확하게 정의하는 역할을 하며, 발주처별 BIM 요구 수준에 따라 다르게 적용될 예정이다. 이는 2025년 한국 BIM 규격에서 구체적으로 제시될 것이다.
- COBie와 FM 연동 데이터 기준은 BIM 시방서(EIR) 작성 시 중요한 요소로 작용할 것으로 보인다. COBie 스키마를 통해 건설물의 정보를 체계화하고, FM 연동을 통해 유지보수 및 관리 효율성을 높일 수 있다.
- BIM 데이터의 적합성을 판단하기 위한 방법론이 제시되며, 발주처가 제시한 EIR에 따라 BIM 데이터의 적합성을 평가할 수 있게 될 것이다. 이는 2025년 한국 BIM 규격에서 구체적으로 명시될 예정이다.
- 항만용 COBie 스키마 개발과 국제표준화 추진을 통해 BIM 표준화를 강화하고, 항만 BIM 운영 지원을 위한 가상현실 실증 테스트가 진행된다.
- 관련: [[건축]] · [[설비장비]] · [[설계_지침서]] · [[시공_지침서]]


## BIM 시방서 최신 기준 업데이트 (2026-05-30)
- Source: auto-enrich via Naver+Tavily+Google+DDG+Ollama 2026-05-30
- Tags: BIM,specification,EIR,COBie,update

- 발주처별 BIM 요구 수준(EIR)에 따라 디지털 데이터의 적합성을 판단할 수 있는 방법론이 제시되고 있습니다.
- COBie(Construction Operations Building Information Exchange) 기준을 준수하여 건설 공정에서부터 유지보수까지 필요한 정보를 효과적으로 관리할 수 있습니다.
- FM(Facility Management) 연동 데이터 기준에 맞춰 BIM 모델링을 진행하면, 프로젝트의 효율성과 지속 가능한 운영이 가능해집니다.
- 2025년부터는 발주처별 정보 요구사항(EIR)에 따른 BIM 데이터의 적합성을 평가하는 기준이 강화될 예정입니다.
- 관련: [[건축]] · [[설비장비]] · [[설계_지침서]] · [[시공_지침서]]


## BIM 시방서 최신 기준 업데이트 (2026-05-31)
- Source: auto-enrich via Naver+Tavily+Google+DDG+Ollama 2026-05-31
- Tags: BIM,specification,EIR,COBie,update

- 2025년 한국 BIM 시방서(EIR 기반)의 최신 동향에서는 발주처별 정보 요구사항(EIR)에 따라 제출되는 BIM 데이터의 적합성을 판단할 수 있는 방법론이 강조되고 있습니다.
- COBie와 FM 연동 데이터 기준은 BIM 실무 적용에서 필수적입니다. COBie 스키마를 활용하여 건물 내 정보를 구조화하고, FM 시스템과 연동하여 유지보수 관리에 활용할 수 있습니다.
- 발주처별로 요구하는 EIR 수준이 다름을 고려해야 하며, 이를 통해 프로젝트 특성에 맞는 BIM 데이터를 생성하고 관리할 수 있어야 합니다.
- 관련: [[건축]] · [[설비장비]] · [[설계_지침서]] · [[시공_지침서]]


## BIM 시방서 최신 기준 업데이트 (2026-06-01)
- Source: auto-enrich via Naver+Tavily+Google+DDG+Ollama 2026-06-01
- Tags: BIM,specification,EIR,COBie,update

- 발주처별 BIM 요구 수준: 2025년부터는 발주처가 제시한 정보요구사항(EIR; Employer's Information Requirement)에 따라 BIM 데이터의 적합성을 판단할 수 있는 방법론이 도입될 예정이다. 이는 발주처별로 다양한 요구 사항을 충족시키기 위해 BIM 시방서가 개발되고 있다.

- COBie 및 FM 연동: COBie와 FM 연동 데이터 기준은 필수적이다. COBie 스키마를 통해 설계, 구축, 유지보수 단계에서 필요한 정보를 체계적으로 관리하고, FM 시스템과의 연동을 통해 건물의 전반적인 운영 효율성을 높일 수 있다.

- BIM 실무 적용 팁: 발주처별 EIR 요구사항에 맞춰 BIM 데이터를 생성하고 관리해야 한다. 이를 위해 BIM 클러스터가 제시하는 방법론을 활용하여, 프로젝트 특성에 따른 적합한 BIM 시방서를 작성하라. COBie와 FM 연동을 위한 표준 스키마를 준수하여, 데이터의 일관성과 통합성을 확보해야 한다.
- 관련: [[건축]] · [[설비장비]] · [[설계_지침서]] · [[시공_지침서]]
