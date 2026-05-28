# 경비정산_AI Q&A 지식

텔레그램 질문·자동 수집 응답 저장소 — 기준 가이드라인(경비정산_AI.md)과 분리 운영.


## 경비정산 FAQ (2026-05-24)
- Source: LUA BIM LABS internal expense management knowledge baseline
- Tags: expense,faq,finance,receipt

영수증 없이 경비 처리가 가능한지 물을 때:
- 원칙적으로 증빙 없는 경비는 처리하지 않는다.
- 분실 시: 거래 내역서(카드사 발급) 또는 간이영수증으로 대체 가능
- 간이영수증은 3만원 이하 소액에 한해 인정 (세법 기준)
- 5만원 이상: 세금계산서 또는 현금영수증 필수

법인카드 사용 후 처리 방법을 물을 때:
1. 사용 당일 Telegram에 목적·사용처·금액·참석자 기록
2. 영수증/전표 사진 전송
3. 경비정산_AI가 비용 유형 분류 및 프로젝트 귀속 여부 확인
4. 월말 CFO 검토 후 확정

경비 지출 승인 기준을 물을 때:
- 10만원 미만: 담당자 선지출 후 증빙 제출 가능
- 10만원 이상: CFO 사전 승인 후 지출 원칙
- 출장비: 사전 출장 계획서 제출 → 귀국 후 [5]일 이내 증빙 정산


## Q: 개인카드로 먼저 결제했을 때 정산은 어떻게 해? (2026-05-24)
- Source: LUA BIM LABS internal expense management knowledge baseline
- Tags: expense,qa,personal-card,reimbursement

개인카드 선지출 정산 프로세스:
1. Telegram에 영수증 사진 + 사용 목적·금액·날짜 전송
2. 경비정산_AI가 비용 유형 분류 (PROJ/OPS/MEAL 등)
3. 10만원 이상이면 CFO 승인 요청
4. 승인 완료 후 [N]영업일 이내 개인 계좌로 이체
5. 정산 내역을 월별 경비 대장에 등록

주의:
- 정산 요청은 사용일로부터 [30]일 이내 제출 (초과 시 다음 정산 주기 처리)
- 음식비·회의비는 참석자 명단 필수
- 해외 카드 결제는 원화 환산액 기준 처리


## Q: 월말 경비 보고서는 어떻게 만들어? (2026-05-24)
- Source: LUA BIM LABS internal expense management knowledge baseline
- Tags: expense,qa,monthly-report,excel

월말 경비 보고서 작성 절차:
1. 월 마지막 영업일: 경비정산_AI가 해당 월 확정 항목 집계
2. 비용 유형별 합계 + 프로젝트별 귀속 비용 정리
3. 미확인·보류 항목 목록 별도 표시
4. Excel 또는 Telegram 텍스트 요약 → CFO에게 보고
5. CFO 확정 후 세무 자료로 제출

집계 항목:
- 비용 유형별 (PROJ/OPS/SOFT/MKTG/EDU/MEAL/TRAVEL/ETC)
- 증빙 유형별 (세금계산서/영수증/카드전표)
- VAT 공제 가능 항목 합계
- 전월 대비 증감률
