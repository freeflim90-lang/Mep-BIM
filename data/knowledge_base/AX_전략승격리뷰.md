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

## 2026-05-30 뉴스 트렌드 18항목 전략 승격 판단
- Source: `obsidian_vaults/lua_bim_lab_global_map/NAS_Knowledge/2026-05-30 뉴스 트렌드 18항목 지식 업데이트.md`
- Tags: ax,strategy-review,openbim,aec-ai,autodesk-forma,construction-robotics

**승격 후보 1: OpenBIM 검증형 납품**
- 판단: 즉시 Sprint 후보는 아니지만 Model Quality Auditor 장기 백로그로 승격한다.
- 이유: buildingSMART 쪽 신호가 IFC, IDS, BCF, IFC Validation, Software Certification을 함께 다루고 있어 발주처 납품 기준의 자동 검증 가능성이 커진다.
- 산출물: IFC/IDS/BCF 용어집, 납품검수 체크리스트, 향후 ifctester/IDS 검토 PoC.

**승격 후보 2: 실무자 자동화 교육 트랙**
- 판단: 즉시 교육 상품 후보.
- 이유: Python in AEC, Grasshopper/Tekla 자동화 신호는 MEP BIM 실무자가 반복 업무를 줄이는 교육 수요와 직접 연결된다.
- 산출물: Python 업무 자동화 → Dynamo/Grasshopper 모델 자동화 → Revit API/Add-in 제품화 3단계 커리큘럼.

**승격 후보 3: 국내 건설 AX 생태계 추적**
- 판단: Watch에서 Strategy Review로 한 단계 승격.
- 이유: AECO AX Summit 보도에서 설계 자동화, 원가·견적·공정관리, 응용솔루션으로 시장 카테고리가 분리되는 모습이 확인된다.
- 산출물: 국내 AX 기업/기술 카테고리 표, 파트너십 후보 분류, 경쟁 기능 관찰 리스트.

**관찰 유지: Autodesk Forma/Revit 클라우드 연결**
- 판단: Add-in 로드맵 점검 항목으로 유지.
- 이유: Autodesk가 Forma 중심의 AECO 클라우드와 Revit 연결을 강화하므로, 독립 Add-in은 데이터 내보내기와 협업 흐름을 고려해야 한다.
- 산출물: Revit Add-in 결과물 export 형식 목록(CSV/JSON/BCF/IFC/Excel)과 Store 문구 점검.

**관찰 유지: 로봇·현장 자동화**
- 판단: 교육 사례 및 장기 전략 Watch.
- 이유: 현장 로봇은 직접 개발·도입 비용이 크지만, BIM/디지털트윈과 as-built 데이터를 맞추는 흐름은 준공 검측 자동화와 맞닿아 있다.
- 산출물: 스마트시공 교육 사례, 현장 검측 데이터 입력값 분류.


## 2026-05-30 뉴스 트렌드 자동 전략 승격 판단
- Source: `obsidian_vaults/lua_bim_lab_global_map/NAS_Knowledge/2026-05-30 뉴스 트렌드 18항목 지식 업데이트.md`
- Tags: ax,strategy-review,auto-deepening,news-trend

**승격/관찰 후보 1: OpenBIM 검증형 납품**
- 관련 신호: 1번, 3번, 4번, 5번
- 판단: Model Quality Auditor 장기 백로그로 승격하고 ifctester/IDS PoC 후보를 만든다.
- 이유: OpenBIM은 파일 교환을 넘어 IDS 요구사항, BCF 이슈 추적, 검증 서비스, 소프트웨어 인증까지 포함하는 납품 계약 언어로 이동한다.

**승격/관찰 후보 2: Python-Dynamo-Grasshopper-Revit API 자동화 교육**
- 관련 신호: 2번, 3번, 5번, 6번, 8번, 9번, 12번, 13번
- 판단: Starter/PM 교육 상품에 장비표, 파라미터, 시트/뷰 자동화 실습을 추가한다.
- 이유: AEC 자동화는 전문 개발자만의 영역이 아니라 실무자가 반복 업무를 줄이는 단계형 역량으로 바뀌고 있다.

**승격/관찰 후보 3: 국내 건설 AX 생태계**
- 관련 신호: 2번, 3번, 5번, 6번, 8번, 9번, 12번, 13번
- 판단: 국내 AX 기업/기술 카테고리 표와 파트너십 후보 분류를 생성한다.
- 이유: 국내 건설 AI는 설계 자동화, 원가·견적·공정관리, 응용솔루션으로 분화되는 단계에 들어섰다.

**승격/관찰 후보 4: Autodesk Forma/Revit 클라우드 연결**
- 관련 신호: 9번, 15번
- 판단: Add-in 결과물 export 형식과 Autodesk Store 문구를 점검한다.
- 이유: Autodesk가 Forma 중심 AECO 클라우드와 Revit 연결을 강화할수록 Add-in은 단독 버튼 기능보다 데이터 내보내기와 협업 흐름이 중요해진다.

**승격/관찰 후보 5: 로봇·현장 자동화**
- 관련 신호: 7번, 10번, 14번
- 판단: 직접 상품화는 Watch 유지, 스마트시공 교육 사례로만 활용한다.
- 이유: 현장 로봇은 BIM의 대체재가 아니라 as-built 현장 상태를 BIM/디지털트윈과 정렬하는 데이터 수집 계층으로 보는 것이 적합하다.

**승격/관찰 후보 6: 넷제로·친환경 BIM 데이터**
- 관련 신호: 15번, 17번
- 판단: 납품검수 파라미터 후보로 보관하고 반복 노출 시 제안서 고급 옵션으로 승격한다.
- 이유: 친환경 건축은 인증 문구가 아니라 재료·수량·열성능·탄소계수 데이터 관리 문제로 바뀌고 있다.


## 2026-05-31 뉴스 트렌드 자동 전략 승격 판단
- Source: `obsidian_vaults/lua_bim_lab_global_map/NAS_Knowledge/2026-05-31 뉴스 트렌드 18항목 지식 업데이트.md`
- Tags: ax,strategy-review,auto-deepening,news-trend

**승격/관찰 후보 1: OpenBIM 검증형 납품**
- 관련 신호: 1번, 3번, 4번, 5번
- 판단: Model Quality Auditor 장기 백로그로 승격하고 ifctester/IDS PoC 후보를 만든다.
- 이유: OpenBIM은 파일 교환을 넘어 IDS 요구사항, BCF 이슈 추적, 검증 서비스, 소프트웨어 인증까지 포함하는 납품 계약 언어로 이동한다.

**승격/관찰 후보 2: Python-Dynamo-Grasshopper-Revit API 자동화 교육**
- 관련 신호: 2번, 3번, 5번, 6번, 8번, 10번, 11번, 12번
- 판단: Starter/PM 교육 상품에 장비표, 파라미터, 시트/뷰 자동화 실습을 추가한다.
- 이유: AEC 자동화는 전문 개발자만의 영역이 아니라 실무자가 반복 업무를 줄이는 단계형 역량으로 바뀌고 있다.

**승격/관찰 후보 3: 국내 건설 AX 생태계**
- 관련 신호: 2번, 3번, 5번, 6번, 8번, 10번, 11번, 12번
- 판단: 국내 AX 기업/기술 카테고리 표와 파트너십 후보 분류를 생성한다.
- 이유: 국내 건설 AI는 설계 자동화, 원가·견적·공정관리, 응용솔루션으로 분화되는 단계에 들어섰다.

**승격/관찰 후보 4: Autodesk Forma/Revit 클라우드 연결**
- 관련 신호: 10번, 12번
- 판단: Add-in 결과물 export 형식과 Autodesk Store 문구를 점검한다.
- 이유: Autodesk가 Forma 중심 AECO 클라우드와 Revit 연결을 강화할수록 Add-in은 단독 버튼 기능보다 데이터 내보내기와 협업 흐름이 중요해진다.

**승격/관찰 후보 5: 로봇·현장 자동화**
- 관련 신호: 7번, 14번, 17번, 18번
- 판단: 직접 상품화는 Watch 유지, 스마트시공 교육 사례로만 활용한다.
- 이유: 현장 로봇은 BIM의 대체재가 아니라 as-built 현장 상태를 BIM/디지털트윈과 정렬하는 데이터 수집 계층으로 보는 것이 적합하다.

**승격/관찰 후보 6: 넷제로·친환경 BIM 데이터**
- 관련 신호: 12번, 15번, 16번
- 판단: 납품검수 파라미터 후보로 보관하고 반복 노출 시 제안서 고급 옵션으로 승격한다.
- 이유: 친환경 건축은 인증 문구가 아니라 재료·수량·열성능·탄소계수 데이터 관리 문제로 바뀌고 있다.


## 2026-06-01 뉴스 트렌드 자동 전략 승격 판단
- Source: `obsidian_vaults/lua_bim_lab_global_map/NAS_Knowledge/2026-06-01 뉴스 트렌드 18항목 지식 업데이트.md`
- Tags: ax,strategy-review,auto-deepening,news-trend

**승격/관찰 후보 1: OpenBIM 검증형 납품**
- 관련 신호: 1번, 3번, 4번, 5번, 18번
- 판단: Model Quality Auditor 장기 백로그로 승격하고 ifctester/IDS PoC 후보를 만든다.
- 이유: OpenBIM은 파일 교환을 넘어 IDS 요구사항, BCF 이슈 추적, 검증 서비스, 소프트웨어 인증까지 포함하는 납품 계약 언어로 이동한다.

**승격/관찰 후보 2: Python-Dynamo-Grasshopper-Revit API 자동화 교육**
- 관련 신호: 2번, 3번, 5번, 6번, 8번, 11번, 12번, 13번
- 판단: Starter/PM 교육 상품에 장비표, 파라미터, 시트/뷰 자동화 실습을 추가한다.
- 이유: AEC 자동화는 전문 개발자만의 영역이 아니라 실무자가 반복 업무를 줄이는 단계형 역량으로 바뀌고 있다.

**승격/관찰 후보 3: 국내 건설 AX 생태계**
- 관련 신호: 2번, 3번, 5번, 6번, 8번, 11번, 12번, 13번
- 판단: 국내 AX 기업/기술 카테고리 표와 파트너십 후보 분류를 생성한다.
- 이유: 국내 건설 AI는 설계 자동화, 원가·견적·공정관리, 응용솔루션으로 분화되는 단계에 들어섰다.

**승격/관찰 후보 4: 로봇·현장 자동화**
- 관련 신호: 7번, 9번, 12번, 14번, 17번
- 판단: 직접 상품화는 Watch 유지, 스마트시공 교육 사례로만 활용한다.
- 이유: 현장 로봇은 BIM의 대체재가 아니라 as-built 현장 상태를 BIM/디지털트윈과 정렬하는 데이터 수집 계층으로 보는 것이 적합하다.

**승격/관찰 후보 5: 넷제로·친환경 BIM 데이터**
- 관련 신호: 15번, 16번
- 판단: 납품검수 파라미터 후보로 보관하고 반복 노출 시 제안서 고급 옵션으로 승격한다.
- 이유: 친환경 건축은 인증 문구가 아니라 재료·수량·열성능·탄소계수 데이터 관리 문제로 바뀌고 있다.

## 2026-06-01 주간 AX 전략 리뷰
- Source: `docs/knowledge_updates/weekly/2026-W23_AX_STRATEGY_REVIEW.md`
- Tags: ax,weekly-review,strategy,bim

분류 요약: AX 전략 신호 12, 시공 BIM/스마트건설 11, OpenBIM/납품검증 8, Model Quality Auditor 6, 교육/확산 2, BIM 자동화/Add-in 1

운영 판단: 상위 반복 신호는 CSO, 제품패키징, Model Quality Auditor, 교육컨설팅 지식으로 연결한다.


## 2026-06-02 뉴스 트렌드 자동 전략 승격 판단
- Source: `obsidian_vaults/lua_bim_lab_global_map/NAS_Knowledge/2026-06-02 뉴스 트렌드 18항목 지식 업데이트.md`
- Tags: ax,strategy-review,auto-deepening,news-trend

**승격/관찰 후보 1: OpenBIM 검증형 납품**
- 관련 신호: 1번, 4번, 5번, 6번
- 판단: Model Quality Auditor 장기 백로그로 승격하고 ifctester/IDS PoC 후보를 만든다.
- 이유: OpenBIM은 파일 교환을 넘어 IDS 요구사항, BCF 이슈 추적, 검증 서비스, 소프트웨어 인증까지 포함하는 납품 계약 언어로 이동한다.

**승격/관찰 후보 2: Python-Dynamo-Grasshopper-Revit API 자동화 교육**
- 관련 신호: 2번, 3번, 4번, 6번, 7번, 8번, 9번, 11번
- 판단: Starter/PM 교육 상품에 장비표, 파라미터, 시트/뷰 자동화 실습을 추가한다.
- 이유: AEC 자동화는 전문 개발자만의 영역이 아니라 실무자가 반복 업무를 줄이는 단계형 역량으로 바뀌고 있다.

**승격/관찰 후보 3: 국내 건설 AX 생태계**
- 관련 신호: 2번, 3번, 4번, 6번, 7번, 8번, 9번, 11번
- 판단: 국내 AX 기업/기술 카테고리 표와 파트너십 후보 분류를 생성한다.
- 이유: 국내 건설 AI는 설계 자동화, 원가·견적·공정관리, 응용솔루션으로 분화되는 단계에 들어섰다.

**승격/관찰 후보 4: Autodesk Forma/Revit 클라우드 연결**
- 관련 신호: 2번, 10번
- 판단: Add-in 결과물 export 형식과 Autodesk Store 문구를 점검한다.
- 이유: Autodesk가 Forma 중심 AECO 클라우드와 Revit 연결을 강화할수록 Add-in은 단독 버튼 기능보다 데이터 내보내기와 협업 흐름이 중요해진다.

**승격/관찰 후보 5: 로봇·현장 자동화**
- 관련 신호: 12번, 14번, 17번
- 판단: 직접 상품화는 Watch 유지, 스마트시공 교육 사례로만 활용한다.
- 이유: 현장 로봇은 BIM의 대체재가 아니라 as-built 현장 상태를 BIM/디지털트윈과 정렬하는 데이터 수집 계층으로 보는 것이 적합하다.

**승격/관찰 후보 6: 넷제로·친환경 BIM 데이터**
- 관련 신호: 7번, 15번, 18번
- 판단: 납품검수 파라미터 후보로 보관하고 반복 노출 시 제안서 고급 옵션으로 승격한다.
- 이유: 친환경 건축은 인증 문구가 아니라 재료·수량·열성능·탄소계수 데이터 관리 문제로 바뀌고 있다.


## 2026-06-03 뉴스 트렌드 자동 전략 승격 판단
- Source: `obsidian_vaults/lua_bim_lab_global_map/NAS_Knowledge/2026-06-03 뉴스 트렌드 18항목 지식 업데이트.md`
- Tags: ax,strategy-review,auto-deepening,news-trend

**승격/관찰 후보 1: OpenBIM 검증형 납품**
- 관련 신호: 1번, 4번, 5번, 6번
- 판단: Model Quality Auditor 장기 백로그로 승격하고 ifctester/IDS PoC 후보를 만든다.
- 이유: OpenBIM은 파일 교환을 넘어 IDS 요구사항, BCF 이슈 추적, 검증 서비스, 소프트웨어 인증까지 포함하는 납품 계약 언어로 이동한다.

**승격/관찰 후보 2: Python-Dynamo-Grasshopper-Revit API 자동화 교육**
- 관련 신호: 2번, 3번, 4번, 6번, 7번, 8번, 9번, 10번
- 판단: Starter/PM 교육 상품에 장비표, 파라미터, 시트/뷰 자동화 실습을 추가한다.
- 이유: AEC 자동화는 전문 개발자만의 영역이 아니라 실무자가 반복 업무를 줄이는 단계형 역량으로 바뀌고 있다.

**승격/관찰 후보 3: 국내 건설 AX 생태계**
- 관련 신호: 2번, 3번, 4번, 6번, 7번, 8번, 9번, 10번
- 판단: 국내 AX 기업/기술 카테고리 표와 파트너십 후보 분류를 생성한다.
- 이유: 국내 건설 AI는 설계 자동화, 원가·견적·공정관리, 응용솔루션으로 분화되는 단계에 들어섰다.

**승격/관찰 후보 4: Autodesk Forma/Revit 클라우드 연결**
- 관련 신호: 2번, 12번, 14번, 17번, 18번
- 판단: Add-in 결과물 export 형식과 Autodesk Store 문구를 점검한다.
- 이유: Autodesk가 Forma 중심 AECO 클라우드와 Revit 연결을 강화할수록 Add-in은 단독 버튼 기능보다 데이터 내보내기와 협업 흐름이 중요해진다.

**승격/관찰 후보 5: 로봇·현장 자동화**
- 관련 신호: 8번, 10번
- 판단: 직접 상품화는 Watch 유지, 스마트시공 교육 사례로만 활용한다.
- 이유: 현장 로봇은 BIM의 대체재가 아니라 as-built 현장 상태를 BIM/디지털트윈과 정렬하는 데이터 수집 계층으로 보는 것이 적합하다.

**승격/관찰 후보 6: 넷제로·친환경 BIM 데이터**
- 관련 신호: 7번
- 판단: 납품검수 파라미터 후보로 보관하고 반복 노출 시 제안서 고급 옵션으로 승격한다.
- 이유: 친환경 건축은 인증 문구가 아니라 재료·수량·열성능·탄소계수 데이터 관리 문제로 바뀌고 있다.


## 2026-06-04 뉴스 트렌드 자동 전략 승격 판단
- Source: `obsidian_vaults/lua_bim_lab_global_map/NAS_Knowledge/2026-06-04 뉴스 트렌드 18항목 지식 업데이트.md`
- Tags: ax,strategy-review,auto-deepening,news-trend

**승격/관찰 후보 1: OpenBIM 검증형 납품**
- 관련 신호: 1번, 4번, 5번, 6번
- 판단: Model Quality Auditor 장기 백로그로 승격하고 ifctester/IDS PoC 후보를 만든다.
- 이유: OpenBIM은 파일 교환을 넘어 IDS 요구사항, BCF 이슈 추적, 검증 서비스, 소프트웨어 인증까지 포함하는 납품 계약 언어로 이동한다.

**승격/관찰 후보 2: Python-Dynamo-Grasshopper-Revit API 자동화 교육**
- 관련 신호: 2번, 3번, 4번, 6번, 7번, 8번, 9번, 10번
- 판단: Starter/PM 교육 상품에 장비표, 파라미터, 시트/뷰 자동화 실습을 추가한다.
- 이유: AEC 자동화는 전문 개발자만의 영역이 아니라 실무자가 반복 업무를 줄이는 단계형 역량으로 바뀌고 있다.

**승격/관찰 후보 3: 국내 건설 AX 생태계**
- 관련 신호: 2번, 3번, 4번, 6번, 7번, 8번, 9번, 10번
- 판단: 국내 AX 기업/기술 카테고리 표와 파트너십 후보 분류를 생성한다.
- 이유: 국내 건설 AI는 설계 자동화, 원가·견적·공정관리, 응용솔루션으로 분화되는 단계에 들어섰다.

**승격/관찰 후보 4: Autodesk Forma/Revit 클라우드 연결**
- 관련 신호: 2번, 9번, 14번, 18번
- 판단: Add-in 결과물 export 형식과 Autodesk Store 문구를 점검한다.
- 이유: Autodesk가 Forma 중심 AECO 클라우드와 Revit 연결을 강화할수록 Add-in은 단독 버튼 기능보다 데이터 내보내기와 협업 흐름이 중요해진다.

**승격/관찰 후보 5: 로봇·현장 자동화**
- 관련 신호: 10번, 11번, 12번, 13번
- 판단: 직접 상품화는 Watch 유지, 스마트시공 교육 사례로만 활용한다.
- 이유: 현장 로봇은 BIM의 대체재가 아니라 as-built 현장 상태를 BIM/디지털트윈과 정렬하는 데이터 수집 계층으로 보는 것이 적합하다.


## 2026-06-04 Autodesk 공식 기술 신호 전략 반영
- Source: `docs/knowledge_updates/daily/2026-06-04_LUA_BIM_LABS_OFFICIAL_AUTODESK_SIGNAL_UPDATE.md`
- Tags: ax,strategy-review,autodesk,aps,revit

Autodesk 공식 Revit 2026 문서와 APS 공식 블로그 기준으로, LUA BIM LABS의 Add-in 전략은 단독 Revit 버튼 기능에서 ACC/APS 데이터 연동, 보안 계정 운영, 비용 예측 가능한 API 사용 구조로 확장될 필요가 있다.

전략 판단:
- Revit 2026 호환성은 Store 문구보다 QA 증빙이 먼저다.
- APS AEC Data Model API는 납품 검수, Model Quality Auditor, BIM Command Center의 장기 데이터 계층 후보로 둔다.
- Secure Service Accounts는 고객 계정·토큰 보안을 강화하는 운영 기준 후보로 반영한다.
- APS 과금 전환은 MVP 기능 범위와 고객 과금 구조에 직접 영향을 주므로 `Watch` 상태로 둔다.

다음 액션:
- APS 데이터 연동은 읽기 전용 PoC부터 시작한다.
- 보안 계정과 토큰 운영 기준은 `라이선스_보안관`과 연결한다.
- 비용 영향은 `CFO`, `라이선스결제`, `제품패키징`에서 재검토한다.

관련: [[Revit_Addin]] · [[ACC BIM360 CDE 지식 베이스]] · [[라이선스_보안관]] · [[제품패키징]]


## 2026-06-05 뉴스 트렌드 자동 전략 승격 판단
- Source: `obsidian_vaults/lua_bim_lab_global_map/NAS_Knowledge/2026-06-05 뉴스 트렌드 18항목 지식 업데이트.md`
- Tags: ax,strategy-review,auto-deepening,news-trend

**승격/관찰 후보 1: OpenBIM 검증형 납품**
- 관련 신호: 1번, 4번, 5번, 6번
- 판단: Model Quality Auditor 장기 백로그로 승격하고 ifctester/IDS PoC 후보를 만든다.
- 이유: OpenBIM은 파일 교환을 넘어 IDS 요구사항, BCF 이슈 추적, 검증 서비스, 소프트웨어 인증까지 포함하는 납품 계약 언어로 이동한다.

**승격/관찰 후보 2: Python-Dynamo-Grasshopper-Revit API 자동화 교육**
- 관련 신호: 2번, 3번, 4번, 6번, 7번, 8번, 9번, 11번
- 판단: Starter/PM 교육 상품에 장비표, 파라미터, 시트/뷰 자동화 실습을 추가한다.
- 이유: AEC 자동화는 전문 개발자만의 영역이 아니라 실무자가 반복 업무를 줄이는 단계형 역량으로 바뀌고 있다.

**승격/관찰 후보 3: 국내 건설 AX 생태계**
- 관련 신호: 2번, 3번, 4번, 6번, 7번, 8번, 9번, 11번
- 판단: 국내 AX 기업/기술 카테고리 표와 파트너십 후보 분류를 생성한다.
- 이유: 국내 건설 AI는 설계 자동화, 원가·견적·공정관리, 응용솔루션으로 분화되는 단계에 들어섰다.

**승격/관찰 후보 4: Autodesk Forma/Revit 클라우드 연결**
- 관련 신호: 9번, 10번, 13번, 16번
- 판단: Add-in 결과물 export 형식과 Autodesk Store 문구를 점검한다.
- 이유: Autodesk가 Forma 중심 AECO 클라우드와 Revit 연결을 강화할수록 Add-in은 단독 버튼 기능보다 데이터 내보내기와 협업 흐름이 중요해진다.

**승격/관찰 후보 5: 로봇·현장 자동화**
- 관련 신호: 11번, 12번
- 판단: 직접 상품화는 Watch 유지, 스마트시공 교육 사례로만 활용한다.
- 이유: 현장 로봇은 BIM의 대체재가 아니라 as-built 현장 상태를 BIM/디지털트윈과 정렬하는 데이터 수집 계층으로 보는 것이 적합하다.


## 2026-06-05 주간 AX 전략 리뷰
- Source: `docs/knowledge_updates/weekly/2026-W23_AX_STRATEGY_REVIEW.md`
- Tags: ax,weekly-review,strategy,bim

분류 요약: AX 전략 신호 164, Model Quality Auditor 74, OpenBIM/납품검증 53, 시공 BIM/스마트건설 51, BIM 자동화/Add-in 15, 교육/확산 10

운영 판단: 상위 반복 신호는 CSO, 제품패키징, Model Quality Auditor, 교육컨설팅 지식으로 연결한다.
