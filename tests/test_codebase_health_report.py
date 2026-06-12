from pathlib import Path

from scripts import codebase_health_report as report


def write(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def test_codebase_health_report_summarizes_project(tmp_path: Path):
    write(tmp_path / "backend" / "server.py", "\n".join(["print('x')"] * 600))
    write(tmp_path / "backend" / "helper.py", "print('small')\n")
    write(tmp_path / "tests" / "test_server.py", "\n".join(["assert True"] * 30))
    write(tmp_path / "data" / "knowledge_base" / "note.md", "\n".join(["note"] * 700))
    write(tmp_path / "data" / "bim_scripts" / "vendor.py", "\n".join(["print('vendor')"] * 900))

    result = report.build_report(tmp_path, ignored_dirs=set(), ignored_path_prefixes={"data/bim_scripts/"})

    assert result["summary"]["backend_lines"] == 601
    assert result["summary"]["test_lines"] == 30
    assert result["summary"]["first_party_code_lines"] == 631
    assert result["summary"]["test_to_first_party_code_ratio_percent"] == 4.75
    assert result["largest_files"][0]["path"] == "data/knowledge_base/note.md"
    assert "data/bim_scripts/" in result["excluded_reference_paths"]
    assert all(not item["path"].startswith("data/bim_scripts/") for item in result["largest_files"])
    assert any(risk["area"] == "large_modules" for risk in result["risks"])
    assert any(item["theme"] == "engineering_velocity" for item in result["growth_opportunities"])


def test_codebase_health_markdown_writer(tmp_path: Path):
    result = {
        "summary": {"code_lines": 10},
        "largest_files": [{"path": "backend/a.py", "lines": 10}],
        "risks": [{"severity": "high", "area": "large_modules", "finding": "big", "action": "split"}],
        "growth_opportunities": [{"theme": "velocity", "opportunity": "ship", "next_step": "test"}],
    }
    out = tmp_path / "report.md"

    report.write_markdown(result, out)

    text = out.read_text(encoding="utf-8")
    assert "Codebase Health Report" in text
    assert "`backend/a.py`" in text
    assert "HIGH" in text


def test_codebase_health_markdown_lists_excluded_reference_paths(tmp_path: Path):
    result = {
        "summary": {"code_lines": 10},
        "excluded_reference_paths": ["data/bim_scripts/"],
        "largest_files": [],
        "risks": [],
        "growth_opportunities": [],
    }
    out = tmp_path / "report.md"

    report.write_markdown(result, out)

    text = out.read_text(encoding="utf-8")
    assert "Excluded Reference Paths" in text
    assert "`data/bim_scripts/`" in text
