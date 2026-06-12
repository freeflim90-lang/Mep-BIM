from __future__ import annotations

from pathlib import Path

from fastapi import APIRouter

from backend.bim_command_center.feature_registry import list_phase1_features, validate_feature_registry
from backend.bim_command_center.settings_profiles import (
    ProfileScope,
    SettingsProfile,
    SettingsProfileError,
    default_profile_store,
)
from backend.core.paths import BIM_COMMAND_CENTER_DIR, PROJECT_ROOT
from backend.models import SettingsProfileSaveRequest

# project_root 주입(테스트 tmp_path 포함)에도 동일한 상대 구조를 쓴다
_BCC_REL = BIM_COMMAND_CENTER_DIR.relative_to(PROJECT_ROOT)


PRODUCT_NAME = "BIM Command Center for Revit"
SELECTED_ITEM = "BIMlize 기능 범위 내재화 - Phase 1 Simple Features"
BENCHMARK_PRINCIPLE = "Use benchmark scope only; do not copy names, UI, icons, text, or implementation."


def create_bim_command_center_router(*, project_root: Path) -> APIRouter:
    router = APIRouter(prefix="/api/bim-command-center", tags=["bim-command-center"])

    def profile_store():
        return default_profile_store(project_root / _BCC_REL / "settings_profiles")

    @router.get("/features")
    async def bim_command_center_features():
        errors = validate_feature_registry()
        return {
            "status": "ok" if not errors else "invalid",
            "product": PRODUCT_NAME,
            "selected_item": SELECTED_ITEM,
            "principle": BENCHMARK_PRINCIPLE,
            "validation_errors": errors,
            "features": list_phase1_features(),
        }

    @router.get("/settings-profiles")
    async def list_bim_command_center_settings_profiles(scope=None):
        try:
            profile_scope = ProfileScope(scope) if scope else None
            rows = profile_store().list_profiles(profile_scope)
        except (ValueError, SettingsProfileError) as exc:
            return {"status": "rejected", "reason": str(exc)}
        return {"status": "ok", "profiles": rows}

    @router.post("/settings-profiles")
    async def save_bim_command_center_settings_profile(request: SettingsProfileSaveRequest):
        try:
            profile = SettingsProfile(
                name=request.name,
                scope=ProfileScope(request.scope),
                description=request.description,
                settings=request.settings,
            )
            path = profile_store().save(profile)
        except (ValueError, SettingsProfileError) as exc:
            return {"status": "rejected", "reason": str(exc)}
        return {
            "status": "saved",
            "profile": profile.to_dict(),
            "path": path.relative_to(project_root).as_posix(),
        }

    return router
