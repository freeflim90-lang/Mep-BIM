from types import SimpleNamespace

from backend.telegram_team_access import (
    allowed_team_chat_ids,
    load_enabled_team_chat_ids,
    parse_allowed_chat_ids,
    telegram_chat_allowed,
    update_chat_id,
)


def update_with_chat(chat_id):
    return SimpleNamespace(effective_chat=SimpleNamespace(id=chat_id))


def test_parse_allowed_chat_ids_strips_empty_values():
    assert parse_allowed_chat_ids(" 1,2,, 3 ") == {"1", "2", "3"}
    assert parse_allowed_chat_ids("") == set()
    assert parse_allowed_chat_ids(None) == set()


def test_load_enabled_team_chat_ids_ignores_disabled_and_bad_json(tmp_path):
    path = tmp_path / "team_telegram_users.json"
    path.write_text(
        '{"users":[{"telegram_chat_id":"100","status":"active"},{"telegram_chat_id":"200","status":"disabled"},{"telegram_chat_id":" 300 "}]}',
        encoding="utf-8",
    )
    bad = tmp_path / "bad.json"
    bad.write_text("{broken", encoding="utf-8")

    assert load_enabled_team_chat_ids(path) == {"100", "300"}
    assert load_enabled_team_chat_ids(bad) == set()
    assert load_enabled_team_chat_ids(tmp_path / "missing.json") == set()


def test_telegram_chat_allowed_combines_env_and_registry(tmp_path):
    path = tmp_path / "team_telegram_users.json"
    path.write_text('{"users":[{"telegram_chat_id":"300","status":"active"}]}', encoding="utf-8")

    assert allowed_team_chat_ids(env_raw="100,200", registry_path=path) == {"100", "200", "300"}
    assert telegram_chat_allowed(update=update_with_chat(100), env_raw="100", registry_path=path) is True
    assert telegram_chat_allowed(update=update_with_chat(300), env_raw="100", registry_path=path) is True
    assert telegram_chat_allowed(update=update_with_chat(999), env_raw="100", registry_path=path) is False


def test_telegram_chat_allowed_defaults_open_when_no_allowlist(tmp_path):
    assert telegram_chat_allowed(update=update_with_chat(999), env_raw="", registry_path=tmp_path / "missing.json") is True
    assert update_chat_id(SimpleNamespace(effective_chat=None)) == ""
