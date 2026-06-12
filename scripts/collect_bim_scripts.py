"""
GitHub BIM/Dynamo/Python 스크립트 수집기
오픈소스 BIM 관련 코드를 GitHub에서 수집해 지식 베이스에 추가한다.
"""

from __future__ import annotations

import json
import os
import re
import sys
import time
import shutil
from datetime import datetime
from pathlib import Path

import requests

PROJECT_ROOT = Path(__file__).resolve().parents[1]
import sys as _sys  # noqa: E402
if str(PROJECT_ROOT) not in _sys.path:
    _sys.path.insert(0, str(PROJECT_ROOT))
from backend.core.paths import BIM_SCRIPTS_DIR  # noqa: E402

SCRIPTS_OUTPUT = Path(os.environ.get("BIM_SCRIPTS_OUTPUT_DIR", BIM_SCRIPTS_DIR)).expanduser()
SCRIPTS_OUTPUT.mkdir(parents=True, exist_ok=True)


def _load_github_token() -> str:
    env_file = PROJECT_ROOT / ".env"
    if env_file.exists():
        for line in env_file.read_text(encoding="utf-8").splitlines():
            line = line.strip()
            if line.startswith("GITHUB_TOKEN="):
                return line.split("=", 1)[1].strip().strip('"').strip("'")
    return os.environ.get("GITHUB_TOKEN", "")


GITHUB_TOKEN = _load_github_token()
GITHUB_API = "https://api.github.com"
HEADERS = {
    "Accept": "application/vnd.github+json",
    "User-Agent": "LUA-BIM-LABS-Knowledge-Collector/1.0",
}
if GITHUB_TOKEN:
    HEADERS["Authorization"] = f"Bearer {GITHUB_TOKEN}"
    print(f"GitHub 인증 토큰 적용 완료 (rate limit: 5000/hour)")

# 검색할 쿼리 목록
SEARCH_QUERIES = [
    "dynamo revit MEP python language:python",
    "dynamo revit sprinkler python language:python",
    "revit api MEP python language:python",
    "BIM clash detection python language:python",
    "IFC python openbim language:python",
    "dynamo script hvac language:python",
    "revit dynamo automation MEP",
    "BIM coordination python language:python",
    "navisworks python automation language:python",
    "speckle bim python language:python",
    "pyrevit python scripts",
    "revitpythonwrapper MEP",
    "IfcOpenShell python",
    "blenderbim python script",
    "Autodesk Revit API python",
    "dynamo player script revit",
    "revit family parameter python",
    "MEP duct routing algorithm python",
    "building energy simulation python",
    "IFC viewer python open source",
]

# 수집할 파일 확장자
ALLOWED_EXTENSIONS = {".py", ".dyn", ".json", ".cs", ".ipynb", ".md"}

# 최대 수집 저장소 수
MAX_REPOS_PER_QUERY = 30
MAX_FILES_PER_REPO = 100
TARGET_SIZE_MB = 10000  # 목표 수집 크기 (MB, 약 10 GB)


def get_disk_usage_percent() -> float:
    usage = shutil.disk_usage("/")
    return (usage.used / usage.total) * 100


def search_repositories(query: str) -> list[dict]:
    """GitHub에서 저장소를 검색한다."""
    try:
        response = requests.get(
            f"{GITHUB_API}/search/repositories",
            headers=HEADERS,
            params={
                "q": query,
                "sort": "stars",
                "order": "desc",
                "per_page": MAX_REPOS_PER_QUERY,
            },
            timeout=15,
        )
        if response.status_code == 200:
            return response.json().get("items", [])
        elif response.status_code == 403:
            print(f"  Rate limit 도달. 60초 대기...")
            time.sleep(60)
            return []
        else:
            print(f"  GitHub API 오류: {response.status_code}")
            return []
    except Exception as e:
        print(f"  검색 오류: {e}")
        return []


def get_repo_contents(owner: str, repo: str, path: str = "") -> list[dict]:
    """저장소의 파일 목록을 가져온다."""
    try:
        response = requests.get(
            f"{GITHUB_API}/repos/{owner}/{repo}/contents/{path}",
            headers=HEADERS,
            timeout=15,
        )
        if response.status_code == 200:
            content = response.json()
            return content if isinstance(content, list) else [content]
        return []
    except Exception:
        return []


def download_file(url: str, dest_path: Path) -> bool:
    """파일을 다운로드한다."""
    try:
        response = requests.get(url, headers=HEADERS, timeout=30)
        if response.status_code == 200:
            dest_path.parent.mkdir(parents=True, exist_ok=True)
            dest_path.write_bytes(response.content)
            return True
        return False
    except Exception:
        return False


def collect_repo_files(owner: str, repo: str, path: str = "", depth: int = 0) -> list[Path]:
    """저장소에서 BIM 관련 파일을 재귀적으로 수집한다."""
    if depth > 3:
        return []

    collected = []
    contents = get_repo_contents(owner, repo, path)
    time.sleep(0.1)  # API rate limit 방지 (인증 토큰으로 여유)

    for item in contents:
        if len(collected) >= MAX_FILES_PER_REPO:
            break

        if item["type"] == "file":
            file_path = Path(item["name"])
            if file_path.suffix.lower() in ALLOWED_EXTENSIONS:
                # 저장소 자체가 BIM 검색으로 찾아졌으므로 모든 파일 수집
                dest = SCRIPTS_OUTPUT / owner / repo / item["path"]
                if not dest.exists():
                    if download_file(item["download_url"], dest):
                        collected.append(dest)
                        size_kb = dest.stat().st_size / 1024
                        print(f"    ↓ {item['path']} ({size_kb:.1f} KB)")
                else:
                    collected.append(dest)

        elif item["type"] == "dir":
            sub_files = collect_repo_files(owner, repo, item["path"], depth + 1)
            collected.extend(sub_files)

    return collected


def save_repo_metadata(owner: str, repo: str, repo_info: dict, files: list[Path]) -> None:
    """수집한 저장소 메타데이터를 저장한다."""
    meta_path = SCRIPTS_OUTPUT / owner / repo / "_metadata.json"
    meta_path.parent.mkdir(parents=True, exist_ok=True)
    metadata = {
        "owner": owner,
        "repo": repo,
        "full_name": repo_info.get("full_name"),
        "description": repo_info.get("description"),
        "stars": repo_info.get("stargazers_count", 0),
        "language": repo_info.get("language"),
        "url": repo_info.get("html_url"),
        "topics": repo_info.get("topics", []),
        "collected_at": datetime.now().isoformat(),
        "files_collected": [str(f.relative_to(SCRIPTS_OUTPUT / owner / repo)) for f in files],
    }
    meta_path.write_text(json.dumps(metadata, ensure_ascii=False, indent=2), encoding="utf-8")


def get_collected_size_mb() -> float:
    """현재 수집된 데이터 크기를 MB로 반환한다."""
    total = sum(f.stat().st_size for f in SCRIPTS_OUTPUT.rglob("*") if f.is_file())
    return total / (1024 * 1024)


def main():
    print("=" * 60)
    print("GitHub BIM/Dynamo/Python 스크립트 수집기")
    print(f"시작: {datetime.now().isoformat()}")
    print(f"출력 디렉토리: {SCRIPTS_OUTPUT}")
    print(f"현재 SSD 사용률: {get_disk_usage_percent():.1f}%")
    print("=" * 60)

    seen_repos: set[str] = set()
    total_files = 0
    total_repos = 0

    for query in SEARCH_QUERIES:
        print(f"\n검색: {query}")
        repos = search_repositories(query)
        time.sleep(0.5)

        for repo_info in repos:
            full_name = repo_info.get("full_name", "")
            if full_name in seen_repos:
                continue
            seen_repos.add(full_name)

            owner = repo_info.get("owner", {}).get("login", "")
            repo_name = repo_info.get("name", "")
            stars = repo_info.get("stargazers_count", 0)

            if not owner or not repo_name:
                continue

            print(f"\n  저장소: {full_name} (⭐{stars})")
            files = collect_repo_files(owner, repo_name)

            if files:
                save_repo_metadata(owner, repo_name, repo_info, files)
                total_files += len(files)
                total_repos += 1
                print(f"  → {len(files)}개 파일 수집 완료")

            current_size = get_collected_size_mb()
            print(f"  현재 수집 크기: {current_size:.1f} MB")

            if current_size >= TARGET_SIZE_MB:
                print(f"\n목표 크기({TARGET_SIZE_MB} MB) 도달!")
                break

            time.sleep(0.3)

        current_size = get_collected_size_mb()
        if current_size >= TARGET_SIZE_MB:
            break

    # 최종 보고
    final_size = get_collected_size_mb()
    print("\n" + "=" * 60)
    print("수집 완료!")
    print(f"저장소: {total_repos}개")
    print(f"파일: {total_files}개")
    print(f"수집 크기: {final_size:.1f} MB")
    print(f"현재 SSD 사용률: {get_disk_usage_percent():.1f}%")


if __name__ == "__main__":
    main()
