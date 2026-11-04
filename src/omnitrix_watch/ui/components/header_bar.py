"""Sci-Fi Omnitrix Header Bar with branding, live clock, and quick audio toggle."""

from __future__ import annotations

import datetime
import tkinter as tk
from tkinter import ttk
from typing import Callable, Optional

from omnitrix_watch.sound import sound_player
from omnitrix_watch.ui.theme import (
    BG_DARK,
    BG_PANEL,
    BG_SURFACE,
    BORDER_COLOR,
    BORDER_BRIGHT,
    FONT_BADGE,
    FONT_HEADING,
    FONT_TITLE,
    OMNI_CORE_GLOW,
    OMNI_GREEN,
    OMNI_GREEN_DARK,
    OMNI_GREEN_DIM,
    OMNI_GREEN_GLOW,
    TEXT_MUTED,
    TEXT_PRIMARY,
)


class HeaderBar(tk.Frame):
    """Top-level sci-fi header banner containing logo, telemetry pills, and audio toggle."""

    def __init__(
        self,
        parent: tk.Widget,
        on_audio_toggle: Optional[Callable[[bool], None]] = None,
        **kwargs,
    ) -> None:
        super().__init__(
            parent,
            bg=BG_PANEL,
            highlightthickness=1,
            highlightbackground=BORDER_COLOR,
            padx=16,
            pady=8,
            **kwargs,
        )
        self.on_audio_toggle = on_audio_toggle

        # Left brand container
        brand_frame = tk.Frame(self, bg=BG_PANEL)
        brand_frame.pack(side="left")

        # Vector Omnitrix mini-logo canvas
        self.logo_canvas = tk.Canvas(brand_frame, width=28, height=28, bg=BG_PANEL, highlightthickness=0)
        self.logo_canvas.pack(side="left", padx=(0, 10))
        self._draw_logo()

        title_box = tk.Frame(brand_frame, bg=BG_PANEL)
        title_box.pack(side="left")

        tk.Label(
            title_box,
            text="OMNITRIX WATCH",
            bg=BG_PANEL,
            fg=OMNI_GREEN,
            font=("Consolas", 14, "bold"),
        ).pack(anchor="w")

        tk.Label(
            title_box,
            text="AZMUTH RESEARCH OS // PROTOCOL v0.1.0",
            bg=BG_PANEL,
            fg=TEXT_MUTED,
            font=("Consolas", 8),
        ).pack(anchor="w")

        # Right actions container
        actions_frame = tk.Frame(self, bg=BG_PANEL)
        actions_frame.pack(side="right")

        # Live Digital System Clock
        self.lbl_clock = tk.Label(
            actions_frame,
            text="--:--:--",
            bg=BG_SURFACE,
            fg=OMNI_GREEN_GLOW,
            font=("Consolas", 10, "bold"),
            padx=10,
            pady=4,
            relief="solid",
            bd=1,
        )
        self.lbl_clock.pack(side="right", padx=(8, 0))

        # Audio Toggle Button
        audio_text = "🔊 SOUND: ON" if sound_player.is_enabled else "🔇 SOUND: MUTED"
        self.btn_sound = tk.Button(
            actions_frame,
            text=audio_text,
            bg=BG_SURFACE,
            fg=OMNI_GREEN if sound_player.is_enabled else TEXT_MUTED,
            activebackground=OMNI_GREEN_DARK,
            activeforeground=OMNI_GREEN_GLOW,
            font=FONT_BADGE,
            padx=10,
            pady=3,
            relief="solid",
            bd=1,
            cursor="hand2",
            command=self._handle_audio_toggle,
        )
        self.btn_sound.pack(side="right", padx=(8, 0))

        # Connection status pill
        self.lbl_status_pill = tk.Label(
            actions_frame,
            text="STANDBY",
            bg=OMNI_GREEN_DARK,
            fg=OMNI_GREEN_GLOW,
            font=FONT_BADGE,
            padx=10,
            pady=4,
            relief="solid",
            bd=1,
        )
        self.lbl_status_pill.pack(side="right", padx=(8, 0))

        self.update_clock()

    def _draw_logo(self) -> None:
        """Render vector mini-Omnitrix hourglass."""
        self.logo_canvas.delete("all")
        cx, cy, r = 14, 14, 12
        self.logo_canvas.create_oval(cx - r, cy - r, cx + r, cy + r, fill="#051009", outline=OMNI_GREEN, width=2)
        # Hourglass triangles
        self.logo_canvas.create_polygon(cx - 7, cy - 8, cx + 7, cy - 8, cx, cy, fill=OMNI_GREEN, outline="")
        self.logo_canvas.create_polygon(cx - 7, cy + 8, cx + 7, cy + 8, cx, cy, fill=OMNI_GREEN, outline="")
        self.logo_canvas.create_oval(cx - 3, cy - 3, cx + 3, cy + 3, fill=BG_DARK, outline=OMNI_GREEN_GLOW, width=1)

    def _handle_audio_toggle(self) -> None:
        """Toggle global sound manager state."""
        new_state = sound_player.toggle()
        if new_state:
            self.btn_sound.config(text="🔊 SOUND: ON", fg=OMNI_GREEN)
            sound_player.play_beep()
        else:
            self.btn_sound.config(text="🔇 SOUND: MUTED", fg=TEXT_MUTED)

        if self.on_audio_toggle:
            self.on_audio_toggle(new_state)

    def set_status(self, text: str, color: str = OMNI_GREEN_GLOW, bg_color: str = OMNI_GREEN_DARK) -> None:
        """Update top-level status pill."""
        self.lbl_status_pill.config(text=text.upper(), fg=color, bg=bg_color)

    def update_clock(self) -> None:
        """Update live system clock display."""
        now_str = datetime.datetime.now().strftime("%H:%M:%S")
        self.lbl_clock.config(text=now_str)
        self.after(1000, self.update_clock)
