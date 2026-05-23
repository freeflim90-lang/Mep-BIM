#!/usr/bin/env python3
"""Utilities for the Model Quality Auditor Obsidian vault.

This script keeps the vault lightweight and local-only:
- generates a visual HTML graph from Obsidian wikilinks
- creates dated error/decision/dev-log notes from simple templates
"""

from __future__ import annotations

import argparse
import datetime as dt
import html
import json
import re
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
VAULT = PROJECT_ROOT / "obsidian_vaults" / "model_quality_auditor"
WIKILINK_RE = re.compile(r"\[\[([^\]|#]+)(?:#[^\]|]+)?(?:\|[^\]]+)?\]\]")

GROUP_LABELS = {
    "00_Home": "Home / 전체 지도",
    "01_Project": "프로젝트 전략",
    "02_Development_Log": "개발 로그",
    "03_Errors_Fixes": "오류 오답노트",
    "04_Decisions": "의사결정",
    "05_Revit_API_Gates": "Revit API 검증 게이트",
    "06_Qwen_Drafts": "Qwen 초안",
    "07_Build_Test": "빌드/테스트",
    "08_Knowledge_Map": "지식화 규칙",
    "09_Canvas": "Canvas",
    "README.md": "Vault 안내",
    "Templates": "작성 템플릿",
}

GROUP_PURPOSES = {
    "00_Home": "전체 지식의 진입점과 핵심 인덱스",
    "01_Project": "제품 방향, 별도 프로젝트 전략, Addin Dashboard 병합 계획",
    "02_Development_Log": "일일 개발 기록과 변경 맥락",
    "03_Errors_Fixes": "오류, 원인, 수정, 재발 방지 오답노트",
    "04_Decisions": "기술/제품/패키징 의사결정 근거",
    "05_Revit_API_Gates": "실제 Revit 환경에서 검증해야 하는 API 항목",
    "06_Qwen_Drafts": "Qwen 산출 초안과 검토 대기 자료",
    "07_Build_Test": "빌드, 설치, 테스트 결과와 증빙",
    "08_Knowledge_Map": "개별 기록을 조직 지식으로 승격하는 규칙",
    "09_Canvas": "시각적 배치와 흐름도",
    "README.md": "Vault 사용법과 시작점 안내",
    "Templates": "반복 기록을 위한 표준 양식",
}


def note_title(path: Path) -> str:
    return path.stem


def iter_markdown_notes() -> list[Path]:
    return sorted(
        path for path in VAULT.rglob("*.md")
        if ".obsidian" not in path.parts and path.is_file()
    )


def build_graph() -> dict:
    notes = iter_markdown_notes()
    title_to_path = {note_title(path): path for path in notes}
    nodes = []
    edges = []
    groups: dict[str, list[dict]] = {}

    for path in notes:
        rel = path.relative_to(VAULT).as_posix()
        group = rel.split("/", 1)[0]
        title = note_title(path)
        node = {
            "id": title,
            "label": title,
            "path": rel,
            "group": group,
            "groupLabel": GROUP_LABELS.get(group, group),
            "kind": "template" if group == "Templates" else "index" if "Index" in title or "Knowledge Map" in title or title == "README" else "note",
        }
        nodes.append(node)
        groups.setdefault(group, []).append({
            "id": title,
            "label": title,
            "path": rel,
            "kind": node["kind"],
        })
        text = path.read_text(encoding="utf-8")
        for target in WIKILINK_RE.findall(text):
            target = target.strip()
            if target in title_to_path:
                edges.append({"source": title, "target": target})

    group_data = [
        {
            "id": group,
            "label": GROUP_LABELS.get(group, group),
            "folder": group,
            "purpose": GROUP_PURPOSES.get(group, "분류 목적 미정"),
            "count": len(items),
            "items": sorted(items, key=lambda item: (item["kind"] != "index", item["label"])),
        }
        for group, items in sorted(groups.items())
    ]

    return {"nodes": nodes, "edges": edges, "groups": group_data}


def write_hierarchy_index(graph: dict) -> Path:
    out = VAULT / "08_Knowledge_Map" / "Organizational Knowledge Hierarchy.md"
    sections = []
    for group in graph["groups"]:
        items = "\n".join(
            f"- [[{item['label']}]] — `{item['path']}`"
            for item in group["items"]
        )
        sections.append(f"""## {group['label']}

폴더: `{group['folder']}`  
목적: {group['purpose']}  
문서 수: {group['count']}

{items}
""")
    out.write_text(f"""---
type: hierarchy-moc
project: Model Quality Auditor
status: active
generated: true
tags:
  - mqa
  - hierarchy
  - obsidian
---

# Organizational Knowledge Hierarchy

이 문서는 `Model Quality Auditor` Vault의 지식을 조직 관점에서 하위 분류별로 파악하기 위한 계층형 MOC이다.

그래프는 관계를 보는 데 강하고, 본 문서는 어느 지식이 어떤 업무 분류 아래에 들어가는지 확인하는 데 사용한다.

{chr(10).join(sections)}

## 관련

- [[Model Quality Auditor - Knowledge Map]]
- [[Knowledge Capture Rules]]
- [[Lessons Learned Matrix]]
""", encoding="utf-8")
    return out


def write_graph_html() -> Path:
    graph = build_graph()
    write_hierarchy_index(graph)
    graph = build_graph()
    write_hierarchy_index(graph)
    out = VAULT / "Assets" / "mqa_knowledge_graph.html"
    data = json.dumps(graph, ensure_ascii=False)
    tree = json.dumps(graph["groups"], ensure_ascii=False)
    out.write_text(f"""<!doctype html>
<html lang="ko">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>Model Quality Auditor Knowledge Graph</title>
  <style>
    html, body {{ margin: 0; height: 100%; background: #111113; color: #e5e7eb; font-family: Inter, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif; }}
    #app {{ width: 100vw; height: 100vh; overflow: hidden; position: relative; }}
    canvas {{ display: block; width: 100%; height: 100%; }}
    .panel {{ position: absolute; top: 18px; left: 18px; width: 382px; max-height: calc(100vh - 36px); overflow: auto; padding: 14px 16px; background: rgba(20, 20, 24, .88); border: 1px solid rgba(139, 92, 246, .35); border-radius: 8px; backdrop-filter: blur(10px); box-sizing: border-box; }}
    .panel h1 {{ margin: 0 0 8px; font-size: 16px; }}
    .panel p {{ margin: 4px 0; color: #a1a1aa; font-size: 12px; line-height: 1.45; }}
    .legend {{ display: grid; grid-template-columns: 14px 1fr; gap: 6px 8px; margin-top: 10px; font-size: 12px; color: #d4d4d8; }}
    .swatch {{ width: 12px; height: 12px; border-radius: 50%; margin-top: 2px; }}
    .toolbar {{ display: flex; gap: 8px; margin: 12px 0 10px; }}
    .search {{ width: 100%; min-width: 0; padding: 9px 10px; border: 1px solid rgba(148, 163, 184, .24); border-radius: 6px; background: rgba(2, 6, 23, .55); color: #e5e7eb; font-size: 12px; outline: none; }}
    .search:focus {{ border-color: rgba(139, 92, 246, .72); }}
    .tree {{ margin-top: 12px; border-top: 1px solid rgba(148, 163, 184, .16); padding-top: 10px; }}
    details {{ border: 1px solid rgba(148, 163, 184, .14); border-radius: 7px; margin: 8px 0; background: rgba(15, 23, 42, .34); }}
    summary {{ cursor: pointer; list-style: none; padding: 9px 10px; font-size: 12px; color: #f4f4f5; display: grid; grid-template-columns: 12px 1fr auto; gap: 8px; align-items: center; }}
    summary::-webkit-details-marker {{ display: none; }}
    .count {{ color: #a1a1aa; font-size: 11px; }}
    .purpose {{ color: #a1a1aa; font-size: 11px; line-height: 1.45; padding: 0 10px 8px 30px; }}
    .item {{ display: grid; grid-template-columns: 1fr auto; gap: 8px; padding: 7px 10px 7px 30px; border-top: 1px solid rgba(148, 163, 184, .10); color: #d4d4d8; font-size: 12px; cursor: pointer; }}
    .item:hover, .item.active {{ background: rgba(139, 92, 246, .16); color: #fff; }}
    .kind {{ color: #71717a; font-size: 10px; text-transform: uppercase; }}
    .detail {{ position: absolute; right: 18px; top: 18px; width: 350px; padding: 13px 15px; background: rgba(20, 20, 24, .84); border: 1px solid rgba(148, 163, 184, .22); border-radius: 8px; backdrop-filter: blur(10px); }}
    .detail h2 {{ margin: 0 0 8px; font-size: 14px; }}
    .detail code {{ display: block; color: #93c5fd; word-break: break-all; white-space: normal; font-size: 11px; }}
    .tip {{ position: absolute; right: 18px; bottom: 18px; color: #71717a; font-size: 12px; }}
  </style>
</head>
<body>
  <div id="app">
    <canvas id="graph"></canvas>
    <div class="panel">
      <h1>Model Quality Auditor Knowledge Graph</h1>
      <p>Markdown wikilink 기반 로컬 시각화입니다. Obsidian 없이 브라우저에서도 관계를 확인할 수 있습니다.</p>
      <p>노드: {len(graph["nodes"])} / 링크: {len(graph["edges"])}</p>
      <div class="toolbar"><input id="search" class="search" placeholder="문서명, 폴더, 경로 검색" /></div>
      <div class="legend">
        <span class="swatch" style="background:#8b5cf6"></span><span>Home / Knowledge Map</span>
        <span class="swatch" style="background:#22c55e"></span><span>Project / Qwen / Merge</span>
        <span class="swatch" style="background:#ef4444"></span><span>Errors & Fixes</span>
        <span class="swatch" style="background:#f59e0b"></span><span>Decisions</span>
        <span class="swatch" style="background:#38bdf8"></span><span>Revit API Gates / Build Test</span>
      </div>
      <div id="tree" class="tree"></div>
    </div>
    <div id="detail" class="detail">
      <h2>선택 없음</h2>
      <p>왼쪽 계층 목록이나 그래프 노드를 선택하면 문서 위치와 분류를 확인할 수 있습니다.</p>
      <code>Obsidian에서는 08_Knowledge_Map/Organizational Knowledge Hierarchy.md도 함께 사용하세요.</code>
    </div>
    <div class="tip">Drag nodes. Click tree items or nodes to focus.</div>
  </div>
  <script>
    const graph = {data};
    const tree = {tree};
    const canvas = document.getElementById('graph');
    const ctx = canvas.getContext('2d');
    const treeEl = document.getElementById('tree');
    const detailEl = document.getElementById('detail');
    const searchEl = document.getElementById('search');
    const colors = {{
      '00_Home': '#8b5cf6',
      '01_Project': '#22c55e',
      '02_Development_Log': '#a3e635',
      '03_Errors_Fixes': '#ef4444',
      '04_Decisions': '#f59e0b',
      '05_Revit_API_Gates': '#38bdf8',
      '06_Qwen_Drafts': '#60a5fa',
      '07_Build_Test': '#38bdf8',
      '08_Knowledge_Map': '#c084fc',
      'Templates': '#71717a'
    }};
    let width = 0, height = 0, drag = null, selected = null, query = '';
    function resize() {{
      width = canvas.width = window.innerWidth * devicePixelRatio;
      height = canvas.height = window.innerHeight * devicePixelRatio;
      canvas.style.width = window.innerWidth + 'px';
      canvas.style.height = window.innerHeight + 'px';
      ctx.setTransform(devicePixelRatio, 0, 0, devicePixelRatio, 0, 0);
    }}
    window.addEventListener('resize', resize);
    resize();

    const nodes = graph.nodes.map((n, i) => {{
      const angle = (i / graph.nodes.length) * Math.PI * 2;
      const radius = 180 + (i % 5) * 34;
      return {{...n, x: window.innerWidth / 2 + Math.cos(angle) * radius, y: window.innerHeight / 2 + Math.sin(angle) * radius, vx: 0, vy: 0}};
    }});
    const byId = new Map(nodes.map(n => [n.id, n]));
    const edges = graph.edges.map(e => ({{source: byId.get(e.source), target: byId.get(e.target)}})).filter(e => e.source && e.target);
    function selectNode(id) {{
      selected = byId.get(id) || null;
      document.querySelectorAll('.item').forEach(el => el.classList.toggle('active', el.dataset.id === id));
      if (!selected) return;
      selected.x = window.innerWidth * .58;
      selected.y = window.innerHeight * .50;
      selected.vx = selected.vy = 0;
      detailEl.innerHTML = `<h2>${{selected.label}}</h2><p>${{selected.groupLabel || selected.group}}</p><code>${{selected.path}}</code>`;
    }}
    function renderTree() {{
      const q = query.trim().toLowerCase();
      treeEl.innerHTML = tree.map(group => {{
        const items = group.items.filter(item => !q || `${{item.label}} ${{item.path}} ${{group.label}} ${{group.folder}}`.toLowerCase().includes(q));
        if (!items.length) return '';
        const itemHtml = items.map(item => `<div class="item" data-id="${{item.id}}"><span>${{item.label}}</span><span class="kind">${{item.kind}}</span></div>`).join('');
        return `<details open><summary><span class="swatch" style="background:${{colors[group.folder] || '#71717a'}}"></span><span>${{group.label}}</span><span class="count">${{items.length}}</span></summary><div class="purpose">${{group.purpose}}</div>${{itemHtml}}</details>`;
      }}).join('');
      treeEl.querySelectorAll('.item').forEach(el => el.addEventListener('click', () => selectNode(el.dataset.id)));
    }}
    searchEl.addEventListener('input', () => {{ query = searchEl.value; renderTree(); }});
    renderTree();

    function step() {{
      for (const e of edges) {{
        const dx = e.target.x - e.source.x, dy = e.target.y - e.source.y;
        const d = Math.max(1, Math.hypot(dx, dy));
        const force = (d - 170) * 0.0025;
        const fx = dx / d * force, fy = dy / d * force;
        e.source.vx += fx; e.source.vy += fy; e.target.vx -= fx; e.target.vy -= fy;
      }}
      for (let i = 0; i < nodes.length; i++) for (let j = i + 1; j < nodes.length; j++) {{
        const a = nodes[i], b = nodes[j], dx = b.x - a.x, dy = b.y - a.y;
        const d2 = Math.max(25, dx * dx + dy * dy);
        const f = 900 / d2;
        const d = Math.sqrt(d2);
        a.vx -= dx / d * f; a.vy -= dy / d * f; b.vx += dx / d * f; b.vy += dy / d * f;
      }}
      for (const n of nodes) {{
        if (drag === n) continue;
        n.vx += (window.innerWidth / 2 - n.x) * 0.0008;
        n.vy += (window.innerHeight / 2 - n.y) * 0.0008;
        n.x += n.vx; n.y += n.vy; n.vx *= 0.86; n.vy *= 0.86;
      }}
    }}
    function draw() {{
      ctx.clearRect(0, 0, window.innerWidth, window.innerHeight);
      ctx.lineWidth = 1;
      for (const e of edges) {{
        const active = selected && (e.source === selected || e.target === selected);
        ctx.strokeStyle = active ? 'rgba(196, 181, 253, .86)' : 'rgba(139, 92, 246, .25)';
        ctx.lineWidth = active ? 2.2 : 1;
        ctx.beginPath(); ctx.moveTo(e.source.x, e.source.y); ctx.lineTo(e.target.x, e.target.y); ctx.stroke();
      }}
      for (const n of nodes) {{
        const color = colors[n.group] || '#a1a1aa';
        const isSelected = selected === n;
        const size = isSelected ? 14 : n.group === '00_Home' ? 13 : 8;
        ctx.fillStyle = color;
        ctx.beginPath(); ctx.arc(n.x, n.y, size, 0, Math.PI * 2); ctx.fill();
        if (isSelected) {{ ctx.strokeStyle = '#f8fafc'; ctx.lineWidth = 2; ctx.stroke(); }}
        ctx.fillStyle = '#e5e7eb';
        ctx.font = n.group === '00_Home' ? '14px sans-serif' : '12px sans-serif';
        if (isSelected || n.kind === 'index' || n.group === '00_Home') ctx.fillText(n.label, n.x + size + 5, n.y + 4);
      }}
    }}
    function frame() {{ step(); draw(); requestAnimationFrame(frame); }}
    frame();
    canvas.addEventListener('pointerdown', (ev) => {{
      const rect = canvas.getBoundingClientRect(), x = ev.clientX - rect.left, y = ev.clientY - rect.top;
      drag = nodes.find(n => Math.hypot(n.x - x, n.y - y) < 18) || null;
      if (drag) selectNode(drag.id);
    }});
    canvas.addEventListener('pointermove', (ev) => {{
      if (!drag) return;
      const rect = canvas.getBoundingClientRect();
      drag.x = ev.clientX - rect.left; drag.y = ev.clientY - rect.top; drag.vx = drag.vy = 0;
    }});
    window.addEventListener('pointerup', () => drag = null);
  </script>
</body>
</html>
""", encoding="utf-8")
    return out


def slug(text: str) -> str:
    cleaned = re.sub(r"[^\w가-힣\- ]+", "", text, flags=re.UNICODE).strip()
    return re.sub(r"\s+", " ", cleaned)[:80] or "Untitled"


def create_note(kind: str, title: str) -> Path:
    today = dt.date.today().isoformat()
    mapping = {
        "error": ("03_Errors_Fixes", "ERR", "TEMPLATE_Error_Fix.md"),
        "decision": ("04_Decisions", "DEC", "TEMPLATE_Decision.md"),
        "devlog": ("02_Development_Log", "DEV", "TEMPLATE_Dev_Log.md"),
        "gate": ("05_Revit_API_Gates", "GATE", "TEMPLATE_Revit_API_Test.md"),
    }
    if kind not in mapping:
        raise SystemExit(f"Unknown note kind: {kind}")

    folder, prefix, template = mapping[kind]
    target_dir = VAULT / folder
    existing = sorted(target_dir.glob(f"{prefix}-{today}-*.md"))
    seq = len(existing) + 1
    note_id = f"{prefix}-{today}-{seq:03d}"
    target = target_dir / f"{note_id} {slug(title)}.md"
    template_text = (VAULT / "Templates" / template).read_text(encoding="utf-8")
    content = template_text.replace(f"{prefix}-YYYY-MM-DD-###", note_id)
    content = content.replace("제목", title)
    content = content.replace("{{date}}", today)
    target.write_text(content, encoding="utf-8")
    return target


def main() -> int:
    parser = argparse.ArgumentParser()
    sub = parser.add_subparsers(dest="command", required=True)
    sub.add_parser("graph")
    note = sub.add_parser("new")
    note.add_argument("kind", choices=["error", "decision", "devlog", "gate"])
    note.add_argument("title")
    args = parser.parse_args()

    if args.command == "graph":
        out = write_graph_html()
        print(out)
        return 0
    if args.command == "new":
        out = create_note(args.kind, args.title)
        print(out)
        return 0
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
