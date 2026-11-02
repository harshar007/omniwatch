"""Unit tests for the release packaging scripts."""

import sys
from unittest.mock import patch

import pytest

from scripts.build_release import find_pyinstaller_cmd


def test_find_pyinstaller_cmd_success() -> None:
    """Verify PyInstaller command is successfully resolved in environment."""
    cmd = find_pyinstaller_cmd()
    assert isinstance(cmd, list)
    assert len(cmd) >= 1
    # Should resolve either to python -m PyInstaller or an executable path
    if len(cmd) == 3:
        assert cmd[0] == sys.executable
        assert cmd[1] == "-m"
        assert cmd[2] == "PyInstaller"
    else:
        assert "pyinstaller" in cmd[0].lower()


def test_find_pyinstaller_cmd_failure() -> None:
    """Verify FileNotFoundError is raised when PyInstaller is completely absent."""
    with patch("subprocess.run", side_effect=FileNotFoundError("not found")), \
         patch("shutil.which", return_value=None), \
         patch("pathlib.Path.is_file", return_value=False):
        with pytest.raises(FileNotFoundError, match="PyInstaller not found"):
            find_pyinstaller_cmd()
