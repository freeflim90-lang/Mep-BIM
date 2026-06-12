# 프로젝트 경로 SSOT — backend/core/paths.py 의 값을 셸로 export 한다.
# 사용법:  source "$(dirname "$0")/lib/paths.sh"   (scripts/ 직속 스크립트 기준)
#
# 이 파일 자체에는 경로를 하드코딩하지 않는다. (paths.py 단일 출처 유지)

_PATHS_SH_DIR="$(cd "$(dirname "${BASH_SOURCE[0]:-$0}")" && pwd)"
LUA_PROJECT_ROOT_BOOTSTRAP="$(cd "$_PATHS_SH_DIR/../.." && pwd)"

eval "$(cd "$LUA_PROJECT_ROOT_BOOTSTRAP" && PYTHONPATH="$LUA_PROJECT_ROOT_BOOTSTRAP" python3 backend/core/paths.py)"

unset _PATHS_SH_DIR LUA_PROJECT_ROOT_BOOTSTRAP
