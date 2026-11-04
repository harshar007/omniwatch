"""Omnitrix Circular Dial Canvas Component with Vector Art and Animations."""

from __future__ import annotations

import math
import tkinter as tk
from typing import Optional

from omnitrix_watch.services.device_session import SessionState
from omnitrix_watch.sound import sound_player
from omnitrix_watch.ui.theme import (
    BG_DARK,
    BG_PANEL,
    BORDER_COLOR,
    COLOR_ERROR,
    COLOR_WARNING,
    FONT_BADGE,
    FONT_DIAL,
    OMNI_CORE_GLOW,
    OMNI_GREEN,
    OMNI_GREEN_DARK,
    OMNI_GREEN_DIM,
    OMNI_GREEN_GLOW,
    TEXT_MUTED,
)


class OmnitrixDial(tk.Canvas):
    """Custom Omnitrix circular dial drawn with vector shapes and state indicators."""

    def __init__(self, parent: tk.Widget, size: int = 260, **kwargs) -> None:
        super().__init__(
            parent,
            width=size,
            height=size,
            bg=BG_DARK,
            highlightthickness=0,
            **kwargs,
        )
        self.size = size
        self.center = size / 2
        self.radius = (size / 2) - 18
        self.angle_offset = 0.0
        self.radar_angle = 0.0
        self.pulse_phase = 0.0
        self.shockwave_radius = 0.0
        self.is_animating = False
        self.current_state = SessionState.IDLE
        self.state_label = "STANDBY"
        self.state_color = OMNI_GREEN

        # Interactive click
        self.bind("<Button-1>", self._on_dial_click)
        self.draw()

    def _on_dial_click(self, _event: tk.Event) -> None:
        """Trigger an expanding shockwave animation when user taps the dial."""
        self.shockwave_radius = 20.0
        sound_player.play_shockwave()
        self.draw()

    def update_state(self, state: SessionState) -> None:
        """Update visual dial status based on session state."""
        self.current_state = state
        if state == SessionState.IDLE:
            self.state_label = "READY"
            self.state_color = OMNI_GREEN
            self.is_animating = False
        elif state == SessionState.SCANNING:
            self.state_label = "SCANNING"
            self.state_color = OMNI_GREEN_GLOW
            self.is_animating = True
            sound_player.play_radar_ping()
        elif state == SessionState.CONNECTING:
            self.state_label = "SYNCING"
            self.state_color = COLOR_WARNING
            self.is_animating = True
        elif state == SessionState.CONNECTED:
            self.state_label = "LINKED"
            self.state_color = OMNI_GREEN_GLOW
            self.is_animating = False
            sound_player.play_alien_select()
        elif state == SessionState.INSPECTING:
            self.state_label = "INSPECT"
            self.state_color = OMNI_GREEN
            self.is_animating = True
            sound_player.play_radar_ping()
        elif state == SessionState.ERROR:
            self.state_label = "FAULT"
            self.state_color = COLOR_ERROR
            self.is_animating = False
            sound_player.play_error()
        self.draw()

    def tick_animation(self) -> None:
        """Advance dial rotation and breathing pulse animation frame."""
        self.pulse_phase = (self.pulse_phase + 0.08) % (2 * math.pi)

        if self.shockwave_radius > 0:
            self.shockwave_radius += 6.0
            if self.shockwave_radius > self.radius * 1.3:
                self.shockwave_radius = 0.0

        if self.is_animating:
            self.angle_offset = (self.angle_offset + 0.08) % (2 * math.pi)
            self.radar_angle = (self.radar_angle + 0.12) % (2 * math.pi)

        self.draw()

    def draw(self) -> None:
        """Render all layers of the futuristic Omnitrix faceplate."""
        self.delete("all")
        cx, cy, r = self.center, self.center, self.radius

        # 1. Cyber Targeting Reticle Corners ⌜ ⌝ ⌞ ⌟
        corner_len = 16
        bracket_pad = 12
        b_left = cx - r - bracket_pad
        b_right = cx + r + bracket_pad
        b_top = cy - r - bracket_pad
        b_bot = cy + r + bracket_pad

        reticle_color = OMNI_GREEN_DARK
        # Top-Left
        self.create_line(b_left, b_top + corner_len, b_left, b_top, fill=reticle_color, width=2)
        self.create_line(b_left, b_top, b_left + corner_len, b_top, fill=reticle_color, width=2)
        # Top-Right
        self.create_line(b_right - corner_len, b_top, b_right, b_top, fill=reticle_color, width=2)
        self.create_line(b_right, b_top, b_right, b_top + corner_len, fill=reticle_color, width=2)
        # Bottom-Left
        self.create_line(b_left, b_bot - corner_len, b_left, b_bot, fill=reticle_color, width=2)
        self.create_line(b_left, b_bot, b_left + corner_len, b_bot, fill=reticle_color, width=2)
        # Bottom-Right
        self.create_line(b_right - corner_len, b_bot, b_right, b_bot, fill=reticle_color, width=2)
        self.create_line(b_right, b_bot, b_right, b_bot - corner_len, fill=reticle_color, width=2)

        # 2. Breathing outer aura
        pulse_alpha = 0.5 + 0.5 * math.sin(self.pulse_phase)
        outer_glow_color = OMNI_GREEN_DIM if pulse_alpha > 0.5 else OMNI_GREEN_DARK

        # Outer casing ring (dark titanium alloy motif)
        self.create_oval(
            cx - r, cy - r, cx + r, cy + r,
            fill=BG_PANEL, outline=BORDER_COLOR, width=3
        )

        # Segmented Power Meter Arcs (12 o'clock, 3 o'clock, 6 o'clock, 9 o'clock)
        for arc_start in [15, 105, 195, 285]:
            self.create_arc(
                cx - r + 4, cy - r + 4, cx + r - 4, cy + r - 4,
                start=arc_start, extent=60, style="arc",
                outline=outer_glow_color, width=3
            )

        # Concentric groove
        self.create_oval(
            cx - r + 8, cy - r + 8, cx + r - 8, cy + r - 8,
            outline=OMNI_GREEN_DARK, width=2
        )

        # 3. Outer bezel tick marks & degree markers
        num_notches = 24
        for i in range(num_notches):
            angle = (i * 2 * math.pi / num_notches) + self.angle_offset
            outer_x = cx + (r - 2) * math.cos(angle)
            outer_y = cy + (r - 2) * math.sin(angle)
            inner_x = cx + (r - 10) * math.cos(angle)
            inner_y = cy + (r - 10) * math.sin(angle)
            tick_color = OMNI_GREEN if (i % 6 == 0) else (OMNI_GREEN_GLOW if (i % 3 == 0) else OMNI_GREEN_DARK)
            self.create_line(outer_x, outer_y, inner_x, inner_y, fill=tick_color, width=2 if (i % 3 == 0) else 1)

        # 4. Degree Labels
        self.create_text(cx, cy - r + 16, text="000°", fill=TEXT_MUTED, font=FONT_BADGE)
        self.create_text(cx + r - 16, cy, text="090°", fill=TEXT_MUTED, font=FONT_BADGE)
        self.create_text(cx, cy + r - 16, text="180°", fill=TEXT_MUTED, font=FONT_BADGE)
        self.create_text(cx - r + 16, cy, text="270°", fill=TEXT_MUTED, font=FONT_BADGE)

        # 5. Inner bezel circle
        core_r = r - 24
        self.create_oval(
            cx - core_r, cy - core_r, cx + core_r, cy + core_r,
            fill="#051009", outline=self.state_color, width=2
        )

        # 6. Active Radar Sweep Line (When scanning or inspecting)
        if self.is_animating:
            sweep_x = cx + core_r * math.cos(self.radar_angle)
            sweep_y = cy + core_r * math.sin(self.radar_angle)
            self.create_line(cx, cy, sweep_x, sweep_y, fill=OMNI_CORE_GLOW, width=3)
            # Fading trail
            trail_angle = self.radar_angle - 0.25
            trail_x = cx + core_r * math.cos(trail_angle)
            trail_y = cy + core_r * math.sin(trail_angle)
            self.create_line(cx, cy, trail_x, trail_y, fill=OMNI_GREEN_DIM, width=1)

        # 7. Omnitrix Hourglass / Silhouette motif (two opposing triangles intersecting at center)
        tri_size = core_r * 0.72
        top_pts = [
            cx - tri_size, cy - tri_size,
            cx + tri_size, cy - tri_size,
            cx, cy,
        ]
        bot_pts = [
            cx - tri_size, cy + tri_size,
            cx + tri_size, cy + tri_size,
            cx, cy,
        ]

        glow_fill = OMNI_GREEN_GLOW if (pulse_alpha > 0.6 and not self.is_animating) else self.state_color
        self.create_polygon(top_pts, fill=glow_fill, outline=OMNI_GREEN_DIM, width=2)
        self.create_polygon(bot_pts, fill=glow_fill, outline=OMNI_GREEN_DIM, width=2)

        # 8. Interactive Shockwave Ripple
        if self.shockwave_radius > 0:
            self.create_oval(
                cx - self.shockwave_radius, cy - self.shockwave_radius,
                cx + self.shockwave_radius, cy + self.shockwave_radius,
                outline=OMNI_CORE_GLOW, width=2
            )

        # 9. Center core ring
        center_core_r = 22
        self.create_oval(
            cx - center_core_r, cy - center_core_r, cx + center_core_r, cy + center_core_r,
            fill=BG_DARK, outline=self.state_color, width=2
        )

        # 10. Status text in center core
        self.create_text(
            cx, cy,
            text=self.state_label,
            fill=self.state_color,
            font=FONT_DIAL,
        )
