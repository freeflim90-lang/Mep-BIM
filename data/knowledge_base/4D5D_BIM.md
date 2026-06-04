# 4D/5D BIM 지식 베이스

## 2026-06-05 국토부 4D/5D BIM 의무화 단계별 기준 보강
- Source: 국토교통부 건설산업 BIM 시행지침, 오토데스크 BIM 의무화 자료
- Tags: 4d-bim,5d-bim,molit,mandatory,public-construction,schedule,cost

**BIM 의무화 단계별 일정 (공공공사):**
| 시행 연도 | 대상 사업비 | 비고 |
|-----------|------------|------|
| 2023년 | 1,000억원 이상 | 철도·건축 공사 |
| 2024년 | 1,000억원 이상 | 하천·항만 등 SOC로 확대 |
| 2026년 | 500억원 이상 | 전 공종 확대 적용 |
| 2028년 | 300억원 이상 | 추가 확대 예정 |

**건설산업 BIM 시행지침 구성 (2022년 7월 발표):**
- 기본지침 (2020년 12월) → 시행지침 (2022년 7월): BIM 적용절차, 데이터 작성, 납품 기준, 품질검토 기준
- [발주자편]: BIM 요구사항 정의, 성과품 검토, 사업관리 활용
- [설계자편]: BIM 모델 작성 기준, 납품 파일 형식, 공종별 모델링 수준
- [시공자편]: BIM 기반 공정관리, 간섭검토, 4D 시뮬레이션 납품

**4D BIM 공공공사 납품 요구사항 (국토부 기준):**
- 납품 포맷: Navisworks .nwd 또는 .nwf (링크 모델 포함)
- 시뮬레이션 영상: MP4 형식, 공종별 색상 코딩 포함
- WBS 연계: Primavera P6 또는 MS Project 공정표와 ActivityID 1:1 매핑 확인
- 간섭 보고서: Navisworks Clash Detective 결과표 (Excel 또는 PDF) 첨부

**5D BIM 원가관리 납품 요구사항:**
- 물량산출서: Revit Schedule 또는 국내 물량산출 소프트웨어와 정합 확인
- 단가 기준: 건설표준품셈 2025, 조달청 나라장터 단가 적용 명시
- 공정별 원가: WBS 진행률(%) × 공종별 예산 = 기성 청구 근거 문서 첨부
- 조달청 적용: 사업비 200억원 이상 → 계획/중간/실시설계 BIM, 100억원 이상 → 계획설계 BIM

**4D 시공 시뮬레이션 결과물 품질 기준:**
- 공정 누락 확인: WBS 모든 액티비티에 대응 모델 객체 존재 여부
- 레벨별 분리: 층별, 구역별 공정 분리 (Selection Set 구성)
- 간섭 해소 이력: Clash 발생→협의→해소 단계 BCF 또는 RFI 연결
- 공기 영향 분석: Critical Path 변경 이력 주별 관리

관련: [[Navisworks_Addin 지식 베이스]] · [[BEP 수행계획서 템플릿]] · [[BIM 프로젝트 견적산정 로직 내부 기준]]

## 4D/5D BIM 개요
- Source: LUA BIM LABS internal BIM knowledge baseline
- Tags: 4d-bim,5d-bim,schedule,cost,timeliner,navisworks,dynamo

**4D BIM**: 3D 모델 + 공정(Time) — 시공 시뮬레이션, 공정 간섭 사전 파악
**5D BIM**: 4D + 원가(Cost) — 물량 자동 산출, 공정별 원가 모니터링

국토부 BIM 업무지침: 500억 이상 공공공사 4D BIM 제출 의무화 (2023~).

## 4D/5D BIM Claude Code 심화 업데이트 (2026-05-28)
- Source: claude-code-enhanced 2026-05-28
- Tags: 4d-bim,5d-bim,timeliner,primavera,ms-project,dynamo,cost-estimation

**4D BIM 구현 워크플로우 (Navisworks TimeLiner):**
- **Step 1 — WBS 연계**: Primavera P6 또는 MS Project .xml 임포트 → TimeLiner Tasks 자동 생성
- **Step 2 — 모델 매핑**: Revit 파라미터 `ActivityID` = WBS 코드 → Navisworks Selection Sets 자동 연결
  - Dynamo 스크립트: `Element.GetParameterValueByName("ActivityID")` → CSV 일괄 추출
- **Step 3 — 시뮬레이션**: 공종별 색상 코딩 (녹색=진행중, 노란색=완료예정, 빨간색=지연)
- **Step 4 — 영상 출력**: AVI/MP4 TimeLiner 시뮬레이션 영상 → 발주처 보고용

**공정-BIM 연동 파라미터:**
- 시공 단계 파라미터: `Construction Phase` (설계/구조체/외장/MEP거칠/마감/준공)
- WBS 코드 파라미터: `ActivityID` (Primavera 액티비티 ID와 1:1 매핑)
- 시공 구역: `Zone` (A/B/C/D 구역 구분, 층별 공정 분리)

**5D BIM 물량 산출 자동화:**
- Revit Schedule → Excel Export: 공종별 물량 (콘크리트 체적·거푸집 면적·철근 중량)
- 단가 DB 연동: 건설표준품셈 2025, 조달청 나라장터 단가 API
- Python 자동화: `openpyxl` 물량표 + 단가 DB Join → 공종별 원가 자동 계산
- 공정률 연동: WBS 진행률(%) × 예산 = 기성 청구 자동 산출

**Add-in 개발 포인트 (Revit API):**
```csharp
// 공종별 Volume 스케줄 자동 생성
ViewSchedule vs = ViewSchedule.CreateSchedule(doc,
    new ElementId(BuiltInCategory.OST_StructuralColumns));
ScheduleField sf = vs.Definition.AddField(
    ScheduleFieldType.Instance,
    new ElementId(BuiltInParameter.HOST_VOLUME_COMPUTED));
sf.DisplayType = ScheduleFieldDisplayType.Totals;
```
- 관련: [[Navisworks_Addin]] · [[BEP_수행계획서]] · [[엔지니어링계산서]] · [[BIM_프로젝트_견적산정]]

## 4D/5D BIM 실전 운영 심화 (2026-05-28)
- Source: claude-code-enhanced 2026-05-28
- Tags: 4d-bim,5d-bim,schedule,cost,timeliner,wbs,quantity-takeoff

**4D 시뮬레이션 색상 코딩 기준:**
| 상태 | 색상 | 의미 |
|---|---|---|
| Early (일찍) | 초록 | 계획 대비 조기 완료 |
| On Time | 파랑 | 계획 공정 정상 |
| Late | 빨강 | 계획 대비 지연 |
| Critical Path | 노랑 | 전체 공기에 영향 |
| Demolition | 회색 | 철거 구간 |

**Primavera P6 ↔ Navisworks TimeLiner 연동 절차:**
1. P6에서 WBS 코드 체계 정의 (공종-구역-층 3단계)
2. Revit 모델에 `ActivityID` 공유 파라미터 입력 (Dynamo 자동화 가능)
3. P6 → `.xml` 내보내기 → Navisworks `TimeLiner > Data Sources > Import`
4. Selection Sets: Revit ActivityID 기준으로 자동 매핑 규칙 설정
5. 시뮬레이션 실행 → MP4 영상 출력 (480p/720p/1080p 선택)

**5D 물량 산출 자동화 파이프라인:**
```python
import openpyxl, pandas as pd

# Revit Schedule CSV → 단가 DB Join → 원가 계산
schedule = pd.read_csv("revit_schedule.csv")
unit_price = pd.read_excel("unit_price_2026.xlsx")

# 공종별 수량 × 단가 = 항목별 금액
merged = schedule.merge(unit_price, on="Category")
merged["Amount"] = merged["Quantity"] * merged["UnitPrice"]

# 공종별 합계
summary = merged.groupby("Category")["Amount"].sum()
summary.to_excel("cost_estimate.xlsx")
```

**4D BIM 공정 지연 조기 경보:**
- S-커브 비교: 계획 S-커브 vs 실적 S-커브 → 누적 공정률 편차 5% 이상 시 경보
- Critical Path 변경: 주 1회 FloatTime 재계산 → 0일 이하 활동 목록 갱신
- 자재 조달 Lead Time: 냉동기 16주, 엘리베이터 24주, 커튼월 20주 기준 역산 발주일
- 관련: [[Navisworks_Addin]] · [[BEP_수행계획서]] · [[엔지니어링계산서]] · [[BIM_프로젝트_견적산정]]
