"""Ultra-lightweight audio subsystem for Omnitrix sound effects.

Zero external dependencies (uses Python standard library winsound on Windows).
Package footprint is under 40 KB.
"""

from __future__ import annotations

import logging
from pathlib import Path
import sys
from typing import Optional

logger = logging.getLogger(__name__)

# Check if winsound is available (Windows standard library)
try:
    import winsound
    HAS_WINSOUND = True
except ImportError:
    winsound = None  # type: ignore
    HAS_WINSOUND = False


class SoundManager:
    """Manages audio playback for Omnitrix UI sound effects."""

    def __init__(self, assets_dir: Optional[Path] = None) -> None:
        self.enabled = True
        self._sound_cache: dict[str, Path] = {}
        self._assets_dir = assets_dir or self._locate_assets_dir()
        self._load_sounds()

    def _locate_assets_dir(self) -> Path:
        """Locate assets directory across dev, editable, and PyInstaller onefile modes."""
        # 1. PyInstaller frozen executable temporary unpack directory
        base_dir = getattr(sys, "_MEIPASS", None)
        if base_dir:
            cand = Path(base_dir) / "assets" / "sounds"
            if cand.exists():
                return cand

        # 2. Project root assets/sounds
        root_cand = Path(__file__).resolve().parent.parent.parent / "assets" / "sounds"
        if root_cand.exists():
            return root_cand

        # 3. Fallback relative
        return Path("assets/sounds")

    def _load_sounds(self) -> None:
        """Cache paths to all known sound effect files."""
        if not self._assets_dir.exists():
            logger.debug("Sounds directory not found at: %s", self._assets_dir)
            return

        for p in self._assets_dir.glob("*.wav"):
            self._sound_cache[p.stem] = p

    @property
    def is_enabled(self) -> bool:
        """Return True if sound effects are active."""
        return self.enabled

    def set_enabled(self, enabled: bool) -> None:
        """Enable or disable sound effects."""
        self.enabled = enabled

    def toggle(self) -> bool:
        """Toggle mute/unmute state. Returns new state."""
        self.enabled = not self.enabled
        if self.enabled:
            self.play_beep()
        return self.enabled

    def play(self, name: str) -> None:
        """Play a sound effect asynchronously by name."""
        if not self.enabled or not HAS_WINSOUND:
            return

        sound_path = self._sound_cache.get(name)
        if not sound_path or not sound_path.exists():
            return

        try:
            # Play completely non-blocking in background without freezing UI
            winsound.PlaySound(
                str(sound_path),
                winsound.SND_FILENAME | winsound.SND_ASYNC | winsound.SND_NODEFAULT,
            )
        except Exception as err:
            logger.debug("Could not play sound '%s': %s", name, err)

    def play_dial_turn(self) -> None:
        """Futuristic mechanical bezel tick."""
        self.play("dial_turn")

    def play_alien_select(self) -> None:
        """Omnitrix alien selection & lock-in power surge."""
        self.play("alien_select")

    def play_shockwave(self) -> None:
        """Sub-bass alien energy blast / shockwave pulse."""
        self.play("shockwave")

    def play_radar_ping(self) -> None:
        """Sonar/radar detection ping."""
        self.play("radar_ping")

    def play_beep(self) -> None:
        """Standard UI interaction blip."""
        self.play("beep")

    def play_error(self) -> None:
        """Omnitrix low-charge / timeout / error warning buzz."""
        self.play("error")

    def play_popup(self) -> None:
        """Omnitrix core spring pop-up and mechanical latch."""
        self.play("popup")

    def play_transform(self) -> None:
        """Omnitrix slam & alien transformation surge."""
        self.play("transform")

    def play_recharge(self) -> None:
        """Omnitrix galvanic recharge completed chime."""
        self.play("recharge")

    def play_timeout(self) -> None:
        """Omnitrix time-out warning alarm beeps."""
        self.play("timeout")

    def play_self_destruct(self) -> None:
        """Omnitrix self-destruct emergency klaxon."""
        self.play("self_destruct")

    def play_dna_scan(self) -> None:
        """Extraterrestrial DNA scan frequency sweep."""
        self.play("dna_scan")

    def play_master_control(self) -> None:
        """Omnitrix master control authorization chime."""
        self.play("master_control")


# Global sound player instance
sound_player = SoundManager()
