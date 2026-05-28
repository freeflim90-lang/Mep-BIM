# LUA BIM LAB
# 아이디어 발굴-상품화 개발 순서 선정 보고

━━━━━━━━━━━━━━━━━━━━

작성일: 2026-05-28 17:19
배포등급: Internal Only
주관: 아이디어발굴
협업: 전략기획, 견적심사원, CFO, CEO, 브랜드마케팅, 요구사항분석, 프로그램개발, Qwen_Coder_8B

## 1. 현재 개발 큐 상태

- 제품: BIM Command Center for Revit
- 선정 아이템: BIMlize 기능 범위 내재화 - Phase 1 Simple Features
- 완료: 7 / 7
- 완료 여부: 완료
- 남은 task: 없음

## 2. 상품화 후보 TOP 3

| 순위 | 후보 | 대상 | 점수 | 예상 시간 | 예상 비용 | 예상 월 순매출 | 회수 기간 |
|---:|---|---|---:|---:|---:|---:|---:|
| 1 | Navisworks 간섭 결과 책임자 배정 보드 | BIM 코디네이터, 현장 조율 PM | 35 | 24h | USD 320 | USD 789.2 | 0.4개월 |
| 2 | Revit 모델 품질 빠른 진단 리포트 | BIM 매니저, 설계사무소 납품 담당자 | 34 | 24h | USD 320 | USD 702.4 | 0.5개월 |
| 3 | 층별 도면 시트 자동 검수기 | 설계 PM, BIM 납품 담당자 | 30 | 10h | USD 120 | USD 615.6 | 0.2개월 |

## 3. 1순위 후보 개발 전환 판단

- 1순위: Navisworks 간섭 결과 책임자 배정 보드
- 고객 문제: Clash Detective 결과를 공종별 담당자와 상태로 관리하는 과정이 Excel 수작업에 묶인다.
- MVP 해법: 간섭 결과를 공종/층/우선순위/담당자 기준으로 정리하고 CSV 리포트를 자동 생성한다.
- 추천 가격: USD 19/month or USD 190/year
- API 모드: local_only

## 4. Handoff

1. 현재 Qwen 큐가 완료되기 전에는 active queue를 덮어쓰지 않는다.
2. 완료 후 CEO 승인 또는 --activate 실행 시 다음 큐로 전환한다.
3. Qwen_Coder_8B는 요구사항, 도메인 계약, dry-run, 테스트, Revit API 게이트 순서로 초안을 작성한다.
4. 오류와 수정사항은 Obsidian 오답노트로 연결한다.

## 5. 생성 결과

- 다음 큐 후보 생성: 예
- 다음 큐 후보 파일: config/qwen_next_product_draft_queue.json
