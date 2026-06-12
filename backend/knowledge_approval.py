from __future__ import annotations

import datetime as dt
import json
from pathlib import Path
from typing import Any

from backend.core.paths import CURATION_DIR, PROJECT_ROOT
from backend.models import KnowledgeUpdateRequest
from backend.text_utils import sanitize_outbound_text


KNOWLEDGE_APPROVAL_FILE = CURATION_DIR / "knowledge_approval_candidates.json"


def load_knowledge_approval_registry(path: Path = KNOWLEDGE_APPROVAL_FILE) -> dict[str, Any]:
    if not path.exists():
        return {"items": []}
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
        if isinstance(data, dict) and isinstance(data.get("items"), list):
            return data
    except (OSError, json.JSONDecodeError) as exc:
        print(f"⚠️ [Knowledge approval registry] {exc}")
    return {"items": []}


def save_knowledge_approval_registry(registry: dict[str, Any], path: Path = KNOWLEDGE_APPROVAL_FILE) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(registry, ensure_ascii=False, indent=2), encoding="utf-8")


def knowledge_approval_required(update: KnowledgeUpdateRequest, result: dict[str, Any]) -> bool:
    if result.get("skipped"):
        return False
    source = update.source.lower()
    tags = {tag.strip().lower() for tag in update.tags.split(",") if tag.strip()}
    return (
        "auto-collect" in tags
        or "needs-review" in tags
        or source.startswith("telegram-auto")
        or source.startswith("system-auto")
    )


def find_knowledge_approval_candidate(candidate_id: str, path: Path = KNOWLEDGE_APPROVAL_FILE) -> tuple[dict[str, Any], dict[str, Any] | None]:
    registry = load_knowledge_approval_registry(path)
    for item in registry.get("items", []):
        if item.get("id") == candidate_id:
            return registry, item
    return registry, None


def knowledge_approval_message(item: dict[str, Any]) -> str:
    assessment = item.get("assessment") or {}
    reasons = ", ".join(assessment.get("reasons") or []) or "자동 수집/중복검사 통과"
    content_preview = sanitize_outbound_text(item.get("content", "").strip())[:1200]
    return (
        "🧠 [지식 후보 승인 요청]\n\n"
        f"후보 ID: {item['id']}\n"
        f"담당 지식: {item['agent']}\n"
        f"제목: {item['title']}\n"
        f"출처: {item['source']}\n"
        f"QA 저장 위치: {item.get('qa_path', '-')}\n\n"
        "자동 검증 요약:\n"
        f"- 판정: {reasons}\n"
        f"- Top score: {assessment.get('top_score', '-')}\n\n"
        "내용 미리보기:\n"
        f"{content_preview}\n\n"
        f"승인: /kapprove {item['id']}\n"
        f"반려: /kreject {item['id']} 사유"
    )


def build_knowledge_approval_candidate(
    *,
    update: KnowledgeUpdateRequest,
    result: dict[str, Any],
    registry: dict[str, Any],
    assessment: dict[str, Any] | None = None,
    now: dt.datetime | None = None,
    project_root: Path = PROJECT_ROOT,
) -> dict[str, Any]:
    timestamp = now or dt.datetime.now()
    candidate_id = f"K{timestamp.strftime('%Y%m%d%H%M%S')}-{len(registry.get('items', [])) + 1:03d}"
    try:
        qa_path = Path(result["path"]).relative_to(project_root).as_posix()
    except Exception:
        qa_path = str(result.get("path", ""))
    return {
        "id": candidate_id,
        "status": "pending_owner_approval",
        "agent": update.agent,
        "title": update.title,
        "content": update.content,
        "source": update.source,
        "tags": update.tags,
        "qa_path": qa_path,
        "assessment": assessment or {},
        "created_at": timestamp.isoformat(timespec="seconds"),
    }


def append_knowledge_approval_candidate(
    *,
    update: KnowledgeUpdateRequest,
    result: dict[str, Any],
    assessment: dict[str, Any] | None = None,
    registry_path: Path = KNOWLEDGE_APPROVAL_FILE,
    project_root: Path = PROJECT_ROOT,
) -> dict[str, Any] | None:
    if not knowledge_approval_required(update, result):
        return None
    registry = load_knowledge_approval_registry(registry_path)
    item = build_knowledge_approval_candidate(
        update=update,
        result=result,
        registry=registry,
        assessment=assessment,
        project_root=project_root,
    )
    registry.setdefault("items", []).append(item)
    save_knowledge_approval_registry(registry, registry_path)
    return item
