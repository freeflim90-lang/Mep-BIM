# 엑셀자동화 Q&A 지식

텔레그램 질문·자동 수집 응답 저장소 — 기준 가이드라인(엑셀자동화.md)과 분리 운영.

## 2026-06-09 엑셀 자동화 실전 Q&A
- Source: LUA BIM LABS 엑셀 자동화 운영 기준, Python/openpyxl 실무 경험
- Tags: excel,automation,openpyxl,python,report,qa,2026

**Q: 엑셀 자동화 개발에서 가장 흔한 문제는?**
A: ① 인코딩 문제: `openpyxl` 기본 UTF-8이나 한글 윈도우에서 `cp949` 파일 읽기 실패 → `encoding='utf-8-sig'` 또는 `charset_normalizer`로 감지 ② 원본 파일 덮어쓰기: 항상 별도 output 경로에 저장 ③ 빈 셀 처리: `cell.value`가 `None`일 때 처리 누락 ④ 대용량 메모리: 50,000행 이상 → `read_only=True` 모드 ⑤ 날짜/시간 형식: Revit 내보내기 엑셀의 날짜가 숫자로 표시되는 경우 → `openpyxl.utils.datetime` 활용.

**Q: BIM 납품 검수 보고서 자동화 구조는?**
A: 기본 구조: ① 입력: 간섭검토 결과 CSV/XLSX + 설계 기준 파라미터 ② 처리: 간섭 상태별 분류(Critical/Major/Minor) + 공종별 집계 ③ 출력: 요약 시트 + 상세 목록 시트 + 차트 시트. Navisworks Clash Detective 내보내기 파일을 입력으로 받는 경우 필드명이 Navisworks 버전에 따라 다르므로 헤더를 동적으로 읽어야 한다.

**Q: 관리팀 엑셀 자동화 요청 처리 절차는?**
A: 관리팀 엑셀 요청은 반드시 승인 절차를 거친다: ① 요청 접수 → 리스크 분류 (개인정보 포함 여부, 외부 전송 여부) ② CEO/COO 승인 ③ 승인 후 샘플 파일 기반 개발 ④ 결과물 검토 후 배포. 개인정보(급여, 주민번호, 연락처)가 포함된 파일은 외부 API로 보내지 않고 로컬에서만 처리한다.

**Q: Revit 스케줄 데이터를 Excel로 내보내는 자동화는 어떻게 하나요?**
A: 방법 1 (Revit 내보내기): Revit View → Export → Reports → Schedule로 내보낸 TXT를 openpyxl로 파싱. 방법 2 (Dynamo): Dynamo로 스케줄 데이터를 추출해 Excel 저장. 방법 3 (API): Revit API `ViewSchedule.Export()`를 사용한 Add-in. 엑셀자동화 에이전트는 Revit 밖에서 처리하는 방법 1, 2를 우선 제안하고 Add-in이 필요하면 Revit_Addin 에이전트에 인계한다.

**Q: 엑셀 자동화 결과물을 검증하는 방법은?**
A: 검증 항목: ① 입력 행 수 = 출력 행 수 (필터 적용 전) ② 합계/집계 값이 수동 계산과 일치 ③ 특수 문자·줄바꿈 포함 셀 정상 처리 ④ 날짜 형식 일치 ⑤ 파일 열기 오류 없음 (xlsx 파일 무결성). 검증 코드를 자동화 스크립트에 내장해 실행 후 로그로 출력하는 것을 권장한다.
