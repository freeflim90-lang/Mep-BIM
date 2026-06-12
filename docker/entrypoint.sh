#!/bin/bash
set -e

# Allow existing scripts that hardcode the Mac path to continue working
mkdir -p "/Users/choejeong-yeon"
if [ ! -e "/Users/choejeong-yeon/LUA BIM LABS" ]; then
    ln -sfn /app "/Users/choejeong-yeon/LUA BIM LABS"
fi

# Create venv-style symlinks so shell scripts that call .dev-venv/bin/python work
mkdir -p /app/.dev-venv/bin
ln -sf "$(which python3)" /app/.dev-venv/bin/python 2>/dev/null || true
ln -sf "$(which python3)" /app/.dev-venv/bin/python3 2>/dev/null || true
which uvicorn > /dev/null 2>&1 && ln -sf "$(which uvicorn)" /app/.dev-venv/bin/uvicorn 2>/dev/null || true

# Make env vars available to cron jobs
printenv | grep -v "^_\|^SHLVL\|^LS_COLORS" > /etc/environment 2>/dev/null || true

exec "$@"
