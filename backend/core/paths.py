from __future__ import annotations

from pathlib import Path

BACKEND_DIR = Path(__file__).resolve().parents[1]
PROJECT_ROOT = BACKEND_DIR.parent
FRONTEND_DIR = PROJECT_ROOT / "frontend"
DATA_DIR = PROJECT_ROOT / "data"
DOCS_DIR = PROJECT_ROOT / "docs"
OBSIDIAN_VAULTS_DIR = PROJECT_ROOT / "obsidian_vaults"
GLOBAL_OBSIDIAN_VAULT = OBSIDIAN_VAULTS_DIR / "lua_bim_lab_global_map"
