# CFO 지식 베이스

## 2026-06-05 상품 Launch Status source of truth 초안
- Source: `knowledge/10_agents/conflict_resolution/PRODUCT_LAUNCH_STATUS_SOURCE_OF_TRUTH_DRAFT_20260605.md`
- Tags: cfo,pricing,launch-status,source-of-truth,draft

CEO/CFO 최종 승인 전 고객 공개 판매 기준은 Starter만 SALE_READY로 본다. Personal Tutor와 Coordinator Mentor는 COMING_SOON, Project Mentor Standard/Intensive는 CONSULTATION_ONLY로 둔다.

CFO 운영 기준:
- SALE_READY가 아닌 상품은 결제 링크를 고객에게 발송하지 않는다.
- Project Mentor 가격은 내부 검토 또는 상담 후보이며, 확정 판매 가격처럼 안내하지 않는다.
- 상품별 가격표, 환불 조건, 운영 리소스, 법무 검토가 모두 확인된 뒤 Launch Status를 변경한다.
- 고객지원CS는 승인 전 "지금 결제 가능", "가격 확정", "바로 시작 가능" 문구를 쓰지 않는다.

관련: `AITEST_20260605_007`

## 2026-06-05 CFO 재무 전략 2026 최신 업데이트
- Source: LUA BIM LABS 내부 재무 기준, Autodesk Store 수익 모델, 정부 지원사업
- Tags: cfo,finance,mrr,revenue,cost,government-support,2026

**CFO 핵심 재무 지표 (2026 목표):**
| 지표 | 현재 | 2026 H2 목표 | 달성 방법 |
|------|------|------------|---------|
| MRR (월 반복 수익) | 초기 단계 | USD 1,000+ | Starter Plan 50명 + App Store |
| AI 운영 비용 | Claude API + DeepSeek | 최적화 중 | 모델 라우팅으로 비용 절감 |
| R&D 지원 | 자체 자금 | AX 바우처 신청 | 정부 13억 지원 타겟 |
| 수익 채널 | 교육 구독 | 교육+App+컨설팅 | 3채널 다각화 |

**AI 운영 비용 최적화 전략:**
- DeepSeek(내부): 고빈도 일반 질문 처리 → 비용 절감
- Claude API(외부): 고품질 필요 답변·최종 검토 → 품질 확보
- 모델 라우팅: 질문 복잡도 기반 자동 모델 선택
- PAID_AI_ENABLED 플래그: 비용 제어 스위치

**정부 지원사업 재무 계획:**
- AX 원스톱 바우처: 최대 13억원, 2년 → AI·클라우드·데이터 비용 커버
- 스마트건설 얼라이언스 기술실증 지원: R&D 비용 일부 지원
- 중소기업 BIM 지원 사업: 교육 서비스 연계

## Autodesk Store 구독 수익 모델 (2026-05-19 09:37:53)
- Source: `docs/autodesk_store/SUBSCRIPTION_PRICING.md`
- Tags: pricing,mrr,subscription

초기 가격은 Individual USD 14/month, USD 140/year다. 상품은 Individual, Team 5-Pack(USD 490/year), Enterprise(라이선스 문의) 세 가지로 유지한다. Individual 월 구독 기준 10명 유료 전환 시 MRR USD 140, 50명 전환 시 MRR USD 700, 100명 전환 시 MRR USD 1,400 수준이다. 초기에는 가격 극대화보다 설치 성공률, 리뷰, 유지율, 지원 비용을 검증한다. 10명 이상 유료 고객과 긍정 리뷰가 생긴 뒤 Individual 가격 인상이나 Enterprise 직접 판매를 검토한다.


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
MRR $1,000 목표: Individual $14/월 기준 약 72명 유료 전환 필요.
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


## AEC SaaS 구독 재무 전략 Claude Code 심화 업데이트 (2026-05-28)
- Source: claude-code-enhanced 2026-05-28
- Tags: CFO,재무,SaaS,구독,LTV,CAC,수익인식

- AEC SaaS 구독 모델의 핵심 재무 지표: 월간반복수익(MRR), 연간반복수익(ARR), 고객생애가치(LTV), 고객획득비용(CAC). 초기 스타트업 기준 LTV/CAC 비율 3:1 이상이 투자 유치 심사 통과 최소 기준이며, 5:1 이상이면 유리한 조건으로 시리즈 A 진행 가능하다.
- Autodesk App Store의 수익 분배 구조는 개발사 70%, Autodesk 30%이며, 결제는 USD 기준 월별 정산이다. 환율 변동 리스크를 줄이기 위해 USD 수입의 30% 이상을 헤지하거나 외화계좌로 유지하는 것이 권장된다.
- IFRS 15 기준 구독 수익 인식: 서비스 제공 기간에 걸쳐 균등 인식해야 하며, 연간 선결제 구독의 경우 선수수익(Deferred Revenue)으로 처리 후 월별 이연 인식한다. 스타트업은 이 처리 오류로 세무조사 리스크가 발생할 수 있으므로 초기부터 정확한 회계 기준을 수립해야 한다.
- 국내 소프트웨어 매출 원가율(COGS)은 통상 20~35% 수준이다. Add-in 유지보수·업데이트 비용, 서버 인프라비, 고객지원 인건비를 포함하면 Gross Margin 65~80% 유지가 목표치다.
- 공공 BIM 프로젝트 수주 시 계약금 30%, 중간금 40%, 잔금 30% 구조가 일반적이다. 용역 매출과 구독 매출을 분리 회계 처리하여 투자자에게 ARR과 프로젝트 매출을 명확히 구분해 보고해야 한다.
- 관련: [[CEO]] · [[라이선스결제]] · [[글로벌_매출관리원]] · [[BIM_프로젝트_견적산정]]

## CFO 마스터급 경험 지식 (2026-05-28)
- Source: claude-code-enhanced 2026-05-28
- Tags: CFO,K-IFRS15,세무조사,자금조달,원가분석,환율헤지

K-IFRS 15 SaaS 수익인식 실무 함정: 연간 구독료를 계약 체결 시 전액 수익으로 인식하면 세무조사 시 과다 수익 인식으로 법인세 추가 납부 리스크가 발생한다. 연 USD 140 연간 플랜은 12개월로 나누어 월 USD 11.67씩 이연 인식해야 한다. 설치비·구현 지원비가 포함된 계약은 "별도 수행 의무" 여부를 판단하여 설치 서비스가 독립적 가치를 가지면 별도 거래 가격으로 분리 인식하고, 그렇지 않으면 구독 기간에 걸쳐 배분한다.

세무조사 대비 R&D 세액공제: 중소기업 연구비 세액공제(조특법 제10조)는 인건비의 최대 25%까지 공제 가능하다. 적격 비용 문서화 요건: 연구노트(날짜·수행자·내용 기재), 연구 프로젝트별 공수 배분표, 외부 연구 용역 계약서 원본. 감가상각비와 일반 운영 인건비를 R&D 비용에 혼입하면 사후 검토 시 전액 소급 취소되므로 계정 분리가 필수다.

자금 조달 희석화 vs 부채 의사결정: ARR USD 100K 미만 단계에서는 VC 투자(지분 희석)보다 정부 지원금(TIPS, 스마트제조혁신, 산업부 R&D)을 우선 활용해야 희석 없이 개발 자금을 조달할 수 있다. 전환사채(CB) 활용 시 전환 가격 리셋 조항이 포함되면 추후 다운라운드 시 희석이 폭발적으로 커지므로 계약서 초안에서 리셋 조항을 반드시 제거해야 한다.

원가 분석으로 비수익 제품 조기 발견: 제품별 직접 원가(개발 인건비 + 지원 비용)를 월별로 추적하여 Gross Margin이 3개월 연속 40% 미만이면 가격 인상 또는 제품 폐기를 CEO에게 권고한다. 달러 매출 발생 시 환율 헤지 기준: 월 USD 수입 USD 5,000 초과부터 외화 예금 유지 또는 선물환 계약으로 30~50% 헤지를 권장한다.

- 관련: [[CEO]] · [[법무조항검토]] · [[조율차장]] · [[프로젝트분석]]

## CFO 재무 인텔리전스 업데이트 (2026-06-26)
- Source: auto-enrich via Naver+Tavily+Google+DDG+Ollama 2026-06-26
- KST04 자동수집: 공식 출처/담당자 검증 전 고객 확정 답변, 납품 기준, 견적 기준으로 사용 금지.
- Tags: cfo,finance,revenue,update

- 구독 수익 인식 기준을 준수하세요: IFRS 15 또는 ASC 606과 같은 국제/국내 재무 보고 표준에 따라 구독 수익을 인식하고 누적하십시오.
- LTV/CAC 관리에 주력하세요: 고객 평균 생존 기간(LTV)은 최대 3년 이상, 고객당 캐스트아웃 비용(CAC)은 연간 매출의 20% 이내를 목표로 설정하십시오.
- 환율 리스크를 관리하기 위해 현지화 전략을 구현하세요: 주요 거래 국가의 통화에 대한 포트폴리오를 구성하고, 옵션 및 선물 계약을 활용하여 환율 변동 위험을 최소화하십시오.
- 관련: [[글로벌_매출관리원]]

