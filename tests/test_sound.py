"""Unit tests for the ultra-lightweight sound subsystem."""

from pathlib import Path
from unittest.mock import patch

from omnitrix_watch.sound import SoundManager


def test_sound_manager_initialization() -> None:
    """Verify sound manager detects available sound assets."""
    sm = SoundManager()
    assert sm.is_enabled is True
    # Should identify at least our 6 generated sounds
    assert "dial_turn" in sm._sound_cache
    assert "alien_select" in sm._sound_cache
    assert "shockwave" in sm._sound_cache
    assert "radar_ping" in sm._sound_cache
    assert "beep" in sm._sound_cache
    assert "error" in sm._sound_cache


def test_sound_manager_toggle_mute() -> None:
    """Verify toggling mute state."""
    sm = SoundManager()
    assert sm.is_enabled is True
    new_state = sm.toggle()
    assert new_state is False
    assert sm.is_enabled is False
    new_state = sm.toggle()
    assert new_state is True
    assert sm.is_enabled is True


def test_sound_manager_play_methods_safely() -> None:
    """Verify play methods execute safely without throwing exceptions."""
    sm = SoundManager()
    with patch("omnitrix_watch.sound.winsound.PlaySound", create=True) as mock_play:
        sm.play_dial_turn()
        sm.play_alien_select()
        sm.play_shockwave()
        sm.play_radar_ping()
        sm.play_beep()
        sm.play_error()
        assert mock_play.call_count == 6


def test_sound_manager_muted_does_not_play() -> None:
    """Verify no sounds are played when sound is disabled."""
    sm = SoundManager()
    sm.set_enabled(False)
    with patch("omnitrix_watch.sound.winsound.PlaySound", create=True) as mock_play:
        sm.play_dial_turn()
        assert mock_play.call_count == 0
