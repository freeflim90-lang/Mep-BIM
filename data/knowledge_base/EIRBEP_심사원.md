# EIR/BEP_심사원 지식 베이스


## 프로젝트별 문서 템플릿 참조 (2026-05-23)
- Source: LUA BIM LABS document template index
- Tags: eir,bep,proposal,template,external

| 문서 | 파일 | 용도 |
|---|---|---|
| BEP 수행계획서 | [[BEP_수행계획서]] | 프로젝트 착수 시 BIM 수행 계획 작성·발주처 제출 |
| BIM 제안서 | [[BIM_제안서]] | 수주 제안 또는 BIM 컨설팅 제안 시 사용 |

> 두 문서 모두 `[대괄호]` 항목을 프로젝트 값으로 교체하고, `<!-- 삭제 가능 -->` 섹션은 해당 없으면 제거해서 사용.


## EIR/BEP 요구사항 검토 기준 (2026-05-19 09:16:50)
- Source: LUA BIM LABS curated baseline, Autodesk official docs checked 2026-05-19
- Tags: eir,bep,bim-requirements

EIR/BEP 심사원은 고객 BIM 요구사항, 모델 명명 규칙, 좌표/레벨 기준, 속성 입력 기준, LOD/LOI, 보고서 제출 양식이 Add-in 기능과 맞는지 확인한다.


## EIR/BEP 핵심 요구사항 검토 기준 (2026-05-19 17:26:40)
- Source: LUA BIM LABS domain knowledge baseline 2026-05-19
- Tags: eir,bep,bim-requirements

EIR (Employer's Information Requirements) 검토 항목:
□ LOD(Level of Development) 단계별 요구사항 (설계 LOD200, 시공 LOD350, 준공 LOD400)
□ LOI(Level of Information) — 각 단계별 필수 파라미터 목록
□ 명명 규칙: 파일명, 레이어명, 패밀리명, 파라미터명 형식
□ 좌표계: 프로젝트 기준점, 측량 기준점, 공유 좌표 설정 방식
□ 납품 형식: RVT, IFC, NWD, PDF, Excel 지정 버전

BEP (BIM Execution Plan) 검토 항목:
□ 팀별 역할·책임(RACI) 명확화
□ 소프트웨어 버전 통일 (Revit 연도 버전 고정)
□ 협업 플랫폼: BIM 360/ACC 워크스페이스 설정
Add-in 기능이 EIR 파라미터 명명 규칙과 불일치하면 현장 적용 불가 → 공유 파라미터 매핑 기능 필요.


## EIR/BEP 납품 검토 보고서 양식 (2026-05-23)
- Source: LUA BIM LABS document template
- Tags: eir,bep,bim,report,template,external

```
프로젝트명:
발주처:
검토일:
검토자:
검토 대상 문서(버전):
```

### EIR 요구사항 충족 여부

| 항목 | 요구 기준 | 납품 현황 | 충족 여부 | 비고 |
|---|---|---|---|---|
| LOD 단계 | LOD___ | LOD___ | ✅/❌ |  |
| LOI 파라미터 목록 |  |  | ✅/❌ |  |
| 파일명 규칙 |  |  | ✅/❌ |  |
| 레이어·패밀리명 규칙 |  |  | ✅/❌ |  |
| 좌표계 설정 |  |  | ✅/❌ |  |
| 납품 형식(RVT/IFC/NWD/PDF) |  |  | ✅/❌ |  |
| 공유 파라미터 매핑 |  |  | ✅/❌ |  |

### BEP 이행 여부

| 항목 | 기준 | 이행 현황 | 충족 여부 | 비고 |
|---|---|---|---|---|
| 팀별 역할·책임(RACI) |  |  | ✅/❌ |  |
| 소프트웨어 버전 통일 |  |  | ✅/❌ |  |
| 협업 플랫폼 설정 |  |  | ✅/❌ |  |
| Add-in 파라미터 명명 일치 |  |  | ✅/❌ |  |

### 미충족 항목 및 조치

| 항목 | 미충족 사유 | 조치 방법 | 기한 | 담당 |
|---|---|---|---|---|
|  |  |  |  |  |

### 결론

- 납품 적합 여부: 적합 / 조건부 적합 / 부적합
- 재검토 필요 항목 수:
- 최종 납품 가능 예정일:
