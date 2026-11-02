"""Unit tests for the Omnitrix Watch Face and Alien DNA roster."""

import datetime
import tempfile
from pathlib import Path

from omnitrix_watch.watchface.aliens import (
    DEFAULT_ALIEN_ROSTER,
    get_alien_by_id,
    get_alien_by_name,
    get_all_aliens,
)
from omnitrix_watch.watchface.builder import (
    WatchFaceConfig,
    WatchFaceGenerator,
)


def test_alien_roster_count_and_uniqueness() -> None:
    """Verify that the initial 10 alien DNA profiles exist with distinct IDs."""
    aliens = get_all_aliens()
    assert len(aliens) == 10
    ids = [a.id for a in aliens]
    assert len(set(ids)) == 10
    names = [a.name.lower() for a in aliens]
    assert "heatblast" in names
    assert "diamondhead" in names
    assert "xlr8" in names
    assert "four arms" in names
    assert "grey matter" in names


def test_get_alien_lookups() -> None:
    """Verify alien lookup by ID and by name."""
    hb = get_alien_by_id(1)
    assert hb is not None
    assert hb.name == "Heatblast"
    assert hb.species == "Pyronite"

    xl = get_alien_by_name("xlr8")
    assert xl is not None
    assert xl.id == 3

    missing = get_alien_by_id(999)
    assert missing is None


def test_watchface_config_default_target_device() -> None:
    """Verify watch face configuration defaults strictly to Redmi Watch Move 2."""
    cfg = WatchFaceConfig()
    assert cfg.target_device == "Redmi Watch Move 2"
    assert cfg.screen_width == 390
    assert cfg.screen_height == 450
    assert cfg.time_format_24h is True


def test_watchface_generator_manifest_and_time() -> None:
    """Verify watch face manifest and time formatting output."""
    cfg = WatchFaceConfig(selected_alien_id=2, time_format_24h=True, show_seconds=True)
    gen = WatchFaceGenerator(cfg)

    # Test time formatting
    dt = datetime.datetime(2026, 11, 2, 10, 10, 30)
    time_str = gen.format_time_preview(dt)
    assert time_str == "10:10:30"

    # Test manifest generation
    manifest = gen.generate_manifest()
    assert manifest.target_hardware == "Redmi Watch Move 2"
    assert manifest.selected_alien["name"] == "Diamondhead"
    assert "time_display" in manifest.layout_elements
    assert "alien_silhouette" in manifest.layout_elements
    assert manifest.layout_elements["alien_silhouette"]["alien_name"] == "Diamondhead"


def test_watchface_export_bundle() -> None:
    """Verify export_bundle generates valid JSON manifest and specification sheet."""
    with tempfile.TemporaryDirectory() as tmp_dir:
        out_dir = Path(tmp_dir) / "build_wf"
        gen = WatchFaceGenerator(WatchFaceConfig(selected_alien_id=1))
        manifest_file = gen.export_bundle(out_dir)

        assert manifest_file.exists()
        assert (out_dir / "WATCHFACE_SPEC.md").exists()
        content = manifest_file.read_text(encoding="utf-8")
        assert "Redmi Watch Move 2" in content
        assert "Heatblast" in content
