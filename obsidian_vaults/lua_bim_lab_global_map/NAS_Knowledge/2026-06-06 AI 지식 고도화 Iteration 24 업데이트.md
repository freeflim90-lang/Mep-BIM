# AI 지식 고도화 Iteration 24 업데이트 (2026-06-06)

## 보강 배경
- 목표: BIM 제안서·설비자동제어 AI 에이전트의 전문 도메인 지식 공백 해소
- 방법: auto-enrich 저품질 섹션 교체 → 입찰·제어 실무 기반 전문 지식으로 보강
- QA 결과: 39/39 → 43/43 (100%) — 새 테스트 케이스 4건 추가, 전원 통과

---

## 보강 파일 1: BIM_제안서.md

### 추가 섹션: `## 2026-06-06 공공 BIM 입찰 기술제안서 작성 실무·수주 전략·실적 등록 전문 지식`

**핵심 지식:**

#### 공공 BIM 용역 기술평가 배점 구조
| 평가 항목 | 배점 | 세부 |
|---------|-----|------|
| 기술능력 | 30~40점 | BIM 수행 방법론 |
| 수행실적 | 20~30점 | 유사 BIM 용역 실적 |
| 수행조직 | 15~20점 | BIM 전담 인력·자격증 |
| 공정관리 | 10~15점 | 납품 마일스톤 |
| 가격 | 10~20점 | 예가 대비 입찰가 |

#### BIM 의무화 확대 일정
- 2024: 1,000억 이상 → 2026: 500억 이상 → 2028: 300억 이상

#### 수주 차별화 5대 전략
1. LOD 매트릭스 (공종별·단계별 표)
2. CDE 환경 구체화 (ACC 폴더 구조·권한 계획)
3. 간섭검토 프로세스 명시 (BCF 처리 기준)
4. 건설BIM정보화 실적 등록 증빙
5. AI/자동화 역량 차별화 (Dynamo, AI Q&A)

#### 제안서 페이지 구성 (A4 40p)
표지→목차→EIR 이해→조직·인력→방법론→CDE→공종별 계획→간섭검토→납품목록→실적

---

## 보강 파일 2: 설비자동제어.md

### 추가 섹션: `## 2026-06-06 BAS/BMS BACnet 포인트리스트·IFC 자동제어 엔티티·Haystack 태깅 전문 지식`

**핵심 지식:**

#### BAS/BMS BIM 연동 3계층 구조
1. **BIM 계층**: IfcSensor/IfcActuator/IfcController → 설비 위치·속성
2. **BACnet 계층**: AI/AO/BI/BO Object → BACnet Instance ↔ BIM GUID 매핑
3. **IoT 계층**: MQTT v5 → 시계열 DB → 에너지 대시보드

#### IFC 자동제어 엔티티
| 설비 | IFC 엔티티 | PredefinedType |
|-----|-----------|----------------|
| 온도 센서 | IfcSensor | TEMPERATURESENSOR |
| CO₂ 센서 | IfcSensor | CO2SENSOR |
| VAV 댐퍼 액추에이터 | IfcActuator | ELECTRICACTUATOR |
| DDC 컨트롤러 | IfcController | PROGRAMMABLE |

#### BACnet 포인트 명명 규칙
- `AHU-01-SAT`: AHU 01호기 급기온도
- `AHU-01-SAF`: AHU 급기팬 상태
- `VAV-B2-101-CFM`: B2층 101호 VAV 풍량

#### Project Haystack v4 태깅
- `equip`: 설비 (AHU/FCU/Chiller)
- `point + sensor + air + temp`: 온도 센서 포인트
- `bimRef`: IFC GUID 참조

---

## QA 검증 결과

| 항목 | Before | After |
|------|--------|-------|
| 전체 테스트 수 | 39 | 43 |
| 통과 수 | 39 | 43 |
| 통과율 | 100% | 100% |

새 추가 테스트 케이스:
- ✅ BIM_제안서: "공공 BIM 입찰 기술제안서 기술평가 배점 기준"
- ✅ BIM_제안서: "BIM 의무화 확대 일정 2024 2026 2028"
- ✅ 설비자동제어: "BAS BACnet 포인트리스트 BIM 연동 IFC 자동제어"
- ✅ 설비자동제어: "Project Haystack 스마트빌딩 BIM 태깅"

---

## 누적 현황 (Iteration 24 기준)
- QA 커버리지: **43개 도메인 질문 100% 통과**
- 전문 지식 보강 완료 도메인: 구조·공조덕트·전기·건축·BIM납품검수·Revit_Addin·BIM견적·인력파견·통신·소방전기·토목·BIM시방서·BIM제안서·설비자동제어

## 다음 보강 후보
- `ACC_BIM360.md`: Autodesk Construction Cloud 실무 워크플로우
- `엑셀자동화.md`: Python openpyxl/xlwings BIM 보고서 자동화
- `설비도면해석.md`: MEP 도면 기호 해석·AS-BUILT 도면 비교

---
tags: [지식고도화, BIM, BIM제안서, 설비자동제어, BACnet, Haystack, QA검증, Iteration24]
date: 2026-06-06
