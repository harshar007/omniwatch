"""Unit tests for configuration loading and defaults."""

import tempfile
from pathlib import Path

from omnitrix_watch.config import AppConfig, BLEConfig, LoggingConfig, UIConfig


def test_default_config() -> None:
    """Verify default configuration has expected fallback parameters."""
    cfg = AppConfig()
    assert cfg.ble.scan_duration == 5.0
    assert cfg.ble.connect_timeout == 10.0
    assert cfg.ble.name_filter == ""
    assert cfg.ui.theme == "omnitrix_classic"
    assert cfg.logging.level == "INFO"


def test_load_from_toml() -> None:
    """Verify loading from valid TOML data."""
    toml_content = """
[ble]
scan_duration = 8.5
name_filter = "Redmi"
connect_timeout = 15.0

[ui]
theme = "custom"
window_width = 1000
window_height = 800

[logging]
level = "DEBUG"
log_to_file = false
log_file = "custom.log"
"""
    with tempfile.NamedTemporaryFile("w", suffix=".toml", delete=False) as f:
        f.write(toml_content)
        f_path = Path(f.name)

    try:
        cfg = AppConfig.load(f_path)
        assert cfg.ble.scan_duration == 8.5
        assert cfg.ble.name_filter == "Redmi"
        assert cfg.ble.connect_timeout == 15.0
        assert cfg.ui.window_width == 1000
        assert cfg.ui.window_height == 800
        assert cfg.logging.level == "DEBUG"
        assert cfg.logging.log_to_file is False
    finally:
        f_path.unlink()


def test_load_nonexistent_falls_back_to_defaults() -> None:
    """Verify non-existent config path cleanly defaults without crash."""
    cfg = AppConfig.load("non_existent_file_xyz.toml")
    assert cfg.ble.scan_duration == 5.0
