#!/bin/zsh
set -euo pipefail

PROJECT_DIR="/Users/choejeong-yeon/LUA BIM LABS"
LOG_DIR="$PROJECT_DIR/logs"
REPORT_DIR="$PROJECT_DIR/docs/knowledge_updates/daily"
LOG_FILE="$LOG_DIR/daily_knowledge_update.log"
TODAY="$(date '+%Y-%m-%d')"
NOW="$(date '+%Y-%m-%d %H:%M:%S')"
REPORT_FILE="$REPORT_DIR/${TODAY}_DAILY_KNOWLEDGE_UPDATE.md"
PYTHON="$PROJECT_DIR/.dev-venv/bin/python"

mkdir -p "$LOG_DIR" "$REPORT_DIR"

# 오늘 이미 실행 완료했으면 스킵 (LaunchAgent 다중 실행 방지)
DONE_MARKER="$LOG_DIR/.daily_knowledge_update_done_${TODAY}"
if [[ -f "$DONE_MARKER" ]]; then
  echo "[$NOW] 오늘 이미 완료됨 — 스킵" >> "$LOG_FILE"
  exit 0
fi

{
  echo "==== $NOW daily knowledge update start ===="
  cd "$PROJECT_DIR"

  if [[ ! -x "$PYTHON" ]]; then
    echo "ERROR: Python virtualenv not found at $PYTHON"
    exit 1
  fi

  MD_COUNT="$(find . -name '*.md' \
    -not -path './.dev-venv/*' \
    -not -path './obsidian_vaults/lua_bim_lab_global_map/*' \
    -not -path './dist/*' \
    -not -path './node_modules/*' | wc -l | tr -d ' ')"

  ERROR_COUNT="$(find obsidian_vaults/model_quality_auditor/03_Errors_Fixes -name 'ERR-*.md' 2>/dev/null | wc -l | tr -d ' ')"
  DECISION_COUNT="$(find obsidian_vaults/model_quality_auditor/04_Decisions -name 'DEC-*.md' 2>/dev/null | wc -l | tr -d ' ')"
  GATE_COUNT="$(find obsidian_vaults/model_quality_auditor/05_Revit_API_Gates -name 'GATE-*.md' 2>/dev/null | wc -l | tr -d ' ')"
  TEAM_QA_COUNT="$(find obsidian_vaults/lua_bim_lab_global_map/NAS_Knowledge/Team_Telegram_QA -name 'QA - *.md' 2>/dev/null | wc -l | tr -d ' ')"

  cat > "$REPORT_FILE" <<EOF
---
type: daily-knowledge-update
date: $TODAY
status: generated
tags:
  - knowledge-update
  - obsidian
  - daily-routine
---

# $TODAY Daily Knowledge Update

생성 시각: $NOW

## 업데이트 범위

| 항목 | 수량 |
|---|---:|
| 원본 Markdown 문서 | $MD_COUNT |
| MQA 오류 오답노트 | $ERROR_COUNT |
| MQA 의사결정 기록 | $DECISION_COUNT |
| MQA Revit API 게이트 | $GATE_COUNT |
| 팀원 Telegram Q&A 지식 노트 | $TEAM_QA_COUNT |

## 자동 갱신 작업

- [x] 일일 지식 업데이트 리포트 생성
- [x] Model Quality Auditor Obsidian 그래프 갱신
- [x] LUA BIM LAB 전역 Obsidian 지식맵 갱신

## 오늘 점검할 항목

- [ ] 신규 문서가 외부 공개 가능 문서인지 내부 전용 문서인지 분류한다.
- [ ] 오류 오답노트에 원인, 수정, 검증, 재발 방지가 모두 채워졌는지 확인한다.
- [ ] 반복 오류가 있으면 [[Lessons Learned Matrix]]에 승격한다.
- [ ] 고객/외부 공개 가능 문서에 내부 경로, 토큰, 개인정보, 미검증 기능 문구가 없는지 확인한다.
- [ ] 교육자료, 상품문서, 개발기록 사이에 연결해야 할 문서가 있는지 확인한다.
- [ ] 팀원 Telegram Q&A 중 반복 질문, 부족한 답변, 표준화 후보를 확인한다.

## 회사 목적성 큐레이션

다음 기준에 해당하는 정보는 유지/승격 후보로 분류한다.

- [ ] MEP BIM 실무 품질 향상에 기여하는 정보
- [ ] Model Quality Auditor 또는 Autodesk Add-in Store 상품화와 연결되는 정보
- [ ] 신규/연차별 BIM 교육 커리큘럼에 재사용 가능한 정보
- [ ] 설계, 시공, 납품, 품질검토의 반복 업무를 줄이는 정보
- [ ] AI와 자동화를 통해 생산성을 높이는 정보
- [ ] 고객에게 설명 가능한 공식 문서 또는 리포트로 전환 가능한 정보
- [ ] 내부 보안, 계약, 운영 리스크를 낮추는 정보

## 승격 후보

| 후보 | 승격 대상 | 담당 | 상태 |
|---|---|---|---|
|  | 표준문서 / 교육자료 / 상품자료 / QA 체크리스트 / 오류 오답노트 | 지식큐레이터 | review |

## 보류 또는 아카이브 후보

| 후보 | 사유 | 조치 |
|---|---|---|
|  | 회사 목적성과 낮은 관련성 / 중복 / 미검증 / 보안 리스크 | 보류 |

## 연결

- [[Global Knowledge Map]]
- [[Model Quality Auditor - Knowledge Map]]
- [[Error Fix Index]]
- [[Lessons Learned Matrix]]
- [[15_KNOWLEDGE_DOCUMENT_REPOSITORY_POLICY]]
- [[21_KNOWLEDGE_CURATION_INTELLIGENCE_CELL]]
- [[인프라_DevOpsObsidian]]
EOF

  "$PYTHON" -m py_compile scripts/mqa_obsidian_tools.py scripts/build_global_obsidian_map.py
  "$PYTHON" -m py_compile scripts/daily_industry_briefing.py scripts/daily_knowledge_curation.py
  "$PYTHON" scripts/daily_industry_briefing.py
  "$PYTHON" scripts/daily_knowledge_curation.py --days 2 --date "$TODAY"

  # KB 파일 자동 성장 (오늘 업데이트 안 된 파일만 처리)
  echo "==== $(date '+%H:%M:%S') KB auto-enrich start ===="
  "$PYTHON" scripts/auto_enrich_knowledge_base.py
  echo "==== $(date '+%H:%M:%S') KB auto-enrich done ===="

  "$PYTHON" scripts/mqa_obsidian_tools.py graph
  "$PYTHON" scripts/build_global_obsidian_map.py

  echo "report=$REPORT_FILE"
  echo "==== $(date '+%Y-%m-%d %H:%M:%S') daily knowledge update done ===="
} >> "$LOG_FILE" 2>&1

# 완료 마커 생성 (오늘 중복 실행 방지)
touch "$DONE_MARKER"
# 이전 날짜 마커 정리 (7일 이상 된 것)
find "$LOG_DIR" -name ".daily_knowledge_update_done_*" -mtime +7 -delete 2>/dev/null || true
