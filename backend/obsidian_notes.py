"""
SECTION 5 ── Obsidian 노트 · QA 아카이브 · 팀 요청 로그
  - append_team_request_log : Telegram 지식 요청을 마크다운 로그에 추가
  - save_team_qa_to_obsidian : 팀원 QA 노트 생성 + MOC 갱신
  - save_revit_qa_to_obsidian : Revit Assistant QA 노트 생성 + MOC 갱신
  - build_revit_context_prompt / build_revit_assistant_answer : 응답 문자열 빌더
  - append_team_qa_feedback : 피드백 블록 추가 및 status 갱신
  - ensure/rebuild *_qa_moc : MOC 파일 초기화 · 재구성
"""
from __future__ import annotations

import datetime
import re
from pathlib import Path

from telegram import Update

from backend.core.paths import (
    GLOBAL_OBSIDIAN_VAULT as _GLOBAL_OBSIDIAN_VAULT,
    PROJECT_ROOT as _PROJECT_ROOT,
    TEAM_REQUESTS_DIR as _TEAM_REQUESTS_DIR,
)
from backend.models import RevitAssistantChatRequest
from backend.text_utils import sanitize_outbound_text, telegram_user_label

TEAM_REQUEST_LOG = _TEAM_REQUESTS_DIR / "telegram_knowledge_requests.md"
TEAM_QA_OBSIDIAN_DIR = _GLOBAL_OBSIDIAN_VAULT / "NAS_Knowledge" / "Team_Telegram_QA"
TEAM_QA_MOC = TEAM_QA_OBSIDIAN_DIR / "MOC - Team Telegram QA.md"
REVIT_QA_OBSIDIAN_DIR = _GLOBAL_OBSIDIAN_VAULT / "NAS_Knowledge" / "Revit_Assistant_QA"
REVIT_QA_MOC = REVIT_QA_OBSIDIAN_DIR / "MOC - Revit Assistant QA.md"


# ── 팀 요청 로그 ──────────────────────────────────────────────────────────────────

def append_team_request_log(
    *, update: Update, query: str, action: str, agent: str, result: str
) -> None:
    TEAM_REQUEST_LOG.parent.mkdir(parents=True, exist_ok=True)
    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    entry = (
        f"\n\n## Telegram 지식 요청 - {action} ({now})\n"
        f"- Requester: {telegram_user_label(update)}\n"
        f"- Chat ID: {update.effective_chat.id if update.effective_chat else '-'}\n"
        f"- Agent: {agent}\n"
        f"- Tags: telegram,team-request,knowledge-loop,{action}\n\n"
        f"### 질문\n{query.strip()}\n\n"
        f"### 처리 결과\n{result.strip()}\n"
    )
    with open(TEAM_REQUEST_LOG, "a", encoding="utf-8") as log_file:
        log_file.write(entry)


# ── 슬러그 · 도메인 추론 ───────────────────────────────────────────────────────────

def slugify_obsidian_title(text: str, fallback: str = "telegram_qa") -> str:
    slug = re.sub(r"[^\w\s가-힣-]", "", text or "")
    slug = re.sub(r"\s+", "_", slug.strip())
    return (slug[:64] or fallback).strip("_")


def infer_qa_domain(query: str, agent: str) -> str:
    lower = query.lower()
    if any(kw in lower for kw in ["revit", "패밀리", "family", "뷰", "시트", "add-in", "addin"]):
        return "Revit"
    if any(kw in lower for kw in ["navisworks", "간섭", "clash"]):
        return "Navisworks"
    if any(kw in lower for kw in ["엑셀", "excel", "xlsx", "자동화", "qwen", "코드", "개발"]):
        return "개발기술"
    if any(kw in lower for kw in ["교육", "커리큘럼", "온보딩", "연차"]):
        return "조직운영"
    if agent in {"공조배관", "공조덕트", "소방기계", "소방전기", "전기", "통신", "위생"}:
        return "MEP"
    return "BIM실무"


# ── 팀 QA MOC ────────────────────────────────────────────────────────────────────

def ensure_team_qa_moc() -> None:
    TEAM_QA_OBSIDIAN_DIR.mkdir(parents=True, exist_ok=True)
    if TEAM_QA_MOC.exists():
        return
    TEAM_QA_MOC.write_text(
        """# MOC - Team Telegram QA

팀원과 LUA BIM LABS Telegram 봇이 주고받은 질문/답변을 조직 지식으로 축적하는 인덱스다.

## 목적

- 반복 질문을 교육자료, FAQ, 표준문서 후보로 승격한다.
- 부족한 답변은 지식 공백으로 표시하고 보강 작업에 연결한다.
- 개인정보, 고객명, 프로젝트명, 계약정보는 Obsidian 지식 노트에 남기지 않는다.

## Q&A Index

<!-- team-qa-index:start -->
<!-- team-qa-index:end -->

## 연결

- [[Global Knowledge Map]]
- [[21_KNOWLEDGE_CURATION_INTELLIGENCE_CELL]]
- [[24_TEAM_TELEGRAM_KNOWLEDGE_REQUEST_LOOP]]
""",
        encoding="utf-8",
    )


def rebuild_team_qa_moc() -> None:
    ensure_team_qa_moc()
    notes = sorted(TEAM_QA_OBSIDIAN_DIR.glob("QA - *.md"))
    lines = []
    for note in notes:
        title = note.stem
        try:
            text = note.read_text(encoding="utf-8", errors="ignore")
        except OSError:
            text = ""
        status_match = re.search(r"^status:\s*(.+)$", text, re.MULTILINE)
        domain_match = re.search(r"^domain:\s*(.+)$", text, re.MULTILINE)
        status = status_match.group(1).strip() if status_match else "captured"
        domain = domain_match.group(1).strip() if domain_match else "BIM실무"
        lines.append(f"- [[{title}]] · `{domain}` · `{status}`")
    moc = TEAM_QA_MOC.read_text(encoding="utf-8")
    block = "\n".join(lines) if lines else "_아직 기록된 팀원 Q&A가 없습니다._"
    moc = re.sub(
        r"<!-- team-qa-index:start -->.*?<!-- team-qa-index:end -->",
        f"<!-- team-qa-index:start -->\n{block}\n<!-- team-qa-index:end -->",
        moc,
        flags=re.DOTALL,
    )
    TEAM_QA_MOC.write_text(moc, encoding="utf-8")


def save_team_qa_to_obsidian(
    *, update: Update, query: str, answer: str, agent: str, matches: list[dict]
) -> Path:
    ensure_team_qa_moc()
    now = datetime.datetime.now()
    date = now.strftime("%Y-%m-%d")
    stamp = now.strftime("%Y%m%d-%H%M%S")
    title = slugify_obsidian_title(query)
    path = TEAM_QA_OBSIDIAN_DIR / f"QA - {stamp} - {title}.md"
    domain = infer_qa_domain(query, agent)
    requester = sanitize_outbound_text(telegram_user_label(update))
    safe_query = sanitize_outbound_text(query.strip())
    safe_answer = sanitize_outbound_text(answer.strip())
    source_lines = []
    for match in matches[:5]:
        match_path = match.get("path")
        if isinstance(match_path, Path):
            try:
                rel = match_path.relative_to(_PROJECT_ROOT).as_posix()
            except ValueError:
                rel = match_path.as_posix()
        else:
            rel = str(match_path)
        source_lines.append(f"- `{rel}` · score `{match.get('score', '-')}`")
    if not source_lines:
        source_lines.append("- 기존 Obsidian 지식에서 충분한 근거를 찾지 못함")
    content = f"""---
type: team-telegram-qa
category: 팀원간질문
domain: {domain}
agent: {agent}
date: {date}
status: answered-pending-feedback
tags:
  - QA
  - team-telegram
  - knowledge-loop
  - {domain}
---

# QA - {query[:80].strip()}

## 질문

> 요청자: {requester}
> 수집일: {now.strftime("%Y-%m-%d %H:%M:%S")}
> 담당 지식: [[{agent}]]

{safe_query}

## 답변

{safe_answer}

## 근거 문서

{chr(10).join(source_lines)}

## 지식화 판단

- [ ] 반복 질문 여부 확인
- [ ] 표준문서/교육자료/FAQ 승격 필요 여부 확인
- [ ] 답변 부족 시 지식 공백으로 전환
- [ ] 개인정보, 고객명, 프로젝트명, 계약정보 제거 확인

## 연결

- [[MOC - Team Telegram QA]]
- [[MOC - QA Index]]
- [[24_TEAM_TELEGRAM_KNOWLEDGE_REQUEST_LOOP]]
- [[21_KNOWLEDGE_CURATION_INTELLIGENCE_CELL]]
- [[Global Knowledge Map]]
"""
    path.write_text(content, encoding="utf-8")
    rebuild_team_qa_moc()
    return path


def append_team_qa_feedback(
    note_path: str | None, feedback_type: str, feedback: str
) -> None:
    if not note_path:
        return
    path = Path(note_path)
    if not path.exists() or not path.is_file():
        return
    safe_feedback = sanitize_outbound_text(feedback.strip())
    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    block = (
        f"\n\n## 피드백 - {feedback_type} ({now})\n\n"
        f"{safe_feedback}\n"
    )
    text = path.read_text(encoding="utf-8")
    if feedback_type == "충분":
        text = re.sub(r"^status:\s*.+$", "status: verified-by-requester", text, count=1, flags=re.MULTILINE)
    elif feedback_type == "보강요청":
        text = re.sub(r"^status:\s*.+$", "status: knowledge-gap-needs-review", text, count=1, flags=re.MULTILINE)
    path.write_text(text + block, encoding="utf-8")
    rebuild_team_qa_moc()


# ── Revit Assistant QA MOC ────────────────────────────────────────────────────────

def ensure_revit_qa_moc() -> None:
    REVIT_QA_OBSIDIAN_DIR.mkdir(parents=True, exist_ok=True)
    if REVIT_QA_MOC.exists():
        return
    REVIT_QA_MOC.write_text(
        """# MOC - Revit Assistant QA

Revit Add-in 안에서 발생한 Revit, Dynamo, 설비, BIM 질문/답변을 LUA BIM LABS 조직 지식으로 축적하는 인덱스다.

## 목적

- Revit 사용 중 나온 실무 질문을 지식 베이스와 연결한다.
- Dynamo/Revit API/MEP BIM 질문을 FAQ, 교육자료, Add-in 기능 후보로 승격한다.
- 모델명, 파일 경로, 고객명, 담당자명 등 민감 정보는 저장 전에 제거한다.

## Q&A Index

<!-- revit-qa-index:start -->
<!-- revit-qa-index:end -->

## 연결

- [[Global Knowledge Map]]
- [[MOC - AI Knowledge Base]]
- [[Revit_Addin]]
- [[설비기초]]
- [[설비도면해석]]
- [[설비시공조율]]
""",
        encoding="utf-8",
    )


def rebuild_revit_qa_moc() -> None:
    ensure_revit_qa_moc()
    notes = sorted(REVIT_QA_OBSIDIAN_DIR.glob("QA - *.md"))
    lines = []
    for note in notes:
        title = note.stem
        try:
            text = note.read_text(encoding="utf-8", errors="ignore")
        except OSError:
            text = ""
        status_match = re.search(r"^status:\s*(.+)$", text, re.MULTILINE)
        domain_match = re.search(r"^domain:\s*(.+)$", text, re.MULTILINE)
        status = status_match.group(1).strip() if status_match else "captured"
        domain = domain_match.group(1).strip() if domain_match else "Revit"
        lines.append(f"- [[{title}]] · `{domain}` · `{status}`")
    moc = REVIT_QA_MOC.read_text(encoding="utf-8")
    block = "\n".join(lines) if lines else "_아직 기록된 Revit Assistant Q&A가 없습니다._"
    moc = re.sub(
        r"<!-- revit-qa-index:start -->.*?<!-- revit-qa-index:end -->",
        f"<!-- revit-qa-index:start -->\n{block}\n<!-- revit-qa-index:end -->",
        moc,
        flags=re.DOTALL,
    )
    REVIT_QA_MOC.write_text(moc, encoding="utf-8")


def build_revit_context_prompt(message: str, revit_context: str) -> str:
    context = sanitize_outbound_text((revit_context or "").strip())
    if not context:
        return message.strip()
    return (
        f"{message.strip()}\n\n"
        "[Revit 선택 요소 컨텍스트]\n"
        f"{context[:1200]}"
    )


def build_revit_assistant_answer(query: str, matches: list[dict], agent: str) -> str:
    if not matches:
        return sanitize_outbound_text(
            "LUA BIM LABS 기준 답변\n\n"
            "현재 Obsidian/지식 베이스에서 충분히 일치하는 근거를 찾지 못했습니다.\n\n"
            "다음처럼 질문을 조금 더 구체화하면 답변 품질이 좋아집니다.\n"
            "- Revit 기능 질문: 사용 중인 기능, 오류 메시지, 원하는 결과\n"
            "- 설비 질문: 공종, 계통, 장비/배관/덕트 종류, 도면 또는 모델 상황\n"
            "- Dynamo 질문: 입력 데이터, 원하는 출력, 사용 중인 노드 또는 Python 여부\n\n"
            "이 질문은 지식 공백 후보로 기록할 수 있습니다."
        )
    source_lines = []
    excerpts = []
    for match in matches[:4]:
        try:
            rel_path = match["path"].relative_to(_PROJECT_ROOT)
        except ValueError:
            rel_path = match["path"]
        source_lines.append(f"- {rel_path} (score {match['score']})")
        if not excerpts:
            excerpts.append(match["excerpt"])
    return sanitize_outbound_text(
        "LUA BIM LABS 기준 답변\n\n"
        f"담당 지식: {agent}\n\n"
        f"{chr(10).join(excerpts)}\n\n"
        "Revit/Dynamo/설비 실무 적용 시 확인할 점:\n"
        "- 모델에서 확인 가능한 정보와 설계자/현장 기준으로 확정해야 할 정보를 분리하세요.\n"
        "- 선택 요소가 있다면 카테고리, 계통명, 타입명, 레벨, 주요 치수를 함께 확인하세요.\n"
        "- 법규, 제조사 수치, 과업별 기준은 확정 답변 전에 기준서를 확인해야 합니다.\n\n"
        "근거 문서:\n"
        + "\n".join(source_lines)
    )[:3600]


def save_revit_qa_to_obsidian(
    *,
    request: RevitAssistantChatRequest,
    answer: str,
    agent: str,
    matches: list[dict],
    search_result: str = "",
    source_tag: str = "",
    top_score: int = 0,
) -> Path:
    ensure_revit_qa_moc()
    now = datetime.datetime.now()
    date = now.strftime("%Y-%m-%d")
    stamp = now.strftime("%Y%m%d-%H%M%S")
    title = slugify_obsidian_title(request.message, fallback="revit_assistant_qa")
    path = REVIT_QA_OBSIDIAN_DIR / f"QA - {stamp} - {title}.md"
    domain = infer_qa_domain(request.message, agent)
    safe_user_id = sanitize_outbound_text(request.user_id.strip() or "revit_user")
    safe_query = sanitize_outbound_text(request.message.strip())
    safe_context = sanitize_outbound_text(request.revit_context.strip())
    safe_answer = sanitize_outbound_text(answer.strip())
    safe_search_result = sanitize_outbound_text(search_result.strip())
    is_search_assisted = bool(safe_search_result)
    status = "search-assisted-needs-review" if is_search_assisted else "answered-pending-feedback"
    source_mode = "search-assisted" if is_search_assisted else "local-knowledge"
    source_lines = []
    for match in matches[:5]:
        match_path = match.get("path")
        if isinstance(match_path, Path):
            try:
                rel = match_path.relative_to(_PROJECT_ROOT).as_posix()
            except ValueError:
                rel = match_path.as_posix()
        else:
            rel = str(match_path)
        source_lines.append(f"- `{rel}` · score `{match.get('score', '-')}`")
    if not source_lines:
        source_lines.append("- 기존 Obsidian 지식에서 충분한 근거를 찾지 못함")
    content = f"""---
type: revit-assistant-qa
category: RevitAddin질문
domain: {domain}
agent: {agent}
date: {date}
status: {status}
source_mode: {source_mode}
top_score: {top_score}
source_tag: "{sanitize_outbound_text(source_tag)}"
tags:
  - QA
  - revit-assistant
  - knowledge-loop
  - {source_mode}
  - {domain}
---

# QA - {request.message[:80].strip()}

## 질문

> 요청자: {safe_user_id}
> 수집일: {now.strftime("%Y-%m-%d %H:%M:%S")}
> 클라이언트: {sanitize_outbound_text(request.client_version)}
> 담당 지식: [[{agent}]]

{safe_query}

## Revit 선택 컨텍스트

```text
{safe_context or "선택 요소 없음"}
```

## 답변

{safe_answer}

## 근거 문서

{chr(10).join(source_lines)}

## 검색 보강 원문

```text
{safe_search_result or "검색 보강 없음"}
```

## 지식화 판단

- [ ] 검색 출처 신뢰도 확인
- [ ] 반복 질문 여부 확인
- [ ] Revit/Dynamo FAQ 승격 필요 여부 확인
- [ ] MEP 교육자료 또는 표준문서 전환 가능 여부 확인
- [ ] Add-in 기능 후보 여부 확인
- [ ] 모델명, 파일 경로, 고객명, 담당자명 제거 확인

## 연결

- [[MOC - Revit Assistant QA]]
- [[Revit_Addin]]
- [[설비기초]]
- [[설비도면해석]]
- [[설비시공조율]]
- [[Global Knowledge Map]]
"""
    path.write_text(content, encoding="utf-8")
    rebuild_revit_qa_moc()
    return path
