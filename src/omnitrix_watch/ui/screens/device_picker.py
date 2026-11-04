"""Omnitrix-themed BLE Device Discovery & Target Lock Screen."""

from __future__ import annotations

import math
import tkinter as tk
from tkinter import ttk
from typing import Callable, Optional

from omnitrix_watch.models.device import DeviceSummary
from omnitrix_watch.sound import sound_player
from omnitrix_watch.ui.components.cards import CyberCard
from omnitrix_watch.ui.components.radar import OmnitrixRadarCanvas
from omnitrix_watch.ui.theme import (
    BG_DARK,
    BG_PANEL,
    BG_SURFACE,
    BORDER_COLOR,
    BORDER_BRIGHT,
    FONT_BADGE,
    FONT_BODY,
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

# Re-export OmnitrixRadarCanvas for backward compatibility
__all__ = ["DevicePickerScreen", "OmnitrixRadarCanvas"]


class DevicePickerScreen(ttk.Frame):
    """Screen for discovering, listing, and explicitly selecting the target BLE device."""

    def __init__(
        self,
        parent: tk.Widget,
        on_start_scan: Callable[[float, str], None],
        on_cancel_scan: Callable[[], None],
        on_device_selected: Callable[[DeviceSummary], None],
    ) -> None:
        super().__init__(parent, style="TFrame")
        self.on_start_scan = on_start_scan
        self.on_cancel_scan = on_cancel_scan
        self.on_device_selected = on_device_selected

        self.discovered_devices: dict[str, DeviceSummary] = {}
        self.selected_device: Optional[DeviceSummary] = None

        self._build_ui()

    def _build_ui(self) -> None:
        # Title bar
        header = tk.Frame(self, bg=BG_DARK)
        header.pack(fill="x", padx=16, pady=(12, 8))

        title_box = tk.Frame(header, bg=BG_DARK)
        title_box.pack(side="left")

        tk.Label(
            title_box,
            text="📡 OMNITRIX RADAR MATRIX // TARGET LOCK",
            bg=BG_DARK,
            fg=OMNI_GREEN,
            font=FONT_TITLE,
        ).pack(anchor="w")

        tk.Label(
            title_box,
            text="DISCOVERING NEARBY PERIPHERALS OVER BLUETOOTH LOW ENERGY",
            bg=BG_DARK,
            fg=TEXT_MUTED,
            font=FONT_BADGE,
        ).pack(anchor="w", pady=(2, 0))

        # Target peripheral badge
        target_badge = tk.Label(
            header,
            text="TARGET: REDMI WATCH MOVE 2",
            bg=OMNI_GREEN_DARK,
            fg=OMNI_GREEN,
            font=FONT_BADGE,
            padx=8,
            pady=3,
            relief="solid",
            bd=1,
        )
        target_badge.pack(side="right")

        # Top Control & Radar Section using CyberCard
        top_card = CyberCard(self, title="Radar Sweep & Targeting Controls", subtitle="Bluetooth Radio Active")
        top_card.pack(fill="x", padx=16, pady=(0, 8))

        # Left side: Radar Canvas
        self.radar = OmnitrixRadarCanvas(top_card.body, size=140)
        self.radar.pack(side="left", padx=(0, 15))

        # Right side: Targeting controls
        ctrl_box = tk.Frame(top_card.body, bg=BG_PANEL)
        ctrl_box.pack(side="left", fill="both", expand=True)

        # Row 1: Filter & Presets
        row1 = tk.Frame(ctrl_box, bg=BG_PANEL)
        row1.pack(fill="x", pady=(0, 8))

        tk.Label(row1, text="TARGET FILTER:", font=FONT_HEADING, bg=BG_PANEL, fg=OMNI_GREEN).pack(side="left", padx=(0, 6))

        self.var_filter = tk.StringVar(value="")
        self.ent_filter = tk.Entry(
            row1,
            textvariable=self.var_filter,
            bg=BG_SURFACE,
            fg=OMNI_GREEN_GLOW,
            insertbackground=OMNI_GREEN,
            relief="solid",
            bd=1,
            font=("Consolas", 10, "bold"),
            width=16,
        )
        self.ent_filter.pack(side="left", padx=(0, 10))

        self.btn_quick_redmi = ttk.Button(
            row1,
            text="🎯 FILTER 'Redmi'",
            style="Omni.TButton",
            command=self._apply_redmi_filter,
        )
        self.btn_quick_redmi.pack(side="left", padx=4)

        self.btn_clear_filter = ttk.Button(
            row1,
            text="SHOW ALL",
            style="Omni.TButton",
            command=self._clear_filter,
        )
        self.btn_clear_filter.pack(side="left", padx=4)

        # Row 2: Scan Action Buttons & Duration
        row2 = tk.Frame(ctrl_box, bg=BG_PANEL)
        row2.pack(fill="x")

        tk.Label(row2, text="SWEEP TIME (s):", font=FONT_BODY, bg=BG_PANEL, fg=TEXT_PRIMARY).pack(side="left", padx=(0, 6))

        self.var_duration = tk.StringVar(value="5.0")
        self.spin_duration = tk.Spinbox(
            row2,
            from_=2.0,
            to=30.0,
            increment=1.0,
            textvariable=self.var_duration,
            bg=BG_SURFACE,
            fg=TEXT_PRIMARY,
            insertbackground=OMNI_GREEN,
            relief="solid",
            bd=1,
            width=5,
            font=FONT_BODY,
        )
        self.spin_duration.pack(side="left", padx=(0, 15))

        self.btn_scan = ttk.Button(
            row2,
            text="⚡ START RADAR SWEEP",
            style="Accent.TButton",
            command=self._handle_scan_click,
        )
        self.btn_scan.pack(side="left", padx=4)

        self.btn_cancel = ttk.Button(
            row2,
            text="ABORT",
            style="Danger.TButton",
            command=self._handle_cancel_click,
        )
        self.btn_cancel.pack(side="left", padx=4)

        # Discovered Devices Table Card
        table_card = CyberCard(self, title="Discovered Peripherals", subtitle="Airwave Inventory")
        table_card.pack(fill="both", expand=True, padx=16, pady=(0, 8))

        columns = ("status", "name", "address", "rssi_meter", "services")
        self.tree = ttk.Treeview(table_card.body, columns=columns, show="headings", selectmode="browse")
        self.tree.heading("status", text="Lock")
        self.tree.heading("name", text="Peripheral Name")
        self.tree.heading("address", text="Sanitized MAC")
        self.tree.heading("rssi_meter", text="Signal Strength")
        self.tree.heading("services", text="Advertised UUIDs")

        self.tree.column("status", width=50, anchor="center")
        self.tree.column("name", width=220, anchor="w")
        self.tree.column("address", width=170, anchor="center")
        self.tree.column("rssi_meter", width=160, anchor="w")
        self.tree.column("services", width=240, anchor="w")

        scrollbar = ttk.Scrollbar(table_card.body, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)

        self.tree.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        self.tree.bind("<<TreeviewSelect>>", self._on_tree_select)
        self.tree.bind("<Double-1>", lambda e: self._handle_confirm_selection())

        # Bottom action bar with target lock confirmation
        footer = tk.Frame(self, bg=BG_DARK)
        footer.pack(fill="x", padx=16, pady=(0, 12))

        self.lbl_selected = tk.Label(
            footer,
            text="No peripheral locked. Select a device from the radar list above.",
            bg=BG_DARK,
            font=FONT_HEADING,
            fg=TEXT_MUTED,
        )
        self.lbl_selected.pack(side="left")

        self.btn_confirm = ttk.Button(
            footer,
            text="🔒 CONFIRM TARGET LOCK",
            style="Omni.TButton",
            state="disabled",
            command=self._handle_confirm_selection,
        )
        self.btn_confirm.pack(side="right")

    def _apply_redmi_filter(self) -> None:
        sound_player.play_beep()
        self.var_filter.set("Redmi")

    def _clear_filter(self) -> None:
        sound_player.play_beep()
        self.var_filter.set("")

    def _handle_scan_click(self) -> None:
        """Initiate scan with audio feedback."""
        try:
            dur = float(self.var_duration.get())
        except ValueError:
            dur = 5.0
        name_filter = self.var_filter.get().strip()

        sound_player.play_radar_ping()
        self.radar.update_scan_state(True)
        self.btn_scan.configure(state="disabled")
        self.lbl_selected.configure(
            text="Radar sweep active... Searching airwaves for Redmi Watch Move 2...",
            fg=OMNI_GREEN_GLOW,
        )

        self.discovered_devices.clear()
        for item in self.tree.get_children():
            self.tree.delete(item)

        self.on_start_scan(dur, name_filter)

    def _handle_cancel_click(self) -> None:
        sound_player.play_error()
        self.radar.update_scan_state(False)
        self.on_cancel_scan()

    def add_or_update_device(self, device: DeviceSummary) -> None:
        """Add or update an item in the discovered devices table."""
        self.discovered_devices[device.address] = device
        self._refresh_tree_item(device)
        self.radar.update_devices(
            list(self.discovered_devices.values()),
            self.selected_device.address if self.selected_device else None,
        )

    def _format_rssi_meter(self, rssi: Optional[int]) -> str:
        """Format signal strength into cyberpunk visual meter."""
        if rssi is None:
            return "N/A"
        if rssi >= -55:
            return f"🟢 ████ {rssi} dBm (Peak)"
        elif rssi >= -70:
            return f"🟢 ███░ {rssi} dBm (Good)"
        elif rssi >= -85:
            return f"🟡 ██░░ {rssi} dBm (Fair)"
        else:
            return f"🔴 █░░░ {rssi} dBm (Weak)"

    def _refresh_tree_item(self, device: DeviceSummary) -> None:
        """Insert or refresh a device row."""
        existing = None
        for item in self.tree.get_children():
            row_addr = self.tree.item(item, "values")[2]
            if row_addr == device.sanitized_address:
                existing = item
                break

        service_list = device.details.get("service_uuids", [])
        services_str = ", ".join(service_list) if service_list else "None advertised"
        meter = self._format_rssi_meter(device.rssi)
        is_sel = (self.selected_device and self.selected_device.address == device.address)
        status_icon = "🎯" if is_sel else "•"

        values = (
            status_icon,
            device.display_name,
            device.sanitized_address,
            meter,
            services_str,
        )

        if existing:
            self.tree.item(existing, values=values)
        else:
            self.tree.insert("", "end", values=values)

    def set_scan_completed(self, devices: list[DeviceSummary]) -> None:
        """Called when scan completes."""
        self.radar.update_scan_state(False)
        self.btn_scan.configure(state="normal")
        self.discovered_devices = {d.address: d for d in devices}
        count = len(devices)
        sound_player.play_beep()
        self.lbl_selected.configure(
            text=f"Sweep complete. Identified {count} peripheral{'s' if count != 1 else ''}. Select target to lock.",
            fg=OMNI_GREEN if count > 0 else TEXT_MUTED,
        )
        self.radar.update_devices(
            list(self.discovered_devices.values()),
            self.selected_device.address if self.selected_device else None,
        )

    def _on_tree_select(self, _event: tk.Event) -> None:
        """Handle user selecting a row in the devices treeview."""
        selected_items = self.tree.selection()
        if not selected_items:
            self.btn_confirm.configure(state="disabled")
            return

        item = selected_items[0]
        sanitized_addr = self.tree.item(item, "values")[2]

        matched = None
        for dev in self.discovered_devices.values():
            if dev.sanitized_address == sanitized_addr:
                matched = dev
                break

        if matched:
            sound_player.play_beep()
            self.selected_device = matched
            self.lbl_selected.configure(
                text=f"TARGET ACQUIRED: {matched.display_name} ({matched.sanitized_address})",
                fg=OMNI_CORE_GLOW,
            )
            self.btn_confirm.configure(state="normal")
            self.radar.update_devices(list(self.discovered_devices.values()), matched.address)

    def _handle_confirm_selection(self) -> None:
        """Confirm selection of the currently highlighted device."""
        if not self.selected_device:
            return
        sound_player.play_alien_select()
        self.on_device_selected(self.selected_device)

    def tick_animation(self) -> None:
        """Tick radar sweep animation frame."""
        self.radar.tick_animation()
