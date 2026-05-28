# 공조덕트 Q&A 지식

텔레그램 질문·자동 수집 응답 저장소 — 기준 가이드라인(공조덕트.md)과 분리 운영.


## Telegram 팀원 보강 요청 (2026-05-21 16:39:09)
- Source: telegram:Jin (8721440825)
- Tags: telegram,team-request,knowledge-gap,needs-review

팀원이 기존 Obsidian 답변이 부족하다고 회신했다.

원 질문: 덕트 대한 종류가 뭐가 있는지 알려줘
추가 요청: 추가 설명 없음

처리 기준:
1. 내부 지식에서 누락된 기준을 우선 보강한다.
2. 외부 검색 또는 공식 문서 확인이 필요한 항목은 추후 지식 업데이트 후보로 표시한다.
3. 고객명, 프로젝트명, 개인정보는 수집하지 않는다.


## Telegram 팀원 보강 요청 (2026-05-22 09:28:56)
- Source: telegram:@FreeFilmer (7899169126)
- Tags: telegram,team-request,knowledge-gap,needs-review

팀원이 기존 Obsidian 답변이 부족하다고 회신했다.

원 질문: 덕트 사용하는 유체의 종류가 뭐가 있어?
추가 요청: 추가 설명 없음

처리 기준:
1. 내부 지식에서 누락된 기준을 우선 보강한다.
2. 외부 검색 또는 공식 문서 확인이 필요한 항목은 자동 수집 후 지식 업데이트 후보로 표시한다.
3. 고객명, 프로젝트명, 개인정보는 수집하지 않는다.


## Telegram 더 찾아줘 자동 수집 결과 (2026-05-22 09:28:59)
- Source: telegram-auto-search:@FreeFilmer (7899169126)
- Tags: telegram,team-request,auto-collect,needs-review

원 질문: 덕트 사용하는 유체의 종류가 뭐가 있어?
추가 요청: 추가 설명 없음

자동 수집 결과:

• [Tavily] Check Duct Systems- REVIT MEP
  HVAC Duct Design: Manual D, Fittings, Friction Rate, Pressure Loss, & Static Pressure w/ Alex Meaney ... Revit Lesson 21 - Hvac Ducts And Duct
  출처: https://www.youtube.com/watch?v=lpqNMj6EfA8

• [Tavily] Revit Duct Pressure Loss Report | Revit MEP | #hvac
  Revit Tagging | Revit MEP | #hvac #ducting #revitmep. Tech Tutorials · 468 views ; HVAC Duct Design: Manual D, Fittings, Friction Rate, Pressure
  출처: https://www.youtube.com/watch?v=X7XqSrQnOTI

• [Tavily] How to Place HVAC Ducts in Revit MEP
  Welcome to our comprehensive tutorial on placing HVAC ducts in Revit MEP! In this video, we guide you through the process of adding supply,
  출처: https://www.youtube.com/watch?v=KKjzFZyeRAA

• [Tavily] ✅To create Supply Air Ducts and Return ...
  To create Supply Air Ducts and Return Air Ducts in Revit: 1. Select Duct Tool: In the "Systems" tab, choose the "Duct" tool and pick the appropriate duct type.
  출처: https://www.instagram.com/reel/DHdGx_7vhJe

• [Tavily] Revit MEP HVAC Ductwork lay out, Supply & Return Duct / ...
  Revit MEP Ductwork lay out, Supply & Return Duct / Diffusers This is a link to the file for download that I'm using in the video.
  출처: https://www.youtube.com/watch?v=Nfju23XYiDg

검토 기준: 공식 문서 여부, 최신성, 프로젝트 적용 가능성, 보안/개인정보 포함 여부를 확인한 뒤 표준/교육/FAQ 후보로 승격한다.


## 공조덕트 일반 FAQ와 답변 포인트 (2026-05-22)
- Source: LUA BIM LABS internal MEP knowledge baseline
- Tags: hvac-duct,faq,bim,coordination
- Links: [[설비기초]], [[설비도면해석]], [[설비시공조율]], [[설비자동제어]]

덕트 종류를 물을 때:
- 기능 기준으로는 SA, RA, EA, OA, MA, PS, SE로 설명한다.
- 형상 기준으로는 장방형 덕트, 원형 덕트, 스파이럴 덕트, 플렉시블 덕트로 설명한다.
- 용도 기준으로는 일반 공조 덕트, 주방 배기 덕트, 화장실 배기 덕트, 주차장 환기 덕트, 제연 덕트로 설명한다.

덕트 크기를 물을 때:
- 덕트 크기는 풍량, 허용 풍속, 정압 손실, 소음 기준에 따라 정한다.
- 같은 풍량이라도 풍속을 낮추면 덕트가 커지고, 풍속을 높이면 덕트가 작아지지만 소음과 정압 손실이 증가한다.
- BIM 답변에서는 설계 풍량, 풍속, 단면적, 덕트 하단고를 함께 확인해야 한다.

덕트 간섭을 물을 때:
- 제연 덕트와 메인 덕트는 우선 보호하고, 말단 덕트와 플렉시블 덕트는 조정 가능성이 높다.
- 덕트 단면 축소는 풍량 부족과 소음 증가로 이어지므로 단순히 "작게 만들면 된다"고 답하지 않는다.
- 디퓨저, 감지기, 조명, 스프링클러 헤드와의 천장 배치를 함께 확인한다.

덕트 점검을 물을 때:
- 댐퍼, 방화댐퍼, 코일, 필터, VAV 박스 주변은 점검구와 접근 공간이 필요하다.
- 천장 안에 물리 충돌이 없어도 점검구가 없으면 유지관리 이슈로 분류한다.


## Q: 인천공항 공조덕트 물량이 얼마나 들어갔어? (2026-05-24)
- Source: telegram-qa
- Tags: hvac-duct,qa,incheon-airport,quantity

인천국제공항 공조덕트 주요 물량 참고 수치:

- 공조 덕트 서비스 면적: T1 단독 약 500,000 m² 추정 (여압·환기·제연 포함)
- AHU (공기조화기): 터미널당 수백 대 설치 (중앙 공조 방식)
- FCU (팬코일유닛): 수천 대 (세부 구역 공조)
- 제연 덕트: 방화구획별 전용 제연 계통 별도 설치
- 방화댐퍼: 방화구획 경계 덕트 관통부마다 설치 (수천 개소 추정)

주의: 공식 BQ는 비공개이며, 위 수치는 공개 자료 기반 추정값이다.


## Q: 국내 대형 프로젝트 공조덕트 주요 이슈 (2026-05-24)
- Source: telegram-qa
- Tags: hvac-duct,qa,domestic-project,large-scale

### 가덕도 신공항 여객터미널
- 대형 오픈 공간: 장스팬 지붕 아래 대형 SA/RA 덕트 노출 계획 다수
- 제연 계통: 여객홀·면세구역 방화구획별 전용 제연 덕트 (NFSC 501A 적용)
- 덕트 재질: 해양 환경 → 아연도금 + 에폭시 코팅 또는 SUS 덕트 검토

### 현대GBC (105층)
- 수직 덕트 샤프트: 초고층 풍압 차이 → 구간별 압력 제어 VAV/CAV 구분
- 아웃리거층 기계실: AHU 교체 공간, 덕트 전이부 설계 복잡
- 방화구획: 105층 × 층별 방화댐퍼 → 수천 개소 댐퍼 BIM 확인 필요

### GTX 지하역사
- 제연 덕트: 지하 승강장 제연은 NFSC 501 적용, 전용 덕트 경로 확보 중요
- 환기 덕트: 터널 환기 + 역사 환기를 단계별 분리 운영
- BIM 협의: 구조물 내 덕트 경로 제약 → 조기 확보가 핵심

주의: 세부 설계 기준은 발주처 설계 지침서 우선 적용.
