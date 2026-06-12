"""프로젝트 경로 단일 출처(SSOT).

모든 백엔드 모듈·스크립트는 경로를 직접 조립하지 말고 이 모듈의 상수를 사용한다.
셸 스크립트는 scripts/lib/paths.sh 를 통해 같은 값을 export 받는다.

환경변수 오버라이드:
  - KNOWLEDGE_BASE_DIR : 에이전트 지식베이스 루트 (롤백/테스트 레버)
  - LUA_KNOWLEDGE_ROOT : knowledge/ 트리 루트
"""
from __future__ import annotations

import os
from pathlib import Path

BACKEND_DIR = Path(__file__).resolve().parents[1]
PROJECT_ROOT = BACKEND_DIR.parent
FRONTEND_DIR = PROJECT_ROOT / "frontend"
DATA_DIR = PROJECT_ROOT / "data"
DOCS_DIR = PROJECT_ROOT / "docs"
CONFIG_DIR = PROJECT_ROOT / "config"
LOGS_DIR = PROJECT_ROOT / "logs"
RUNTIME_DIR = PROJECT_ROOT / "runtime"
SCRIPTS_DIR = PROJECT_ROOT / "scripts"
OBSIDIAN_VAULTS_DIR = PROJECT_ROOT / "obsidian_vaults"
GLOBAL_OBSIDIAN_VAULT = OBSIDIAN_VAULTS_DIR / "lua_bim_lab_global_map"

# ---------------------------------------------------------------------------
# 지식 트리 (knowledge/) — product_knowledge_layers.json 의 4층 승격 모델 기준
#   00_catalog   자동 생성 인덱스 (FILE_MAP.json, KNOWLEDGE_CATALOG.md)
#   10_agents    에이전트별 지식베이스 (팀 폴더 하위)
#   20_qa        에이전트별 QA 지식
#   30_intake    raw_intake 층 (미검수 수집물)
#   40_curation  reviewed_insight 층 (큐레이션·품질 로그)
#   50_domain    product_knowledge 층 (도메인 원천자료)
#   60_public    public_or_training_reuse 층 (공개·교육 재사용)
# ---------------------------------------------------------------------------
KNOWLEDGE_ROOT = Path(os.environ.get("LUA_KNOWLEDGE_ROOT", str(PROJECT_ROOT / "knowledge")))

AGENT_KB_DIR = Path(os.environ.get("KNOWLEDGE_BASE_DIR", str(KNOWLEDGE_ROOT / "10_agents")))
QA_KB_DIR = Path(os.environ.get("KNOWLEDGE_QA_DIR", str(KNOWLEDGE_ROOT / "20_qa")))

# 에이전트 KB 파일 배치: "flat" = 루트 평면 배치, "teams" = 팀 폴더 하위 배치
AGENT_KB_LAYOUT = "teams"
CATALOG_DIR = KNOWLEDGE_ROOT / "00_catalog"

INTAKE_DIR = KNOWLEDGE_ROOT / "30_intake"
TEAM_REQUESTS_DIR = INTAKE_DIR / "team_requests"
CURATION_DIR = KNOWLEDGE_ROOT / "40_curation" / "quality"
KNOWLEDGE_UPDATES_DIR = KNOWLEDGE_ROOT / "40_curation" / "updates"

DOMAIN_DIR = KNOWLEDGE_ROOT / "50_domain"
TECHNICAL_PDFS_DIR = DOMAIN_DIR / "technical_pdfs"
BIM_SCRIPTS_DIR = DOMAIN_DIR / "bim_scripts"
BIMOBJECT_DIR = DOMAIN_DIR / "bimobject"
QA_DATASET_DIR = DOMAIN_DIR / "qa_dataset"
BIM_EDUCATION_DIR = DOMAIN_DIR / "bim_education"

PUBLIC_DIR = KNOWLEDGE_ROOT / "60_public"
BLOGGER_QUEUE_DIR = PUBLIC_DIR / "blogger_queue"
TRAINING_CURRICULUM_DIR = PUBLIC_DIR / "training_curriculum"

# ---------------------------------------------------------------------------
# 제품 트리 (products/)
# ---------------------------------------------------------------------------
PRODUCTS_DIR = PROJECT_ROOT / "products"
STARTER_PLAN_DIR = PRODUCTS_DIR / "starter_plan"
BIM_LAND_DIR = PRODUCTS_DIR / "bim_land"
BIM_COMMAND_CENTER_DIR = PRODUCTS_DIR / "bim_command_center"
AUTODESK_MARKET_DIR = PRODUCTS_DIR / "autodesk_market"

# ---------------------------------------------------------------------------
# 에이전트 팀 → knowledge/10_agents/ 하위 폴더명
# (knowledge_store.ORGANIZATION 의 키와 1:1 — 순환 import 방지를 위해 여기서는
#  폴더명만 정의하고, agent → 폴더 매핑은 knowledge_store 가 조립한다)
# ---------------------------------------------------------------------------
TEAM_DIR_NAMES = {
    "MANAGEMENT": "01_경영진",
    "ESTIMATION_TEAM": "02_견적팀",
    "ENGINEERING_TEAM": "03_엔지니어링팀",
    "REPORTING_TEAM": "04_리포팅팀",
    "ADDIN_DEVELOPMENT_TEAM": "05_애드인개발팀",
    "STORE_COMMERCIALIZATION_TEAM": "06_스토어상용화팀",
    "ADMIN_FINANCE_TEAM": "07_경영지원팀",
    "PEOPLE_ENABLEMENT_TEAM": "08_인재육성팀",
    "KNOWLEDGE_TEAM": "09_지식팀",
}
EXTRA_AGENTS_DIR_NAME = "90_확장에이전트"


def shell_exports() -> str:
    """scripts/lib/paths.sh 가 eval 할 수 있는 export 문 생성."""
    exports = {
        "LUA_PROJECT_ROOT": PROJECT_ROOT,
        "LUA_DATA_DIR": DATA_DIR,
        "LUA_DOCS_DIR": DOCS_DIR,
        "LUA_LOGS_DIR": LOGS_DIR,
        "LUA_RUNTIME_DIR": RUNTIME_DIR,
        "LUA_KNOWLEDGE_ROOT": KNOWLEDGE_ROOT,
        "LUA_AGENT_KB_DIR": AGENT_KB_DIR,
        "LUA_QA_KB_DIR": QA_KB_DIR,
        "LUA_CATALOG_DIR": CATALOG_DIR,
        "LUA_INTAKE_DIR": INTAKE_DIR,
        "LUA_CURATION_DIR": CURATION_DIR,
        "LUA_QA_DATASET_DIR": QA_DATASET_DIR,
        "LUA_TECHNICAL_PDFS_DIR": TECHNICAL_PDFS_DIR,
        "LUA_KNOWLEDGE_UPDATES_DIR": KNOWLEDGE_UPDATES_DIR,
        "LUA_BLOGGER_QUEUE_DIR": BLOGGER_QUEUE_DIR,
        "LUA_PRODUCTS_DIR": PRODUCTS_DIR,
        "LUA_OBSIDIAN_VAULTS_DIR": OBSIDIAN_VAULTS_DIR,
    }
    return "\n".join(f'export {key}="{value}"' for key, value in exports.items())


if __name__ == "__main__":
    print(shell_exports())
