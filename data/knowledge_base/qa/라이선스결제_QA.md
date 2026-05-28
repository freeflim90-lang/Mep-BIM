# 라이선스결제 Q&A 지식

텔레그램 질문·자동 수집 응답 저장소 — 기준 가이드라인(라이선스결제.md)과 분리 운영.


## 라이선스결제 FAQ (2026-05-24)
- Source: LUA BIM LABS internal license/billing knowledge baseline
- Tags: license,billing,faq,autodesk-store,subscription

Autodesk App Store 구독 플랜을 물을 때:
- Individual: USD 19/month 또는 USD 190/year (1인 라이선스)
- Team 5-Pack: USD 79/month 또는 USD 790/year (5인)
- Enterprise: 직접 판매 (10인 이상, 별도 견적)
- 30일 무료 체험 제공 (Entitlement API 연동 필요)

구독 상태별 동작을 물을 때:
- 유효 구독: 전체 기능 활성화
- 체험판: 기능 제한 또는 실행 횟수 제한 + 업그레이드 안내
- 만료: 유료 기능 비활성화 + 갱신 링크 표시
- 오프라인 캐시 유효 (7일): 전체 기능 허용
- 오프라인 캐시 만료: 읽기 전용 모드 + 인터넷 연결 안내

Autodesk Entitlement API 연동 방법을 물을 때:
- 엔드포인트: GET https://apps.autodesk.com/webservices/checkentitlement
- 파라미터: userid(Autodesk ID), appid(Store App ID)
- 응답: isValid(true/false), message
- Add-in 시작 시 검증 → 실패 시 유료 기능 잠금
- 캐시: 마지막 검증 결과를 암호화해 로컬 저장 (최대 7일)


## Q: 한국 법인이 Autodesk Store 수익을 받으면 세금 처리가 어떻게 돼? (2026-05-24)
- Source: LUA BIM LABS internal finance knowledge baseline
- Tags: license,qa,tax,revenue,korea

Autodesk App Store 수익 세금 처리:
- 결제: BlueSnap/PayPal 처리 (publisher 직접 관여 없음)
- VAT: 구매자 국가 기준 Autodesk가 처리
- Publisher 정산: 월별 수익 정산, 최소 지급액 USD 50 이상 시 지급
- 한국 법인 처리:
  - 해외 플랫폼 수익 = 외화 수입
  - 외화 수입 계좌 별도 관리 권장
  - 원화 환전 시 환차손익 회계 처리 필요
  - 부가세: 해외 플랫폼 매출은 영세율 적용 (수출 서비스)
  - 법인세: 해외 수익 포함 법인세 신고 (세무사 확인 필요)


## Q: 구독 갱신율을 높이려면? (2026-05-24)
- Source: LUA BIM LABS internal product/revenue knowledge baseline
- Tags: license,qa,renewal,retention,churn

구독 갱신율 향상 전략:
- 만료 30일 전: 갱신 안내 이메일 발송 (갱신 할인 쿠폰 포함)
- 만료 7일 전: in-app TaskDialog 알림 + 갱신 버튼 (App Store 링크)
- 만료 1일 전: 최종 알림
- 갱신 후 즉시 감사 이메일 + 신규 기능 안내
- 목표 월간 해지율(Churn Rate): 3% 이하
- 연간 구독 전환 유도: 월간 대비 17% 할인 → 전환율 향상
