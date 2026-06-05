# Revit 패밀리 제작 지식 베이스

## 2026-06-05 MEP 패밀리 제작 AI 즉시 답변 패턴 보강
- Source: Revit 패밀리 공식 가이드, SCK 오토데스크 MEP 패밀리 가이드북, BIMobject
- Tags: revit-family,mep-family,rfa,parameter,connector,lod,2026

**AI 즉시 답변 패턴 — "MEP 패밀리를 Revit에서 만들 때 무엇이 중요한가요?"**
```
MEP Revit 패밀리 제작 핵심:
1. 패밀리 카테고리 선택: Mechanical Equipment(공조기·펌프), 
   Pipe Fittings(배관 피팅), Duct Fittings(덕트 피팅) 등 정확히 선택
2. 커넥터(Connector) 설정:
   - 파이프 커넥터: 유체 종류·압력·흐름 방향 설정
   - 덕트 커넥터: 풍량·압력·덕트 형상 설정
   - 전기 커넥터: 전압·상·소비전력 설정
3. 참조 레벨(Reference Plane): 삽입 기준점·방향 명확히
4. 파라미터 설정: 인스턴스/타입 구분, 공유 파라미터 사용
5. COBie 파라미터: SerialNumber, Manufacturer, ModelNumber 추가
```

**MEP 패밀리 제작 단계별 체크리스트:**
| 단계 | 확인 항목 |
|------|---------|
| 템플릿 선택 | 공조기→Mechanical Equipment, 배관→Pipe Fitting |
| 형상 모델링 | 실제 치수 기반, LOD 300 상세 수준 |
| 커넥터 배치 | 유입·유출 방향 정확, 계통 타입 일치 |
| 파라미터 | 용량·규격·COBie 파라미터 입력 |
| 테스트 | 프로젝트 로드 후 배관 연결 확인 |
| 저장 | .rfa로 저장, 버전 명시 (Revit 2024 등) |

**BIMobject 패밀리 활용 (공급사 공식 패밀리):**
- BIMobject.com: 제조사 공식 Revit 패밀리 무료 다운로드
- LG전자·삼성·한화·Grundfos 등 국내외 제조사 패밀리 제공
- 주의: 다운로드 패밀리도 커넥터 타입·파라미터 확인 후 사용

## 패밀리 개요
- Source: LUA BIM LABS internal BIM knowledge baseline
- Tags: revit,family,rfa,bim,lod,parameter,template

Revit 패밀리(Family)는 BIM 모델의 최소 단위 객체. .rfa 파일로 저장되며 프로젝트 .rvt에 로드하여 사용.

**패밀리 3가지 유형:**
- System Family: 벽·바닥·천장·지붕 (파일로 저장 불가, 프로젝트 내장)
- Loadable Family: 문·창·가구·MEP 기기 (.rfa 파일, Add-in에서 가장 많이 다루는 유형)
- In-Place Family: 단발성 프로젝트 고유 형태 (재사용 불가, 성능 불리)

**템플릿 선택 기준:**
- 기계 장비: `Metric Mechanical Equipment.rft`
- 파이프 피팅: `Metric Pipe Fitting.rft`
- 전기 기기: `Metric Electrical Equipment.rft`
- 일반 모델: `Metric Generic Model.rft`

## Revit Family 제작 Claude Code 심화 업데이트 (2026-05-28)
- Source: claude-code-enhanced 2026-05-28
- Tags: revit,family,rfa,lod,parameter,connector,shared-parameter

**패밀리 파라미터 설계 원칙:**
- **공유 파라미터(Shared Parameter)**: 스케줄·태그·IFC 익스포트에서 일관성 — GUID 불변 원칙
- **패밀리 파라미터**: 패밀리 내부 형상 제어용 (외부 노출 불필요 시 사용)
- **인스턴스 vs 유형**: 설치 위치별 다른 값 → 인스턴스, 동일 규격 여러 개 → 유형 파라미터
- LOD 300 필수 파라미터: 제조사(Manufacturer), 모델명(Model), 유량/풍량, 전원(Voltage/Phase)
- LOD 400 추가: 연결 플랜지 규격(Connection Size), 하중(Weight), 서비스 공간 치수

**MEP 커넥터(Connector) 설정:**
- Pipe Connector: 유체 유형(냉수/온수/오배수/소화수), 관경(DN), 유량(L/s), 압력(kPa)
- Duct Connector: 형상(직사각/원형), 풍량(CMH), 정압(Pa), 유속(m/s)
- Electrical Connector: 전압(V), 위상(단상/3상), 부하 분류(Apparent Load/kVA)
- 커넥터 방향: 꼭 외부를 향해야 MEP 배관 자동 연결 가능

**패밀리 제작 품질 체크리스트:**
- [ ] 원점(Origin) = 기준점 (삽입 시 좌표 정확도)
- [ ] 모든 치수 파라미터화 (하드코딩 금지)
- [ ] Subcategory 분류 (가시성 그래픽 제어 가능하게)
- [ ] 2D 표현(Symbolic Line): 평면도/입면도 LOD별 심볼
- [ ] Purge 후 불필요 요소 제거 (파일 크기 최소화)
- [ ] Revit 2024/2025 호환 저장 (하위 버전 저장 설정)

**Revit API로 패밀리 자동 생성:**
```csharp
// FamilyDocument 생성 및 파라미터 추가
Document famDoc = uiApp.Application.NewFamilyDocument(templatePath);
FamilyManager mgr = famDoc.FamilyManager;
using (Transaction t = new Transaction(famDoc, "Add Param")) {
    t.Start();
    ExternalDefinition extDef = sharedParamFile.Groups
        .get_Item("MEP").Definitions
        .get_Item("ManufacturerName") as ExternalDefinition;
    mgr.AddParameter(extDef, BuiltInParameterGroup.PG_IDENTITY_DATA, true);
    t.Commit();
}
```
- 관련: [[Revit_Addin]] · [[BIM_템플릿기획관]] · [[설비장비]] · [[설계_지침서]]

## Revit Family 제작 실전 심화: 트러블슈팅과 고급 기법 (2026-05-28)
- Source: claude-code-enhanced 2026-05-28
- Tags: revit,family,rfa,troubleshooting,flex,formula,nested-family

**패밀리 제작 고급 기법:**

**중첩 패밀리(Nested Family):**
- 용도: 복잡한 기기 조립체 (밸브+플랜지+게이트 세트)
- 규칙: 중첩 깊이 최대 2단계 (3단계부터 성능 저하·로드 오류 빈발)
- 공유 파라미터 연결: 상위 패밀리 파라미터 → 중첩 패밀리로 연결(Associate)

**공식(Formula) 활용:**
```
# 보온재 두께 자동 계산 (배관 관경 기반)
Insulation_Thickness = if(Pipe_Diameter < 50, 25, if(Pipe_Diameter < 100, 40, 50))

# LOD에 따른 상세도 제어
Show_Detail = if(LOD_Level >= 300, true, false)
```

**Flex 파라미터 테스트:**
- Flex 버튼(초록 화살표)으로 파라미터 범위 검증 필수
- 테스트 값: 최솟값·최댓값·중간값 3개 모두 테스트
- 실패 패턴: 참조선 미연결 → `The family has errors` → 제약조건 재정의

**MEP 커넥터 설정 실수 Top 5:**
1. 커넥터 방향 반대 → 배관 연결 시 꺾임 발생 → Y축 방향 반전
2. 관경 파라미터 미연결 → Revit이 기본값으로 고정 → Connector Radius = Pipe_Diameter / 2
3. 유체 유형 미설정 → 시스템 분류 불가 → Fluid Type = Hydronic Supply/Return 지정
4. 전기 커넥터 Load Classification 누락 → 전력 집계 오류
5. 커넥터 수 불일치 → 입구 1개 출구 1개 원칙 (분기는 Tee 패밀리 별도)

**Revit API 패밀리 배치 자동화:**
```csharp
// 특정 레벨에 패밀리 인스턴스 일괄 배치
FamilySymbol symbol = doc.GetElement(symbolId) as FamilySymbol;
if (!symbol.IsActive) symbol.Activate();
foreach (var pt in insertionPoints)
{
    doc.Create.NewFamilyInstance(pt, symbol, level,
        StructuralType.NonStructural);
}
```
- 관련: [[Revit_Addin]] · [[BIM_템플릿기획관]] · [[설비장비]] · [[설계_지침서]]

## Revit 패밀리 마스터급 경험 지식 (2026-05-28)
- Source: claude-code-enhanced 2026-05-28
- Tags: CorruptRFA, 패밀리충돌, 표준라이브러리교체, 파라미터마이그레이션, 버전호환

**현장에서 패밀리 충돌로 Revit 다운되는 원인(Corrupt RFA 파일)**: Revit이 패밀리 로드 중 충돌(크래시)하는 주요 원인은 손상된 RFA 파일, 중첩 패밀리 순환 참조, 과도한 파라미터 공식 오류 3가지다. 손상 RFA 원인: ① 네트워크 드라이브에서 RFA를 직접 편집(저장 중 네트워크 끊김으로 파일 손상), ② 구버전(Revit 2019 이하)에서 제작된 패밀리를 Revit 2024/2025에서 로드 시 업그레이드 과정의 오류, ③ 다른 소프트웨어(FamilyEditor 외부 도구)로 편집된 비표준 RFA. 진단 방법: 크래시 유발 패밀리를 별도 빈 프로젝트에서 로드 테스트하여 충돌 여부 확인. 손상 의심 시: Revit 패밀리 편집기에서 열어 "Purge Unused"와 "Remove All Unused"를 반복 실행 후 저장하면 일부 손상이 복구된다. 복구 불가 시: 동일 템플릿으로 패밀리를 재제작하고 파라미터와 커넥터 설정을 수동으로 옮긴다.

**대형 건설사 표준 패밀리 라이브러리 도입 시 기존 프로젝트 교체 전략**: 표준 라이브러리 패밀리로 기존 프로젝트 패밀리를 교체할 때 "이름이 같으면 덮어씌워진다"는 오해로 잘못된 교체가 발생하는 경우가 많다. 안전한 교체 절차: ① 기존 패밀리 목록을 Revit 일람표로 추출(패밀리명, 유형명, 사용 개수). ② 표준 라이브러리 패밀리와 기존 패밀리의 파라미터 매핑 비교표 작성. ③ 표준 패밀리를 로드할 때 기존 패밀리와 이름이 동일하면 "Overwrite the existing version"으로 덮어쓰기되므로, 파라미터 구조가 다를 경우 기존 파라미터 값이 삭제될 수 있음 — 교체 전 BIM 모델 전체 백업 필수. ④ Dynamo 스크립트로 대량 교체: `FamilyInstance.Symbol` 변경 노드를 활용해 구 패밀리 인스턴스를 신규 표준 패밀리 타입으로 일괄 전환. ⑤ 교체 후 모든 MEP 커넥터 연결 상태와 파라미터 값이 유지되는지 샘플링 검증.

**패밀리 버전 간 파라미터 마이그레이션**: 패밀리 v1에서 v2로 업그레이드 시 파라미터명이 변경되거나 삭제된 경우, 기존 인스턴스에 입력된 파라미터 값이 유실되는 문제가 발생한다. 마이그레이션 전략: ① 파라미터 이름 변경 시 기존 파라미터를 삭제하지 말고 새 파라미터를 추가한 후, Dynamo 스크립트로 구 파라미터 값을 새 파라미터로 복사. ② 공유 파라미터(Shared Parameter)는 GUID가 파라미터 동일성을 보장하므로 이름을 바꿔도 기존 데이터가 유지된다 — 가능하면 공유 파라미터로 전환. ③ 패밀리 버전 이력을 GitHub 또는 ACC에서 관리하고, 버전별 "변경된 파라미터 목록"을 CHANGELOG.md로 유지하면 마이그레이션 작업 계획 수립이 용이해진다. ④ 프로젝트에 이미 배치된 패밀리 인스턴스 수가 1,000개 이상인 경우 Revit API 배치 스크립트로 자동 마이그레이션이 사실상 필수.

- 관련: [[Revit_Addin]] · [[BIM_템플릿기획관]] · [[설비장비]] · [[설계_지침서]]
