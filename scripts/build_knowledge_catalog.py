#!/usr/bin/env python3
"""지식 카탈로그(FILE_MAP) 빌더 — AI 조직원의 지식 탐색 인덱스 생성.

산출물 (knowledge/00_catalog/):
  - FILE_MAP.json        : 검색엔진용 — 파일 메타데이터 + agent/team/keyword 역색인
  - KNOWLEDGE_CATALOG.md : 사람/Obsidian용 — 층·팀별 지식 지도

인덱싱 범위는 backend.knowledge_engine.knowledge_search_files() 의 검색 루트와
동일하다 (10_agents, 20_qa, docs, obsidian model_quality_auditor).
daily_knowledge_update.sh 가 매일 07:00 에 재생성한다.
"""
from __future__ import annotations

import datetime
import json
import re
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from backend.core.paths import (  # noqa: E402
    AGENT_KB_DIR,
    CATALOG_DIR,
    KNOWLEDGE_ROOT,
    PROJECT_ROOT as _ROOT,
    QA_KB_DIR,
    TEAM_DIR_NAMES,
)
from backend.knowledge_engine import knowledge_search_files  # noqa: E402
from backend.knowledge_store import ORGANIZATION  # noqa: E402

_AGENT_TO_TEAM_KEY = {
    agent: team for team, agents in ORGANIZATION.items() for agent in agents
}

_TOKEN_RE = re.compile(r"[A-Za-z0-9_#+.\-가-힣]{2,30}")
_HEADING_RE = re.compile(r"^(#{1,3})\s+(.+)$", re.MULTILINE)

_TEAM_BY_DIR = {v: k for k, v in TEAM_DIR_NAMES.items()}


def layer_for(path: Path) -> str:
    try:
        rel = path.relative_to(KNOWLEDGE_ROOT)
    except ValueError:
        return "docs" if "docs" in path.parts else "obsidian"
    return rel.parts[0] if rel.parts else "knowledge"


def agent_team_for(path: Path) -> tuple[str, str]:
    """(agent, team_key) — 에이전트 KB/QA 파일이 아니면 빈 문자열."""
    if path.is_relative_to(AGENT_KB_DIR):
        agent = path.stem
        rel = path.relative_to(AGENT_KB_DIR)
        team_dir = rel.parts[0] if len(rel.parts) > 1 else ""
        return agent, _TEAM_BY_DIR.get(team_dir, "")
    if path.is_relative_to(QA_KB_DIR):
        agent = path.stem.removesuffix("_QA")
        return agent, _AGENT_TO_TEAM_KEY.get(agent, "")
    return "", ""


def main() -> int:
    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    files_meta: list[dict] = []
    agent_to_file: dict[str, str] = {}
    team_to_files: dict[str, list[int]] = {}
    keyword_to_files: dict[str, list[int]] = {}

    for path in sorted(knowledge_search_files()):
        try:
            content = path.read_text(encoding="utf-8", errors="ignore")
            stat = path.stat()
        except OSError:
            continue
        rel = path.relative_to(_ROOT).as_posix()
        idx = len(files_meta)
        agent, team = agent_team_for(path)

        headings = [m.group(2).strip() for m in _HEADING_RE.finditer(content)][:30]
        title = headings[0] if headings else path.stem

        tokens = {t.lower() for t in _TOKEN_RE.findall(content)}
        tokens.add(path.stem.lower())
        for token in tokens:
            keyword_to_files.setdefault(token, []).append(idx)

        files_meta.append({
            "path": rel,
            "agent": agent,
            "team": team,
            "layer": layer_for(path),
            "title": title,
            "headings": headings[:10],
            "size": stat.st_size,
            "mtime": int(stat.st_mtime),
        })
        if agent and path.is_relative_to(AGENT_KB_DIR):
            agent_to_file[agent] = rel
        if team:
            team_to_files.setdefault(team, []).append(idx)

    CATALOG_DIR.mkdir(parents=True, exist_ok=True)
    file_map = {
        "generated_at": now,
        "file_count": len(files_meta),
        "files": files_meta,
        "agent_to_file": agent_to_file,
        "team_to_files": team_to_files,
        "keyword_to_files": keyword_to_files,
    }
    (CATALOG_DIR / "FILE_MAP.json").write_text(
        json.dumps(file_map, ensure_ascii=False, separators=(",", ":")),
        encoding="utf-8",
    )

    # ── 사람/Obsidian용 카탈로그 ──────────────────────────────────────────
    lines = [
        "# LUA BIM LABS 지식 카탈로그",
        "",
        f"생성: {now} · 문서 {len(files_meta)}건 (자동 생성 — 수동 편집 금지)",
        "",
        "| 층 | 위치 | 내용 |",
        "|---|---|---|",
        "| 10_agents | knowledge/10_agents/ | 에이전트별 지식베이스 (팀 폴더) |",
        "| 20_qa | knowledge/20_qa/ | 에이전트별 Q&A 누적 지식 |",
        "| 30_intake | knowledge/30_intake/ | 미검수 수집물 (raw intake) |",
        "| 40_curation | knowledge/40_curation/ | 큐레이션·품질 로그 |",
        "| 50_domain | knowledge/50_domain/ | 도메인 원천자료 (PDF·스크립트·데이터셋) |",
        "| 60_public | knowledge/60_public/ | 공개·교육 재사용 콘텐츠 |",
        "",
    ]
    by_layer: dict[str, list[dict]] = {}
    for meta in files_meta:
        by_layer.setdefault(meta["layer"], []).append(meta)

    if "10_agents" in by_layer:
        lines.append("## 에이전트 지식베이스 (10_agents)")
        lines.append("")
        by_team: dict[str, list[dict]] = {}
        for meta in by_layer["10_agents"]:
            team_dir = Path(meta["path"]).relative_to(
                AGENT_KB_DIR.relative_to(_ROOT)
            ).parts[0]
            by_team.setdefault(team_dir, []).append(meta)
        for team_dir in sorted(by_team):
            lines.append(f"### {team_dir}")
            for meta in sorted(by_team[team_dir], key=lambda m: m["path"]):
                lines.append(f"- [{Path(meta['path']).stem}]({meta['path']}) — {meta['title'][:60]}")
            lines.append("")

    for layer, label in [("20_qa", "QA 지식 (20_qa)"), ("docs", "회사 문서 (docs)"), ("obsidian", "MQA Obsidian")]:
        metas = by_layer.get(layer)
        if not metas:
            continue
        lines.append(f"## {label}")
        lines.append("")
        for meta in sorted(metas, key=lambda m: m["path"])[:200]:
            lines.append(f"- [{Path(meta['path']).stem}]({meta['path']})")
        lines.append("")

    (CATALOG_DIR / "KNOWLEDGE_CATALOG.md").write_text("\n".join(lines), encoding="utf-8")

    print(f"catalog_files={len(files_meta)} keywords={len(keyword_to_files)}")
    print(f"file_map={CATALOG_DIR / 'FILE_MAP.json'}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
