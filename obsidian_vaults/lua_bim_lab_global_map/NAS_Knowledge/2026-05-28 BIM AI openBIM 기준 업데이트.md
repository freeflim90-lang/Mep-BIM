---
type: verified-knowledge-update
date: 2026-05-28
status: curated
tags:
  - bim
  - revit
  - autodesk
  - openbim
  - ids
  - kcsc
  - knowledge-update
---

# 2026-05-28 BIM AI openBIM 기준 업데이트

## 요약

2026-05-28 기준으로 BIM 지식 수집에서 우선 반영할 신호는 네 가지다.

- Revit 2027은 Forma 연결, Autodesk Assistant, Revit Public MCP Server, Embodied Carbon 분석 확장 등 AI/클라우드/데이터 연결 방향이 뚜렷하다.
- Revit 2027 업데이트는 누적 업데이트 체계이며, 공식 문서 기준 2027.0.2 Update가 2026-04-30에 공개되었다.
- Revit 2026 계열은 2026.4.1 Update가 2026-04-16 기준 최신 업데이트로 확인된다.
- buildingSMART IDS 1.0은 2024-06-01 공식 표준이 되었고, IFC 모델 납품 요구사항을 기계 판독 가능한 방식으로 검증하는 흐름이 실무 품질관리와 직접 연결된다.
- 국가건설기준센터는 2026-02-23 기준 KDS 31 10 10, KDS 31 25 05, KDS 31 25 06, KDS 31 25 10 등 설비 분야 기준 개정을 표시하고 있다.

## LUA BIM LAB 적용 판단

### Model Quality Auditor

- IFC/IDS 기반 납품 검증 룰을 장기 백로그로 승격한다.
- Revit 2027의 MCP/Assistant 흐름은 모델 검사 자동화의 인터페이스 후보로 본다.
- Revit 2026/2027 업데이트 차이는 고객 환경 점검 체크리스트에 반영한다.

### Revit Add-in / Store

- Revit 2027 호환성 테스트 매트릭스를 추가한다.
- Store 설명 문구에는 "AI 보조", "MCP", "Forma" 같은 표현을 과장하지 않고, 실제 구현된 기능과 검증 범위만 적는다.
- Add-in 배포 전 `Revit 2026.4.1`, `Revit 2027.0.2` 최소 스모크 테스트를 분리한다.

### MEP BIM 교육

- 연차별 커리큘럼에 `IDS로 납품 요구사항 확인하기`, `IFC 4.3/IDS 개념`, `Revit 버전별 호환성 리스크`를 사례형 모듈로 추가한다.
- 설비 기준은 KCSC 코드와 개정일을 함께 기록하고, 수치 기준은 원문 코드 확인 전까지 교육자료에 단정 표기하지 않는다.

### 지식 운영

- 공식 문서, 표준기관, 국가 기준센터를 우선 출처로 둔다.
- 뉴스/블로그는 신호 수집에는 사용하되, 수치/법규/버전 판단은 공식 문서로 재확인한다.
- 동일 질문이 반복되면 첫 답변의 출처와 기준일을 Obsidian 노트에 남기고, 이후 답변은 로컬 지식 우선으로 재사용한다.

## 출처

- Autodesk Help, What is New in Revit 2027: https://help.autodesk.com/view/RVT/2027/ENU/?guid=GUID-C81929D7-02CB-4BF7-A637-9B98EC9EB38B
- Autodesk Help, Revit 2027 Updates: https://help.autodesk.com/view/RVT/2027/ENU/?guid=RevitReleaseNotes_2027updates_html
- Autodesk Support, Revit 2026 Product Updates: https://www.autodesk.com/support/technical/article/caas/tsarticles/ts/2zk6i75pWCeI5s5YOVIbMJ.html
- buildingSMART IDS: https://www.buildingsmart.org/standards/bsi-standards/information-delivery-specification-ids/
- 국가건설기준센터(KCSC): https://kcsc.re.kr/

## 연결

- [[Global Knowledge Map]]
- [[MOC - NAS Knowledge]]
- [[산업동향_데일리브리핑]]
- [[지식업데이트]]
- [[BIM_지침서]]
- [[Revit_Addin]]
- [[Navisworks_Addin]]
- [[BIM_시방서]]
