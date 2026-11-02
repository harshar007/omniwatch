"""Omnitrix Home Screen featuring the animated circular Omnitrix Dial."""

from __future__ import annotations

import math
import tkinter as tk
from tkinter import ttk
from typing import Callable, Optional

from omnitrix_watch.models.device import DeviceSummary
from omnitrix_watch.services.device_session import SessionState
from omnitrix_watch.ui.theme import (
    BG_DARK,
    BG_PANEL,
    BORDER_COLOR,
    COLOR_ERROR,
    COLOR_WARNING,
    FONT_BADGE,
    FONT_BODY,
    FONT_DIAL,
    FONT_HEADING,
    FONT_TITLE,
    OMNI_CORE_GLOW,
    OMNI_GREEN,
    OMNI_GREEN_DARK,
    OMNI_GREEN_DIM,
    OMNI_GREEN_GLOW,
    TEXT_DIM,
    TEXT_MUTED,
    TEXT_PRIMARY,
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
        elif state == SessionState.CONNECTING:
            self.state_label = "SYNCING"
            self.state_color = COLOR_WARNING
            self.is_animating = True
        elif state == SessionState.CONNECTED:
            self.state_label = "LINKED"
            self.state_color = OMNI_GREEN_GLOW
            self.is_animating = False
        elif state == SessionState.INSPECTING:
            self.state_label = "INSPECT"
            self.state_color = OMNI_GREEN
            self.is_animating = True
        elif state == SessionState.ERROR:
            self.state_label = "FAULT"
            self.state_color = COLOR_ERROR
            self.is_animating = False
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

        # 3. Outer bezel tick marks & alien degree markers
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
        # Top triangle pointing down
        top_pts = [
            cx - tri_size, cy - tri_size,
            cx + tri_size, cy - tri_size,
            cx, cy,
        ]
        # Bottom triangle pointing up
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


class HomeScreen(ttk.Frame):
    """Main dashboard screen with dial, telemetry summary, and command actions."""

    def __init__(
        self,
        parent: tk.Widget,
        on_scan: Callable[[], None],
        on_connect: Callable[[], None],
        on_disconnect: Callable[[], None],
        on_inspect: Callable[[], None],
        on_open_picker: Callable[[], None],
        on_open_inventory: Callable[[], None],
    ) -> None:
        super().__init__(parent, style="TFrame")
        self.on_scan = on_scan
        self.on_connect = on_connect
        self.on_disconnect = on_disconnect
        self.on_inspect = on_inspect
        self.on_open_picker = on_open_picker
        self.on_open_inventory = on_open_inventory

        self._build_ui()

    def _build_ui(self) -> None:
        # Header banner
        header_frame = ttk.Frame(self, style="TFrame")
        header_frame.pack(fill="x", padx=20, pady=(15, 10))

        title = ttk.Label(
            header_frame,
            text="OMNITRIX RESEARCH PROTOCOL",
            style="Header.Label",
            font=FONT_TITLE,
            foreground=OMNI_GREEN,
        )
        title.pack(side="left")

        # Security & Mode Badges
        badge_frame = ttk.Frame(header_frame, style="TFrame")
        badge_frame.pack(side="right")

        mode_badge = tk.Label(
            badge_frame,
            text="READ-ONLY MODE",
            bg=OMNI_GREEN_DARK,
            fg=OMNI_GREEN,
            font=FONT_BADGE,
            padx=8,
            pady=3,
            relief="solid",
            bd=1,
        )
        mode_badge.pack(side="right", padx=(5, 0))

        target_badge = tk.Label(
            badge_frame,
            text="TARGET: REDMI WATCH MOVE",
            bg=BG_PANEL,
            fg=TEXT_MUTED,
            font=FONT_BADGE,
            padx=8,
            pady=3,
            relief="solid",
            bd=1,
        )
        target_badge.pack(side="right")

        # Main content layout (Dial on left, Status & Controls on right)
        body = ttk.Frame(self, style="TFrame")
        body.pack(fill="both", expand=True, padx=20, pady=10)

        left_panel = ttk.Frame(body, style="Panel.TFrame", padding=15)
        left_panel.pack(side="left", fill="both", expand=False)

        self.dial = OmnitrixDial(left_panel, size=280)
        self.dial.pack(pady=10)

        # Dial hint
        dial_note = ttk.Label(
            left_panel,
            text="NON-DESTRUCTIVE BLE MONITOR",
            style="Muted.TLabel",
            font=FONT_BADGE,
        )
        dial_note.pack(pady=(0, 5))

        # Right panel: Status cards & controls
        right_panel = ttk.Frame(body, style="TFrame")
        right_panel.pack(side="right", fill="both", expand=True, padx=(15, 0))

        # Device card
        dev_card = ttk.Frame(right_panel, style="Surface.TFrame", padding=12)
        dev_card.pack(fill="x", pady=(0, 10))

        card_title = ttk.Label(
            dev_card,
            text="TARGET DEVICE LINK",
            foreground=OMNI_GREEN,
            font=FONT_HEADING,
        )
        card_title.pack(anchor="w")

        self.lbl_device_name = ttk.Label(
            dev_card,
            text="No peripheral selected",
            foreground=TEXT_PRIMARY,
            font=FONT_BODY,
        )
        self.lbl_device_name.pack(anchor="w", pady=(4, 2))

        self.lbl_device_addr = ttk.Label(
            dev_card,
            text="MAC: N/A | RSSI: N/A",
            foreground=TEXT_MUTED,
            font=FONT_BODY,
        )
        self.lbl_device_addr.pack(anchor="w")

        self.lbl_status = ttk.Label(
            dev_card,
            text="STATUS: Idle / Awaiting Command",
            foreground=TEXT_MUTED,
            font=FONT_BODY,
        )
        self.lbl_status.pack(anchor="w", pady=(6, 0))

        # Controls panel
        controls_card = ttk.Frame(right_panel, style="Surface.TFrame", padding=12)
        controls_card.pack(fill="x", pady=(0, 10))

        ctrl_title = ttk.Label(
            controls_card,
            text="SYSTEM ACTIONS",
            foreground=OMNI_GREEN,
            font=FONT_HEADING,
        )
        ctrl_title.pack(anchor="w", pady=(0, 10))

        btn_grid = ttk.Frame(controls_card, style="Surface.TFrame")
        btn_grid.pack(fill="x")

        self.btn_scan = ttk.Button(
            btn_grid,
            text="1. SCAN BLE",
            style="Omni.TButton",
            command=self.on_scan,
        )
        self.btn_scan.grid(row=0, column=0, padx=4, pady=4, sticky="ew")

        self.btn_pick = ttk.Button(
            btn_grid,
            text="2. SELECT DEVICE",
            style="Omni.TButton",
            command=self.on_open_picker,
        )
        self.btn_pick.grid(row=0, column=1, padx=4, pady=4, sticky="ew")

        self.btn_connect = ttk.Button(
            btn_grid,
            text="3. CONNECT",
            style="Omni.TButton",
            command=self.on_connect,
        )
        self.btn_connect.grid(row=1, column=0, padx=4, pady=4, sticky="ew")

        self.btn_inspect = ttk.Button(
            btn_grid,
            text="4. INSPECT GATT",
            style="Omni.TButton",
            command=self.on_inspect,
        )
        self.btn_inspect.grid(row=1, column=1, padx=4, pady=4, sticky="ew")

        self.btn_disconnect = ttk.Button(
            btn_grid,
            text="DISCONNECT",
            style="Danger.TButton",
            command=self.on_disconnect,
        )
        self.btn_disconnect.grid(row=2, column=0, columnspan=2, padx=4, pady=(8, 4), sticky="ew")

        btn_grid.columnconfigure(0, weight=1)
        btn_grid.columnconfigure(1, weight=1)

        # Telemetry / Log console card
        log_card = ttk.Frame(right_panel, style="Surface.TFrame", padding=10)
        log_card.pack(fill="both", expand=True)

        log_head = ttk.Frame(log_card, style="Surface.TFrame")
        log_head.pack(fill="x")

        ttk.Label(log_head, text="SYSTEM TELEMETRY CONSOLE", foreground=OMNI_GREEN, font=FONT_HEADING).pack(side="left")

        self._wave_index = 0
        self._waveforms = [
            "[ ▂▃▅▆▇▆▅▃ ] MATRIX ONLINE",
            "[ ▃▅▆▇█▇▆▅ ] MATRIX ONLINE",
            "[ ▅▆▇█▇▆▅▃ ] MATRIX ONLINE",
            "[ ▆▇█▇▆▅▃▂ ] MATRIX ONLINE",
            "[ ▇█▇▆▅▃▂  ] MATRIX ONLINE",
            "[ █▇▆▅▃▂ ▂ ] MATRIX ONLINE",
        ]
        self.lbl_matrix_monitor = ttk.Label(
            log_head,
            text=self._waveforms[0],
            foreground=OMNI_GREEN_GLOW,
            font=FONT_BADGE,
        )
        self.lbl_matrix_monitor.pack(side="left", padx=(10, 0))

        btn_view_inv = ttk.Button(
            log_head,
            text="View Inventory",
            style="Omni.TButton",
            command=self.on_open_inventory,
        )
        btn_view_inv.pack(side="right")

        self.txt_log = tk.Text(
            log_card,
            bg=BG_PANEL,
            fg=TEXT_PRIMARY,
            insertbackground=OMNI_GREEN,
            height=7,
            font=("Consolas", 9),
            relief="flat",
            wrap="word",
        )
        self.txt_log.pack(fill="both", expand=True, pady=(6, 0))
        self.txt_log.configure(state="disabled")

    def append_log(self, text: str) -> None:
        """Append log line to telemetry console."""
        self.txt_log.configure(state="normal")
        self.txt_log.insert("end", f"> {text}\n")
        self.txt_log.see("end")
        self.txt_log.configure(state="disabled")

    def tick_animation(self) -> None:
        """Advance dial and HUD telemetry animations."""
        self.dial.tick_animation()
        self._wave_index = (self._wave_index + 1) % len(self._waveforms)
        self.lbl_matrix_monitor.configure(text=self._waveforms[self._wave_index])

    def set_device_info(self, device: Optional[DeviceSummary]) -> None:
        """Update selected device display."""
        if device:
            self.lbl_device_name.configure(text=f"Device: {device.display_name}")
            rssi_str = f"{device.rssi} dBm" if device.rssi is not None else "Unknown"
            self.lbl_device_addr.configure(text=f"Address: {device.sanitized_address} | RSSI: {rssi_str}")
        else:
            self.lbl_device_name.configure(text="No peripheral selected")
            self.lbl_device_addr.configure(text="MAC: N/A | RSSI: N/A")

    def set_status(self, text: str, state: SessionState) -> None:
        """Update status line and dial."""
        self.lbl_status.configure(text=f"STATUS: {text}")
        self.dial.update_state(state)
