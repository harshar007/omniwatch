"""Visual preview of the Omnitrix watch face on the Redmi Watch Move 2 AMOLED display."""

from __future__ import annotations

import datetime
import math
import tkinter as tk
from typing import Optional

from omnitrix_watch.ui.theme import (
    BG_DARK,
    BORDER_COLOR,
    OMNI_GREEN,
    OMNI_GREEN_DARK,
    OMNI_GREEN_GLOW,
)
from omnitrix_watch.watchface.aliens import DEFAULT_ALIEN_ROSTER, AlienProfile


class WatchPreviewCanvas(tk.Canvas):
    """Visual preview of the watch face on the Redmi Watch Move 2 AMOLED display."""

    def __init__(self, parent: tk.Widget, width: int = 260, height: int = 300, **kwargs) -> None:
        super().__init__(
            parent,
            width=width,
            height=height,
            bg="#020503",
            highlightthickness=2,
            highlightbackground=BORDER_COLOR,
            **kwargs,
        )
        self.w = width
        self.h = height
        self.selected_alien: AlienProfile = DEFAULT_ALIEN_ROSTER[0]
        self.show_seconds = True
        self.format_24h = True
        self.pulse_phase = 0.0

        self.draw()

    def update_alien(self, alien: AlienProfile) -> None:
        """Switch current alien display."""
        self.selected_alien = alien
        self.draw()

    def tick_animation(self) -> None:
        """Advance time and pulsing glow."""
        self.pulse_phase = (self.pulse_phase + 0.1) % (2 * math.pi)
        self.draw()

    def draw(self) -> None:
        """Render watch face elements simulating Redmi Watch Move 2 screen."""
        self.delete("all")
        cx = self.w / 2
        cy = self.h / 2

        # 1. Bezel of Redmi Watch Move 2 (curved rectangular smartwatch frame)
        self.create_rectangle(
            6, 6, self.w - 6, self.h - 6,
            outline="#1e3828", width=3
        )

        # 2. Outer Omnitrix ring with pulsing glow
        glow_width = 2 + int(math.sin(self.pulse_phase) * 1.5 + 1.5)
        accent_color = self.selected_alien.signature_color
        dial_r = min(self.w, self.h) / 2 - 28

        self.create_oval(
            cx - dial_r, cy - dial_r, cx + dial_r, cy + dial_r,
            outline=OMNI_GREEN, width=glow_width
        )
        self.create_oval(
            cx - dial_r + 6, cy - dial_r + 6, cx + dial_r - 6, cy + dial_r - 6,
            outline=OMNI_GREEN_DARK, width=1
        )

        # 3. Timekeeper display (Top section of watch face)
        now = datetime.datetime.now()
        if self.format_24h:
            time_str = now.strftime("%H:%M:%S" if self.show_seconds else "%H:%M")
        else:
            time_str = now.strftime("%I:%M:%S" if self.show_seconds else "%I:%M")

        self.create_text(
            cx, cy - dial_r + 28,
            text=time_str,
            fill=OMNI_GREEN_GLOW,
            font=("Consolas", 16, "bold"),
        )

        # Date subtitle
        date_str = now.strftime("%a, %b %d").upper()
        self.create_text(
            cx, cy - dial_r + 48,
            text=date_str,
            fill="#a0e8b0",
            font=("Consolas", 8),
        )

        # 4. Omnitrix Hourglass motif in center
        tri_size = 40
        top_pts = [cx - tri_size, cy - 10, cx + tri_size, cy - 10, cx, cy + 20]
        bot_pts = [cx - tri_size, cy + 50, cx + tri_size, cy + 50, cx, cy + 20]
        self.create_polygon(top_pts, fill=accent_color, outline=OMNI_GREEN_DARK, width=1)
        self.create_polygon(bot_pts, fill=accent_color, outline=OMNI_GREEN_DARK, width=1)

        # 5. Alien Core Emblem & Name
        self.create_oval(cx - 18, cy + 18, cx + 18, cy + 54, fill=BG_DARK, outline=OMNI_GREEN_GLOW, width=2)
        self.create_text(
            cx, cy + 36,
            text=f"#{self.selected_alien.id:02d}",
            fill=OMNI_GREEN,
            font=("Consolas", 10, "bold"),
        )

        self.create_text(
            cx, cy + 76,
            text=self.selected_alien.name.upper(),
            fill=accent_color,
            font=("Consolas", 10, "bold"),
        )

        # 6. Complications at bottom (Battery & Pulse)
        self.create_text(
            35, self.h - 22,
            text="⚡ 98%",
            fill=OMNI_GREEN,
            font=("Consolas", 8, "bold"),
        )
        self.create_text(
            self.w - 38, self.h - 22,
            text="♥ 74 BPM",
            fill="#ff3355",
            font=("Consolas", 8, "bold"),
        )
