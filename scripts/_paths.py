"""scripts/ 용 경로 shim — backend.core.paths 를 그대로 재노출한다.

스크립트에서는 PROJECT_ROOT 를 직접 조립하지 말고 다음처럼 사용:

    import sys
    from pathlib import Path
    sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
    from scripts._paths import AGENT_KB_DIR, KNOWLEDGE_ROOT  # noqa
"""
from __future__ import annotations

import sys
from pathlib import Path

_PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(_PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(_PROJECT_ROOT))

from backend.core.paths import *  # noqa: F401,F403,E402
