from __future__ import annotations

import datetime
import os
from pathlib import Path

from backend.core.paths import (
    AGENT_KB_DIR,
    AGENT_KB_LAYOUT,
    DATA_DIR,
    EXTRA_AGENTS_DIR_NAME,
    PROJECT_ROOT,
    QA_KB_DIR,
    TEAM_DIR_NAMES,
)
from backend import agent_registry as _registry
from backend.models import KnowledgeUpdateRequest

# ---------------------------------------------------------------------------
# 에이전트 정체성은 config/organization.json (SSOT) 에서 파생한다.
# 과거 이 모듈에 하드코딩돼 흩어져 있던 리터럴(ORGANIZATION, DISCIPLINE_KEYWORDS,
# EXTRA_KNOWLEDGE_AGENTS, DEFAULT_KNOWLEDGE, AGENT_TEAM_DIR 등)은 이제 모두
# backend/agent_registry.py 가 재구성한다. 에이전트 추가/세분화는 config 만 편집.
# 값·순서 동일성은 tests/test_registry_matches_legacy.py 가 보증한다.
# ---------------------------------------------------------------------------
ORGANIZATION = dict(_registry.organization())
ALL_AGENTS = _registry.all_agents()
DISCIPLINE_GROUPS = dict(_registry.discipline_groups())
DISCIPLINE_KEYWORDS = dict(_registry.discipline_keywords())

KNOWLEDGE_DIR = str(AGENT_KB_DIR)
QA_KNOWLEDGE_DIR = str(QA_KB_DIR)

EXTRA_KNOWLEDGE_AGENTS = _registry.extra_knowledge_agents()
KNOWLEDGE_AGENTS = _registry.knowledge_agents()
DEFAULT_KNOWLEDGE = dict(_registry.default_knowledge())

# 에이전트 → knowledge/10_agents/ 하위 팀 폴더명 (teams 레이아웃 전용)
AGENT_TEAM_DIR = _registry.agent_team_dir()


def agent_kb_dir(agent: str) -> str:
    """레이아웃에 따른 에이전트 KB 파일의 디렉토리를 반환."""
    if AGENT_KB_LAYOUT == "teams":
        return os.path.join(KNOWLEDGE_DIR, AGENT_TEAM_DIR.get(agent, EXTRA_AGENTS_DIR_NAME))
    return KNOWLEDGE_DIR


def knowledge_file_path(agent: str) -> str:
    safe_name = "".join(ch for ch in agent if ch.isalnum() or ch in ("_", "-"))
    return os.path.join(agent_kb_dir(agent), f"{safe_name}.md")


def qa_knowledge_file_path(agent: str) -> str:
    safe_name = "".join(ch for ch in agent if ch.isalnum() or ch in ("_", "-"))
    return os.path.join(QA_KNOWLEDGE_DIR, f"{safe_name}_QA.md")


def ensure_knowledge_base() -> None:
    os.makedirs(KNOWLEDGE_DIR, exist_ok=True)
    os.makedirs(QA_KNOWLEDGE_DIR, exist_ok=True)
    for agent, seed in DEFAULT_KNOWLEDGE.items():
        path = knowledge_file_path(agent)
        os.makedirs(os.path.dirname(path), exist_ok=True)
        if not os.path.exists(path):
            with open(path, "w", encoding="utf-8") as kb_file:
                kb_file.write(f"# {agent} 지식 베이스\n\n## 초기 기준\n{seed}\n")


def _is_qa_update(source: str, tags: str) -> bool:
    src = source.lower()
    tag_set = {tag.strip() for tag in tags.lower().split(",")}
    if "manual-knowledge" in tag_set:
        return False
    return (
        src.startswith("telegram-auto")
        or src.startswith("system-auto")
        or src == "telegram-qa"
        or "auto-collect" in tag_set
        or "needs-review" in tag_set
    )


def _extract_content_fingerprints(content: str) -> set[str]:
    fingerprints: set[str] = set()
    for line in content.splitlines():
        line = line.strip()
        if len(line) < 20:
            continue
        if any(marker in line for marker in ("http", "https", "[link]", "| ")):
            fingerprints.add(line[:120].lower())
        elif line.startswith("- ") and len(line) > 30:
            fingerprints.add(line[:120].lower())
    return fingerprints


import re as _re
_CHINESE_RE = _re.compile(r"[一-鿿]{3,}")
_CHAT_TOKEN_RE = _re.compile(r"<\|im_start\|[^|]*\|>|<\|im_end\|>|<\|endoftext\|>")


def _has_contamination(text: str) -> bool:
    return bool(_CHINESE_RE.search(text) or _CHAT_TOKEN_RE.search(text))


def _is_duplicate_content(new_content: str, existing_text: str, threshold: float = 0.5) -> bool:
    new_fps = _extract_content_fingerprints(new_content)
    if not new_fps:
        return False
    existing_lower = existing_text.lower()
    matched = sum(1 for fp in new_fps if fp in existing_lower)
    return (matched / len(new_fps)) >= threshold


def append_knowledge_update(update: KnowledgeUpdateRequest) -> dict:
    if update.agent not in KNOWLEDGE_AGENTS:
        raise ValueError(f"지원하지 않는 지식 에이전트입니다: {update.agent}")
    if not update.content.strip():
        raise ValueError("지식 업데이트 내용이 비어 있습니다.")

    ensure_knowledge_base()
    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    path = qa_knowledge_file_path(update.agent) if _is_qa_update(update.source, update.tags) else knowledge_file_path(update.agent)

    if _has_contamination(update.content):
        return {"agent": update.agent, "path": path, "updated_at": now, "skipped": True, "reason": "contaminated"}

    try:
        existing_text = Path(path).read_text(encoding="utf-8") if Path(path).exists() else ""
        if existing_text and _is_duplicate_content(update.content, existing_text):
            return {"agent": update.agent, "path": path, "updated_at": now, "skipped": True, "reason": "duplicate"}
    except Exception:
        pass

    entry = (
        f"\n\n## {update.title.strip()} ({now})\n"
        f"- Source: {update.source.strip() or 'manual'}\n"
        f"- Tags: {update.tags.strip() or '-'}\n\n"
        f"{update.content.strip()}\n"
    )
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "a", encoding="utf-8") as kb_file:
        kb_file.write(entry)
    return {"agent": update.agent, "path": path, "updated_at": now, "skipped": False}
