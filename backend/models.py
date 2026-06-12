"""
SECTION 2 ── Pydantic 요청/응답 스키마
  서버 전반에서 공유하는 FastAPI 입력 모델 모음.
  DashboardReply 는 send_state_to_dashboard 에 의존하므로 server_total.py 에 유지.
"""
from __future__ import annotations

from typing import Optional
from pydantic import BaseModel, Field


class AddinTaskRequest(BaseModel):
    target: str = "Revit"
    discipline: str = "공통"
    title: str = "Add-in 개발 요청"
    request: str
    priority: str = "normal"


class KnowledgeUpdateRequest(BaseModel):
    agent: str
    title: str = "공정 지식 업데이트"
    content: str
    source: str = "manual"
    tags: str = ""


class RoutePreviewRequest(BaseModel):
    request: str


class GitHubRepoListRequest(BaseModel):
    limit: int = 20


class LocalCoderDraftRequest(BaseModel):
    request: str
    workflow: str = "excel_qwen_automation"


class QwenProductDraftRunRequest(BaseModel):
    max_tasks: int = 1
    send_telegram: bool = True
    advance_on_blocked: bool = False


class SettingsProfileSaveRequest(BaseModel):
    name: str
    scope: str = "office"
    description: str = ""
    settings: dict = Field(default_factory=dict)


class RevitAssistantChatRequest(BaseModel):
    user_id: str = "revit_user"
    message: str
    revit_context: str = ""
    client_version: str = "RevitLOAChat"
    source: str = "revit-addin"


class RevitAssistantFeedbackRequest(BaseModel):
    user_id: str = "revit_user"
    message: str
    answer: str
    is_good: bool
    note_path: str = ""
    feedback: str = ""


# ── BIM LAND 전용 요청 모델 ──────────────────────────────────────────────────────

class ReportRequest(BaseModel):
    reporter_email: str
    reporter_phone: str
    reported_email: str
    project_code: str
    reason: str


class ContactSubmitRequest(BaseModel):
    report_id: str
    email: str
    phone: str


class BlockRequest(BaseModel):
    email: str
    reason: str
    blocked_by: str = "admin"


class ResolveRequest(BaseModel):
    action: str       # 'block' | 'dismiss'
    resolved_by: str = "admin"


class ProjectRegisterRequest(BaseModel):
    project_code: str = ""
    project_name: str
    team_name: str = ""
    person_name: str = ""
    address: str = ""
    latitude: float = 0.0
    longitude: float = 0.0
    gross_floor_area_m2: float = 0.0
    disciplines: list[str] = Field(default_factory=list)
    start_date: str = ""
    end_date: str = ""
    description: str = ""
    registered_by: str = "admin"


class TeamTransferRequest(BaseModel):
    new_team_name: str
    transferred_by: str = "admin"
    reason: str = ""


class ProjectUpdateRequest(BaseModel):
    project_name: str = ""
    address: str = ""
    latitude: float = 0.0
    longitude: float = 0.0
    gross_floor_area_m2: float = 0.0
    disciplines: list[str] = Field(default_factory=list)
    start_date: str = ""
    end_date: str = ""
    description: str = ""
    polygon_latlngs: Optional[list] = None


class ParticipationClaimRequest(BaseModel):
    user_email: str
    project_code: str
    role: str
    discipline: str
    start_date: str
    end_date: str
    description: str
    user_phone: str = ""
    company: str = ""


class ClaimResolveRequest(BaseModel):
    action: str       # 'approve' | 'reject'
    reviewed_by: str = "admin"


class LocationChangeRequest(BaseModel):
    new_lat: float
    new_lng: float
    requester: str = "admin"
    reason: str = ""


class GfaReviewRequest(BaseModel):
    action: str       # "approve" | "suspend"
    reviewer: str = "admin"
    reason: str = ""
