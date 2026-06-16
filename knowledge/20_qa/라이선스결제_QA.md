# 라이선스결제 Q&A 지식

텔레그램 질문·자동 수집 응답 저장소 — 기준 가이드라인(라이선스결제.md)과 분리 운영.

## 2026-06-05 라이선스·결제 실전 Q&A 추가
- Source: Autodesk 공식 라이선스 정책, LUA BIM LABS Starter Plan 운영 기준
- Tags: license,payment,autodesk,subscription,qa,2026

**Q: Autodesk Revit 라이선스 종류가 어떻게 되나요?**
A: 2024년부터 Named User 구독 방식만 지원합니다. 개인 단위 Named User 라이선스(1인 1라이선스)와 Autodesk Flex(토큰 방식, 사용한 만큼 결제)가 있습니다. AEC Collection은 Revit·AutoCAD·Civil 3D·Navisworks 등 패키지로 연간 구독합니다. 기존 기업용 Network License(동시 사용)는 2024년 종료되었습니다. *(KST01 공식확인)*

**Q: Autodesk 라이선스를 팀원이 함께 써도 되나요?**
A: 안됩니다. Named User 방식이므로 1개 라이선스는 1명만 사용 가능합니다. 같은 계정으로 여러 기기에서 동시 사용도 불가합니다. 팀원 수만큼 라이선스를 구매해야 합니다. 위반 시 Autodesk 감사 대상이 될 수 있습니다. *(KST01 공식확인)*

**Q: LUA BIM LABS Starter Plan은 어떻게 결제하나요?**
A: 텔레그램 봇을 통해 결제 링크를 전달드립니다. 월 구독과 연간 구독 중 선택 가능하며, 연간 구독 시 약 15~20% 할인이 적용됩니다. 결제 후 텔레그램 봇에 자동으로 MEP BIM 튜터 권한이 부여됩니다. 구체적인 가격은 운영 채널에서 확인하시기 바랍니다. *(KST03 적용주의: 최신 가격 정책 확인)*

**Q: Autodesk App Store에서 구매한 Add-in은 환불되나요?**
A: Autodesk App Store 환불 정책에 따라 구매 후 30일 이내, 미사용 시 환불 요청 가능합니다. 유료 구독형 Add-in은 다음 결제 전에 구독 취소하면 됩니다. 구체적인 환불 절차는 Autodesk 고객지원 또는 개발사 정책을 확인하세요. *(KST03 적용주의)*


## 라이선스결제 FAQ (2026-05-24)
- Source: LUA BIM LABS internal license/billing knowledge baseline
- Tags: license,billing,faq,autodesk-store,subscription

Autodesk App Store 구독 플랜을 물을 때:
- Individual: USD 14/month 또는 USD 140/year (1인 라이선스, 연간 결제 시 월 환산 약 USD 11.67 · 약 17% 절감)
- Team 5-Pack: USD 490/year (5 seats, 인당 약 USD 8.17/월 · 약 30% 절감)
- Enterprise: 공개 가격 없음, 라이선스 문의(개별 견적)
- 30일 무료 체험 제공 예정 (Entitlement API 연동 필요)

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
