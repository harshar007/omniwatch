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
        self.radius = (size / 2) - 15
        self.angle_offset = 0.0
        self.is_animating = False
        self.state_label = "STANDBY"
        self.state_color = OMNI_GREEN
        self.draw()

    def update_state(self, state: SessionState) -> None:
        """Update visual dial status based on session state."""
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
        """Advance dial rotation animation frame."""
        if self.is_animating:
            self.angle_offset = (self.angle_offset + 0.08) % (2 * math.pi)
            self.draw()

    def draw(self) -> None:
        """Render all layers of the Omnitrix faceplate."""
        self.delete("all")
        cx, cy, r = self.center, self.center, self.radius

        # Outer casing ring (dark titanium alloy motif)
        self.create_oval(
            cx - r, cy - r, cx + r, cy + r,
            fill=BG_PANEL, outline=BORDER_COLOR, width=3
        )

        # Concentric groove
        self.create_oval(
            cx - r + 8, cy - r + 8, cx + r - 8, cy + r - 8,
            outline=OMNI_GREEN_DARK, width=2
        )

        # Outer bezel tick marks
        num_notches = 16
        for i in range(num_notches):
            angle = (i * 2 * math.pi / num_notches) + self.angle_offset
            outer_x = cx + (r - 2) * math.cos(angle)
            outer_y = cy + (r - 2) * math.sin(angle)
            inner_x = cx + (r - 9) * math.cos(angle)
            inner_y = cy + (r - 9) * math.sin(angle)
            tick_color = OMNI_GREEN if (i % 4 == 0) else OMNI_GREEN_DIM
            self.create_line(outer_x, outer_y, inner_x, inner_y, fill=tick_color, width=2)

        # Inner bezel circle
        core_r = r - 22
        self.create_oval(
            cx - core_r, cy - core_r, cx + core_r, cy + core_r,
            fill="#051009", outline=self.state_color, width=2
        )

        # Omnitrix Hourglass / Silhouette motif (two opposing triangles intersecting at center)
        tri_size = core_r * 0.75
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

        glow_fill = self.state_color
        self.create_polygon(top_pts, fill=glow_fill, outline=OMNI_GREEN_DIM, width=2)
        self.create_polygon(bot_pts, fill=glow_fill, outline=OMNI_GREEN_DIM, width=2)

        # Center core ring
        center_core_r = 20
        self.create_oval(
            cx - center_core_r, cy - center_core_r, cx + center_core_r, cy + center_core_r,
            fill=BG_DARK, outline=self.state_color, width=2
        )

        # Status text in center core
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
