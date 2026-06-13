#!/usr/bin/env python3
"""Build a global Obsidian knowledge map for all important Markdown files.

The generated vault is an index/mirror vault. It does not move or rewrite source
documents. Each source .md gets a lightweight index note with source path,
category, keywords and graph links.
"""

from __future__ import annotations

import html
import hashlib
import json
import re
import shutil
from collections import Counter, defaultdict
from dataclasses import dataclass, field
from pathlib import Path

WIKILINK_RE = re.compile(r"\[\[([^\]|#]+)(?:#[^\]|]+)?(?:\|[^\]]+)?\]\]")


PROJECT_ROOT = Path(__file__).resolve().parents[1]
import sys  # noqa: E402
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))
from backend.core.paths import (  # noqa: E402
    AGENT_KB_DIR,
    BLOGGER_QUEUE_DIR,
    INTAKE_DIR,
    KNOWLEDGE_ROOT,
    PRODUCTS_DIR,
    QA_KB_DIR,
    TRAINING_CURRICULUM_DIR,
)

VAULT = PROJECT_ROOT / "obsidian_vaults" / "lua_bim_lab_global_map"


def _rel_prefix(path) -> str:
    return path.relative_to(PROJECT_ROOT).as_posix() + "/"


_KB_PREFIX = _rel_prefix(AGENT_KB_DIR)
_QA_PREFIX = _rel_prefix(QA_KB_DIR)
_INTAKE_PREFIX = _rel_prefix(INTAKE_DIR)
_CURATION_PREFIX = _rel_prefix(KNOWLEDGE_ROOT / "40_curation")
_DOMAIN_PREFIX = _rel_prefix(KNOWLEDGE_ROOT / "50_domain")
_BLOGGER_PREFIX = _rel_prefix(BLOGGER_QUEUE_DIR)
_TRAINING_PREFIX = _rel_prefix(TRAINING_CURRICULUM_DIR)
_PRODUCTS_PREFIX = _rel_prefix(PRODUCTS_DIR)

EXCLUDE_PARTS = {
    ".git",
    ".dev-venv",
    ".pytest_cache",
    ".wrangler",
    "__pycache__",
    "node_modules",
    "bin",
    "obj",
    "dist",
    "logs",
    "runtime",
    ".bkit",
    ".claude",
    ".pdca-snapshots",
}
EXCLUDE_VAULTS = {
    "obsidian_vaults/lua_bim_lab_global_map",
}
EXCLUDE_PREFIXES = {
    "commercial_addins/BIM_Command_Center_For_Revit/03_store_submission/autodesk_store_upload",
}

KEYWORDS = [
    "revit", "navisworks", "autodesk", "store", "addin", "add-in", "api",
    "mep", "bim", "quality", "audit", "clash", "qa", "model", "health",
    "교육", "커리큘럼", "온보딩", "슬라이드", "notebooklm",
    "품질", "진단", "간섭", "납품", "물량", "roi", "회의", "변경", "리스크",
    "견적", "sow", "보안", "라이선스", "구독", "결제", "스토어", "심사",
    "조직", "역할", "권한", "자산", "kpi", "okr", "지식", "옵시디언",
    "qwen", "개발", "테스트", "빌드", "패키징", "지원", "cs",
]


@dataclass
class Doc:
    id: str
    title: str
    path: Path
    rel: str
    category: str
    keywords: set[str]
    summary: str
    wikilinks: set[str] = field(default_factory=set)


_VAULT_EXCEPTIONS = {
    "obsidian_vaults/lua_bim_lab_global_map/NAS_Knowledge",
}


def should_skip(path: Path) -> bool:
    rel = path.relative_to(PROJECT_ROOT).as_posix()
    if any(rel.startswith(exc) for exc in _VAULT_EXCEPTIONS):
        return False  # NAS_Knowledge는 인덱싱 대상
    if any(rel.startswith(prefix) for prefix in EXCLUDE_VAULTS):
        return True
    if any(rel.startswith(prefix) for prefix in EXCLUDE_PREFIXES):
        return True
    return any(part in EXCLUDE_PARTS for part in path.parts)


def category_for(rel: str) -> str:
    if rel.startswith("obsidian_vaults/lua_bim_lab_global_map/NAS_Knowledge/"):
        return "NAS Knowledge"
    if rel.startswith(_KB_PREFIX):
        return "AI Knowledge Base"
    if rel.startswith(_QA_PREFIX):
        return "AI Knowledge Base - QA"
    if rel.startswith(_INTAKE_PREFIX):
        return "Knowledge Intake"
    if rel.startswith(_CURATION_PREFIX):
        return "Knowledge Curation"
    if rel.startswith(_BLOGGER_PREFIX):
        return "Public Content - Blogger"
    if rel.startswith(_DOMAIN_PREFIX):
        return "Domain Sources"
    if rel.startswith(_PRODUCTS_PREFIX):
        return "Products"
    if rel.startswith("knowledge/00_catalog/"):
        return "Knowledge Catalog"
    if rel.startswith("docs/standard_documents/"):
        return "Standard Documents"
    if rel.startswith("docs/internal_organization_documents/"):
        return "Internal Organization"
    if rel.startswith("docs/lua_bim_lab_official_documents/"):
        return "Official External Documents"
    if rel.startswith("docs/revenue_products/model_quality_audit/"):
        return "Revenue Product - Model Quality Auditor"
    if rel.startswith(_TRAINING_PREFIX):
        return "Training Curriculum"
    if rel.startswith("docs/autodesk_store/"):
        return "Autodesk Store"
    if rel.startswith("commercial_addins/"):
        return "Commercial Addins"
    if rel.startswith("obsidian_vaults/model_quality_auditor/"):
        return "Obsidian - Model Quality Auditor"
    if rel.startswith("260519"):
        if "90_Archives_Backups" in rel:
            return "Archive Source Notes"
        if "01_Revit_Addins" in rel:
            return "Source - Revit Addins"
        if "02_Navisworks_Tools" in rel:
            return "Source - Navisworks Tools"
        return "Source Folder"
    if rel.startswith("docs/"):
        return "Docs - General"
    return "Workspace Markdown"


GENERIC_STEMS = {
    "readme",
    "license",
    "changelog",
    "claude",
    "identity",
    "bug_report",
}


GENERIC_TITLES = {
    "readme",
    "license",
    "changelog",
    "claude.md",
    "identity.md - who am i?",
    "lua bim lab",
    "lua bim labs",
}


def clean_label(value: str) -> str:
    cleaned = re.sub(r"[^\w가-힣\- ]+", " ", value, flags=re.UNICODE).strip()
    cleaned = re.sub(r"\s+", " ", cleaned) or "Untitled"
    return cleaned


def path_context(rel: str, depth: int = 2) -> str:
    path = Path(rel)
    parts = [part for part in path.parent.parts if part not in {".", ""}]
    if not parts:
        return clean_label(path.stem)
    selected = parts[-depth:]
    return clean_label(" - ".join(selected))


def display_title_for(rel: str, raw_title: str) -> str:
    path = Path(rel)
    stem = path.stem
    title = clean_label(raw_title or stem)
    lower_title = title.lower()
    lower_stem = stem.lower()
    context = path_context(rel)

    if lower_stem in GENERIC_STEMS or lower_title in GENERIC_TITLES:
        return f"{context} - {title}"
    if lower_title in {"qa", "index"}:
        return f"{context} - {title}"
    return title


def make_id(rel: str, title: str, used: set[str]) -> str:
    candidate = display_title_for(rel, title)[:110]
    if candidate not in used:
        used.add(candidate)
        return candidate
    suffix = 2
    while f"{candidate} {suffix}" in used:
        suffix += 1
    final = f"{candidate} {suffix}"
    used.add(final)
    return final


def extract_title(text: str, rel: str) -> str:
    for line in text.splitlines()[:30]:
        if line.startswith("# "):
            return display_title_for(rel, line[2:].strip())
    return display_title_for(rel, Path(rel).stem)


def extract_summary(text: str) -> str:
    lines = []
    in_frontmatter = False
    for raw in text.splitlines():
        line = raw.strip()
        if line == "---":
            in_frontmatter = not in_frontmatter
            continue
        if in_frontmatter or not line or line.startswith("#") or line.startswith("|"):
            continue
        line = re.sub(r"\[\[([^\]|]+)(?:\|([^\]]+))?\]\]", r"\1", line)
        lines.append(line)
        if len(" ".join(lines)) > 220:
            break
    return " ".join(lines)[:260]


def extract_keywords(text: str, rel: str, category: str) -> set[str]:
    lower = f"{rel}\n{text[:6000]}".lower()
    found = {kw for kw in KEYWORDS if kw.lower() in lower}
    found.update(token.lower() for token in re.findall(r"[A-Za-z][A-Za-z0-9_+\-.]{2,}", rel))
    found.update(part.lower() for part in category.split())
    return {kw for kw in found if len(kw) >= 2}


def extract_wikilinks(text: str) -> set[str]:
    return {m.strip() for m in WIKILINK_RE.findall(text) if m.strip()}


def scan_docs() -> list[Doc]:
    raw_docs: list[tuple[Path, str, str, str, set[str], str, set[str]]] = []
    for path in sorted(PROJECT_ROOT.rglob("*.md")):
        if should_skip(path):
            continue
        rel = path.relative_to(PROJECT_ROOT).as_posix()
        try:
            text = path.read_text(encoding="utf-8", errors="ignore")
        except OSError:
            continue
        category = category_for(rel)
        title = extract_title(text, rel)
        raw_docs.append((
            path,
            rel,
            category,
            title,
            extract_keywords(text, rel, category),
            extract_summary(text),
            extract_wikilinks(text),
        ))

    title_counts = Counter(item[3] for item in raw_docs)
    used: set[str] = set()
    docs: list[Doc] = []
    for path, rel, category, title, keywords, summary, wikilinks in raw_docs:
        if title_counts[title] > 1:
            stem = clean_label(Path(rel).stem)
            context = path_context(rel, depth=2)
            if stem.lower() not in title.lower():
                title = f"{context} - {stem} - {title}"
            else:
                title = f"{context} - {title}"
        doc_id = make_id(rel, title, used)
        docs.append(Doc(
            id=doc_id,
            title=title,
            path=path,
            rel=rel,
            category=category,
            keywords=keywords,
            summary=summary,
            wikilinks=wikilinks,
        ))
    final_title_counts = Counter(doc.title for doc in docs)
    if not any(count > 1 for count in final_title_counts.values()):
        return docs

    final_docs: list[Doc] = []
    final_used: set[str] = set()
    for doc in docs:
        title = doc.title
        if final_title_counts[title] > 1:
            suffix = hashlib.sha1(doc.rel.encode("utf-8")).hexdigest()[:6]
            title = f"{title} - {suffix}"
        final_docs.append(Doc(
            id=make_id(doc.rel, title, final_used),
            title=title,
            path=doc.path,
            rel=doc.rel,
            category=doc.category,
            keywords=doc.keywords,
            summary=doc.summary,
            wikilinks=doc.wikilinks,
        ))
    return final_docs


def wikilink(name: str) -> str:
    return f"[[{name}]]"


def safe_filename(name: str) -> str:
    name = re.sub(r"[/\\:]+", " - ", name)
    return name[:120]


def write_text(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


def related_docs(docs: list[Doc]) -> dict[str, list[Doc]]:
    by_id = {doc.id: doc for doc in docs}
    out: dict[str, list[Doc]] = {}
    for doc in docs:
        candidates = []
        for other in docs:
            if other.id == doc.id:
                continue
            score = 0
            if other.category == doc.category:
                score += 4
            overlap = doc.keywords & other.keywords
            score += min(len(overlap), 8)
            if Path(other.rel).parent == Path(doc.rel).parent:
                score += 5
            if score >= 6:
                candidates.append((score, other))
        candidates.sort(key=lambda item: (-item[0], item[1].title))
        out[doc.id] = [item[1] for item in candidates[:8]]
    return out


def graph_data(docs: list[Doc], related: dict[str, list[Doc]]) -> dict:
    nodes = [
        {"id": f"CAT::{cat}", "label": cat, "group": "Category",
         "path": "", "summary": "", "keywords": []}
        for cat in sorted({d.category for d in docs})
    ]
    for doc in docs:
        nodes.append({
            "id": doc.id,
            "label": doc.title[:72],
            "group": doc.category,
            "path": doc.rel,
            "summary": doc.summary[:220],
            "keywords": sorted(doc.keywords)[:12],
        })

    # 위키링크 매핑: 제목 / 파일스템 → doc.id
    title_to_id: dict[str, str] = {doc.title: doc.id for doc in docs}
    stem_to_id: dict[str, str] = {Path(doc.rel).stem: doc.id for doc in docs}

    edges = []
    seen_edges: set[tuple[str, str]] = set()

    def add_edge(src: str, tgt: str, etype: str) -> None:
        key = (src, tgt) if src <= tgt else (tgt, src)
        if key not in seen_edges:
            seen_edges.add(key)
            edges.append({"source": src, "target": tgt, "type": etype})

    for doc in docs:
        add_edge(f"CAT::{doc.category}", doc.id, "category")
        # 키워드 유사도 기반 관련 엣지
        for other in related.get(doc.id, [])[:4]:
            add_edge(doc.id, other.id, "related")
        # [[위키링크]] 기반 엣지 — KB/문서가 성장할수록 자동으로 늘어남
        for link in doc.wikilinks:
            target_id = title_to_id.get(link) or stem_to_id.get(link)
            if target_id and target_id != doc.id:
                add_edge(doc.id, target_id, "wikilink")

    return {"nodes": nodes, "edges": edges}


def write_obsidian_config() -> None:
    write_text(VAULT / ".obsidian" / "app.json", json.dumps({
        "alwaysUpdateLinks": True,
        "newFileLocation": "current",
        "attachmentFolderPath": "Assets",
        "promptDelete": False,
    }, ensure_ascii=False, indent=2))
    write_text(VAULT / ".obsidian" / "appearance.json", json.dumps({
        "theme": "obsidian",
        "accentColor": "#8b5cf6",
        "baseFontSize": 15,
    }, ensure_ascii=False, indent=2))
    write_text(VAULT / ".obsidian" / "graph.json", json.dumps({
        "showTags": True,
        "showAttachments": False,
        "hideUnresolved": False,
        "showOrphans": False,
        "nodeSizeMultiplier": 1.1,
        "lineSizeMultiplier": 1,
        "centerStrength": 0.55,
        "repelStrength": 10,
        "linkStrength": 1,
        "linkDistance": 170,
    }, ensure_ascii=False, indent=2))


_PRESERVE_DIRS = {"NAS_Knowledge"}  # 재생성 시 보존할 폴더


def write_vault(docs: list[Doc]) -> dict:
    if VAULT.exists():
        # 보존 폴더를 임시 위치로 이동 후 vault 삭제
        preserved: list[tuple[Path, Path]] = []
        for name in _PRESERVE_DIRS:
            src = VAULT / name
            if src.exists():
                tmp = VAULT.parent / f"_tmp_preserve_{name}"
                shutil.copytree(src, tmp)
                preserved.append((tmp, src))
        shutil.rmtree(VAULT)
    else:
        preserved = []
    (VAULT / "Assets").mkdir(parents=True, exist_ok=True)
    # 보존 폴더 복원
    for tmp, dst in preserved:
        shutil.copytree(tmp, dst)
        shutil.rmtree(tmp)
    write_obsidian_config()
    related = related_docs(docs)
    categories = defaultdict(list)
    for doc in docs:
        categories[doc.category].append(doc)

    category_links = "\n".join(f"- [[MOC - {cat}]] ({len(items)} files)" for cat, items in sorted(categories.items()))
    write_text(VAULT / "00_Home" / "Global Knowledge Map.md", f"""---
type: global-moc
generated: true
source_count: {len(docs)}
---

# Global Knowledge Map

현재 workspace의 주요 `.md` 파일을 Obsidian에서 찾기 쉽도록 미러링한 전역 지식맵이다.

## 분류별 지도

{category_links}

## 주요 허브

- [[MOC - Revenue Product - Model Quality Auditor]]
- [[MOC - Training Curriculum]]
- [[MOC - Standard Documents]]
- [[MOC - Internal Organization]]
- [[MOC - AI Knowledge Base]]
- [[MOC - Autodesk Store]]
- [[MOC - Commercial Addins]]

## 시각화

- Obsidian Graph View
- Canvas: [[Global Knowledge Canvas.canvas]]
- Browser HTML: `Assets/global_knowledge_graph.html`
""")

    for cat, items in sorted(categories.items()):
        body = "\n".join(
            f"- [[{doc.id}]] — `{doc.rel}`"
            for doc in sorted(items, key=lambda d: d.title)
        )
        write_text(VAULT / "01_MOC" / f"MOC - {safe_filename(cat)}.md", f"""---
type: category-moc
category: {cat}
generated: true
count: {len(items)}
---

# MOC - {cat}

{body}

## 상위

- [[Global Knowledge Map]]
""")

    for doc in docs:
        rel_related = "\n".join(f"- [[{other.id}]]" for other in related.get(doc.id, [])[:8]) or "- 없음"
        kw = ", ".join(sorted(doc.keywords)[:30])
        source_abs = doc.path.as_posix()
        write_text(VAULT / "10_Document_Index" / f"{safe_filename(doc.id)}.md", f"""---
type: source-index
generated: true
category: {doc.category}
source_path: "{doc.rel}"
---

# {doc.title}

## Source

`{doc.rel}`

Absolute path:

`{source_abs}`

## Category

- [[MOC - {doc.category}]]

## Summary

{doc.summary or "요약 없음"}

## Keywords

{kw}

## Related

{rel_related}

## Home

- [[Global Knowledge Map]]
""")

    write_canvas(docs, categories)
    write_html(graph_data(docs, related))
    write_text(VAULT / "README.md", f"""# LUA BIM LAB Global Obsidian Map

이 vault는 원본 문서를 복사하지 않고, workspace의 `.md` 문서 {len(docs)}개를 검색/그래프용 인덱스 노트로 미러링한다.

시작 문서: [[Global Knowledge Map]]

브라우저 시각화: `Assets/global_knowledge_graph.html`

재생성:

```bash
source .dev-venv/bin/activate && python scripts/build_global_obsidian_map.py
```
""")
    return graph_data(docs, related)


def write_canvas(docs: list[Doc], categories: dict[str, list[Doc]]) -> None:
    nodes = [{
        "id": "global",
        "type": "file",
        "file": "00_Home/Global Knowledge Map.md",
        "x": 0,
        "y": 0,
        "width": 360,
        "height": 220,
    }]
    edges = []
    positions = [
        (-520, -300), (-120, -360), (300, -330), (620, -120),
        (560, 240), (140, 380), (-320, 330), (-660, 80),
        (-780, -210), (780, -330), (800, 260), (-760, 360),
    ]
    for idx, cat in enumerate(sorted(categories)):
        x, y = positions[idx % len(positions)]
        node_id = f"cat{idx}"
        nodes.append({
            "id": node_id,
            "type": "file",
            "file": f"01_MOC/MOC - {cat}.md",
            "x": x,
            "y": y,
            "width": 320,
            "height": 180,
        })
        edges.append({
            "id": f"e{idx}",
            "fromNode": "global",
            "fromSide": "right" if x > 0 else "left",
            "toNode": node_id,
            "toSide": "left" if x > 0 else "right",
        })
    write_text(VAULT / "09_Canvas" / "Global Knowledge Canvas.canvas", json.dumps({"nodes": nodes, "edges": edges}, ensure_ascii=False, indent=2))


def write_html(graph: dict) -> None:
    # </script> in JSON string content must be escaped to prevent premature tag close
    data = json.dumps(graph, ensure_ascii=False).replace("</script>", r"<\/script>").replace("<script", r"<\x73cript")
    groups = sorted({node["group"] for node in graph["nodes"]})
    palette = [
        "#8b5cf6", "#22c55e", "#38bdf8", "#f59e0b", "#ef4444", "#14b8a6",
        "#e879f9", "#84cc16", "#f97316", "#60a5fa", "#d946ef", "#a3a3a3",
        "#fb923c", "#34d399", "#818cf8", "#e11d48",
    ]
    color_map = {group: palette[i % len(palette)] for i, group in enumerate(groups)}
    color_json = json.dumps(color_map, ensure_ascii=False)
    node_count = len(graph["nodes"])
    edge_count = len(graph["edges"])
    write_text(VAULT / "Assets" / "global_knowledge_graph.html", f"""<!doctype html>
<html lang="ko">
<head>
  <meta charset="utf-8"/>
  <meta name="viewport" content="width=device-width,initial-scale=1"/>
  <title>LUA BIM LAB Global Knowledge Graph</title>
  <style>
    *{{box-sizing:border-box;margin:0;padding:0}}
    html,body{{height:100%;display:flex;background:#0f0f11;color:#e5e7eb;font-family:Inter,-apple-system,BlinkMacSystemFont,"Segoe UI",sans-serif;overflow:hidden}}
    /* ── 사이드바 ── */
    #sidebar{{display:none}}
    #sb-head{{padding:14px 14px 10px;border-bottom:1px solid rgba(148,163,184,.1);flex-shrink:0}}
    #sb-head h1{{font-size:13px;font-weight:700;color:#f4f4f5;letter-spacing:-.01em}}
    #sb-head p{{font-size:11px;color:#52525b;margin-top:2px}}
    #search{{width:100%;margin-top:9px;padding:8px 10px;background:rgba(2,6,23,.7);border:1px solid rgba(148,163,184,.2);border-radius:6px;color:#e5e7eb;font-size:12px;outline:none;transition:border-color .15s}}
    #search:focus{{border-color:rgba(139,92,246,.65)}}
    #search-count{{font-size:10px;color:#52525b;margin-top:4px;min-height:14px}}
    #tree{{flex:1;overflow-y:auto;padding:4px 0 20px}}
    #tree::-webkit-scrollbar{{width:4px}}
    #tree::-webkit-scrollbar-thumb{{background:rgba(139,92,246,.25);border-radius:2px}}
    details{{border-bottom:1px solid rgba(255,255,255,.04)}}
    details[open] summary .arrow{{transform:rotate(90deg)}}
    summary{{cursor:pointer;list-style:none;padding:7px 12px;font-size:11.5px;color:#c4c4cc;display:flex;align-items:center;gap:7px;user-select:none;transition:background .1s}}
    summary:hover{{background:rgba(139,92,246,.09)}}
    summary::-webkit-details-marker{{display:none}}
    .arrow{{font-size:9px;color:#52525b;transition:transform .15s;flex-shrink:0}}
    .cat-dot{{width:8px;height:8px;border-radius:50%;flex-shrink:0}}
    .cat-label{{flex:1;font-weight:500}}
    .cat-count{{color:#52525b;font-size:10px;flex-shrink:0}}
    .doc-item{{padding:5px 12px 5px 32px;font-size:11px;color:#8a8a99;cursor:pointer;line-height:1.4;white-space:nowrap;overflow:hidden;text-overflow:ellipsis;transition:background .1s,color .1s;border-left:2px solid transparent}}
    .doc-item:hover{{background:rgba(139,92,246,.1);color:#d4d4d8;border-left-color:rgba(139,92,246,.4)}}
    .doc-item.selected{{background:rgba(139,92,246,.18);color:#fff;font-weight:500;border-left-color:#8b5cf6}}
    .doc-item.dimmed{{opacity:.35}}
    /* ── 캔버스 영역 ── */
    #canvas-wrap{{flex:1;position:relative;overflow:hidden}}
    canvas{{display:block;width:100%;height:100%;cursor:grab}}
    canvas.grabbing{{cursor:grabbing}}
    /* ── 상세 패널 ── */
    #detail{{position:absolute;right:14px;top:14px;width:270px;padding:14px;background:rgba(12,12,14,.94);border:1px solid rgba(148,163,184,.18);border-radius:8px;backdrop-filter:blur(14px);display:none;max-height:calc(100vh - 80px);overflow-y:auto}}
    #detail h2{{font-size:13px;font-weight:600;color:#f4f4f5;word-break:break-word;line-height:1.4;margin-bottom:5px}}
    #detail .d-cat{{font-size:10px;color:#8b5cf6;text-transform:uppercase;letter-spacing:.05em;margin-bottom:8px}}
    #detail .d-summary{{font-size:11.5px;color:#a1a1aa;line-height:1.55;margin-bottom:10px;white-space:pre-wrap}}
    #detail .d-kw{{display:flex;flex-wrap:wrap;gap:4px;margin-bottom:10px}}
    #detail .tag{{font-size:10px;padding:2px 7px;background:rgba(139,92,246,.16);border-radius:10px;color:#c4b5fd}}
    #detail .d-path{{font-size:10px;color:#52525b;word-break:break-all;line-height:1.5}}
    #detail .d-related{{margin-top:10px;border-top:1px solid rgba(255,255,255,.06);padding-top:8px}}
    #detail .d-related-title{{font-size:10px;color:#71717a;margin-bottom:5px;text-transform:uppercase;letter-spacing:.05em}}
    #detail .rel-item{{font-size:11px;color:#a78bfa;cursor:pointer;padding:2px 0;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}}
    #detail .rel-item:hover{{color:#c4b5fd}}
    /* ── 줌 도구 ── */
    #zoom-btns{{position:absolute;right:14px;bottom:14px;display:flex;flex-direction:column;gap:4px}}
    .z-btn{{width:28px;height:28px;background:rgba(20,20,24,.88);border:1px solid rgba(148,163,184,.18);border-radius:5px;color:#d4d4d8;font-size:16px;cursor:pointer;display:flex;align-items:center;justify-content:center;line-height:1;user-select:none}}
    .z-btn:hover{{background:rgba(139,92,246,.25);border-color:rgba(139,92,246,.5)}}
    #hint{{position:absolute;left:14px;bottom:14px;color:#3f3f46;font-size:10px;pointer-events:none}}
    /* ── 범례 ── */
    #legend{{flex-shrink:0;padding:12px 14px;border-top:1px solid rgba(148,163,184,.1);background:rgba(8,8,10,.6)}}
    #legend-title{{font-size:10px;font-weight:600;color:#52525b;text-transform:uppercase;letter-spacing:.07em;margin-bottom:8px}}
    .leg-row{{display:flex;align-items:center;gap:8px;margin-bottom:6px}}
    .leg-row:last-child{{margin-bottom:0}}
    .leg-line{{flex-shrink:0}}
    .leg-text{{font-size:11px;color:#8a8a99;line-height:1.3}}
    .leg-text b{{color:#c4c4cc;font-weight:500}}
  </style>
</head>
<body>
<div id="sidebar">
  <div id="sb-head">
    <h1>LUA BIM LAB Knowledge</h1>
    <p>노드 {node_count}개 &middot; 연결 {edge_count}개</p>
    <input id="search" type="search" placeholder="&#128269; 문서명 · 키워드 · 경로 검색..." autocomplete="off"/>
    <div id="search-count"></div>
  </div>
  <div id="tree"></div>
  <div id="legend">
    <div id="legend-title">범례 · Legend</div>
    <div class="leg-row">
      <svg class="leg-line" width="36" height="14">
        <circle cx="5" cy="7" r="5" fill="#8b5cf6"/>
        <circle cx="31" cy="7" r="3" fill="#22c55e"/>
      </svg>
      <span class="leg-text"><b>노드</b> — 큰 원: 카테고리 &nbsp;/&nbsp; 작은 원: 문서</span>
    </div>
    <div class="leg-row">
      <svg class="leg-line" width="36" height="14">
        <line x1="2" y1="7" x2="34" y2="7" stroke="#8b5cf6" stroke-width="2"/>
      </svg>
      <span class="leg-text"><b>카테고리 연결</b> — 문서가 속한 분류</span>
    </div>
    <div class="leg-row">
      <svg class="leg-line" width="36" height="14">
        <line x1="2" y1="7" x2="34" y2="7" stroke="#6b7280" stroke-width="1.2"/>
      </svg>
      <span class="leg-text"><b>키워드 유사도</b> — 관련 키워드 공유</span>
    </div>
    <div class="leg-row">
      <svg class="leg-line" width="36" height="14">
        <line x1="2" y1="7" x2="34" y2="7" stroke="#fbbf24" stroke-width="1.5" stroke-dasharray="4,3"/>
      </svg>
      <span class="leg-text"><b>[[위키링크]]</b> — 문서 간 직접 참조 <span style="color:#52525b">(매일 성장)</span></span>
    </div>
  </div>
</div>
<div id="canvas-wrap">
  <canvas id="graph"></canvas>
  <div id="detail"></div>
  <div id="zoom-btns">
    <div class="z-btn" id="z-in">+</div>
    <div class="z-btn" id="z-fit">&#8635;</div>
    <div class="z-btn" id="z-out">&minus;</div>
  </div>
  <div id="hint">휠: 확대/축소 &nbsp;·&nbsp; 드래그: 이동 &nbsp;·&nbsp; 노드 클릭: 상세 보기</div>
</div>
<script>
const RAW = {data};
const COLORS = {color_json};

// ── 노드/엣지 초기화 ──────────────────────────────────────────────────────
const nodes = RAW.nodes.map((n, i) => {{
  const a = (i / RAW.nodes.length) * Math.PI * 2;
  const r = n.group === 'Category' ? 160 : 320 + (i % 13) * 22;
  return {{...n, x: 800 + Math.cos(a)*r, y: 500 + Math.sin(a)*r, vx:0, vy:0}};
}});
const byId = new Map(nodes.map(n => [n.id, n]));
const edges = RAW.edges
  .map(e => ({{s: byId.get(e.source), t: byId.get(e.target), type: e.type}}))
  .filter(e => e.s && e.t);

// 이웃 인덱스
const nbrs = new Map(nodes.map(n => [n.id, []]));
for (const e of edges) {{
  nbrs.get(e.s.id).push(e.t);
  nbrs.get(e.t.id).push(e.s);
}}

// ── 캔버스 설정 ───────────────────────────────────────────────────────────
const canvas = document.getElementById('graph');
const ctx = canvas.getContext('2d');
const wrap = document.getElementById('canvas-wrap');
let W = 0, H = 0;
function resize() {{
  const dpr = devicePixelRatio || 1;
  W = wrap.clientWidth; H = wrap.clientHeight;
  canvas.width = W * dpr; canvas.height = H * dpr;
  canvas.style.width = W + 'px'; canvas.style.height = H + 'px';
  ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
}}
function resizeAndFit() {{
  resize();
  if (typeof fitAll === 'function' && nodes && nodes.length) fitAll();
}}
window.addEventListener('resize', resizeAndFit);
if (window.ResizeObserver) {{
  new ResizeObserver(resizeAndFit).observe(wrap);
}}
resize();

// ── 뷰 상태 ──────────────────────────────────────────────────────────────
let scale = 0.18, ox = 0, oy = 0;
let drag = null, panning = false, panAnchor = null;
let pointerDownPos = null, didMove = false;
let selected = null, hovered = null;
let matchSet = null;
let simSteps = 0, simActive = true;

// ── 좌표 변환 ─────────────────────────────────────────────────────────────
const toGraph = (cx, cy) => [(cx - ox) / scale, (cy - oy) / scale];

// ── 전체 fit ─────────────────────────────────────────────────────────────
function fitAll() {{
  if (!nodes.length) return;
  let minX=Infinity, maxX=-Infinity, minY=Infinity, maxY=-Infinity;
  for (const n of nodes) {{
    minX=Math.min(minX,n.x); maxX=Math.max(maxX,n.x);
    minY=Math.min(minY,n.y); maxY=Math.max(maxY,n.y);
  }}
  const gw=maxX-minX, gh=maxY-minY;
  scale=Math.min(W/(gw+120), H/(gh+120), 1.5);
  ox=W/2-(minX+gw/2)*scale; oy=H/2-(minY+gh/2)*scale;
}}

// ── 물리 시뮬레이션 ──────────────────────────────────────────────────────
function step() {{
  if (!simActive) return;
  simSteps++;
  if (simSteps > 600) {{ simActive = false; fitAll(); return; }}
  if (simSteps % 60 === 0) fitAll();
  for (const e of edges) {{
    const dx = e.t.x - e.s.x, dy = e.t.y - e.s.y;
    const d = Math.max(1, Math.hypot(dx, dy));
    const want = e.type === 'category' ? 130 : e.type === 'wikilink' ? 160 : 200;
    const f = (d - want) * 0.002;
    const fx = dx/d*f, fy = dy/d*f;
    e.s.vx += fx; e.s.vy += fy; e.t.vx -= fx; e.t.vy -= fy;
  }}
  for (let i = 0; i < nodes.length; i++) {{
    const a = nodes[i];
    for (let j = i+1; j < nodes.length; j++) {{
      const b = nodes[j];
      const dx = b.x-a.x, dy = b.y-a.y;
      const d2 = Math.max(16, dx*dx+dy*dy), d = Math.sqrt(d2);
      const isCAT = a.group==='Category'||b.group==='Category';
      const f = (isCAT ? 2400 : 700) / d2;
      a.vx -= dx/d*f; a.vy -= dy/d*f;
      b.vx += dx/d*f; b.vy += dy/d*f;
    }}
  }}
  const cx = 800, cy = 500;
  for (const n of nodes) {{
    if (drag === n) continue;
    n.vx += (cx - n.x) * 0.0003;
    n.vy += (cy - n.y) * 0.0003;
    n.x += n.vx; n.y += n.vy;
    n.vx *= 0.86; n.vy *= 0.86;
  }}
}}

// ── 그리기 ───────────────────────────────────────────────────────────────
function draw() {{
  ctx.clearRect(0, 0, W, H);
  ctx.save();
  ctx.translate(ox, oy); ctx.scale(scale, scale);

  const selNbrs = selected ? new Set(nbrs.get(selected.id).map(n=>n.id)) : null;

  // 엣지
  for (const e of edges) {{
    const active = selected && (e.s===selected || e.t===selected);
    const dimmed = matchSet && !matchSet.has(e.s.id) && !matchSet.has(e.t.id);
    const isCat  = e.type === 'category';
    const isWiki = e.type === 'wikilink';
    ctx.globalAlpha = dimmed ? 0.04 : active ? 0.9 : isCat ? 0.3 : isWiki ? 0.55 : 0.1;
    ctx.strokeStyle = active ? '#c4b5fd' : isCat ? '#8b5cf6' : isWiki ? '#fbbf24' : '#6b7280';
    ctx.lineWidth = (active ? 2 : isCat ? 0.9 : isWiki ? 1.2 : 0.7) / scale;
    if (isWiki && !active) {{ ctx.setLineDash([4/scale, 3/scale]); }}
    else {{ ctx.setLineDash([]); }}
    ctx.beginPath(); ctx.moveTo(e.s.x, e.s.y); ctx.lineTo(e.t.x, e.t.y); ctx.stroke();
  }}
  ctx.setLineDash([]);
  ctx.globalAlpha = 1;

  // 노드
  for (const n of nodes) {{
    const isCAT = n.group === 'Category';
    const isSel = n === selected;
    const isNbr = selNbrs?.has(n.id);
    const isHov = n === hovered;
    const dimmed = matchSet && !matchSet.has(n.id);
    const r = isCAT ? 12 : isSel ? 9 : isNbr ? 7 : isHov ? 7 : 4.5;
    ctx.globalAlpha = dimmed ? 0.1 : 1;
    ctx.fillStyle = COLORS[n.group] || '#a1a1aa';
    ctx.beginPath(); ctx.arc(n.x, n.y, r, 0, Math.PI*2); ctx.fill();
    if (isSel) {{ ctx.strokeStyle='#f8fafc'; ctx.lineWidth=2/scale; ctx.stroke(); }}
    if (isHov && !isSel) {{ ctx.strokeStyle='rgba(255,255,255,.5)'; ctx.lineWidth=1.5/scale; ctx.stroke(); }}

    // 라벨 표시 조건
    const showLabel = isCAT || isSel || isNbr || isHov || scale > 2.8;
    if (showLabel && !dimmed) {{
      const fs = isCAT ? 12 : isSel ? 11 : 10;
      ctx.font = (isCAT ? '600 ' : isSel ? '500 ' : '') + fs/scale + 'px sans-serif';
      ctx.fillStyle = isCAT ? '#f4f4f5' : isSel ? '#fff' : isNbr ? '#d4d4d8' : '#a1a1aa';
      ctx.globalAlpha = isCAT ? 1 : isSel ? 1 : isNbr ? 0.9 : 0.8;
      const label = n.label.length > 30 ? n.label.slice(0,29)+'…' : n.label;
      ctx.fillText(label, n.x + r + 4/scale, n.y + 4/scale);
    }}
  }}
  ctx.globalAlpha = 1;
  ctx.restore();
}}

// ── 프레임 루프 ───────────────────────────────────────────────────────────
function frame() {{ step(); draw(); requestAnimationFrame(frame); }}
frame();

// ── 선택 & 상세 패널 ──────────────────────────────────────────────────────
const detailEl = document.getElementById('detail');
function selectNode(n) {{
  selected = n;
  document.querySelectorAll('.doc-item').forEach(el =>
    el.classList.toggle('selected', el.dataset.id === (n?.id||''))
  );
  if (n) {{
    const el = document.querySelector(`.doc-item[data-id="${{n.id}}"]`);
    el?.scrollIntoView({{block:'nearest',behavior:'smooth'}});
  }}
  if (!n || n.group==='Category') {{ detailEl.style.display='none'; return; }}
  detailEl.style.display = 'block';
  const kw = (n.keywords||[]).map(k=>`<span class="tag">${{k}}</span>`).join('');
  const related = (nbrs.get(n.id)||[]).slice(0,8)
    .map(r=>`<div class="rel-item" data-id="${{r.id}}">${{r.label}}</div>`).join('');
  detailEl.innerHTML = `
    <h2>${{n.label}}</h2>
    <div class="d-cat">${{n.group}}</div>
    ${{n.summary ? `<div class="d-summary">${{n.summary}}</div>` : ''}}
    ${{kw ? `<div class="d-kw">${{kw}}</div>` : ''}}
    <div class="d-path">${{n.path}}</div>
    ${{related ? `<div class="d-related"><div class="d-related-title">연결 문서</div>${{related}}</div>` : ''}}
  `;
  detailEl.querySelectorAll('.rel-item').forEach(el =>
    el.addEventListener('click', () => jumpTo(byId.get(el.dataset.id)))
  );
}}

function jumpTo(n) {{
  if (!n) return;
  ox = W/2 - n.x*scale; oy = H/2 - n.y*scale;
  selectNode(n);
}}

// ── 사이드바 트리 ─────────────────────────────────────────────────────────
const treeEl = document.getElementById('tree');
const searchEl = document.getElementById('search');
const countEl = document.getElementById('search-count');

function buildTree() {{
  const map = {{}};
  for (const n of nodes) {{
    if (n.group==='Category') continue;
    if (!map[n.group]) map[n.group] = [];
    map[n.group].push(n);
  }}
  return Object.entries(map).sort(([a],[b])=>a.localeCompare(b))
    .map(([cat, items]) => ({{cat, items: items.sort((a,b)=>a.label.localeCompare(b.label))}}));
}}
const TREE = buildTree();

function renderTree(query) {{
  const q = (query||'').trim().toLowerCase();
  let total = 0;
  const html = TREE.map(g => {{
    const cat = g.cat, items = g.items;
    const filtered = q ? items.filter(n =>
      n.label.toLowerCase().includes(q) ||
      (n.path||'').toLowerCase().includes(q) ||
      (n.keywords||[]).some(k=>k.toLowerCase().includes(q)) ||
      (n.summary||'').toLowerCase().includes(q)
    ) : items;
    if (!filtered.length) return '';
    total += filtered.length;
    const color = COLORS[cat]||'#71717a';
    const rows = filtered.map(n =>
      `<div class="doc-item" data-id="${{n.id}}" title="${{n.path||''}}">${{n.label}}</div>`
    ).join('');
    return `<details${{q ? ' open' : ''}}>
      <summary>
        <span class="arrow">&#9654;</span>
        <span class="cat-dot" style="background:${{color}}"></span>
        <span class="cat-label">${{cat}}</span>
        <span class="cat-count">${{filtered.length}}</span>
      </summary>
      ${{rows}}
    </details>`;
  }}).join('');
  treeEl.innerHTML = html;

  // matchSet 업데이트
  if (q) {{
    matchSet = new Set();
    treeEl.querySelectorAll('.doc-item').forEach(el => matchSet.add(el.dataset.id));
    countEl.textContent = total + '개 검색됨';
  }} else {{
    matchSet = null;
    countEl.textContent = '';
  }}

  // 이벤트 바인딩
  treeEl.querySelectorAll('.doc-item').forEach(el => {{
    el.addEventListener('click', () => jumpTo(byId.get(el.dataset.id)));
    el.addEventListener('mouseenter', () => {{ hovered = byId.get(el.dataset.id)||null; }});
    el.addEventListener('mouseleave', () => {{ hovered = null; }});
  }});
}}

searchEl.addEventListener('input', () => renderTree(searchEl.value));
renderTree('');

// ── 줌/팬/드래그 ─────────────────────────────────────────────────────────
canvas.addEventListener('wheel', ev => {{
  ev.preventDefault();
  const rect = canvas.getBoundingClientRect();
  const mx = ev.clientX - rect.left, my = ev.clientY - rect.top;
  const d = ev.deltaY > 0 ? 0.82 : 1.22;
  ox = mx - (mx-ox)*d; oy = my - (my-oy)*d;
  scale = Math.min(10, Math.max(0.1, scale*d));
}}, {{passive:false}});

canvas.addEventListener('pointerdown', ev => {{
  const rect = canvas.getBoundingClientRect();
  const mx = ev.clientX-rect.left, my = ev.clientY-rect.top;
  const [gx, gy] = toGraph(mx, my);
  pointerDownPos = [ev.clientX, ev.clientY]; didMove = false;
  drag = nodes.find(n => Math.hypot(n.x-gx, n.y-gy) < 14/scale) || null;
  if (!drag) {{ panning=true; panAnchor=[ev.clientX-ox, ev.clientY-oy]; }}
  canvas.classList.add('grabbing');
  canvas.setPointerCapture(ev.pointerId);
}});

canvas.addEventListener('pointermove', ev => {{
  if (pointerDownPos) {{
    const dx = ev.clientX-pointerDownPos[0], dy = ev.clientY-pointerDownPos[1];
    if (Math.hypot(dx,dy) > 4) {{ didMove=true; if (!simActive){{simActive=true; simSteps=Math.min(simSteps,550);}} }}
  }}
  const rect = canvas.getBoundingClientRect();
  const mx = ev.clientX-rect.left, my = ev.clientY-rect.top;
  if (drag) {{
    const [gx,gy] = toGraph(mx,my);
    drag.x=gx; drag.y=gy; drag.vx=drag.vy=0;
  }} else if (panning && panAnchor) {{
    ox=ev.clientX-panAnchor[0]; oy=ev.clientY-panAnchor[1];
  }} else {{
    const [gx,gy] = toGraph(mx,my);
    hovered = nodes.find(n=>Math.hypot(n.x-gx,n.y-gy)<10/scale)||null;
  }}
}});

canvas.addEventListener('pointerup', ev => {{
  if (!didMove) {{
    const rect = canvas.getBoundingClientRect();
    const mx=ev.clientX-rect.left, my=ev.clientY-rect.top;
    const [gx,gy] = toGraph(mx,my);
    const clicked = nodes.find(n=>Math.hypot(n.x-gx,n.y-gy)<14/scale)||null;
    selectNode(clicked);
  }}
  drag=null; panning=false; panAnchor=null; pointerDownPos=null;
  canvas.classList.remove('grabbing');
}});

// ── 줌 버튼 ──────────────────────────────────────────────────────────────
document.getElementById('z-in').addEventListener('click', () => {{
  scale=Math.min(10,scale*1.3); ox=W/2-(W/2-ox)*1.3; oy=H/2-(H/2-oy)*1.3;
}});
document.getElementById('z-out').addEventListener('click', () => {{
  scale=Math.max(0.1,scale*0.77); ox=W/2-(W/2-ox)*0.77; oy=H/2-(H/2-oy)*0.77;
}});
document.getElementById('z-fit').addEventListener('click', fitAll);
</script>
</body>
</html>""")


def main() -> int:
    docs = scan_docs()
    graph = write_vault(docs)
    print(VAULT)
    print(f"source_docs={len(docs)} nodes={len(graph['nodes'])} edges={len(graph['edges'])}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
