"""
지식 축적 모니터 & 마스터 컨트롤러
SSD 사용률을 추적하고 50% 도달 시 텔레그램으로 알림을 보낸다.
Q&A 생성, PDF 수집, 스크립트 수집을 순서대로 실행한다.
"""

from __future__ import annotations

import json
import os
import shutil
import subprocess
import sys
import time
from datetime import datetime
from pathlib import Path

import requests

PROJECT_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_BIM_SCRIPTS_DIR = PROJECT_ROOT / "data" / "bim_scripts"

# 텔레그램 설정
def load_env() -> dict[str, str]:
    env = {}
    env_file = PROJECT_ROOT / ".env"
    if env_file.exists():
        for line in env_file.read_text(encoding="utf-8").splitlines():
            line = line.strip()
            if line and "=" in line and not line.startswith("#"):
                k, v = line.split("=", 1)
                env[k.strip()] = v.strip().strip('"').strip("'")
    return env

ENV = load_env()
TELEGRAM_BOT_TOKEN = ENV.get("TELEGRAM_BOT_TOKEN", "")
TELEGRAM_CHAT_ID = ENV.get("TELEGRAM_CHAT_ID", "")

# 목표 설정
TARGET_PERCENT = 50.0     # 목표 SSD 사용률 (%)
WARN_PERCENT = 45.0       # 경고 알림 사용률 (%)
CHECK_INTERVAL_SEC = 300  # 5분마다 체크

# 상태 파일
STATE_FILE = PROJECT_ROOT / "logs" / "knowledge_accumulation_state.json"


def get_disk_info() -> dict:
    """현재 디스크 사용 정보를 반환한다."""
    usage = shutil.disk_usage("/")
    total_gb = usage.total / (1024**3)
    used_gb = usage.used / (1024**3)
    free_gb = usage.free / (1024**3)
    percent = (usage.used / usage.total) * 100
    return {
        "total_gb": round(total_gb, 2),
        "used_gb": round(used_gb, 2),
        "free_gb": round(free_gb, 2),
        "percent": round(percent, 1),
    }


def get_knowledge_stats() -> dict:
    """지식 베이스 현황 통계를 반환한다."""
    kb_dir = PROJECT_ROOT / "data" / "knowledge_base"
    qa_dir = PROJECT_ROOT / "data" / "qa_dataset"
    pdf_dir = PROJECT_ROOT / "data" / "technical_pdfs"
    scripts_dir = Path(os.environ.get("BIM_SCRIPTS_OUTPUT_DIR", DEFAULT_BIM_SCRIPTS_DIR)).expanduser()

    def dir_size_mb(path: Path) -> float:
        if not path.exists():
            return 0.0
        total = sum(f.stat().st_size for f in path.rglob("*") if f.is_file())
        return round(total / (1024**2), 2)

    def count_files(path: Path, pattern: str = "*") -> int:
        if not path.exists():
            return 0
        return len(list(path.rglob(pattern)))

    kb_lines = 0
    if kb_dir.exists():
        for f in kb_dir.glob("*.md"):
            try:
                kb_lines += len(f.read_text(encoding="utf-8", errors="ignore").splitlines())
            except OSError:
                pass

    qa_count = 0
    if qa_dir.exists():
        for f in qa_dir.glob("*.jsonl"):
            try:
                qa_count += sum(1 for line in f.read_text(encoding="utf-8", errors="ignore").splitlines() if line.strip())
            except OSError:
                pass

    return {
        "knowledge_base": {
            "files": count_files(kb_dir, "*.md"),
            "total_lines": kb_lines,
            "size_mb": dir_size_mb(kb_dir),
        },
        "qa_dataset": {
            "jsonl_files": count_files(qa_dir, "*.jsonl"),
            "total_pairs": qa_count,
            "size_mb": dir_size_mb(qa_dir),
        },
        "technical_pdfs": {
            "pdf_files": count_files(pdf_dir, "*.pdf"),
            "size_mb": dir_size_mb(pdf_dir),
        },
        "bim_scripts": {
            "py_files": count_files(scripts_dir, "*.py"),
            "dyn_files": count_files(scripts_dir, "*.dyn"),
            "size_mb": dir_size_mb(scripts_dir),
        },
    }


def send_telegram(message: str) -> bool:
    """텔레그램 메시지를 전송한다."""
    if not TELEGRAM_BOT_TOKEN or not TELEGRAM_CHAT_ID:
        print(f"[텔레그램 미설정] {message}")
        return False
    try:
        response = requests.post(
            f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage",
            json={
                "chat_id": TELEGRAM_CHAT_ID,
                "text": message,
                "parse_mode": "HTML",
            },
            timeout=10,
        )
        return response.status_code == 200
    except Exception as e:
        print(f"텔레그램 전송 실패: {e}")
        return False


def format_progress_message(disk: dict, stats: dict, milestone: str = "") -> str:
    """진행 상황 텔레그램 메시지를 포맷한다."""
    bar_len = 20
    filled = int(disk["percent"] / 100 * bar_len)
    bar = "█" * filled + "░" * (bar_len - filled)

    msg = f"""📊 <b>LUA BIM LABS 지식 축적 현황</b>
{milestone}
🖥 <b>SSD 사용률: {disk['percent']}%</b>
[{bar}]
총 {disk['total_gb']} GB | 사용 {disk['used_gb']} GB | 여유 {disk['free_gb']} GB

📚 <b>지식 베이스</b>
• MD 파일: {stats['knowledge_base']['files']}개 ({stats['knowledge_base']['total_lines']:,}줄)

❓ <b>Q&A 데이터셋</b>
• 질문-답변 쌍: {stats['qa_dataset']['total_pairs']:,}개 ({stats['qa_dataset']['size_mb']} MB)

📄 <b>기술 문서</b>
• PDF/문서 파일: {stats['technical_pdfs']['pdf_files']}개 ({stats['technical_pdfs']['size_mb']} MB)

🔧 <b>BIM 스크립트</b>
• Python: {stats['bim_scripts']['py_files']}개
• Dynamo: {stats['bim_scripts']['dyn_files']}개 ({stats['bim_scripts']['size_mb']} MB)

🕐 {datetime.now().strftime('%Y-%m-%d %H:%M')}"""
    return msg


def save_state(disk: dict, stats: dict, phase: str) -> None:
    """현재 상태를 파일에 저장한다."""
    STATE_FILE.parent.mkdir(parents=True, exist_ok=True)
    state = {
        "timestamp": datetime.now().isoformat(),
        "phase": phase,
        "disk": disk,
        "stats": stats,
    }
    STATE_FILE.write_text(json.dumps(state, ensure_ascii=False, indent=2), encoding="utf-8")


def run_script(script_name: str) -> bool:
    """수집 스크립트를 실행한다."""
    script_path = PROJECT_ROOT / "scripts" / script_name
    if not script_path.exists():
        print(f"스크립트 없음: {script_path}")
        return False
    print(f"\n▶ {script_name} 실행...")
    try:
        result = subprocess.run(
            [sys.executable, str(script_path)],
            timeout=3600,  # 1시간 타임아웃
            capture_output=False,
            cwd=str(PROJECT_ROOT),
        )
        return result.returncode == 0
    except subprocess.TimeoutExpired:
        print(f"{script_name} 타임아웃")
        return False
    except Exception as e:
        print(f"{script_name} 실행 오류: {e}")
        return False


def main():
    print("=" * 60)
    print("LUA BIM LABS 지식 축적 모니터")
    print(f"시작: {datetime.now().isoformat()}")
    print(f"목표: SSD {TARGET_PERCENT}% 도달")
    print("=" * 60)

    disk = get_disk_info()
    stats = get_knowledge_stats()
    print(f"\n현재 SSD 사용률: {disk['percent']}% ({disk['used_gb']}/{disk['total_gb']} GB)")

    # 초기 상태 알림
    send_telegram(format_progress_message(disk, stats, "🚀 지식 축적 시작"))
    save_state(disk, stats, "시작")

    # Phase 1: Q&A 데이터셋 생성
    print("\n[Phase 1] Q&A 데이터셋 생성...")
    send_telegram("📝 Phase 1: Q&A 데이터셋 생성 시작")
    run_script("generate_qa_dataset.py")

    disk = get_disk_info()
    stats = get_knowledge_stats()
    send_telegram(format_progress_message(disk, stats, "✅ Phase 1 완료 (Q&A 생성)"))
    save_state(disk, stats, "Phase 1 완료")

    # Phase 2: 기술 문서 수집
    print("\n[Phase 2] 기술 문서 수집...")
    send_telegram("📄 Phase 2: 기술 문서 수집 시작")
    run_script("collect_technical_pdfs.py")

    disk = get_disk_info()
    stats = get_knowledge_stats()
    send_telegram(format_progress_message(disk, stats, "✅ Phase 2 완료 (기술 문서)"))
    save_state(disk, stats, "Phase 2 완료")

    # Phase 3: GitHub 스크립트 수집
    print("\n[Phase 3] GitHub BIM 스크립트 수집...")
    send_telegram("🔧 Phase 3: GitHub BIM 스크립트 수집 시작")
    run_script("collect_bim_scripts.py")

    disk = get_disk_info()
    stats = get_knowledge_stats()
    send_telegram(format_progress_message(disk, stats, "✅ Phase 3 완료 (BIM 스크립트)"))
    save_state(disk, stats, "Phase 3 완료")

    # 최종 체크
    disk = get_disk_info()
    stats = get_knowledge_stats()

    print(f"\n최종 SSD 사용률: {disk['percent']}%")

    if disk["percent"] >= TARGET_PERCENT:
        msg = format_progress_message(disk, stats, f"🎉 목표 달성! SSD {TARGET_PERCENT}% 도달")
        send_telegram(msg)
        print(f"\n🎉 목표 달성! SSD {disk['percent']}% ({TARGET_PERCENT}% 목표)")
    else:
        remaining_gb = (disk["total_gb"] * TARGET_PERCENT / 100) - disk["used_gb"]
        msg = format_progress_message(
            disk, stats,
            f"📈 수집 진행 중. 목표까지 약 {remaining_gb:.1f} GB 추가 필요"
        )
        send_telegram(msg)
        print(f"\n현재 {disk['percent']}%. 목표({TARGET_PERCENT}%)까지 {remaining_gb:.1f} GB 더 필요합니다.")
        print("더 많은 데이터 수집을 위해 추가 스크립트 실행이 필요합니다.")

    save_state(disk, stats, "완료")
    print("\n완료!")


if __name__ == "__main__":
    main()
