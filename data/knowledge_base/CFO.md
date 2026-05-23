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
