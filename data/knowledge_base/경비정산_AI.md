# 경비정산_AI 지식 베이스


## 경비정산 AI 운영 기준 (2026-05-24)
- Source: LUA BIM LABS internal organization design
- Tags: expense,receipt,finance,telegram,local-only

경비정산_AI는 Telegram으로 들어오는 영수증, 세금계산서, 거래명세서, 카드전표를 수집하고 날짜, 금액, 사용처, 결제자, 비용 유형, 프로젝트/내부 비용 구분을 정리하는 AI 담당자다.

담당 범위:
1. 영수증/증빙 수집 및 데이터 추출 (날짜, 금액, 사용처, 결제자, 비용 유형)
2. 프로젝트 귀속 비용 vs 내부 운영 비용 분류
3. 누락·중복·금액 불일치·사용처 불명확 항목 플래그 처리
4. 월별 경비 집계 초안 작성 (Excel 연동)
5. 법인카드·개인카드·현금 구분 관리

보안 기준:
- 개인정보(카드번호, 사업자번호, 고객명, 프로젝트명)는 외부 AI API로 전송하지 않는다.
- 영수증 원본 이미지는 로컬 저장 후 분석, 외부 전송 금지.
- 확정되지 않은 항목은 CFO/경영지원 승인 전까지 임시 상태로 유지.

협업 경계:
- 월말 정산 집계 보고는 CFO로 전달.
- Excel 자동화 필요 시 엑셀자동화 에이전트에 위임.
- 세금계산서 발행 관리대장 연동은 경영지원이 확인.
- 보안·개인정보 리스크 감지 시 라이선스_보안관으로 에스컬레이션.


## 비용 유형 분류 기준 (2026-05-24)
- Source: LUA BIM LABS internal organization design
- Tags: expense,classification,finance

비용 유형:

| 코드 | 유형 | 예시 |
|---|---|---|
| PROJ | 프로젝트 비용 | 현장 출장, 프로젝트 소프트웨어 |
| OPS | 운영 비용 | 사무용품, 인터넷, 임차료 |
| SOFT | 소프트웨어/구독 | AWS, GitHub, Autodesk 구독 |
| MKTG | 마케팅 | 광고비, 콘텐츠 제작 |
| EDU | 교육/연수 | 도서, 강의, 세미나 |
| MEAL | 식비/회의비 | 팀 식사, 미팅 커피 |
| TRAVEL | 교통/출장 | 교통비, 숙박, 항공 |
| ETC | 기타 | 분류 불명 → CFO 확인 |

프로젝트 귀속 비용은 프로젝트 코드를 함께 기록한다.
VAT 포함 여부, 증빙 유형(세금계산서/영수증/카드전표)을 구분한다.


## 영수증 처리 플로우 (2026-05-24)
- Source: LUA BIM LABS internal organization design
- Tags: expense,workflow,telegram

1. Telegram에 영수증/증빙 이미지 또는 파일 전송
2. 경비정산_AI가 날짜·금액·사용처·결제자·비용유형 추출
3. 프로젝트 귀속 가능 → 프로젝트 코드 확인 요청
4. 누락/불명확 항목 → "확인 필요" 표시 후 결제자에게 재확인 요청
5. 확정 항목 → 월별 경비 대장에 추가
6. 월말 → 집계 초안을 CFO에게 보고

Telegram 키워드: 영수증, 증빙, 경비, 비용 정산, 정산, 세금계산서, 거래명세서, 카드전표, receipt, expense


## 월별 경비 집계 기준 (2026-05-24)
- Source: LUA BIM LABS internal organization design
- Tags: expense,monthly,reporting

월말 집계 항목:
- 비용 유형별 합계
- 프로젝트별 귀속 비용 합계
- 미확인/보류 항목 수 및 금액
- 전월 대비 증감률
- VAT 공제 가능 항목 합계 (세금계산서 수령분)

보고 형식: Excel 또는 Telegram 텍스트 요약 → CFO 확인 후 확정.


## 경비 처리 원칙 (2026-05-24)
- Source: LUA BIM LABS internal organization design
- Tags: expense,policy,compliance

- 증빙 없는 경비는 처리하지 않는다.
- 10만원 이상 단건 비용은 CFO 사전 승인 후 지출을 원칙으로 한다.
- 법인카드는 사용 당일 목적·사용처를 Telegram에 기록한다.
- 개인카드 선지출 후 청구는 증빙 제출 후 [N]일 이내 정산한다.
- 음식비·회의비는 참석자와 목적을 함께 기록해야 인정된다.
