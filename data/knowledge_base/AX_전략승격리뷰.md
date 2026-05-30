# AX 전략승격리뷰 지식 베이스

시간별 신호와 일일 브리핑을 주간 단위로 묶어 AX 전략, 제품, 교육, 자동화 후보로 승격한다.


## 2026-05-28 주간 AX 전략 리뷰
- Source: `docs/knowledge_updates/weekly/2026-W22_AX_STRATEGY_REVIEW.md`
- Tags: ax,weekly-review,strategy,bim

분류 요약: 시공 BIM/스마트건설 16, AX 전략 신호 15, OpenBIM/납품검증 14, Model Quality Auditor 7, BIM 자동화/Add-in 5, 교육/확산 3

운영 판단: 상위 반복 신호는 CSO, 제품패키징, Model Quality Auditor, 교육컨설팅 지식으로 연결한다.

## AX 전략승격리뷰 Claude Code 심화 업데이트 (2026-05-28)
- Source: claude-code-enhanced 2026-05-28
- Tags: ax,strategy-review,weekly,product-roadmap,bim-automation

**주간 전략 리뷰 프레임워크:**
- 검토 주기: 매주 월요일 09:00 KST (LaunchAgent cron 기반 자동 리포트 생성)
- 입력 소스: 시간별 신호 DB (SQLite) + 일일 브리핑 5건 + 고객 지원 이슈 요약
- 승격 기준 4가지: ①반복성(동일 신호 3회 이상) ②긴급성(규제 변경·경쟁사 출시) ③시장 규모(KRW 10억+ 잠재 시장) ④내부 역량 적합성(3개월 내 구현 가능)
- 출력 형식: Obsidian 노트 + GitHub Projects 이슈 자동 생성 + Google Calendar 마일스톤 등록

**2026 AX 전략 축:**
- **제품화**: Revit Add-in 신규 모듈 (MEP 자동 간섭 해소, LOD 자동 검증 → Autodesk App Store 출시)
- **자동화**: Python + Dynamo 워크플로우 패키지화 (MEPover 3.x + 자체 노드 라이브러리)
- **교육**: buildingSMART OPEN BIM 커리큘럼 연계 인증 과정 (ISO 19650 기반 5단계)
- **글로벌**: Autodesk App Store 영어/일본어 현지화 → APAC 3개국 동시 출시 (JP/SG/AU 우선)

**평가 매트릭스:**
- 전략 적합성 40% / 시장 기회 30% / 구현 난이도(역산) 20% / 타이밍 10%
- 90점 이상: 즉시 Sprint 편입 / 70~89점: 다음 분기 로드맵 / 69점 이하: 관찰 대기
- 관련: [[AX_시간별_신호모니터링]] · [[최고전략CSO]] · [[산업동향_데일리브리핑]] · [[내부성장루프]]

## AX 전략 실행 심화: 신호 → 제품화 파이프라인 (2026-05-28)
- Source: claude-code-enhanced 2026-05-28
- Tags: ax,strategy,product-pipeline,signal-to-product,weekly-review

**주간 리뷰 → 제품 백로그 승격 판단 기준:**

| 신호 유형 | 승격 조건 | 담당자 | 산출물 |
|---|---|---|---|
| 법규 변경 | NFTC/KCS/건축법 개정 공포 | CSO → 개발팀 | 호환성 업데이트 이슈 |
| 경쟁사 신기능 | App Store 신규 출시 | CSO → 제품기획 | 기능 갭 분석 보고서 |
| 고객 반복 요청 | 동일 요청 3건+ | CS → 제품기획 | 요구사항 명세서 |
| 기술 트렌드 | buildingSMART IFC 4.4 Draft | 개발팀 → CSO | 기술 적합성 검토서 |

**2026 상반기 승격 완료 신호 (예시):**
- Revit 2025 .NET 8 마이그레이션 의무화 → 빌드 시스템 업그레이드 완료
- NFTC 103 2025 개정 (헤드 간격 기준 강화) → 소방 파라미터 검증 로직 업데이트
- Autodesk Named User 2025 변경 (Machine License 폐지) → 라이선스 관리 모듈 대응

**정기 AX 전략 캘린더:**
- 매주 월요일 09:00: 주간 AX 전략 리뷰 (CSO + 팀장급)
- 매월 첫째 주 금요일: 월간 OKR 점검 (CEO + CSO + CFO)
- 매분기 마지막 주: 분기 리뷰 + 다음 분기 로드맵 확정
- 연 2회 (6월/12월): 경쟁사 전략 분석 보고서 발행

**승격 실패 신호 처리 (Drop/Watch):**
- Watch(관찰 유지): 잠재력 있으나 시기 미성숙 → 6개월 후 재검토 태그
- Drop(폐기): 3회 연속 우선순위 하락 → 백로그 정리, 이유 기록
- 관련: [[AX_시간별_신호모니터링]] · [[최고전략CSO]] · [[전략기획]] · [[아이디어발굴]]
