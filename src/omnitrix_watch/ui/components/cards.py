"""Reusable Cyber/Omnitrix styled UI cards, telemetry widgets, and signal meters."""

from __future__ import annotations

import tkinter as tk
from tkinter import ttk
from typing import Optional

from omnitrix_watch.ui.theme import (
    BG_DARK,
    BG_PANEL,
    BG_SURFACE,
    BORDER_COLOR,
    BORDER_BRIGHT,
    COLOR_CYAN,
    FONT_BADGE,
    FONT_HEADING,
    FONT_MONO,
    OMNI_CORE_GLOW,
    OMNI_GREEN,
    OMNI_GREEN_DARK,
    OMNI_GREEN_DIM,
    OMNI_GREEN_GLOW,
    TEXT_MUTED,
    TEXT_PRIMARY,
)


class CyberCard(tk.Frame):
    """Futuristic card container with illuminated header, borders, and corner brackets."""

    def __init__(
        self,
        parent: tk.Widget,
        title: Optional[str] = None,
        subtitle: Optional[str] = None,
        accent_color: str = OMNI_GREEN,
        **kwargs,
    ) -> None:
        super().__init__(
            parent,
            bg=BG_PANEL,
            highlightthickness=1,
            highlightbackground=BORDER_COLOR,
            padx=12,
            pady=10,
            **kwargs,
        )
        self.accent_color = accent_color

        if title:
            header_bar = tk.Frame(self, bg=BG_PANEL)
            header_bar.pack(fill="x", pady=(0, 8))

            # Left illuminated accent bar
            accent_bar = tk.Frame(header_bar, bg=accent_color, width=3, height=14)
            accent_bar.pack(side="left", padx=(0, 6), fill="y")

            lbl_title = tk.Label(
                header_bar,
                text=title.upper(),
                bg=BG_PANEL,
                fg=accent_color,
                font=FONT_HEADING,
            )
            lbl_title.pack(side="left")

            if subtitle:
                lbl_sub = tk.Label(
                    header_bar,
                    text=f"// {subtitle.upper()}",
                    bg=BG_PANEL,
                    fg=TEXT_MUTED,
                    font=FONT_BADGE,
                )
                lbl_sub.pack(side="left", padx=(8, 0))

        # Inner body container
        self.body = tk.Frame(self, bg=BG_PANEL)
        self.body.pack(fill="both", expand=True)


class StatBadge(tk.Frame):
    """Compact telemetry chip displaying label and active value."""

    def __init__(
        self,
        parent: tk.Widget,
        label: str,
        value: str = "--",
        color: str = OMNI_GREEN_GLOW,
        **kwargs,
    ) -> None:
        super().__init__(
            parent,
            bg=BG_SURFACE,
            highlightthickness=1,
            highlightbackground=BORDER_COLOR,
            padx=8,
            pady=4,
            **kwargs,
        )
        self.lbl_tag = tk.Label(
            self,
            text=label.upper(),
            bg=BG_SURFACE,
            fg=TEXT_MUTED,
            font=("Consolas", 8, "bold"),
        )
        self.lbl_tag.pack(anchor="w")

        self.lbl_val = tk.Label(
            self,
            text=value,
            bg=BG_SURFACE,
            fg=color,
            font=("Consolas", 11, "bold"),
        )
        self.lbl_val.pack(anchor="w", pady=(1, 0))

    def set_value(self, value: str, color: Optional[str] = None) -> None:
        """Update displayed stat value and color."""
        self.lbl_val.config(text=value)
        if color:
            self.lbl_val.config(fg=color)


class SignalMeter(tk.Canvas):
    """Graphic 5-bar signal strength meter for Bluetooth RSSI."""

    def __init__(self, parent: tk.Widget, width: int = 50, height: int = 18, **kwargs) -> None:
        super().__init__(
            parent,
            width=width,
            height=height,
            bg=BG_PANEL,
            highlightthickness=0,
            **kwargs,
        )
        self.w = width
        self.h = height
        self.rssi: Optional[int] = None
        self.draw()

    def set_rssi(self, rssi: Optional[int]) -> None:
        """Update signal bars based on RSSI value (e.g. -45 dBm is excellent, -95 dBm is weak)."""
        self.rssi = rssi
        self.draw()

    def draw(self) -> None:
        """Draw 5 vertical signal bars."""
        self.delete("all")
        bar_count = 5
        bar_w = 6
        spacing = 3

        if self.rssi is None:
            active_bars = 0
        elif self.rssi >= -55:
            active_bars = 5
        elif self.rssi >= -68:
            active_bars = 4
        elif self.rssi >= -78:
            active_bars = 3
        elif self.rssi >= -88:
            active_bars = 2
        else:
            active_bars = 1

        for i in range(bar_count):
            x0 = i * (bar_w + spacing) + 4
            x1 = x0 + bar_w
            bar_height = (i + 1) * (self.h - 4) / bar_count
            y0 = self.h - 2 - bar_height
            y1 = self.h - 2

            if i < active_bars:
                color = OMNI_GREEN_GLOW if active_bars >= 4 else (OMNI_GREEN if active_bars >= 2 else "#fbbf24")
            else:
                color = "#15241b"

            self.create_rectangle(x0, y0, x1, y1, fill=color, outline="")
