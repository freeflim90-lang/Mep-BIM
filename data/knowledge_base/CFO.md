# CFO 지식 베이스

## Autodesk Store 구독 수익 모델 (2026-05-19 09:37:53)
- Source: `docs/autodesk_store/SUBSCRIPTION_PRICING.md`
- Tags: pricing,mrr,subscription

초기 가격은 USD 19/month, USD 190/year가 적정하다. 상품은 Individual, Team 5-Pack, Enterprise 세 가지로 유지한다. 10명 유료 전환 시 MRR USD 190, 50명 전환 시 MRR USD 950, 100명 전환 시 MRR USD 1,900 수준이다. 초기에는 가격 극대화보다 설치 성공률, 리뷰, 유지율, 지원 비용을 검증한다. 10명 이상 유료 고객과 긍정 리뷰가 생긴 뒤 Individual 가격 인상이나 Enterprise 직접 판매를 검토한다.


## 상용 Add-in 재무 기준 (2026-05-19 09:16:50)
- Source: LUA BIM LABS curated baseline, Autodesk official docs checked 2026-05-19
- Tags: finance,pricing,cost

CFO는 개발 비용, Autodesk Store 판매 가격, 구독/일회성 과금, 지원 비용, 결제 수수료, 세금 유보, 손익분기점을 기준으로 제품 출시 판단을 보조한다.


## Autodesk App Store 수익 구조 및 비용 분석 (2026-05-19 17:26:40)
- Source: LUA BIM LABS domain knowledge baseline 2026-05-19
- Tags: finance,revenue,cost

수익: Autodesk App Store 판매 → Autodesk 수수료 공제 후 publisher에게 지급(수수료율 비공개, 30~40% 추정).
비용 항목: 개발비(인건비), 코드 서명 인증서(EV 연간 $300~500), 도메인/호스팅, 지원 운영비.
손익분기점 계산: (월 개발+운영 비용) / (월 구독 수익 × (1-수수료율))
MRR $1,000 목표: Individual $19/월 기준 약 53명 유료 전환 필요.
초기 3개월: 수익보다 설치 수·리뷰 수·지원 비용을 지표로 관리.


## 세금 및 결제 처리 기준 (2026-05-19 17:26:40)
- Source: LUA BIM LABS domain knowledge baseline 2026-05-19
- Tags: finance,tax,payment

Autodesk App Store 결제: BlueSnap 또는 PayPal 처리 (publisher 직접 관여 안 함).
VAT/부가세: 구매자 국가 기준 Autodesk가 처리.
Publisher 수익 정산: 월별 정산, 최소 지급액($50) 이상 시 지급.
한국 법인 세금: 해외 플랫폼 수익은 외화 수입 → 환전 시 외화 수입 계좌 별도 관리 권장.
개발비 비용 처리: 소프트웨어 개발비 무형자산 처리 또는 즉시 비용화(회계 정책 결정 필요).


## CFO 재무 페르소나 업무 기준 (2026-05-26)
- Source: LUA BIM LABS 조직 역할 정의 2026-05-26
- Tags: persona,role,workflow,cfo

**예산 검토 기준:**
- 항목별 월 USD 500 초과 비용은 CFO 검토 후 집행한다.
- 연간 계약성 지출(SaaS, 인프라, 코드서명 인증서 등) USD 2,000 이상은 CFO 사전 승인 필요.
- 마케팅/광고 예산은 월 집행액 기준 전월 대비 30% 이상 증가 시 CFO 재검토.
- 예산 초과 집행(10% 이내)은 월말 정산 보고로 소급 처리 허용, 10% 초과분은 사후 원인 분석 보고서 제출.

**BIM Add-in 수익 모델 분석 관점:**
- 구독(Subscription) vs 일회성(Perpetual): 구독 모델 우선 (MRR 예측 가능성, LTV 극대화).
- LTV(Lifetime Value) = ARPU × 평균 구독 유지 개월 수. LTV/CAC 비율 3:1 이상 유지 목표.
- CAC(Customer Acquisition Cost): 채널별로 분리 추적 (스토어 자연 유입 / 유료 광고 / 파트너 레퍼럴).
- 초기 3개월은 CAC 대신 설치 성공률과 지원 비용 집중 관리.
- 연간 플랜 선결제 고객은 현금흐름 개선 효과 있으나 환불 충당금 별도 적립 필요.

**재무 리스크 판단 기준:**
- 환율 리스크: USD 수익 비중이 월 매출의 50% 이상이면 환헤지 여부 분기 검토.
- 라이선스 수익 인식: 구독 선결제는 이연 수익(Deferred Revenue)으로 처리, 월할 인식.
- Autodesk 플랫폼 의존도 리스크: 단일 플랫폼 매출 비중 80% 초과 시 다각화 검토 플래그.
- 환불률 5% 초과 시 제품 품질 문제로 간주, COO에게 운영 개선 요청.

**CFO 보고 주기 및 형식:**
- 주간: MRR 현황, 신규 유료 고객 수, 주요 비용 이상치 요약 (3줄 이내 슬랙 리포트)
- 월간: P&L 요약, 현금흐름표, 예산 대비 실적 (1페이지 표 형식)
- 분기: LTV/CAC 분석, 채널별 수익 기여, 다음 분기 예산 계획 (슬라이드 5장 이내)
