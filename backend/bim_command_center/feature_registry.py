from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Iterable


class FeatureRisk(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"


class ApiDependency(str, Enum):
    NONE = "none"
    REVIT_READ = "revit_read"
    REVIT_WRITE = "revit_write"


@dataclass(frozen=True)
class InternalizedFeature:
    command_id: str
    internal_name: str
    phase: str
    priority: str
    risk: FeatureRisk
    api_dependency: ApiDependency
    dry_run_required: bool
    report_supported: bool
    default_mode: str
    source_direction: str
    safety_notes: tuple[str, ...]

    @property
    def requires_revit_api_gate(self) -> bool:
        return self.api_dependency != ApiDependency.NONE

    def to_dict(self) -> dict:
        return {
            "command_id": self.command_id,
            "internal_name": self.internal_name,
            "phase": self.phase,
            "priority": self.priority,
            "risk": self.risk.value,
            "api_dependency": self.api_dependency.value,
            "dry_run_required": self.dry_run_required,
            "report_supported": self.report_supported,
            "default_mode": self.default_mode,
            "source_direction": self.source_direction,
            "requires_revit_api_gate": self.requires_revit_api_gate,
            "safety_notes": list(self.safety_notes),
        }


INTERNALIZATION_PRINCIPLES = (
    "Do not copy competitor product names, command labels, icons, ribbon layout, help text, or implementation.",
    "Use publicly visible feature categories only as a scope benchmark.",
    "Ship features under BIM Command Center naming and workflows.",
    "Prefer preview, dry-run, and report-first behavior before any model-changing command.",
    "Treat Revit write operations as gated work requiring owner validation on a Revit machine.",
)


PHASE1_FEATURES: tuple[InternalizedFeature, ...] = (
    InternalizedFeature(
        command_id="BCC-SETTINGS-PROFILE",
        internal_name="Settings Profile Manager",
        phase="phase1",
        priority="P0",
        risk=FeatureRisk.LOW,
        api_dependency=ApiDependency.NONE,
        dry_run_required=False,
        report_supported=True,
        default_mode="json_profile_validate",
        source_direction="Common settings backbone for future commands.",
        safety_notes=(
            "Non-Revit core only.",
            "Reject profiles with unsupported schema versions.",
            "Keep office default and project profiles separate.",
        ),
    ),
    InternalizedFeature(
        command_id="BCC-VIEW-TEMPLATE-COPY",
        internal_name="View Template Copier",
        phase="phase1",
        priority="P1",
        risk=FeatureRisk.MEDIUM,
        api_dependency=ApiDependency.REVIT_WRITE,
        dry_run_required=True,
        report_supported=True,
        default_mode="preview_skip_collisions",
        source_direction="Copy selected view templates with a safe collision policy.",
        safety_notes=(
            "Default same-name policy is skip.",
            "Rename and replace require explicit user selection.",
            "Actual copy operation must pass the Revit API gate.",
        ),
    ),
    InternalizedFeature(
        command_id="BCC-TYPE-BATCH-DEFINE",
        internal_name="Type Batch Definer",
        phase="phase1",
        priority="P1",
        risk=FeatureRisk.HIGH,
        api_dependency=ApiDependency.REVIT_WRITE,
        dry_run_required=True,
        report_supported=True,
        default_mode="mandatory_dry_run",
        source_direction="Create or update standard types from controlled JSON/CSV mapping.",
        safety_notes=(
            "Existing types are skipped by default.",
            "Read-only parameters are skipped and reported.",
            "Creation/update requires owner validation on a sample model.",
        ),
    ),
    InternalizedFeature(
        command_id="BCC-TAG-TEXT-ALIGN",
        internal_name="Tag/Text Aligner",
        phase="phase1",
        priority="P1",
        risk=FeatureRisk.MEDIUM,
        api_dependency=ApiDependency.REVIT_WRITE,
        dry_run_required=True,
        report_supported=True,
        default_mode="current_selection_preview",
        source_direction="Align or distribute selected tags and text notes.",
        safety_notes=(
            "Current selection only.",
            "Pinned annotations are skipped.",
            "Leader preservation is the default policy.",
        ),
    ),
    InternalizedFeature(
        command_id="BCC-PROJECT-CLEANUP-AUDIT",
        internal_name="Project Cleanup Lite",
        phase="phase1",
        priority="P1",
        risk=FeatureRisk.LOW,
        api_dependency=ApiDependency.REVIT_READ,
        dry_run_required=True,
        report_supported=True,
        default_mode="audit_report_only",
        source_direction="Report project clutter before any cleanup action is added.",
        safety_notes=(
            "Audit/report only in first release.",
            "Deletion and cleanup actions are explicitly excluded.",
            "Use results as Model Health and QA evidence.",
        ),
    ),
    InternalizedFeature(
        command_id="BCC-SCHEDULE-EXCEL-EXPORT",
        internal_name="Schedule Excel Export",
        phase="phase1",
        priority="P1",
        risk=FeatureRisk.LOW,
        api_dependency=ApiDependency.REVIT_READ,
        dry_run_required=False,
        report_supported=True,
        default_mode="export_only",
        source_direction="Export active schedule data for review and office workflows.",
        safety_notes=(
            "Export only in Phase 1.",
            "Import/sync is Phase 2 and must have a separate write gate.",
            "Preserve field names and visible order in the export report.",
        ),
    ),
)


def list_phase1_features() -> list[dict]:
    return [feature.to_dict() for feature in PHASE1_FEATURES]


def get_feature(command_id: str) -> InternalizedFeature:
    normalized = command_id.strip().upper()
    for feature in PHASE1_FEATURES:
        if feature.command_id == normalized:
            return feature
    raise KeyError(f"Unknown BIM Command Center feature: {command_id}")


def features_requiring_revit_gate(features: Iterable[InternalizedFeature] = PHASE1_FEATURES) -> list[InternalizedFeature]:
    return [feature for feature in features if feature.requires_revit_api_gate]


def validate_feature_registry(features: Iterable[InternalizedFeature] = PHASE1_FEATURES) -> list[str]:
    errors: list[str] = []
    seen: set[str] = set()
    for feature in features:
        if feature.command_id in seen:
            errors.append(f"duplicate command_id: {feature.command_id}")
        seen.add(feature.command_id)
        if not feature.internal_name:
            errors.append(f"{feature.command_id}: internal_name is required")
        if feature.api_dependency == ApiDependency.REVIT_WRITE and not feature.dry_run_required:
            errors.append(f"{feature.command_id}: Revit write commands must require dry-run")
        if not feature.report_supported:
            errors.append(f"{feature.command_id}: Phase 1 commands must support report output")
    return errors

