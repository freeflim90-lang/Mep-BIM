from pathlib import Path

import pytest

from scripts.addin_dev_paths import addin_dev_source_root, require_addin_dev_source_root


def test_addin_dev_source_root_reads_env_path(tmp_path: Path):
    assert addin_dev_source_root({"BCC_ADDIN_DEV_SOURCE_ROOT": str(tmp_path)}) == tmp_path


def test_require_addin_dev_source_root_rejects_missing_env():
    with pytest.raises(SystemExit) as exc:
        require_addin_dev_source_root({})

    assert "BCC_ADDIN_DEV_SOURCE_ROOT is required" in str(exc.value)


def test_require_addin_dev_source_root_rejects_missing_path(tmp_path: Path):
    missing = tmp_path / "missing"

    with pytest.raises(SystemExit) as exc:
        require_addin_dev_source_root({"BCC_ADDIN_DEV_SOURCE_ROOT": str(missing)})

    assert "does not exist" in str(exc.value)

