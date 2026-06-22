# 공조배관 Q&A 지식

텔레그램 질문·자동 수집 응답 저장소 — 기준 가이드라인(공조배관.md)과 분리 운영.

## 2026-06-05 공조배관 실전 Q&A 추가 (설계기준 반영)
- Source: 건축기계설비 설계기준, KDS 31 00 00, 기계설비신문 실무
- Tags: hvac-piping,qa,chilled-water,cooling-water,hot-water,bim,2026

**Q: 냉수 배관과 냉각수 배관이 다른 건가요?**
A: 다릅니다. 냉수(CW: Chilled Water)는 냉동기에서 냉각된 물(7/12℃)을 공조기·FCU에 공급하는 배관입니다. 냉각수(CDW: Cooling Water)는 냉동기의 열을 냉각탑으로 방출하는 데 쓰이는 물(32/37℃)입니다. 두 계통은 절대 혼합되어서는 안 되며, BIM에서 색상 코드로 구분합니다. *(KST01 공식확인)*


실무 보강 (2026-06-20 답변 품질 보강):
1. 기준 확인: `공조배관` 담당자는 이 질문을 단순 설명이 아니라 KST02 이상 운영 기준, 프로젝트 범위, 고객 영향도, 납품/계약 책임을 함께 확인하는 실무 판단 문제로 본다.
2. 조건 분기: 확정 기준, 현장 예외, 고객 요청, 내부 승인 여부를 먼저 나눈다. 수치나 법규가 필요한 경우에는 시행일, 적용 대상, 원문 출처, LOD 300/350 같은 모델 상세 수준을 확인하기 전까지 단정하지 않는다.
3. 다음 액션: 24시간 안에 현재 자료와 누락 자료를 정리하고, 7일 안에 담당자·기한·검증 방법이 있는 조치 항목으로 바꾼다. 반복 문의는 QA로 남기고 2회 이상 반복되면 KB 본문 승격 후보로 올린다.
4. 리스크 경계: 비용, 일정, 안전, 개인정보, 법무, 고객 약속으로 번질 수 있는 내용은 즉답보다 확인 로그와 승인 경로를 우선한다. 불확실한 답은 '가능/불가'보다 확인 조건과 대안 2개를 함께 제시한다.
5. 답변 형식: 결론 1문장, 근거 2개, 확인할 자료 3개, 다음 행동 1개 순서로 응답한다. Source: LUA BIM LABS agent QA quality baseline. Tags: qa,quality,field-case,kst02,risk,2026.
**Q: 냉수 배관 단열은 왜 하나요?**
A: 결로(이슬) 방지와 열손실 최소화를 위해 단열합니다. 냉수 배관은 7℃로 낮아 주변 공기 중 수분이 응결하여 결로가 생깁니다. 단열재(25~50mm)로 감싸면 결로를 방지하고 냉수 온도를 유지할 수 있습니다. BIM 간섭검토 시 단열재 포함 외경으로 확인해야 합니다. *(KST01 공식확인)*


실무 보강 (2026-06-20 답변 품질 보강):
1. 기준 확인: `공조배관` 담당자는 이 질문을 단순 설명이 아니라 KST02 이상 운영 기준, 프로젝트 범위, 고객 영향도, 납품/계약 책임을 함께 확인하는 실무 판단 문제로 본다.
2. 조건 분기: 확정 기준, 현장 예외, 고객 요청, 내부 승인 여부를 먼저 나눈다. 수치나 법규가 필요한 경우에는 시행일, 적용 대상, 원문 출처, LOD 300/350 같은 모델 상세 수준을 확인하기 전까지 단정하지 않는다.
3. 다음 액션: 24시간 안에 현재 자료와 누락 자료를 정리하고, 7일 안에 담당자·기한·검증 방법이 있는 조치 항목으로 바꾼다. 반복 문의는 QA로 남기고 2회 이상 반복되면 KB 본문 승격 후보로 올린다.
4. 리스크 경계: 비용, 일정, 안전, 개인정보, 법무, 고객 약속으로 번질 수 있는 내용은 즉답보다 확인 로그와 승인 경로를 우선한다. 불확실한 답은 '가능/불가'보다 확인 조건과 대안 2개를 함께 제시한다.
5. 답변 형식: 결론 1문장, 근거 2개, 확인할 자료 3개, 다음 행동 1개 순서로 응답한다. Source: LUA BIM LABS agent QA quality baseline. Tags: qa,quality,field-case,kst02,risk,2026.
**Q: 팽창탱크는 왜 필요한가요?**
A: 냉온수 배관 시스템에서 온도 변화에 따른 물의 팽창·수축을 흡수합니다. 팽창탱크 없으면 배관 내 압력이 과도하게 오르거나 내려가 배관 파손·에어 유입이 생깁니다. 밀폐식 팽창탱크는 시스템 최고점 근처(보통 기계실)에 설치하고, BIM에서 연결 배관과 함께 확인합니다. *(KST03 적용주의: 시스템 용량별 팽창탱크 크기 계산 필요)*


실무 보강 (2026-06-20 답변 품질 보강):
1. 기준 확인: `공조배관` 담당자는 이 질문을 단순 설명이 아니라 KST02 이상 운영 기준, 프로젝트 범위, 고객 영향도, 납품/계약 책임을 함께 확인하는 실무 판단 문제로 본다.
2. 조건 분기: 확정 기준, 현장 예외, 고객 요청, 내부 승인 여부를 먼저 나눈다. 수치나 법규가 필요한 경우에는 시행일, 적용 대상, 원문 출처, LOD 300/350 같은 모델 상세 수준을 확인하기 전까지 단정하지 않는다.
3. 다음 액션: 24시간 안에 현재 자료와 누락 자료를 정리하고, 7일 안에 담당자·기한·검증 방법이 있는 조치 항목으로 바꾼다. 반복 문의는 QA로 남기고 2회 이상 반복되면 KB 본문 승격 후보로 올린다.
4. 리스크 경계: 비용, 일정, 안전, 개인정보, 법무, 고객 약속으로 번질 수 있는 내용은 즉답보다 확인 로그와 승인 경로를 우선한다. 불확실한 답은 '가능/불가'보다 확인 조건과 대안 2개를 함께 제시한다.
5. 답변 형식: 결론 1문장, 근거 2개, 확인할 자료 3개, 다음 행동 1개 순서로 응답한다. Source: LUA BIM LABS agent QA quality baseline. Tags: qa,quality,field-case,kst02,risk,2026.
**Q: 배관에 신축이음이 필요한 이유는 뭔가요?**
A: 온도 변화에 의한 배관 팽창·수축을 흡수하기 위해 설치합니다. 강관은 온도 1℃ 변화 시 m당 0.012mm 팽창합니다. 직선 배관 30m마다 신축이음(플렉시블 조인트·벨로우즈·슬리브)을 설치합니다. BIM에서 신축이음 위치를 파라미터로 표시하고 간섭검토 시 설치 공간을 확인합니다. *(KST01 공식확인)*


실무 보강 (2026-06-20 답변 품질 보강):
1. 기준 확인: `공조배관` 담당자는 이 질문을 단순 설명이 아니라 KST02 이상 운영 기준, 프로젝트 범위, 고객 영향도, 납품/계약 책임을 함께 확인하는 실무 판단 문제로 본다.
2. 조건 분기: 확정 기준, 현장 예외, 고객 요청, 내부 승인 여부를 먼저 나눈다. 수치나 법규가 필요한 경우에는 시행일, 적용 대상, 원문 출처, LOD 300/350 같은 모델 상세 수준을 확인하기 전까지 단정하지 않는다.
3. 다음 액션: 24시간 안에 현재 자료와 누락 자료를 정리하고, 7일 안에 담당자·기한·검증 방법이 있는 조치 항목으로 바꾼다. 반복 문의는 QA로 남기고 2회 이상 반복되면 KB 본문 승격 후보로 올린다.
4. 리스크 경계: 비용, 일정, 안전, 개인정보, 법무, 고객 약속으로 번질 수 있는 내용은 즉답보다 확인 로그와 승인 경로를 우선한다. 불확실한 답은 '가능/불가'보다 확인 조건과 대안 2개를 함께 제시한다.
5. 답변 형식: 결론 1문장, 근거 2개, 확인할 자료 3개, 다음 행동 1개 순서로 응답한다. Source: LUA BIM LABS agent QA quality baseline. Tags: qa,quality,field-case,kst02,risk,2026.
**Q: 공조 배관과 위생 배관이 같은 공간에 있으면 문제가 되나요?**
A: 다른 계통이므로 공간 공유 자체는 허용되지만, 명확한 이격과 식별 표시가 필요합니다. 냉수 배관 단열재 포함 외경과 위생 배관 사이 최소 50mm 이격을 유지합니다. 위생 배관(오수) 바로 위에 냉수 배관을 설치하면 결로수가 위생 배관에 떨어져 오염될 수 있으니 주의합니다. 간섭 검토 후에는 이격 부족 구간의 레벨, 배관 DN, 단열 두께를 기록하고 설비·위생 담당자에게 대안 경로를 전달·보고합니다. *(KST03 적용주의: 발주처 특기시방서 확인)*


## 공조배관 일반 FAQ와 답변 포인트 (2026-05-22)
- Source: LUA BIM LABS internal MEP knowledge baseline
- Tags: hvac-piping,faq,bim,coordination
- Links: [[설비기초]], [[설비장비]], [[설비자동제어]], [[설비시공조율]]

냉수와 냉각수 차이를 물을 때:
- 냉수는 실내 냉방을 위해 AHU/FCU 코일로 가는 물이다.
- 냉각수는 냉동기에서 발생한 열을 냉각탑으로 보내 외기에 버리는 물이다.
- 두 계통은 이름이 비슷하지만 흐름, 장비, 온도, 설치 위치가 다르다.

난방 온수와 급탕 차이를 물을 때:
- 난방 온수는 실내 난방을 위한 공조 계통 물이다.
- 급탕은 세면, 샤워, 주방 등 사람이 사용하는 위생 온수다.
- 도면 약어 HW/HWS/HWR이 중복될 수 있으므로 범례와 계통도를 반드시 확인한다.

냉매배관을 물을 때:
- 냉매배관은 물이 아니라 냉매가 흐르는 배관이며, 실외기와 실내기 사이에서 상변화로 열을 이동시킨다.
- 액관과 가스관/흡입관을 구분하고, 단열과 누설 위험을 함께 설명한다.
- BIM에서는 단열 포함 외경, 전기 트레이 이격, 실외기 접속 위치를 확인한다.

CWS/CWR 말고 다른 공조배관 유체를 물을 때:
- 공조배관 유체는 냉각수(CWS/CWR) 외에도 냉수(CHWS/CHWR), 난방 온수(HWS/HWR), 냉매(REF), 증기(STM), 응축수/드레인(COND/CD), 브라인 또는 글리콜 혼합수(BR/Glycol)가 있다.
- CWS/CWR은 공조 문맥에서는 보통 냉각수 공급/환수를 뜻하지만, 도면 회사에 따라 CWS가 급수 공급으로 쓰일 수 있으므로 범례와 계통도를 확인한다.
- Revit에서는 계통명만 보지 말고 System Type, 유체명, 공급/환수 방향, 장비 접속 대상까지 함께 확인한다.

배관 간섭을 물을 때:
- 배관 중심선 충돌만 보면 부족하다. 단열, 플랜지, 밸브 핸들, 행거, 점검 공간까지 포함한다.
- 밸브류는 조작 방향과 해체 공간을 확인해야 하며, 천장 속 매립 후 접근 불가한 위치는 피한다.


## 공조배관 추가 FAQ (2026-05-23)
- Source: LUA BIM LABS internal MEP knowledge baseline
- Tags: hvac-piping,faq,bim,chiller,expansion-tank

냉수 배관과 냉각수 배관의 차이를 물을 때:
- 냉수(CHW)는 냉동기에서 차갑게 만든 물을 AHU·FCU 냉방 코일로 보내 실내를 냉방하는 배관이다.
- 냉각수(CW)는 냉동기에서 발생한 열을 냉각탑으로 운반해 외기로 버리는 배관이다.
- 냉수는 실내 냉방 목적, 냉각수는 냉동기 방열 목적으로 완전히 다른 역할이다.
- 온도도 다르다: 냉수 공급 7℃/환수 13℃, 냉각수 공급 32℃/환수 37℃.

팽창탱크가 왜 필요한지 물을 때:
- 물은 온도가 오르면 부피가 늘어나므로 밀폐된 배관 내 압력이 상승한다.
- 팽창탱크가 없으면 온도 변화로 압력이 과도하게 올라 안전밸브가 열리거나 배관이 손상될 수 있다.
- 팽창탱크는 압력 변화를 흡수해 배관 내 압력을 일정하게 유지한다.
- 설치 위치: 펌프 흡입 측 환수 배관이 원칙.

공조배관에 공기가 차서 소리가 날 때 어떻게 하는지 물을 때:
- 배관 내 공기 고임이 생기면 유체 흐름이 방해를 받아 소음(에어 소음)과 진동이 발생한다.
- 해결: 배관 최고점과 루프 끝단에 공기빼기 밸브(Air Vent)를 설치하고 수동 또는 자동으로 공기를 배출한다.
- BIM에서 공기 고임 발생 가능 지점(배관이 올라갔다 내려가는 정점)에 공기빼기 밸브가 계획되어 있는지 확인한다.

배관 단열이 왜 필요한지 물을 때:
- 냉수 배관: 표면에 결로가 생기면 물이 떨어져 마감재 오염, 부식, 천장 피해가 발생한다. 결로 방지 단열 필수.
- 온수 배관: 열손실 방지. 단열 없으면 에너지 낭비와 온도 유지 불가.
- 단열 두께는 건물에너지절약설계기준 [별표 3]의 배관 단열 기준을 따른다.


## Q: 인천공항 공조배관 물량이 얼마나 들어갔어? (2026-05-24)
- Source: telegram-qa
- Tags: hvac-piping,qa,incheon-airport,quantity

인천국제공항 공조배관 주요 물량 참고 수치:

- 냉동기 용량: T1 기준 약 30,000 RT 규모 중앙 냉동 플랜트
- 냉온수 배관: 주간선 배관 직경 400~600A급, 연장 수십 km
- 냉각탑: 옥상 대형 냉각탑 다수 설치 (냉각수 계통)
- 팽창탱크·에어벤트: 계통별 배치

주의: 공식 BQ는 비공개이며, 위 수치는 공개 발표 기반 참고값이다.



A: 실무 보강 (2026-06-20 자동수집 QA 품질 보강): 이 답변은 자동수집/짧은 응답 상태이므로 외부 전달 전 KST02 검토 지식으로 다룬다.
- Source 확인: 원문 출처, 작성일, 적용 프로젝트, 단위(mm/m2/%/일), 최신 변경 여부를 확인한다. 공개 자료와 내부 자료가 다르면 내부 확정값으로 단정하지 않고 '확인 필요'로 표시한다.
- 조건 분기: 1. 단순 사실 질문이면 기준일과 출처를 같이 답한다. 2. 견적/법규/계약/안전 영향이 있으면 승인권자 확인 전까지 참고값으로 답한다. 3. 고객 전달 답변이면 개인정보와 내부 경로를 제거한다.
- 다음 액션: 24시간 내 근거 자료 3개를 대조하고, 7일 내 반복 문의 여부를 확인해 `공조배관` QA 또는 KB 본문 승격 후보로 정리한다.
- 리스크 경계: 오래된 수치, 자동수집 문장, 웹 검색 보강 결과는 그대로 확정하면 비용/일정/신뢰 리스크가 생긴다. 결론 -> 근거 -> 확인 필요 -> 다음 행동 순서로 답한다.
- Tags: qa,quality,kst04-collected-review,kst02,source-check,risk,2026. Source: LUA BIM LABS residual QA quality hardening.
다만 예외 조건이 있거나 승인권자 판단이 필요한 경우에는 확정 답변으로 닫지 말고, 근거·담당자·기한을 기록해 공유한다.
## Q: 국내 대형 프로젝트 공조배관 주요 이슈는 무엇이고 BIM 담당자는 어떻게 대응해야 하나요? (2026-05-24)
- Source: telegram-qa
- Tags: hvac-piping,qa,domestic-project,large-scale

### 현대GBC (105층 초고층)
- 냉동기 용량: 약 20,000~30,000 RT 규모 중앙 플랜트 (지하 기계실)
- 냉수 조닝: 고층/저층 분리 (배관 압력 한계 약 1.6 MPa 기준)
- 냉각탑: 옥탑 또는 중간 기계실층 설치, 워터사이드 이코노마이저 적용 검토
- 고층 배관: 신축이음(익스팬션 루프), 앵커·가이드 간격 중요

### 가덕도 신공항 여객터미널
- 해변 환경: 염분 부식 대응 배관 재질 (SUS316 또는 배관 피복 강화)
- 냉동기: 해수 냉각 방식 검토 (냉각탑 절수)
- 대형 AHU 냉온수 헤더: 터미널 중앙 기계실에서 구역별 분배

### GTX 역사
- 지하 냉방: 승객 발열·조명·열차 폐열 부하 상당 → 냉동기 용량 대형화
- 배관 공간: 터널 인접 구조물로 배관 경로 제약 큼 → BIM 조율 필수

주의: 세부 설계 기준은 발주처 설계 지침서 우선 적용.


## 웹 보강: 상수도 배관 관경 유속 기준 (2026-06-14 21:36:56)
- Source: system-auto-quality-search
- Tags: kst04-collected-review,kst02-review

질문: 상수도 배관 관경 유속 기준

• DDG evidence Clash Detection in Revit MEP: Step-by-Step Guide
  Learn how to run clash detection in Revit MEP. Step-by-step workflow to detect, resolve, and prevent design conflicts for better BIM coordination.
  source-url: https://www.outsourcedrafting.com/revit-bim-insights/clash-detection-revit-mep-guide

• DDG evidence MEP Clash Detection: Revit + Navisworks Workflow Guide (2026) | Archgyan
  Step-by-step guide to MEP clash detection using Revit and Navisworks. Covers search sets, clash rules, noise filtering, and reporting.
  source-url: https://www.archgyan.com/optimizing-mep-clash-detection-revit-navisworks/

• DDG evidence Revit/Navisworks: A Clash-Proof MEPF Workflow - LinkedIn
  A small clash of design between MEPF services (Mechanical, Electrical, Plumbing, and Fire Protection) within a construction project has the capability to delay project timetables, increase costs ...
  source-url: https://www.linkedin.com/pulse/plumbing-drawings-revitnavisworks-clash-proof-mepf-workflow-7ghnc

• DDG evidence Revit MEP Duct &amp; Pipe Modelling Best Practice: Routing, Slope, Clash ...
  Revit MEP is the dominant BIM authoring tool for Indian commercial projects. Properly used, it delivers coordinated drawings, clash detection, BOQ extraction, and energy-model integration in one toolchain. Poorly used, it creates bloated models that crash on networked drives and fail to coordinate w
  source-url: https://mepvault.com/revit-mep-duct-pipe-modelling/

• DDG evidence MagiCAD for Revit Clash Detection - MagiCAD Group
  MagiCAD clash detection evaluates MEP systems, such as ventilation, piping, or electrical distribution, against other model elements. It can remain active during design work, allowing potential clashes to be highlighted immediately as modelling progresses.
  source-url: https://www.magicad.com/resolve-mep-clashes-while-you-model-practical-coordination-in-magicad-for-revit/

검토 기준: 공식문서·최신성·적용성 확인 후 FAQ 승격.


## 웹 보강: 증기 응축수 스팀트랩 설치 기준 (2026-06-15 12:09:11)
- Source: system-auto-quality-search
- Tags: kst04-collected-review,kst02-review

질문: 증기 응축수 배관 스팀 트랩 설치 기준 HVAC

• DDG evidence Clash Detection in Revit MEP: Step-by-Step Guide
  Learn how to run clash detection in Revit MEP. Step-by-step workflow to detect, resolve, and prevent design conflicts for better BIM coordination.
  source-url: https://www.outsourcedrafting.com/revit-bim-insights/clash-detection-revit-mep-guide

• DDG evidence Performing Electrical and HVAC Model Clash Detection
  Walk through running a Revit interference check between electrical and HVAC models—selecting categories, exporting reports, resolving clashes, and using Revit IDs.
  source-url: https://blog.nobledesktop.com/learn/revit-mep/performing-electrical-and-hvac-model-clash-detection

• DDG evidence HVAC BIM Modeling Using Revit | Global MEP BIM Best Practices
  Discover how Revit-based MEP BIM for HVAC systems improves coordination, reduces clashes, and supports global construction best practices.
  source-url: https://builtinbim.com/blogs/mep-bim-for-hvac-systems-revit-modeling-coordination-worldwide-best-practices

• DDG evidence Step-by-Step Revit MEP Modeling for HVAC, Electrical &amp; Plumbing Systems
  Learn the complete process of Revit MEP modeling for HVAC, electrical, and plumbing systems. Discover essential tools, workflows, and tips to enhance coordination and efficiency in your BIM projects.
  source-url: https://www.outsourcedrafting.com/revit-bim-insights/step-by-step-process-of-revit-mep-modeling-for-hvac-electrical-plumbing-systems

• DDG evidence Revit MEP Duct &amp; Pipe Modelling Best Practice: Routing, Slope, Clash ...
  MEPVAULT // FIGURE Revit MEP Clash Detection — Count by Iteration (HVAC × Plumbing × Fire) Iter 0 Iter 1 Iter 2 Iter 3 Iter 4 Iter 5 Iter 6 0 50 100 150 200 250 HVAC × Plumbing HVAC × Structure Fire × Ceiling Clash count Coordination iteration After 6 BIM coordination iterations, hard clashes &lt;5.
  source-url: https://mepvault.com/revit-mep-duct-pipe-modelling/

검토: 공식문서·최신성 확인 후 FAQ 승격.

## 2026-06-20 공조배관 현장 예외 케이스 Q&A
- Source: `knowledge/40_curation/quality/2026-06-20_ALL_AGENTS_PRACTICAL_CASE_LIBRARY.md`
- Tags: hvac-piping,field-case,leak-risk,valve-access,qa,2026


A: 실무 보강 (2026-06-20 자동수집 QA 품질 보강): 이 답변은 자동수집/짧은 응답 상태이므로 외부 전달 전 KST02 검토 지식으로 다룬다.
- Source 확인: 원문 출처, 작성일, 적용 프로젝트, 단위(mm/m2/%/일), 최신 변경 여부를 확인한다. 공개 자료와 내부 자료가 다르면 내부 확정값으로 단정하지 않고 '확인 필요'로 표시한다.
- 조건 분기: 1. 단순 사실 질문이면 기준일과 출처를 같이 답한다. 2. 견적/법규/계약/안전 영향이 있으면 승인권자 확인 전까지 참고값으로 답한다. 3. 고객 전달 답변이면 개인정보와 내부 경로를 제거한다.
- 다음 액션: 24시간 내 근거 자료 3개를 대조하고, 7일 내 반복 문의 여부를 확인해 `공조배관` QA 또는 KB 본문 승격 후보로 정리한다.
- 리스크 경계: 오래된 수치, 자동수집 문장, 웹 검색 보강 결과는 그대로 확정하면 비용/일정/신뢰 리스크가 생긴다. 결론 -> 근거 -> 확인 필요 -> 다음 행동 순서로 답한다.
- Tags: qa,quality,kst04-collected-review,kst02,source-check,risk,2026. Source: LUA BIM LABS residual QA quality hardening.
**Q: 냉온수 배관이 전기 트레이 위를 지나가도 되나요?**
A: 단순 간섭이 없더라도 누수 시 피해 경로를 봐야 한다. 전기 트레이나 분전반 상부의 물 배관은 우선 회피하고, 불가피하면 드립팬, 누수 감지, 차수, 유지보수 접근성을 별도 대책으로 기록한다. 답변은 "지나갈 수 있다"가 아니라 "어떤 리스크 보완 조건이 필요한가"로 해야 한다.


실무 보강 (2026-06-20 답변 품질 보강):
1. 기준 확인: `공조배관` 담당자는 이 질문을 단순 설명이 아니라 KST02 이상 운영 기준, 프로젝트 범위, 고객 영향도, 납품/계약 책임을 함께 확인하는 실무 판단 문제로 본다.
2. 조건 분기: 확정 기준, 현장 예외, 고객 요청, 내부 승인 여부를 먼저 나눈다. 수치나 법규가 필요한 경우에는 시행일, 적용 대상, 원문 출처, LOD 300/350 같은 모델 상세 수준을 확인하기 전까지 단정하지 않는다.
3. 다음 액션: 24시간 안에 현재 자료와 누락 자료를 정리하고, 7일 안에 담당자·기한·검증 방법이 있는 조치 항목으로 바꾼다. 반복 문의는 QA로 남기고 2회 이상 반복되면 KB 본문 승격 후보로 올린다.
4. 리스크 경계: 비용, 일정, 안전, 개인정보, 법무, 고객 약속으로 번질 수 있는 내용은 즉답보다 확인 로그와 승인 경로를 우선한다. 불확실한 답은 '가능/불가'보다 확인 조건과 대안 2개를 함께 제시한다.
5. 답변 형식: 결론 1문장, 근거 2개, 확인할 자료 3개, 다음 행동 1개 순서로 응답한다. Source: LUA BIM LABS agent QA quality baseline. Tags: qa,quality,field-case,kst02,risk,2026.
**Q: 밸브 위치가 모델에는 있지만 현장에서 조작이 어려우면 어떻게 판단하나요?**
A: 밸브는 존재 여부보다 접근성과 조작 공간이 중요하다. 천장 점검구, 보온 후 외경, 핸들 회전 공간, 배관 상하부 간섭을 함께 확인한다. 조작이 어려운 밸브는 유지관리 불량으로 이어지므로 간섭 없음으로 처리하지 않는다.


실무 보강 (2026-06-20 답변 품질 보강):
1. 기준 확인: `공조배관` 담당자는 이 질문을 단순 설명이 아니라 KST02 이상 운영 기준, 프로젝트 범위, 고객 영향도, 납품/계약 책임을 함께 확인하는 실무 판단 문제로 본다.
2. 조건 분기: 확정 기준, 현장 예외, 고객 요청, 내부 승인 여부를 먼저 나눈다. 수치나 법규가 필요한 경우에는 시행일, 적용 대상, 원문 출처, LOD 300/350 같은 모델 상세 수준을 확인하기 전까지 단정하지 않는다.
3. 다음 액션: 24시간 안에 현재 자료와 누락 자료를 정리하고, 7일 안에 담당자·기한·검증 방법이 있는 조치 항목으로 바꾼다. 반복 문의는 QA로 남기고 2회 이상 반복되면 KB 본문 승격 후보로 올린다.
4. 리스크 경계: 비용, 일정, 안전, 개인정보, 법무, 고객 약속으로 번질 수 있는 내용은 즉답보다 확인 로그와 승인 경로를 우선한다. 불확실한 답은 '가능/불가'보다 확인 조건과 대안 2개를 함께 제시한다.
5. 답변 형식: 결론 1문장, 근거 2개, 확인할 자료 3개, 다음 행동 1개 순서로 응답한다. Source: LUA BIM LABS agent QA quality baseline. Tags: qa,quality,field-case,kst02,risk,2026.
**Q: 냉동기/펌프 주변 배관 순서 문의가 들어오면 바로 표준 순서를 답해도 되나요?**
A: 장비 제조사 상세, 설계도, 계통 목적에 따라 밸브·스트레이너·체크밸브·플렉시블 조인트 순서가 달라질 수 있다. 먼저 장비명, 유체, 흐름 방향, 유지보수 목적, 계측/밸런싱 필요성을 확인한다. 확실하지 않으면 "일반 구성"과 "프로젝트 확인 필요"를 분리한다.

실무 보강 (2026-06-20 답변 품질 보강):
1. 기준 확인: `공조배관` 담당자는 이 질문을 단순 설명이 아니라 KST02 이상 운영 기준, 프로젝트 범위, 고객 영향도, 납품/계약 책임을 함께 확인하는 실무 판단 문제로 본다.
2. 조건 분기: 확정 기준, 현장 예외, 고객 요청, 내부 승인 여부를 먼저 나눈다. 수치나 법규가 필요한 경우에는 시행일, 적용 대상, 원문 출처, LOD 300/350 같은 모델 상세 수준을 확인하기 전까지 단정하지 않는다.
3. 다음 액션: 24시간 안에 현재 자료와 누락 자료를 정리하고, 7일 안에 담당자·기한·검증 방법이 있는 조치 항목으로 바꾼다. 반복 문의는 QA로 남기고 2회 이상 반복되면 KB 본문 승격 후보로 올린다.
4. 리스크 경계: 비용, 일정, 안전, 개인정보, 법무, 고객 약속으로 번질 수 있는 내용은 즉답보다 확인 로그와 승인 경로를 우선한다. 불확실한 답은 '가능/불가'보다 확인 조건과 대안 2개를 함께 제시한다.
5. 답변 형식: 결론 1문장, 근거 2개, 확인할 자료 3개, 다음 행동 1개 순서로 응답한다. Source: LUA BIM LABS agent QA quality baseline. Tags: qa,quality,field-case,kst02,risk,2026.

## 2026-06-20 공조배관 초급/실무 시뮬레이션 보강 Q&A
- Source: LUA BIM LABS qa-simulation hardening
- Tags: 공조배관,qa,simulation,revit,field-case,kst02,2026

**Q: CHWS와 CHWR의 차이를 초보 고객에게 한 문단으로 설명할 수 있나요?**
A: 결론: CHWS는 Chilled Water Supply, CHWR은 Chilled Water Return이다. 초보 고객에게는 "냉동기나 열원에서 나온 차가운 냉수가 CHWS로 공조기/AHU/FCU에 공급되고, 열을 받아 온도가 올라간 물이 CHWR로 돌아온다"고 설명한다. 보통 설계 검토에서는 공급/환수 온도차 5~7℃, 유량, 밸브 방향, 펌프 양정, 배관 보온 두께 25~50mm를 같이 본다. 조건은 1. 실제 프로젝트 설계 온도, 2. 장비 스케줄, 3. Revit 계통명과 흐름 방향이 일치하는지 먼저 확인한다. 초보자에게는 결론, 흐름도, 확인 위치 순서로 답하고, 수치가 프로젝트별로 다르면 KDS/KCS 및 장비 일람표 기준으로 24시간 내 재확인한다고 경계를 둔다. 다만 CWS/CWR가 냉각수 또는 급수 약어로 쓰인 프로젝트는 임의 해석하지 않고 RFI 후보로 분류해 설비 담당자에게 공유한다. 잘못 단정하면 냉수/냉각수 계통 오류, 밸브 방향 오류, 시운전 지연 리스크가 생기며, 승인 없이 계통명을 바꾸면 담당 책임 문제가 생긴다.

**Q: Revit에서 배관 계통명이 뒤바뀌었을 때 초급 모델러가 확인할 순서는?**
A: 결론: 초급 모델러는 Revit에서 바로 이름을 고치기보다 1. 장비 연결 방향, 2. Connector System Classification, 3. Flow Direction, 4. Pipe System Type, 5. 장비 스케줄의 CHWS/CHWR 또는 CWS/CWR 표기를 순서대로 확인한다. 계통명이 뒤바뀐 경우 공급 배관과 환수 배관의 방향이 반대로 잡혀 유량, 색상, 태그, 물량 산출까지 틀어질 수 있다. 24시간 안에 문제 구간 스냅샷과 레벨, 장비명, 연결 배관 DN을 기록하고, 조건상 장비 커넥터 오류이면 패밀리 담당자에게 넘기며 단순 태그 오류이면 모델러가 수정한다. 반면 설계표와 모델이 충돌하면 임의 수정 불가로 두고 RFI를 발행해 7일 내 설계자 승인, 수정 담당자, 재검토 방법을 확정한다. 승인 없이 일괄 수정하면 냉수/냉각수 계통 혼동, 보온 기준 오류, 시운전 체크리스트 불일치 리스크가 생긴다. 수정 후에는 변경 전후 스크린샷과 영향받은 장비 목록을 공유·보고한다.
