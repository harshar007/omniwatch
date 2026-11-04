"""Omnitrix Home Screen featuring the animated circular Omnitrix Dial."""

from __future__ import annotations

import datetime
import math
import tkinter as tk
from tkinter import ttk
from typing import Callable, Optional

from omnitrix_watch.models.device import DeviceSummary
from omnitrix_watch.services.device_session import SessionState
from omnitrix_watch.sound import sound_player
from omnitrix_watch.ui.components.cards import CyberCard, SignalMeter, StatBadge
from omnitrix_watch.ui.components.dial import OmnitrixDial
from omnitrix_watch.ui.theme import (
    BG_DARK,
    BG_PANEL,
    BG_SURFACE,
    BORDER_COLOR,
    BORDER_BRIGHT,
    COLOR_ERROR,
    COLOR_WARNING,
    FONT_BADGE,
    FONT_BODY,
    FONT_DIAL,
    FONT_HEADING,
    FONT_MONO,
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

# Re-export OmnitrixDial for backward compatibility
__all__ = ["HomeScreen", "OmnitrixDial"]


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
        on_open_watchface: Optional[Callable[[], None]] = None,
        on_open_simulator: Optional[Callable[[], None]] = None,
    ) -> None:
        super().__init__(parent, style="TFrame")
        self.on_scan = on_scan
        self.on_connect = on_connect
        self.on_disconnect = on_disconnect
        self.on_inspect = on_inspect
        self.on_open_picker = on_open_picker
        self.on_open_inventory = on_open_inventory
        self.on_open_watchface = on_open_watchface
        self.on_open_simulator = on_open_simulator

        self._build_ui()

    def _build_ui(self) -> None:
        # Header banner
        header_frame = tk.Frame(self, bg=BG_DARK)
        header_frame.pack(fill="x", padx=16, pady=(12, 8))

        title_box = tk.Frame(header_frame, bg=BG_DARK)
        title_box.pack(side="left")

        tk.Label(
            title_box,
            text="OMNITRIX RESEARCH PROTOCOL",
            bg=BG_DARK,
            fg=OMNI_GREEN,
            font=FONT_TITLE,
        ).pack(anchor="w")

        tk.Label(
            title_box,
            text="GALVAN PRIMARY TELEMETRY & ATTRIBUTE INSPECTOR",
            bg=BG_DARK,
            fg=TEXT_MUTED,
            font=FONT_BADGE,
        ).pack(anchor="w")

        # Security & Mode Badges
        badge_frame = tk.Frame(header_frame, bg=BG_DARK)
        badge_frame.pack(side="right")

        self.btn_sound = tk.Button(
            badge_frame,
            text="🔊 AUDIO: ON",
            bg=BG_PANEL,
            fg=OMNI_GREEN,
            activebackground=OMNI_GREEN_DARK,
            activeforeground=OMNI_GREEN_GLOW,
            font=FONT_BADGE,
            padx=8,
            pady=2,
            relief="solid",
            bd=1,
            cursor="hand2",
            command=self._toggle_audio,
        )
        self.btn_sound.pack(side="right", padx=(6, 0))

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
        mode_badge.pack(side="right", padx=(6, 0))

        target_badge = tk.Label(
            badge_frame,
            text="TARGET: REDMI WATCH MOVE 2",
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
        body = tk.Frame(self, bg=BG_DARK)
        body.pack(fill="both", expand=True, padx=16, pady=6)

        # LEFT COLUMN: Dial & Quick Launchers
        left_col = tk.Frame(body, bg=BG_DARK)
        left_col.pack(side="left", fill="both", expand=False)

        card_dial = CyberCard(left_col, title="Omnitrix Core Dial", subtitle="Vector Reticle")
        card_dial.pack(fill="both", expand=True)

        self.dial = OmnitrixDial(card_dial.body, size=270)
        self.dial.pack(pady=4)

        # Omnitrix Live Timekeeper Display
        self.lbl_timekeeper = tk.Label(
            card_dial.body,
            text="--:--:--",
            bg=BG_PANEL,
            fg=OMNI_GREEN_GLOW,
            font=("Consolas", 11, "bold"),
            padx=10,
            pady=3,
            relief="ridge",
            bd=1,
        )
        self.lbl_timekeeper.pack(fill="x", pady=(2, 4))

        if self.on_open_simulator:
            self.btn_open_sim = tk.Button(
                card_dial.body,
                text="⚡ LAUNCH 3D SIMULATOR",
                bg="#0c3d18",
                fg=OMNI_GREEN_GLOW,
                activebackground=OMNI_GREEN,
                activeforeground="#000000",
                font=("Consolas", 10, "bold"),
                relief="raised",
                bd=2,
                cursor="hand2",
                command=self.on_open_simulator,
            )
            self.btn_open_sim.pack(fill="x", pady=(4, 2))

        if self.on_open_watchface:
            self.btn_open_wf = ttk.Button(
                card_dial.body,
                text="🧬 WATCH FACE & ALIENS",
                style="Omni.TButton",
                command=self.on_open_watchface,
            )
            self.btn_open_wf.pack(fill="x", pady=(2, 0))

        # RIGHT COLUMN: Device Target, Command Center, Console
        right_col = tk.Frame(body, bg=BG_DARK)
        right_col.pack(side="right", fill="both", expand=True, padx=(12, 0))

        # 1. TARGET DEVICE CARD
        card_target = CyberCard(right_col, title="Target Peripheral Link", subtitle="GATT Endpoint")
        card_target.pack(fill="x", pady=(0, 8))

        target_row = tk.Frame(card_target.body, bg=BG_PANEL)
        target_row.pack(fill="x")

        target_info = tk.Frame(target_row, bg=BG_PANEL)
        target_info.pack(side="left", fill="both", expand=True)

        self.lbl_device_name = tk.Label(
            target_info,
            text="No peripheral selected",
            bg=BG_PANEL,
            fg=TEXT_PRIMARY,
            font=("Consolas", 11, "bold"),
            anchor="w",
        )
        self.lbl_device_name.pack(fill="x", pady=(0, 2))

        self.lbl_device_addr = tk.Label(
            target_info,
            text="MAC: N/A | RSSI: N/A",
            bg=BG_PANEL,
            fg=TEXT_MUTED,
            font=FONT_MONO,
            anchor="w",
        )
        self.lbl_device_addr.pack(fill="x")

        self.lbl_status = tk.Label(
            target_info,
            text="STATUS: Standby / Awaiting Scan",
            bg=BG_PANEL,
            fg=OMNI_GREEN,
            font=FONT_BADGE,
            anchor="w",
        )
        self.lbl_status.pack(fill="x", pady=(4, 0))

        # Signal meter on right of card
        meter_box = tk.Frame(target_row, bg=BG_PANEL)
        meter_box.pack(side="right", padx=(10, 0))

        tk.Label(meter_box, text="SIGNAL", bg=BG_PANEL, fg=TEXT_MUTED, font=FONT_BADGE).pack()
        self.signal_meter = SignalMeter(meter_box, width=46, height=18)
        self.signal_meter.pack(pady=(2, 0))

        # 2. ACTIONS COMMAND CENTER CARD
        card_actions = CyberCard(right_col, title="Protocol Operations", subtitle="Step-by-step Workflow")
        card_actions.pack(fill="x", pady=(0, 8))

        btn_grid = tk.Frame(card_actions.body, bg=BG_PANEL)
        btn_grid.pack(fill="x")

        self.btn_scan = ttk.Button(
            btn_grid,
            text="1. SCAN BLUETOOTH",
            style="Omni.TButton",
            command=self._wrap_sound(self.on_scan),
        )
        self.btn_scan.grid(row=0, column=0, padx=4, pady=3, sticky="ew")

        self.btn_pick = ttk.Button(
            btn_grid,
            text="2. SELECT DEVICE",
            style="Omni.TButton",
            command=self._wrap_sound(self.on_open_picker),
        )
        self.btn_pick.grid(row=0, column=1, padx=4, pady=3, sticky="ew")

        self.btn_connect = ttk.Button(
            btn_grid,
            text="3. CONNECT GATT",
            style="Omni.TButton",
            command=self._wrap_sound(self.on_connect),
        )
        self.btn_connect.grid(row=1, column=0, padx=4, pady=3, sticky="ew")

        self.btn_inspect = ttk.Button(
            btn_grid,
            text="4. MAP ATTRIBUTES",
            style="Omni.TButton",
            command=self._wrap_sound(self.on_inspect),
        )
        self.btn_inspect.grid(row=1, column=1, padx=4, pady=3, sticky="ew")

        self.btn_disconnect = ttk.Button(
            btn_grid,
            text="DISCONNECT LINK",
            style="Danger.TButton",
            command=self._wrap_sound(self.on_disconnect),
        )
        self.btn_disconnect.grid(row=2, column=0, columnspan=2, padx=4, pady=(6, 2), sticky="ew")

        btn_grid.columnconfigure(0, weight=1)
        btn_grid.columnconfigure(1, weight=1)

        # 3. TELEMETRY ACTIVITY CONSOLE CARD
        card_console = CyberCard(right_col, title="System Telemetry Console", subtitle="Event Log")
        card_console.pack(fill="both", expand=True)

        log_head = tk.Frame(card_console.body, bg=BG_PANEL)
        log_head.pack(fill="x", pady=(0, 4))

        self._wave_index = 0
        self._waveforms = [
            "[ ▂▃▅▆▇▆▅▃ ] MATRIX ONLINE",
            "[ ▃▅▆▇█▇▆▅ ] MATRIX ONLINE",
            "[ ▅▆▇█▇▆▅▃ ] MATRIX ONLINE",
            "[ ▆▇█▇▆▅▃▂ ] MATRIX ONLINE",
            "[ ▇█▇▆▅▃▂  ] MATRIX ONLINE",
            "[ █▇▆▅▃▂ ▂ ] MATRIX ONLINE",
        ]
        self.lbl_matrix_monitor = tk.Label(
            log_head,
            text=self._waveforms[0],
            bg=BG_PANEL,
            fg=OMNI_GREEN_GLOW,
            font=FONT_BADGE,
        )
        self.lbl_matrix_monitor.pack(side="left")

        btn_clear = tk.Button(
            log_head,
            text="CLEAR",
            bg=BG_SURFACE,
            fg=TEXT_MUTED,
            font=("Consolas", 7, "bold"),
            padx=6,
            pady=1,
            relief="solid",
            bd=1,
            cursor="hand2",
            command=self.clear_log,
        )
        btn_clear.pack(side="right", padx=(4, 0))

        btn_view_inv = ttk.Button(
            log_head,
            text="View Inventory",
            style="Omni.TButton",
            command=self.on_open_inventory,
        )
        btn_view_inv.pack(side="right")

        self.txt_log = tk.Text(
            card_console.body,
            bg="#080e0a",
            fg=TEXT_PRIMARY,
            insertbackground=OMNI_GREEN,
            height=6,
            font=FONT_MONO,
            relief="solid",
            bd=1,
            highlightthickness=0,
            wrap="word",
        )
        self.txt_log.pack(fill="both", expand=True)
        self.txt_log.configure(state="disabled")

    def append_log(self, text: str) -> None:
        """Append log line to telemetry console with timestamp."""
        ts = datetime.datetime.now().strftime("%H:%M:%S")
        self.txt_log.configure(state="normal")
        self.txt_log.insert("end", f"[{ts}] > {text}\n")
        self.txt_log.see("end")
        self.txt_log.configure(state="disabled")

    def clear_log(self) -> None:
        """Clear the telemetry log."""
        self.txt_log.configure(state="normal")
        self.txt_log.delete("1.0", "end")
        self.txt_log.configure(state="disabled")

    def tick_animation(self) -> None:
        """Advance dial and HUD telemetry animations."""
        self.dial.tick_animation()
        self._wave_index = (self._wave_index + 1) % len(self._waveforms)
        self.lbl_matrix_monitor.configure(text=self._waveforms[self._wave_index])
        now = datetime.datetime.now()
        self.lbl_timekeeper.configure(text=f"GALVAN TIME // {now.strftime('%H:%M:%S')}")

    def set_device_info(self, device: Optional[DeviceSummary]) -> None:
        """Update selected device display and signal meter."""
        if device:
            self.lbl_device_name.configure(text=f"Device: {device.display_name}")
            rssi_str = f"{device.rssi} dBm" if device.rssi is not None else "Unknown"
            self.lbl_device_addr.configure(text=f"MAC: {device.sanitized_address} | RSSI: {rssi_str}")
            self.signal_meter.set_rssi(device.rssi)
        else:
            self.lbl_device_name.configure(text="No peripheral selected")
            self.lbl_device_addr.configure(text="MAC: N/A | RSSI: N/A")
            self.signal_meter.set_rssi(None)

    def _wrap_sound(self, callback: Callable[[], None]) -> Callable[[], None]:
        """Wrap an action callback with a light futuristic interaction sound."""
        def wrapper() -> None:
            sound_player.play_beep()
            callback()
        return wrapper

    def _toggle_audio(self) -> None:
        """Toggle UI sound effects on or off."""
        is_on = sound_player.toggle()
        self.btn_sound.config(
            text="🔊 AUDIO: ON" if is_on else "🔇 AUDIO: OFF",
            fg=OMNI_GREEN if is_on else TEXT_MUTED,
        )

    def set_status(self, text: str, state: SessionState) -> None:
        """Update status line and dial."""
        self.lbl_status.configure(text=f"STATUS: {text.upper()}")
        self.dial.update_state(state)
