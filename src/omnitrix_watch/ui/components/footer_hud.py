"""Omnitrix Global HUD Telemetry Bar."""

from __future__ import annotations

import tkinter as tk
from typing import Optional

from omnitrix_watch.sound import sound_player
from omnitrix_watch.ui.theme import (
    BG_DARK,
    BG_PANEL,
    BORDER_COLOR,
    FONT_BADGE,
    OMNI_GREEN,
    OMNI_GREEN_DARK,
    OMNI_GREEN_GLOW,
    TEXT_MUTED,
)


class FooterHUD(tk.Frame):
    """Bottom telemetry HUD bar showing core status, radio state, and safety mode."""

    def __init__(self, parent: tk.Widget, **kwargs) -> None:
        super().__init__(
            parent,
            bg=BG_PANEL,
            bd=1,
            relief="solid",
            highlightthickness=0,
            padx=8,
            pady=3,
            **kwargs,
        )
        # Left status pills
        self.lbl_core = tk.Label(
            self,
            text="⚡ CORE: 100% NOMINAL",
            bg=BG_PANEL,
            fg=OMNI_GREEN,
            font=FONT_BADGE,
            padx=8,
            pady=2,
        )
        self.lbl_core.pack(side="left")

        self.lbl_ble = tk.Label(
            self,
            text="📡 BLE 5.0 ACTIVE",
            bg=BG_PANEL,
            fg=OMNI_GREEN_GLOW,
            font=FONT_BADGE,
            padx=8,
            pady=2,
        )
        self.lbl_ble.pack(side="left")

        self.lbl_safety = tk.Label(
            self,
            text="🛡️ ZERO-WRITE SANCTIONED",
            bg=BG_PANEL,
            fg="#6ee7b7",
            font=FONT_BADGE,
            padx=8,
            pady=2,
        )
        self.lbl_safety.pack(side="left")

        # Right status pills
        self.lbl_target = tk.Label(
            self,
            text="⌚ TARGET: REDMI WATCH MOVE 2",
            bg=OMNI_GREEN_DARK,
            fg=OMNI_GREEN,
            font=FONT_BADGE,
            padx=10,
            pady=2,
        )
        self.lbl_target.pack(side="right")

        self.lbl_hints = tk.Label(
            self,
            text="NAV: [1-6] | SPACE: SLAM | ESC: REVERT",
            bg=BG_PANEL,
            fg=TEXT_MUTED,
            font=("Consolas", 8),
            padx=10,
            pady=2,
        )
        self.lbl_hints.pack(side="right")

    def set_ble_status(self, text: str, color: str = OMNI_GREEN_GLOW) -> None:
        """Update BLE radio status pill."""
        self.lbl_ble.config(text=text, fg=color)

    def set_core_status(self, text: str, color: str = OMNI_GREEN) -> None:
        """Update core status telemetry pill."""
        self.lbl_core.config(text=text, fg=color)
