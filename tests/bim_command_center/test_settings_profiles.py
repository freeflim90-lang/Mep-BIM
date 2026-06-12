from pathlib import Path

from backend.bim_command_center.settings_profiles import (
    ProfileScope,
    SettingsProfile,
    SettingsProfileError,
    SettingsProfileStore,
)


def test_save_and_load_office_profile(tmp_path: Path):
    store = SettingsProfileStore(tmp_path)
    profile = SettingsProfile(
        name="office-default",
        scope=ProfileScope.OFFICE,
        description="Office defaults",
        settings={"collision_policy": "skip"},
    )

    path = store.save(profile)
    loaded = store.load(ProfileScope.OFFICE, "office-default")

    assert path.exists()
    assert loaded.settings["collision_policy"] == "skip"
    assert loaded.scope == ProfileScope.OFFICE


def test_office_and_project_profiles_are_separated(tmp_path: Path):
    store = SettingsProfileStore(tmp_path)

    store.save(SettingsProfile(name="default", scope=ProfileScope.OFFICE, settings={"mode": "office"}))
    store.save(SettingsProfile(name="default", scope=ProfileScope.PROJECT, settings={"mode": "project"}))

    assert store.load(ProfileScope.OFFICE, "default").settings["mode"] == "office"
    assert store.load(ProfileScope.PROJECT, "default").settings["mode"] == "project"


def test_rejects_unsupported_version():
    try:
        SettingsProfile.from_dict({
            "name": "bad",
            "scope": "office",
            "version": "9.9",
            "settings": {},
        })
    except SettingsProfileError:
        return
    raise AssertionError("Expected SettingsProfileError")


def test_list_profiles_reports_broken_json(tmp_path: Path):
    store = SettingsProfileStore(tmp_path)
    broken_dir = tmp_path / "office"
    broken_dir.mkdir(parents=True)
    (broken_dir / "broken.json").write_text("{not json", encoding="utf-8")

    rows = store.list_profiles(ProfileScope.OFFICE)

    assert rows[0]["name"] == "broken"
    assert "error" in rows[0]
