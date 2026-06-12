from backend.bim_command_center.feature_registry import (
    ApiDependency,
    PHASE1_FEATURES,
    get_feature,
    list_phase1_features,
    validate_feature_registry,
)


def test_phase1_registry_has_expected_features():
    command_ids = {feature.command_id for feature in PHASE1_FEATURES}

    assert command_ids == {
        "BCC-SETTINGS-PROFILE",
        "BCC-VIEW-TEMPLATE-COPY",
        "BCC-TYPE-BATCH-DEFINE",
        "BCC-TAG-TEXT-ALIGN",
        "BCC-PROJECT-CLEANUP-AUDIT",
        "BCC-SCHEDULE-EXCEL-EXPORT",
    }


def test_registry_validation_passes():
    assert validate_feature_registry() == []


def test_revit_write_features_require_dry_run():
    for feature in PHASE1_FEATURES:
        if feature.api_dependency == ApiDependency.REVIT_WRITE:
            assert feature.dry_run_required is True
            assert feature.requires_revit_api_gate is True


def test_list_phase1_features_is_serializable_contract():
    rows = list_phase1_features()

    assert rows
    assert all("command_id" in row for row in rows)
    assert all("requires_revit_api_gate" in row for row in rows)


def test_get_feature_normalizes_command_id():
    feature = get_feature(" bcc-settings-profile ")

    assert feature.internal_name == "Settings Profile Manager"
