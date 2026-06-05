# BIM 납품검수 지식 베이스

## 2026-06-05 AI 기반 IFC 자동검증 최신 연구 결과 심화 보강 (2차)
- Source: 대한공간정보학회 - AI 기반 IFC 표준안 자동화(2026), 한국연구재단, n8n+AI+벡터DB
- Tags: delivery-quality,ifc-validation,ai-automation,model-quality-auditor,research,2026

**국내 AI 기반 IFC 자동검증 연구 결과 (2026 최신):**
```
대한공간정보학회지 논문 결과:
- n8n(워크플로우 자동화) + AI 모델 + 벡터DB + IFC 표준 파일 연동
- 인위적으로 오류를 삽입한 IFC 데이터 테스트 결과:
  · 정밀도(Precision): 평균 0.93
  · 재현율(Recall): 평균 0.97
- IFC 파일에서 속성 정보 누락·오류를 AI가 자동 탐지 가능

LUA BIM LABS Model Quality Auditor 적용 방향:
1. n8n 워크플로우 + ifcopenshell 조합으로 검증 파이프라인 구성
2. IFC 표준 규칙(IDS) → 벡터DB에 저장 → RAG 방식 적합성 검토
3. AI 오류 감지 → 구체적 위치·파라미터 보고서 자동 생성
```

**IFC 자동검증 구현 전략 (LUA BIM LABS MQA):**
```python
# ifcopenshell + AI 검증 파이프라인 예시
import ifcopenshell
from ifctester import ids, reporter

# 1. IFC 파일 로드
ifc = ifcopenshell.open("project.ifc")

# 2. IDS 규칙 파일 로드 (발주처별 납품 요건)
spec = ids.open("delivery_requirements.ids")

# 3. 검증 실행 (정밀도 0.93, 재현율 0.97 목표)
engine = ids.Ids()
engine.validate(spec, ifc)

# 4. 결과 보고서 생성 (PDF/HTML)
result = reporter.Reporter(engine)
result.to_html("mqa_report.html")
```

## 2026-06-05 IFC 자동검증 SaaS 시장 및 Model Quality Auditor 기회 보강
- Source: 국토부 BIM 납품 자동검증 동향, buildingSMART Korea, 한국BIM평가원, 학술자료
- Tags: delivery-quality,ifc-validation,ids,model-quality-auditor,saas,2026

**AI 즉시 답변 패턴 — "BIM 납품 자동 검증이 가능한가요?"**
```
IFC 기반 BIM 납품 자동검증 현황 (2026):
1. buildingSMART IDS(Information Delivery Specification):
   - IFC 모델의 정보 요구사항을 XML로 정의 → 자동 적합성 검토
   - ifctester(Python): 오픈소스 IDS 검증 라이브러리
   - 국토부 IDS 기반 납품 검수 도입 예고 (2026~)

2. 상용 검증 도구:
   - Solibri Model Checker: 규칙 기반 BIM 품질 검토
   - BIMcollab: 클라우드 협업 + IFC 품질 검토
   - Autodesk Model Coordination: ACC 기반 간섭검토

3. LUA BIM LABS Model Quality Auditor 위치:
   - 국내 특화: 국내 발주처 납품 기준 + IDS 통합 검증
   - 텔레그램 봇 연동: 검증 결과 즉시 알림
   - 2026 기회: 500억↑ BIM 의무화로 납품 검수 수요 급증
```

**BIM 납품 자동검증 시스템 국내 동향 (2025~2026):**
- **초고속정보통신건물인증 자동화**: BIM 기반 검토 프로세스 구현 연구 (KCI 논문)
- **국토부 디지털 건설기준 API**: 2026년 무료 개방 후 민간 검증 솔루션 개발 가능
- **IFC + 체크리스트**: 2026년 이후 IFC 데이터 + 확인 체크리스트를 함께 납품

**Model Quality Auditor 기능 로드맵:**
| 기능 | 현재 | 2026 목표 |
|------|------|---------|
| IFC 기본 검증 | ✅ (ifcopenshell) | ✅ |
| IDS 규칙 검증 | ⚠️ 개발 중 | ✅ |
| 국내 지침 자동 대조 | ❌ | ✅ (디지털 건설기준 API) |
| 텔레그램 알림 | ✅ | ✅ |
| 납품 리포트 PDF | ❌ | ✅ |

## 2026-06-04 BF/편의시설 기반 건축 BIM 납품검수 보강
- Source: `docs/knowledge_updates/daily/2026-06-04_LUA_BIM_LABS_BF_ACCESSIBILITY_STANDARD_UPDATE.md`
- Tags: delivery-quality,BF,accessibility,architecture,official-source

BF/편의시설 대응 프로젝트의 BIM 납품검수는 치수 자동검수만으로 닫지 않는다. 대상시설 여부, 의무/권장 구분, 예비인증/본인증 단계, 지자체 조례 또는 사전검사 조건, 발주처 특기시방서를 함께 확인한다.

검수 추가 필드:
- BF 인증 또는 편의시설 설치 대상 여부
- 시설 용도, 규모, 공공/민간 여부
- 적용 법령/시행령 별표/시행규칙 별표/인증 기준
- 의무 편의시설과 권장 편의시설 구분
- 주출입구 접근로, 장애인전용주차구역, 출입구, 복도, 승강기, 화장실, 안내설비, 피난설비 모델 확인 여부
- 자동 검토 가능 항목과 수동 검토 필요 항목
- 예비인증/본인증 신청·심사 문서 링크
- 지자체 사전검사 또는 발주처 RFI 번호

운영 기준:
- 자동 수집된 문폭, 경사, 단차, 회전반경, 화장실 치수 문장은 공식 기준 확인 전 납품 판정 기준으로 사용하지 않는다.
- BF 인증 통과 여부는 모델 형상만으로 확정하지 않고, 인증 심사 문서와 설계자/인증기관 확인 증빙을 연결한다.

관련: [[건축 지식 베이스]] · [[견적심사원]] · [[법규변경모니터링]] · [[2026-06-04 LUA BIM LABS BF Accessibility Standard Update]]

## 2026-06-04 BF 기준 미확정 리스크의 납품검수 연결
- Source: `docs/training_curriculum/team_distribution/samples/2026-06-04_ESTIMATOR_BF_SCOPE_RISK_MEMO_SAMPLE.md`
- Tags: delivery-quality,BF,estimate,risk,KST

BF/편의시설이 납품 범위에 포함되는지 미확정이면 납품검수팀은 모델 적합/부적합 판정을 닫지 않는다. 먼저 견적서와 과업범위에 BF 대상성 검토, 체크리스트, 인증 대응, 지자체 사전검사, 재검수 공수가 포함됐는지 확인한다.

검수 운영 기준:
- 자동검수 치수 결과는 후보 증빙이며 인증 통과 근거가 아니다.
- BF 인증 심사 대응과 BIM 납품검수는 책임 범위가 다르다.
- BF 범위가 추가되면 변경 견적, RFI, 검수표 버전 변경 이력을 남긴다.

관련: [[견적심사원 지식 베이스]] · [[2026-06-04 견적심사원 BF 기준 미확정 리스크 메모 샘플]]

## 2026-06-04 BF 자동검수 룰 후보의 납품검수 연결
- Source: `docs/training_curriculum/team_distribution/samples/2026-06-04_QA_BF_AUTOCHECK_RULE_CANDIDATE_SAMPLE.md`
- Tags: delivery-quality,BF,QA,autocheck,KST

납품검수팀은 BF 자동검수 결과를 최종 합격 판정으로 사용하지 않는다. 자동검수 결과는 누락 후보, 증빙 링크, 파라미터 입력, 장애물 후보를 발견하는 1차 증빙으로 사용하고, 대상성·의무/권장·예비인증/본인증·지자체 조건은 별도 검토한다.

검수 상태 연결:
- `QA_PASS`: 자동검수 후보 항목 입력 완료, 수동 검토로 전달
- `QA_PASS_WITH_NOTES`: KST03 주의가 남아 있어 PM/RFI 병행
- `QA_BLOCKED`: 대상성 또는 인증 단계 정보 부족
- `QA_FAIL`: 더미 값, 누락, 인증 통과 보장 문구, 증빙 미비

관련: [[QA_테스터 지식 베이스]] · [[2026-06-04 QA 테스터 BF 자동검수 룰 후보 샘플]]

## 2026-06-04 CS BF 고객 응답과 납품검수 연결
- Source: `docs/training_curriculum/team_distribution/samples/2026-06-04_CS_BF_EVIDENCE_RESPONSE_SAMPLE.md`
- Tags: delivery-quality,BF,cs,evidence-response,KST

납품검수팀은 CS가 고객에게 안내한 BF 확인 자료 요청 목록을 검수 입력으로 사용한다. 도면, 특기시방서, 인증 단계, 지자체 사전검사 조건, 자동검수 리포트, RFI/BCF 링크가 확인되지 않으면 BF 적합/부적합 판정을 닫지 않는다.

운영 기준:
- CS 답변의 `확정 불가 범위`는 납품검수 보류 또는 RFI 후보로 등록한다.
- 자동검수 결과는 검수 증빙 후보이며 최종 인증 판정이 아니다.
- 고객이 수정 지시를 원하면 설계자/PM 확인 후 변경 범위를 기록한다.

관련: [[고객지원 CS 지식 베이스]] · [[2026-06-04 CS BF 근거기반 고객 응답 샘플]]

## 2026-06-04 PM BF RFI 회의 안건과 납품검수 연결
- Source: `docs/training_curriculum/team_distribution/samples/2026-06-04_PM_BF_RFI_MEETING_AGENDA_SAMPLE.md`
- Tags: delivery-quality,BF,PM,RFI,KST

납품검수팀은 PM의 BF RFI 회신 전까지 자동검수 후보를 최종 부적합 판정으로 닫지 않는다. 회신 결과가 BF 미대상, 대상이나 단계 미확정, 본인증 대응 필요, 지자체 조건 추가, 모델 수정 필요 중 어디에 해당하는지에 따라 검수표 상태를 갱신한다.

검수 상태:
- RFI_WAIT: 적용 기준 회신 대기
- QA_CANDIDATE: 자동검수 후보, 수동 검토 필요
- CHANGE_SCOPE: 모델 수정 또는 변경 견적 필요
- EVIDENCE_LINKED: 도면/RFI/BCF/인증 단계 증빙 연결 완료

관련: [[COO 지식 베이스]] · [[2026-06-04 PM BF RFI 회의 안건 샘플]]

## BIM 납품검수 개요
- Source: LUA BIM LABS internal BIM knowledge baseline
- Tags: bim,quality-check,ids,kbims,checker,deliverable,iso19650

BIM 납품검수는 발주처가 요구한 EIR(발주자 정보요구서) 기준으로 제출된 BIM 모델·문서의 적합성을 검증하는 프로세스.
국토부 BIM 업무지침에 따라 설계 단계별(계획/기본/실시) 납품 전 반드시 수행.

**검수 유형:**
- 형식 검수: 파일 포맷(IFC 버전), 파일명 규칙, 폴더 구조
- 내용 검수: 파라미터 입력 완결성, LOD 달성 수준
- 기술 검수: 클래시(간섭) 건수, 좌표 일치, 단위 통일

## BIM 납품검수 Claude Code 심화 업데이트 (2026-05-28)
- Source: claude-code-enhanced 2026-05-28
- Tags: bim,quality-check,ids,solibri,navisworks,python,kbims-checker

**국토부 BIM 납품 체크리스트 (2023 기준):**
- [ ] 파일명 규칙 준수: `[프로젝트코드]_[공종]_[단계]_[날짜].rvt/ifc`
- [ ] IFC 버전: IFC 2×3 또는 IFC 4 (발주처 요구사항 확인)
- [ ] 공유 파라미터: 룸코드·공종코드·마감코드 입력 완결성 100%
- [ ] 단위 통일: 미터법(mm 기준), 각도(도)
- [ ] 클래시: Hard Clash 0건, Clearance Clash 관리 목록 제출
- [ ] 좌표: Survey Point 국가좌표계(GRS80 or Bessel 1841) 일치
- [ ] 모델 파일 크기: 단일 Revit 파일 300MB 이하 권고

**자동 품질 검수 도구:**
- **Solibri Model Checker**: IDS XML 기반 규칙 검증, BCF 이슈 내보내기
- **KBIMS Checker** (국토부): 국내 BIM 업무지침 자동 검증 (무료 배포)
- **ifctester** (Python): IDS 1.0 검증 라이브러리
  ```python
  import ifctester
  ids = ifctester.ids.open("project_ids.xml")
  ifc = ifcopenshell.open("model.ifc")
  results = ids.validate(ifc)
  for spec in results.specifications:
      print(spec.name, "PASS" if spec.passed else "FAIL")
  ```
- **Revit Warning Export**: `FilledRegion` 경고·교차 경고 목록 → 납품 전 0건 달성

**BCF(BIM Collaboration Format) 이슈 관리:**
- BCF 2.1 표준: buildingSMART International (ISO 21597-1:2020)
- 클래시/품질 이슈 → .bcfzip 파일 → ACC Build 이슈 자동 임포트
- Python bcf-client: BCF API 서버 연동, 이슈 상태(Open/In Progress/Closed) 자동 업데이트

**LUA BIM LABS Add-in 납품검수 모듈 아이디어:**
- Revit 공유 파라미터 입력률(%) 실시간 대시보드 (WPF TaskPane)
- IFC Export → ifctester 자동 실행 → 결과 요약 Excel 생성
- Hard Clash Count → 납품 가능 판정 기준: 0건
- 관련: [[BIM_지침서]] · [[IFC_OpenBIM]] · [[EIRBEP_심사원]] · [[QA_테스터]]

## BIM 납품검수 실전 심화: 검수관 절차와 판정 기준 (2026-05-28)
- Source: claude-code-enhanced 2026-05-28
- Tags: bim,deliverable,inspection,ids,bcf,kbims,grade,acceptance

**단계별 납품 검수 절차 (EIRBEP 심사원 관점):**
1. **형식 검수** (자동): 파일명 규칙, 폴더 구조, 파일 크기 → Python 스크립트 자동 확인
2. **IFC 변환 검수** (자동): ifctester IDS 검증 → 통과/실패 항목 목록 생성
3. **모델 정합성** (반자동): 클래시 건수 확인, 좌표 일치 검증, 단위 통일 확인
4. **파라미터 완결성** (자동): 필수 파라미터 입력률 ≥ 95% 요건
5. **내용 검수** (수동): LOD 달성 수준 샘플링 20개 요소 검토
6. **최종 판정**: 전 항목 통과 시 `Accepted` 스탬프 발행

**납품 판정 기준:**
| 항목 | 합격 기준 | 불합격 조건 |
|---|---|---|
| 파일명 규칙 | 100% 준수 | 1건이라도 위반 |
| IFC Export | Hard Clash 0건 | 1건 이상 |
| 필수 파라미터 | 입력률 95% 이상 | 95% 미만 |
| LOD 달성 | 요구 LOD의 90% 이상 요소 적합 | 90% 미만 |
| 좌표 일치 | 공종 간 오차 ±5mm 이내 | 5mm 초과 |

**불합격 시 RFI 발행 절차:**
1. 검수 결과 → BCF 2.1 이슈 생성 (항목별)
2. ACC Build RFI 자동 등록 (Webhook 연동)
3. 납품자 수정 기간: P1 이슈 3영업일 / P2 이슈 7영업일
4. 재검수: 수정본 재제출 → 해당 항목만 재검증
5. 2회 불합격 시: 프로젝트 매니저 + 발주처 통보

**KBIMS Checker 자동화 연동:**
```bash
# KBIMS Checker CLI 실행 (국토부 무료 배포)
kbims-checker --ifc model.ifc --standard MOLIT2023 --output report.json
# 결과 파싱: 통과/실패 항목 추출
python parse_kbims_report.py report.json
```
- 관련: [[IFC_OpenBIM]] · [[EIRBEP_심사원]] · [[QA_테스터]] · [[ACC_BIM360]]


## 2026-06-04 수도법·하수도법 기반 위생 납품검수 보강
- Source: `docs/knowledge_updates/daily/2026-06-04_LUA_BIM_LABS_PLUMBING_WATER_TANK_DRAINAGE_STANDARD_UPDATE.md`
- Tags: delivery-quality,plumbing,water-tank,drainage,water-quality

위생 BIM 납품검수는 급수/배수 배관 형상과 clash뿐 아니라 저수조 설치기준, 위생점검, 수질검사, 배수설비 신고, 공공하수도 접속 정보를 확인한다.

검수 추가 필드:
- 수도법 시행규칙 저수조 설치기준 적용 여부
- 저수조 위생점검 대상 여부
- 저수조 맨홀, 통기관, 월류관, 배수구, 경보장치 모델링 여부
- 저수조 청소·점검 접근 공간과 출입 안전성
- 소화용수 역류방지장치 여부
- 급수/급탕/급탕환수/오수/배수/통기/우수 계통 분리 여부
- 배수설비 설치 신고 대상 여부
- 공공하수도 접속 위치, 접속방법, 평균관경, 연장, 배출수량 데이터
- 먹는물 수질검사 또는 위생점검 기록 링크

운영 기준:
- 자동 수집된 구배, 청소구 간격, 수압시험, 집수정 용량, 급수압 문장은 공식 기준 확인 전 납품 판정 기준으로 사용하지 않는다.
- 토목 인입, 공공하수도 접속, 지자체 협의가 필요한 항목은 위생 단독 검수로 닫지 않는다.

관련: [[위생 지식 베이스]] · [[설비장비 지식 베이스]] · [[FM 시설관리 자산관리 BIM 지식 베이스]] · [[2026-06-04 LUA BIM LABS Plumbing Water Tank Drainage Standard Update]]


## 2026-06-04 에너지절약설계기준/ZEB 기반 납품검수 보강
- Source: `docs/knowledge_updates/daily/2026-06-04_LUA_BIM_LABS_ENERGY_ZEB_STANDARD_UPDATE.md`
- Tags: delivery-quality,energy-saving-design,ZEB,green-building,BEMS

에너지 인증 대응 프로젝트의 BIM 납품검수는 모델 형상뿐 아니라 에너지절약계획서, 에너지효율등급, ZEB 인증, BEMS/BAS, 신재생에너지 설비 데이터와의 일치성을 확인한다.

검수 추가 필드:
- 건축물의 에너지절약설계기준 적용 여부
- 에너지절약계획서 제출 대상 여부
- 에너지효율등급/ZEB/녹색건축 인증 대상 여부
- 외피 열성능과 창호 파라미터 입력 여부
- 공간/존 경계와 에너지 평가면적 일치 여부
- 냉방, 난방, 급탕, 조명, 환기 설비 데이터 일치 여부
- BEMS/BAS 포인트 및 에너지미터 매핑 여부
- 신재생에너지 설비와 대지 내/외 구분
- 예비인증/본인증 문서와 준공 모델 변경 이력 연결 여부

운영 기준:
- 자동 수집된 열관류율, 보온두께, ZEB 의무화 일정, EUI 문장은 공식 기준 확인 전 납품 판정 기준으로 사용하지 않는다.
- 인증 컨설턴트 산출물과 BIM 파라미터가 다르면 BEP/EIR 기준에 따라 책임 주체와 재계산 공수를 분리한다.

관련: [[건축 지식 베이스]] · [[설비자동제어 지식 베이스]] · [[FM 시설관리 자산관리 BIM 지식 베이스]] · [[2026-06-04 LUA BIM LABS Energy ZEB Standard Update]]


## 2026-06-04 IDS/BCF 공식 표준 기반 납품검수 보강
- Source: `docs/knowledge_updates/daily/2026-06-04_LUA_BIM_LABS_OPENBIM_IDS_BCF_UPDATE.md`
- Tags: bim,delivery-quality,ids,bcf,openbim,official-source

buildingSMART 공식 문서 기준으로 IDS 1.0은 납품 정보 요구사항을 IFC 모델에서 자동 검토하는 기준 후보이며, BCF는 검수 이슈를 추적하는 openBIM 이슈 언어다. LUA BIM LABS 납품검수는 체크리스트를 자동 검수, 이슈 추적, 수동 판정으로 분리한다.

검수 분리 기준:
- IDS 후보: 필수 파라미터, 분류, 재료, 값, 정보 요구사항
- BCF 이슈: 검수 실패 항목, 담당, 상태, 재검수일, 뷰포인트
- 수동/반자동 검토: 간섭, 시공성, MEP 연결성, 좌표, LOD 샘플링

운영 기준:
- IDS 통과는 납품 통과와 동일하지 않다. 실무 부적합, 형상 문제, 연결성 문제는 별도 검토한다.
- BCF 이슈는 고객 커뮤니케이션과 재검수 증빙에 활용한다.
- IFC 4.3 적용은 최신 표준이라는 이유만으로 결정하지 않고 발주처 요구와 수신 소프트웨어 지원을 확인한다.

다음 액션:
- 납품검수 결과표에 `IDS 판정`, `BCF 이슈 ID`, `수동 검토 필요`, `재검수일` 필드를 추가한다.
- 다음 확인일: 2026-06-11

관련: [[IFC OpenBIM 지식 베이스]] · [[QA_테스터]] · [[ACC BIM360 CDE 지식 베이스]] · [[2026-06-04 LUA BIM LABS OpenBIM IDS BCF Update]]


## 2026-06-04 KEC 기반 전기 BIM 납품검수 보강
- Source: `docs/knowledge_updates/daily/2026-06-04_LUA_BIM_LABS_KEC_ELECTRICAL_STANDARD_UPDATE.md`
- Tags: delivery-quality,electrical,KEC,KDS32,KCS32,official-source

전기 BIM 납품검수는 형상 검토와 기준 근거 검토를 분리한다. 케이블 트레이, 전선관, 분전반, 접지, 피뢰, 비상전원, UPS, ESS, EV 충전 설비는 KEC, 전기설비기술기준, KDS/KCS 32, 발주처 특기시방서, 소방·통신 기준을 함께 확인한다.

검수 추가 필드:
- KEC 공고 번호 및 기준일
- 적용 KEC 장/절/조항
- 적용 KDS/KCS 32 코드
- 발주처 특기시방서 조항
- 전기 설계자 확인 여부
- 모델 파라미터와 기준 항목 매핑 여부
- 자동 검토 가능/수동 검토 필요 구분

운영 기준:
- 자동 수집된 KEC 조항번호와 수치 문장은 공식 전문 확인 전 납품 판정 기준으로 사용하지 않는다.
- 강전·약전 이격, 분전반 접근 공간, 트레이 충전율 등은 기준 출처와 발주처 해석을 함께 기록한다.

관련: [[전기 지식 베이스]] · [[법규변경모니터링]] · [[2026-06-04 LUA BIM LABS KEC Electrical Standard Update]]


## 2026-06-04 NFPC/NFTC 기반 소방 BIM 납품검수 보강
- Source: `docs/knowledge_updates/daily/2026-06-04_LUA_BIM_LABS_NFTC_NFPC_FIRE_STANDARD_UPDATE.md`
- Tags: delivery-quality,fire-safety,NFPC,NFTC,official-source

소방 BIM 납품검수는 일반 MEP clash와 분리한다. 스프링클러 헤드 장애, 감지기 사각, 내화·내열 배선, 제연 구역, 방화댐퍼, 비상방송, 유도등, 비상조명, 연결송수관, 소화수조·펌프실은 NFPC/NFTC 기준 근거와 소방 설계자 확인 여부를 함께 기록한다.

검수 추가 필드:
- 적용 NFPC 코드
- 적용 NFTC 코드
- 공고 번호 및 시행일
- 소방기계/소방전기/제연/피난 기준 구분
- 관할 소방서 또는 소방 설계자 확인 여부
- 모델 파라미터와 기준 항목 매핑 여부
- 자동 검토 가능/수동 검토 필요 구분

운영 기준:
- 자동 수집된 NFTC/KCS 조항번호와 수치 문장은 공식 전문 확인 전 납품 판정 기준으로 사용하지 않는다.
- 구 NFSC 명칭으로 작성된 검토표는 최신 NFPC/NFTC 대응 기준을 확인한 뒤 제출한다.

관련: [[소방기계 지식 베이스]] · [[소방전기 지식 베이스]] · [[법규변경모니터링]] · [[2026-06-04 LUA BIM LABS NFTC NFPC Fire Standard Update]]


## 2026-06-04 기계설비 유지관리·성능점검 기반 납품검수 보강
- Source: `docs/knowledge_updates/daily/2026-06-04_LUA_BIM_LABS_MECHANICAL_EQUIPMENT_MAINTENANCE_LAW_UPDATE.md`
- Tags: delivery-quality,mechanical-equipment-law,maintenance,performance-check,FM

기계설비 BIM 납품검수는 설계·시공 모델의 형상 검토뿐 아니라 유지관리와 성능점검 대응 데이터를 확인한다. 공조, 환기, 위생, 자동제어, 열원, 펌프, 팬, 냉동기, 보일러, AHU, FCU, 집수정, 급수펌프 등은 점검대상 여부와 FM 이관 가능성을 검수 필드로 둔다.

검수 추가 필드:
- 기계설비법 적용 여부
- 기계설비 유지관리기준 적용 여부
- 점검대상 장비·계통 여부
- 성능점검 대상 여부
- 측정 위치와 점검 접근성
- 장비대장/COBie/FM 파라미터 매핑 여부
- 유지관리지침서/O&M 문서 확인 여부

운영 기준:
- 자동 수집된 유지관리 주기, LOD, 장비 점검공간 수치는 공식 기준과 발주처 요구 확인 전 납품 판정 기준으로 사용하지 않는다.
- FM 이관 프로젝트는 장비대장, COBie, 유지관리지침서, 성능점검 보고서 대응 데이터를 별도 검수한다.

관련: [[설비장비 지식 베이스]] · [[FM 시설관리 자산관리 BIM 지식 베이스]] · [[2026-06-04 LUA BIM LABS Mechanical Equipment Maintenance Law Update]]


## 2026-06-04 KDS/KCS 기반 납품검수 보강
- Source: `docs/knowledge_updates/daily/2026-06-04_LUA_BIM_LABS_KDS_KCS_CONSTRUCTION_STANDARD_UPDATE.md`
- Tags: delivery-quality,KDS,KCS,construction-standard,official-source

BIM 납품검수에서 KDS/KCS는 EIR, BEP, 과업지시서, 특기시방서의 근거 기준으로 연결한다. KDS는 설계기준, KCS는 시공기준·표준시방서 계열로 분리해 검토하며, 두 기준을 하나의 일반 법규 체크로 섞지 않는다.

검수 추가 필드:
- 적용 KDS 코드
- 적용 KCS 코드
- 기준 시행일 또는 개정 고시일
- 발주처 특기시방서 우선 여부
- 모델 파라미터와 기준 항목 매핑 여부
- 공식 전문 확인 URL 또는 문서 번호

운영 기준:
- 자동 수집된 KDS/KCS 수치 문장은 공식 전문 확인 전 납품 판정 기준으로 사용하지 않는다.
- KDS/KCS 기준과 발주처 특기시방서가 다르면 발주처 질의응답 또는 회의록으로 적용 기준을 확정한다.
- KDS/KCS 확인은 IDS 자동검증 대상이 아니라 기준 적용성 검토와 수동 판정 증빙으로 관리한다.

관련: [[법규변경모니터링]] · [[견적심사원 지식 베이스]] · [[2026-06-04 LUA BIM LABS KDS KCS Construction Standard Update]]


## 2026-06-04 ISO 19650/CDE 기반 납품검수 보강
- Source: `docs/knowledge_updates/daily/2026-06-04_LUA_BIM_LABS_ISO19650_CDE_INFORMATION_MANAGEMENT_UPDATE.md`
- Tags: delivery-quality,cde,iso19650,BEP,EIR

납품검수는 모델 내용뿐 아니라 정보관리 증빙을 확인해야 한다. ISO 19650 정보관리 관점에서 고객 제출본은 CDE의 Published 상태, revision, 승인자, 발행 일시가 확인되어야 한다.

검수 추가 필드:
- CDE 상태: WIP/Shared/Published/Archived
- Revision
- 승인자
- Published 일시
- EIR 항목 대응 여부
- BEP 기준과의 일치 여부
- 자동 검증 대상과 수동 검토 대상 구분

운영 기준:
- WIP 또는 Shared 상태 파일은 최종 납품본으로 보지 않는다.
- 고객 제출본은 Published 상태와 승인 기록이 있어야 한다.
- EIR 요구사항이 모호하면 자동 검증 도구 적용 전에 기준 보정 회의를 요청한다.

관련: [[ACC BIM360 CDE 지식 베이스]] · [[BEP 수행계획서 템플릿]] · [[EIR BEP_심사원 지식 베이스]]

## BIM 납품검수 마스터급 경험 지식 (2026-05-28)
- Source: claude-code-enhanced 2026-05-28
- Tags: 납품거절, 검수기준변경, IDS통과실패, 발주처담당교체, 실무부적합

**현장에서 납품 검수 거절 당하는 현실적 이유 5가지와 대응법**:
① 파일명 규칙 단 1건 위반 — BEP에 명시된 파일명 규칙(`[프로젝트코드]_[공종]_[단계]_[날짜]`)에서 언더스코어 대신 공백을 쓰거나 날짜 형식이 다른 경우 전체 납품물 반려. 대응: 납품 전 Python 정규식으로 파일명 일괄 자동 검증 스크립트 실행.
② Hard Clash 1건이라도 미해소 — 검수 기준이 "Hard Clash 0건"인 상태에서 덕트 vs 구조 보 클래시 1건이 남아있는 경우 전체 납품 반려. 대응: Navisworks 클래시 보고서에서 "Approved" 처리 없이 "Active" 상태로 남은 건수를 납품 전날 재확인.
③ 필수 파라미터 입력률 95% 미만 — 자동 검증 도구 없이 "다 입력했다"고 믿는 경우 스케줄로 빈값 필터링 시 탈락. 대응: Revit 일람표에서 필수 파라미터를 열로 추가하고 빈값 필터를 걸어 0건 달성 확인.
④ IFC Export 좌표계 불일치 — 특정 공종이 Internal Origin으로 내보내 다른 공종과 수십 미터 오프셋. 대응: 납품 전 Navisworks에 전 공종 IFC 통합 후 그리드 오버레이 확인.
⑤ LOD 달성 수준 미달 — 발주처가 샘플 20개 요소를 선택해 LOD 300 기준 치수·파라미터 완결성을 직접 확인 시 일부 요소가 LOD 200 수준으로 미달. 대응: LOD 기준표 대비 공종별 자체 샘플링 점검 후 미달 요소 목록 작성 및 사전 보완.

**발주처 담당자 교체 시 검수 기준 변경 리스크 관리**: 기존 담당자와 합의한 검수 기준을 신임 담당자가 번복하거나 추가 요구사항을 제시하는 경우, 기존 합의 근거가 없으면 대응이 어렵다. 예방 원칙: ① 모든 검수 기준 합의는 BEP 서명본으로 문서화하고 ACC에 Published 상태로 보관. ② 담당자 교체 발생 시 신임 담당자에게 BEP 브리핑 회의를 요청하고, 기존 합의 사항 재확인 확인서를 이메일로 수령. ③ 기존 합의 범위 초과 요구는 "변경 계약 대상"임을 명시하고, 이에 동의할 경우에만 이행. ④ 납품 이력(과거 승인된 모델 버전)을 ACC 버전 이력으로 제시하여 "이전에 같은 기준으로 승인된 납품물"임을 입증.

**IDS 검증 통과했지만 실무 부적합 판정 받는 경우**: IDS 기계 검증(ifctester 또는 Solibri)은 통과했으나 발주처 BIM 담당이 "실제 현장에서 쓸 수 없는 모델"이라며 부적합 판정을 내리는 패턴. 주요 원인: ① 파라미터 값이 채워져 있으나 의미 없는 더미 데이터(예: 제조사명 = "TBD", 모델번호 = "00000") — IDS는 존재 여부만 검증하므로 통과되지만 실무 부적합. 대응: IDS 규칙에 정규식 패턴 검증(`<Value type="pattern">[^T][^B][^D].*</Value>`) 추가. ② 형상은 있으나 MEP 커넥터 미연결 — Revit 경고는 없지만 실제 배관 계통이 끊어진 상태. 대응: Revit MEP 시스템 완결성 검사(`Systems` 탭의 "Unconnected" 필터로 미연결 요소 0건 확인). ③ 공간(Space) 미배치 구역 — IFC에 IfcSpace가 존재하지만 일부 구역 공간이 누락된 경우 FM 시스템 데이터 연동 불완전. 대응: 납품 전 "All Rooms/Spaces" 일람표에서 미배치 공간 0건 확인.

- 관련: [[IFC_OpenBIM]] · [[EIRBEP_심사원]] · [[QA_테스터]] · [[ACC_BIM360]]
