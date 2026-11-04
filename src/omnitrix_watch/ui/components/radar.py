"""Futuristic 360-degree circular radar display component for BLE scanning."""

from __future__ import annotations

import math
import tkinter as tk
from typing import Optional

from omnitrix_watch.models.device import DeviceSummary
from omnitrix_watch.ui.theme import (
    BORDER_COLOR,
    OMNI_CORE_GLOW,
    OMNI_GREEN,
    OMNI_GREEN_DARK,
    OMNI_GREEN_DIM,
    OMNI_GREEN_GLOW,
)


class OmnitrixRadarCanvas(tk.Canvas):
    """Futuristic 360-degree radar display plotting discovered Bluetooth peripherals."""

    def __init__(self, parent: tk.Widget, size: int = 150, **kwargs) -> None:
        super().__init__(
            parent,
            width=size,
            height=size,
            bg="#030805",
            highlightthickness=1,
            highlightbackground=BORDER_COLOR,
            **kwargs,
        )
        self.size = size
        self.cx = size / 2
        self.cy = size / 2
        self.radius = (size / 2) - 12
        self.radar_angle = 0.0
        self.is_scanning = False
        self.devices: list[tuple[float, float, str, bool]] = []
        self.draw()

    def update_scan_state(self, scanning: bool) -> None:
        """Update active scanning state."""
        self.is_scanning = scanning
        self.draw()

    def update_devices(self, dev_list: list[DeviceSummary], selected_addr: Optional[str] = None) -> None:
        """Map discovered devices to radar coordinates based on hash and signal strength."""
        self.devices.clear()
        for dev in dev_list:
            addr_hash = sum(ord(c) for c in dev.address)
            angle = (addr_hash % 360) * (math.pi / 180.0)

            rssi = dev.rssi if dev.rssi is not None else -75
            clamped_rssi = max(-95, min(-40, rssi))
            dist_ratio = 0.25 + ((-40 - clamped_rssi) / 55.0) * 0.62

            is_sel = (dev.address == selected_addr)
            label = dev.display_name[:10]
            self.devices.append((angle, dist_ratio, label, is_sel))
        self.draw()

    def tick_animation(self) -> None:
        """Advance the rotating radar beam."""
        if self.is_scanning:
            self.radar_angle = (self.radar_angle + 0.12) % (2 * math.pi)
            self.draw()

    def draw(self) -> None:
        """Render radar grid, sweep beam, and target blips."""
        self.delete("all")
        cx, cy, r = self.cx, self.cy, self.radius

        # 1. Bezel ring and concentric range rings
        self.create_oval(cx - r, cy - r, cx + r, cy + r, outline=OMNI_GREEN_DARK, width=2)
        self.create_oval(cx - r * 0.66, cy - r * 0.66, cx + r * 0.66, cy + r * 0.66, outline="#0d2818", width=1)
        self.create_oval(cx - r * 0.33, cy - r * 0.33, cx + r * 0.33, cy + r * 0.33, outline="#0d2818", width=1)

        # 2. Crosshair grid axes
        self.create_line(cx - r, cy, cx + r, cy, fill="#0d2818", width=1)
        self.create_line(cx, cy - r, cx, cy + r, fill="#0d2818", width=1)

        # 3. Rotating radar sweep line
        if self.is_scanning:
            sweep_x = cx + r * math.cos(self.radar_angle)
            sweep_y = cy + r * math.sin(self.radar_angle)
            self.create_line(cx, cy, sweep_x, sweep_y, fill=OMNI_GREEN_GLOW, width=2)

            trail_angle = self.radar_angle - 0.2
            tx = cx + r * math.cos(trail_angle)
            ty = cy + r * math.sin(trail_angle)
            self.create_line(cx, cy, tx, ty, fill=OMNI_GREEN_DIM, width=1)

        # 4. Draw Device Blips
        for angle, dist_ratio, label, is_sel in self.devices:
            bx = cx + (r * dist_ratio) * math.cos(angle)
            by = cy + (r * dist_ratio) * math.sin(angle)

            if is_sel:
                self.create_rectangle(bx - 6, by - 6, bx + 6, by + 6, outline=OMNI_CORE_GLOW, width=2)
                self.create_oval(bx - 3, by - 3, bx + 3, by + 3, fill=OMNI_GREEN_GLOW, outline="")
                self.create_text(bx, by - 11, text=label, fill=OMNI_GREEN_GLOW, font=("Consolas", 7, "bold"))
            else:
                self.create_oval(bx - 3, by - 3, bx + 3, by + 3, fill=OMNI_GREEN, outline="")

        # 5. Radar status text
        status_txt = "SCANNING" if self.is_scanning else f"{len(self.devices)} TARGETS"
        self.create_text(cx, cy + r - 8, text=status_txt, fill=OMNI_GREEN_DIM, font=("Consolas", 7, "bold"))
