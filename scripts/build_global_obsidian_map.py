#!/usr/bin/env python3
"""Build a global Obsidian knowledge map for all important Markdown files.

The generated vault is an index/mirror vault. It does not move or rewrite source
documents. Each source .md gets a lightweight index note with source path,
category, keywords and graph links.
"""

from __future__ import annotations

import html
import json
import re
import shutil
from collections import Counter, defaultdict
from dataclasses import dataclass
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
VAULT = PROJECT_ROOT / "obsidian_vaults" / "lua_bim_lab_global_map"

EXCLUDE_PARTS = {
    ".git",
    ".dev-venv",
    "__pycache__",
    "node_modules",
    "bin",
    "obj",
    "dist",
    ".bkit",
    ".claude",
    ".pdca-snapshots",
}
EXCLUDE_VAULTS = {
    "obsidian_vaults/lua_bim_lab_global_map",
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


_VAULT_EXCEPTIONS = {
    "obsidian_vaults/lua_bim_lab_global_map/NAS_Knowledge",
}


def should_skip(path: Path) -> bool:
    rel = path.relative_to(PROJECT_ROOT).as_posix()
    if any(rel.startswith(exc) for exc in _VAULT_EXCEPTIONS):
        return False  # NAS_Knowledge는 인덱싱 대상
    if any(rel.startswith(prefix) for prefix in EXCLUDE_VAULTS):
        return True
    return any(part in EXCLUDE_PARTS for part in path.parts)


def category_for(rel: str) -> str:
    if rel.startswith("obsidian_vaults/lua_bim_lab_global_map/NAS_Knowledge/"):
        return "NAS Knowledge"
    if rel.startswith("data/knowledge_base/"):
        return "AI Knowledge Base"
    if rel.startswith("docs/standard_documents/"):
        return "Standard Documents"
    if rel.startswith("docs/internal_organization_documents/"):
        return "Internal Organization"
    if rel.startswith("docs/lua_bim_lab_official_documents/"):
        return "Official External Documents"
    if rel.startswith("docs/revenue_products/model_quality_audit/"):
        return "Revenue Product - Model Quality Auditor"
    if rel.startswith("docs/training_curriculum/"):
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


def make_id(rel: str, used: set[str]) -> str:
    stem = Path(rel).stem
    cleaned = re.sub(r"[^\w가-힣\- ]+", " ", stem, flags=re.UNICODE).strip()
    cleaned = re.sub(r"\s+", " ", cleaned) or "Untitled"
    candidate = cleaned[:90]
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
            return line[2:].strip()
    return Path(rel).stem


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


def scan_docs() -> list[Doc]:
    used: set[str] = set()
    docs: list[Doc] = []
    for path in sorted(PROJECT_ROOT.rglob("*.md")):
        if should_skip(path):
            continue
        rel = path.relative_to(PROJECT_ROOT).as_posix()
        try:
            text = path.read_text(encoding="utf-8", errors="ignore")
        except OSError:
            continue
        category = category_for(rel)
        doc_id = make_id(rel, used)
        docs.append(Doc(
            id=doc_id,
            title=extract_title(text, rel),
            path=path,
            rel=rel,
            category=category,
            keywords=extract_keywords(text, rel, category),
            summary=extract_summary(text),
        ))
    return docs


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
    nodes = [{"id": f"CAT::{cat}", "label": cat, "group": "Category", "path": ""} for cat in sorted({d.category for d in docs})]
    for doc in docs:
        nodes.append({
            "id": doc.id,
            "label": doc.title[:72],
            "group": doc.category,
            "path": doc.rel,
        })
    edges = []
    for doc in docs:
        edges.append({"source": f"CAT::{doc.category}", "target": doc.id, "type": "category"})
        for other in related.get(doc.id, [])[:4]:
            edges.append({"source": doc.id, "target": other.id, "type": "related"})
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
    data = json.dumps(graph, ensure_ascii=False)
    groups = sorted({node["group"] for node in graph["nodes"]})
    palette = [
        "#8b5cf6", "#22c55e", "#38bdf8", "#f59e0b", "#ef4444", "#14b8a6",
        "#e879f9", "#84cc16", "#f97316", "#60a5fa", "#d946ef", "#a3a3a3",
    ]
    color_map = {group: palette[i % len(palette)] for i, group in enumerate(groups)}
    color_json = json.dumps(color_map, ensure_ascii=False)
    legend = "\n".join(
        f'<span class="swatch" style="background:{html.escape(color_map[group])}"></span><span>{html.escape(group)}</span>'
        for group in groups[:18]
    )
    write_text(VAULT / "Assets" / "global_knowledge_graph.html", f"""<!doctype html>
<html lang="ko">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>LUA BIM LAB Global Knowledge Graph</title>
  <style>
    html,body{{margin:0;height:100%;background:#111113;color:#e5e7eb;font-family:Inter,-apple-system,BlinkMacSystemFont,"Segoe UI",sans-serif}}
    canvas{{display:block;width:100vw;height:100vh}}
    .panel{{position:absolute;top:18px;left:18px;width:360px;max-height:80vh;overflow:auto;padding:14px 16px;background:rgba(20,20,24,.84);border:1px solid rgba(139,92,246,.38);border-radius:8px;backdrop-filter:blur(10px)}}
    h1{{font-size:16px;margin:0 0 8px}} p{{font-size:12px;color:#a1a1aa;line-height:1.45}}
    .legend{{display:grid;grid-template-columns:14px 1fr;gap:6px 8px;font-size:12px;color:#d4d4d8}}
    .swatch{{width:12px;height:12px;border-radius:50%;margin-top:2px}}
    .tip{{position:absolute;right:18px;bottom:18px;color:#71717a;font-size:12px}}
  </style>
</head>
<body>
<canvas id="graph"></canvas>
<div class="panel">
  <h1>LUA BIM LAB Global Knowledge Graph</h1>
  <p>모든 주요 Markdown 문서를 카테고리와 관련 키워드로 연결한 로컬 그래프입니다.</p>
  <p>Nodes: {len(graph["nodes"])} / Edges: {len(graph["edges"])}</p>
  <div class="legend">{legend}</div>
</div>
<div class="tip">Drag nodes. Category nodes are larger.</div>
<script>
const graph={data};
const colors={color_json};
const canvas=document.getElementById('graph'),ctx=canvas.getContext('2d');
let w=0,h=0,drag=null;
function resize(){{w=canvas.width=innerWidth*devicePixelRatio;h=canvas.height=innerHeight*devicePixelRatio;canvas.style.width=innerWidth+'px';canvas.style.height=innerHeight+'px';ctx.setTransform(devicePixelRatio,0,0,devicePixelRatio,0,0)}} addEventListener('resize',resize); resize();
const nodes=graph.nodes.map((n,i)=>{{let a=i/graph.nodes.length*Math.PI*2,r=n.group==='Category'?170:310+(i%9)*28;return {{...n,x:innerWidth/2+Math.cos(a)*r,y:innerHeight/2+Math.sin(a)*r,vx:0,vy:0}}}});
const by=new Map(nodes.map(n=>[n.id,n]));
const edges=graph.edges.map(e=>({{source:by.get(e.source),target:by.get(e.target),type:e.type}})).filter(e=>e.source&&e.target);
function step(){{for(const e of edges){{let dx=e.target.x-e.source.x,dy=e.target.y-e.source.y,d=Math.max(1,Math.hypot(dx,dy)),want=e.type==='category'?150:210,f=(d-want)*0.0018,fx=dx/d*f,fy=dy/d*f;e.source.vx+=fx;e.source.vy+=fy;e.target.vx-=fx;e.target.vy-=fy}} for(let i=0;i<nodes.length;i++)for(let j=i+1;j<nodes.length;j++){{let a=nodes[i],b=nodes[j],dx=b.x-a.x,dy=b.y-a.y,d2=Math.max(36,dx*dx+dy*dy),d=Math.sqrt(d2),f=(a.group==='Category'||b.group==='Category'?1800:650)/d2;a.vx-=dx/d*f;a.vy-=dy/d*f;b.vx+=dx/d*f;b.vy+=dy/d*f}} for(const n of nodes){{if(drag===n)continue;n.vx+=(innerWidth/2-n.x)*0.00055;n.vy+=(innerHeight/2-n.y)*0.00055;n.x+=n.vx;n.y+=n.vy;n.vx*=0.87;n.vy*=0.87}}}}
function draw(){{ctx.clearRect(0,0,innerWidth,innerHeight);for(const e of edges){{ctx.strokeStyle=e.type==='category'?'rgba(139,92,246,.35)':'rgba(120,120,130,.16)';ctx.lineWidth=e.type==='category'?1.4:.7;ctx.beginPath();ctx.moveTo(e.source.x,e.source.y);ctx.lineTo(e.target.x,e.target.y);ctx.stroke()}} for(const n of nodes){{let category=n.group==='Category',size=category?13:5.5,color=colors[n.group]||'#a1a1aa';ctx.fillStyle=color;ctx.beginPath();ctx.arc(n.x,n.y,size,0,Math.PI*2);ctx.fill();if(category||size>5){{ctx.fillStyle=category?'#f4f4f5':'#d4d4d8';ctx.font=category?'13px sans-serif':'10px sans-serif';ctx.fillText(n.label,n.x+size+5,n.y+4)}}}}}}
function frame(){{step();draw();requestAnimationFrame(frame)}} frame();
canvas.addEventListener('pointerdown',ev=>{{let x=ev.clientX,y=ev.clientY;drag=nodes.find(n=>Math.hypot(n.x-x,n.y-y)<18)||null}});
canvas.addEventListener('pointermove',ev=>{{if(!drag)return;drag.x=ev.clientX;drag.y=ev.clientY;drag.vx=drag.vy=0}});
addEventListener('pointerup',()=>drag=null);
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
