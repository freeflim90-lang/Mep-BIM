"""
BIM LAND 게임 엔진 API 라우터
  모든 /api/bim-land/* 엔드포인트를 APIRouter 로 묶어 server_total.py 에서 include_router 로 등록한다.
"""
from __future__ import annotations

from fastapi import APIRouter

import backend.bim_land as bim_land
from backend.models import (
    BlockRequest,
    ClaimResolveRequest,
    ContactSubmitRequest,
    GfaReviewRequest,
    LocationChangeRequest,
    ParticipationClaimRequest,
    ProjectRegisterRequest,
    ProjectUpdateRequest,
    ReportRequest,
    ResolveRequest,
    TeamTransferRequest,
)

router = APIRouter(prefix="/api/bim-land", tags=["bim-land"])


# ── 핵심 게임 엔진 ───────────────────────────────────────────────────────────────

@router.post("/sync")
async def bim_land_sync(req: bim_land.SyncRequest):
    """Revit Add-in 이 Central 동기화 완료 시 호출. BIM 밀도 → 영토 등급 → XP → Shadow Strike."""
    try:
        return bim_land.process_sync(req)
    except Exception as exc:
        return {"status": "error", "message": str(exc)}


@router.get("/territories")
async def bim_land_territories():
    return bim_land.get_all_territories()


@router.get("/leaderboard")
async def bim_land_leaderboard(top: int = 10):
    return bim_land.get_leaderboard(top_n=top)


# ── 신고 시스템 ──────────────────────────────────────────────────────────────────

@router.post("/report")
async def bim_land_file_report(req: ReportRequest):
    return bim_land.file_report(
        req.reporter_email, req.reported_email,
        req.project_code, req.reason, req.reporter_phone,
    )


@router.post("/submit-contact")
async def bim_land_submit_contact(req: ContactSubmitRequest):
    return bim_land.submit_contact(req.report_id, req.email, req.phone)


# ── 어드민 전용 ──────────────────────────────────────────────────────────────────

@router.get("/admin/blocked-users")
async def admin_blocked_users():
    return bim_land.get_blocked_users()


@router.post("/admin/block")
async def admin_block_user(req: BlockRequest):
    return bim_land.block_user(req.email, req.reason, req.blocked_by)


@router.delete("/admin/block/{email}")
async def admin_unblock_user(email: str):
    return bim_land.unblock_user(email)


@router.get("/admin/reports")
async def admin_get_reports(status: str = "all"):
    return bim_land.get_reports(status_filter=status)


@router.post("/admin/reports/{report_id}/resolve")
async def admin_resolve_report(report_id: str, req: ResolveRequest):
    return bim_land.resolve_report(report_id, req.action, req.resolved_by)


# ── 프로젝트 레지스트리 ──────────────────────────────────────────────────────────

@router.patch("/admin/projects/{project_code}")
async def admin_update_project(project_code: str, req: ProjectUpdateRequest):
    updates = {k: v for k, v in req.dict().items() if v not in ("", 0.0, []) and v is not None}
    if req.polygon_latlngs is not None:
        updates["polygon_latlngs"] = req.polygon_latlngs
    return bim_land.admin_update_project(project_code, updates)


@router.get("/projects")
async def list_projects():
    return bim_land.get_projects()


@router.get("/projects/{project_code}")
async def get_project(project_code: str):
    project = bim_land.get_project(project_code)
    return project if project else {"status": "not_found"}


@router.post("/admin/projects")
async def admin_register_project(req: ProjectRegisterRequest):
    return bim_land.admin_register_project(
        req.project_code, req.project_name, req.team_name, req.person_name,
        req.address, req.latitude, req.longitude, req.gross_floor_area_m2,
        req.disciplines, req.start_date, req.end_date,
        req.description, req.registered_by,
    )


@router.delete("/admin/projects/{project_code}")
async def admin_delete_project(project_code: str):
    return bim_land.admin_delete_project(project_code)


@router.post("/admin/projects/{project_code}/transfer-team")
async def transfer_team(project_code: str, req: TeamTransferRequest):
    return bim_land.admin_transfer_team(
        project_code, req.new_team_name, req.transferred_by, req.reason
    )


# ── 참여 이력 신청 ────────────────────────────────────────────────────────────────

@router.post("/participation")
async def submit_participation(req: ParticipationClaimRequest):
    return bim_land.submit_participation_claim(
        req.user_email, req.project_code, req.role, req.discipline,
        req.start_date, req.end_date, req.description,
        req.user_phone, req.company,
    )


@router.get("/admin/participation-claims")
async def admin_get_claims(project_code: str = "", status: str = "all"):
    return bim_land.get_participation_claims(project_code, status)


@router.post("/admin/participation-claims/{claim_id}/resolve")
async def admin_resolve_claim(claim_id: str, req: ClaimResolveRequest):
    return bim_land.resolve_participation_claim(claim_id, req.action, req.reviewed_by)


# ── 위치 변경 요청 ────────────────────────────────────────────────────────────────

@router.post("/admin/location-change-requests")
async def submit_location_change(req: LocationChangeRequest, project_code: str = ""):
    return bim_land.submit_location_change_request(
        project_code, req.new_lat, req.new_lng, req.requester, req.reason
    )


@router.post("/admin/location-change-requests/{project_code}")
async def submit_location_change_for_project(project_code: str, req: LocationChangeRequest):
    return bim_land.submit_location_change_request(
        project_code, req.new_lat, req.new_lng, req.requester, req.reason
    )


@router.get("/admin/location-change-requests")
async def get_location_requests(status: str = "all"):
    return bim_land.get_location_change_requests(status)


@router.post("/admin/location-change-requests/{request_id}/resolve")
async def resolve_location_request(request_id: str, req: ClaimResolveRequest):
    return bim_land.resolve_location_change_request(
        request_id, req.action, req.reviewed_by
    )


# ── GFA 심사 ──────────────────────────────────────────────────────────────────────

@router.get("/admin/gfa-review")
async def get_gfa_review(status: str = "all"):
    return bim_land.get_gfa_review_queue(status)


@router.post("/admin/gfa-review/{project_code}")
async def review_gfa(project_code: str, req: GfaReviewRequest):
    return bim_land.review_gfa(project_code, req.action, req.reviewer, req.reason)
