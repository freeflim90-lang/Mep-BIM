from fastapi import FastAPI
from fastapi.testclient import TestClient

from backend.routers.bim_command_center import create_bim_command_center_router


def test_integrated_app_exposes_bim_command_center_routes():
    import backend.server_total as server

    client = TestClient(server.app)

    response = client.get("/api/bim-command-center/features")

    assert response.status_code == 200
    assert response.json()["product"] == "BIM Command Center for Revit"


def test_bim_command_center_router_exposes_feature_contract(tmp_path):
    app = FastAPI()
    app.include_router(create_bim_command_center_router(project_root=tmp_path))
    client = TestClient(app)

    response = client.get("/api/bim-command-center/features")

    assert response.status_code == 200
    payload = response.json()
    assert payload["status"] == "ok"
    assert payload["product"] == "BIM Command Center for Revit"
    assert payload["validation_errors"] == []
    assert any(feature["command_id"] == "BCC-SETTINGS-PROFILE" for feature in payload["features"])


def test_bim_command_center_router_saves_and_lists_settings_profiles(tmp_path):
    app = FastAPI()
    app.include_router(create_bim_command_center_router(project_root=tmp_path))
    client = TestClient(app)

    saved = client.post(
        "/api/bim-command-center/settings-profiles",
        json={
            "name": "office-default",
            "scope": "office",
            "description": "Default office profile",
            "settings": {"collision_policy": "skip"},
        },
    )
    listed = client.get("/api/bim-command-center/settings-profiles", params={"scope": "office"})

    assert saved.status_code == 200
    assert saved.json()["status"] == "saved"
    assert saved.json()["path"] == "data/bim_command_center/settings_profiles/office/office-default.json"
    assert listed.json()["status"] == "ok"
    assert listed.json()["profiles"] == [
        {
            "name": "office-default",
            "scope": "office",
            "version": "1.0",
            "description": "Default office profile",
            "path": str(tmp_path / "data" / "bim_command_center" / "settings_profiles" / "office" / "office-default.json"),
        }
    ]


def test_bim_command_center_router_rejects_invalid_scope(tmp_path):
    app = FastAPI()
    app.include_router(create_bim_command_center_router(project_root=tmp_path))
    client = TestClient(app)

    response = client.post(
        "/api/bim-command-center/settings-profiles",
        json={"name": "bad", "scope": "invalid", "settings": {}},
    )

    assert response.status_code == 200
    assert response.json()["status"] == "rejected"
