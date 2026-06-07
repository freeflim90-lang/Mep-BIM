# AI 지식 고도화 Iteration 25 업데이트

날짜: 2026-06-07
루프 회차: Iteration 25
QA 결과: 47/47 (100%)

## 보강 대상

### 1. 엑셀자동화.md — pyRevit·BOQ·S커브 전문 지식 추가
- **pyRevit·Revit API 직접 Excel 연동**: FilteredElementCollector → ViewSchedule → openpyxl 직접 저장 코드, CSV 내보내기 없이 스케줄 직접 추출, xlwings 실시간 연동 패턴
- **한국 공공 건설 내역서 자동화(BOQ)**: 조달청 기준 5단 계층(갑지/원가계산서/집계표/내역서/단가표), openpyxl 자동 생성 코드, 원가계산서 공식(일반관리비 6%/이윤 15%), 나라장터 업로드 주의사항
- **대용량 BIM 데이터 처리**: 행 수별 전략표(~1만/~10만/~100만), write_only 모드 스트리밍, pandas chunksize 패턴
- **공정표·S커브 자동화**: MS Project XML 파싱 → 월별 누적 계획/실적 → openpyxl AreaChart S커브, 공정 지연 조기 경보 이메일

### 2. 설비도면해석.md — KS 기호 표 + BIM 대조 체크리스트 추가
- **설비 공종별 KS 핵심 기호 표**: 배관(게이트/체크/글로브/볼 밸브), 공조(AHU/FCU/SA/RA/FD/SD), 위생(CW/HW/SD), 소방(SP/FR/DS), 전기(실선/파선/비상구) — KS A 0005·KS B 6007·KS C 0015 출처 포함, Revit 패밀리명 대응표
- **공종별 도면 읽기 순서**: 공조·위생·소방·전기 각 4단계 순서 + 핵심 확인 포인트
- **BIM vs 2D 도면 대조 8단계 체크리스트**: 기준층 레벨, 기기 위치, 관경 사이즈, 밸브 위치, 계통 연결, 정비공간, 슬리브, 소방·방화 준수
- **Revit MEP 도면 추출 기준**: View Template Fine/Hidden Line, 스케일 기준, 기기 태그 설정, Revision Cloud 활용법

## 누적 QA 현황

| 회차 | 테스트 수 | 결과 |
|------|---------|------|
| Iteration 21 | 31/31 | ✅ 100% |
| Iteration 22 | 35/35 | ✅ 100% |
| Iteration 23 | 39/39 | ✅ 100% |
| Iteration 24 | 43/43 | ✅ 100% |
| **Iteration 25** | **47/47** | **✅ 100%** |

## 다음 대상 (Iteration 26 예정)
- `FM_자산관리.md` — COBie 자산 등록, FM 데이터 수집 BIM 워크플로우
- `간섭검토.md` — Navisworks 클래시 유형 분류, BIM 클래시 검토 회의 기준
- `BIM_납품검수.md` — 납품 체크리스트 강화

관련: [[엑셀자동화]] · [[설비도면해석]] · [[BIM_납품검수]] · [[4D5D_BIM]]
