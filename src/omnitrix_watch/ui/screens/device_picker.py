"""Omnitrix-themed BLE Device Discovery & Target Lock Screen."""

from __future__ import annotations

import math
import tkinter as tk
from tkinter import ttk
from typing import Callable, Optional

from omnitrix_watch.models.device import DeviceSummary
from omnitrix_watch.sound import sound_player
from omnitrix_watch.ui.theme import (
    BG_DARK,
    BG_PANEL,
    BG_SURFACE,
    BORDER_COLOR,
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
        for i, dev in enumerate(dev_list):
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
        header = ttk.Frame(self, style="TFrame")
        header.pack(fill="x", padx=20, pady=(15, 8))

        title_box = ttk.Frame(header, style="TFrame")
        title_box.pack(side="left")

        ttk.Label(
            title_box,
            text="📡 OMNITRIX RADAR MATRIX // TARGET LOCK",
            foreground=OMNI_GREEN,
            font=FONT_TITLE,
        ).pack(anchor="w")

        ttk.Label(
            title_box,
            text="DISCOVERING PERIPHERALS OVER ENCRYPTED BLUETOOTH LOW ENERGY",
            foreground=TEXT_MUTED,
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

        # Top Control & Radar Section
        top_box = ttk.Frame(self, style="Surface.TFrame", padding=10)
        top_box.pack(fill="x", padx=20, pady=(0, 10))

        # Left side: Radar Canvas
        self.radar = OmnitrixRadarCanvas(top_box, size=140)
        self.radar.pack(side="left", padx=(0, 15))

        # Right side: Targeting controls
        ctrl_box = ttk.Frame(top_box, style="Surface.TFrame")
        ctrl_box.pack(side="left", fill="both", expand=True)

        # Row 1: Filter & Presets
        row1 = ttk.Frame(ctrl_box, style="Surface.TFrame")
        row1.pack(fill="x", pady=(0, 8))

        ttk.Label(row1, text="TARGET FILTER:", font=FONT_HEADING, foreground=OMNI_GREEN).pack(side="left", padx=(0, 6))

        self.var_filter = tk.StringVar(value="")
        self.ent_filter = tk.Entry(
            row1,
            textvariable=self.var_filter,
            bg=BG_PANEL,
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
            text="🎯 LOCK 'Redmi'",
            style="Omni.TButton",
            command=self._apply_redmi_filter,
        )
        self.btn_quick_redmi.pack(side="left", padx=4)

        self.btn_clear_filter = ttk.Button(
            row1,
            text="ALL DEVICES",
            style="Omni.TButton",
            command=self._clear_filter,
        )
        self.btn_clear_filter.pack(side="left", padx=4)

        # Row 2: Scan Action Buttons & Duration
        row2 = ttk.Frame(ctrl_box, style="Surface.TFrame")
        row2.pack(fill="x")

        ttk.Label(row2, text="SWEEP TIME (s):", font=FONT_BODY, foreground=TEXT_PRIMARY).pack(side="left", padx=(0, 6))

        self.var_duration = tk.StringVar(value="5.0")
        self.spin_duration = tk.Spinbox(
            row2,
            from_=2.0,
            to=30.0,
            increment=1.0,
            textvariable=self.var_duration,
            bg=BG_PANEL,
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
            style="Omni.TButton",
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

        # Discovered Devices Table
        table_frame = ttk.Frame(self, style="Surface.TFrame", padding=2)
        table_frame.pack(fill="both", expand=True, padx=20, pady=(0, 10))

        columns = ("status", "name", "address", "rssi_meter", "services")
        self.tree = ttk.Treeview(table_frame, columns=columns, show="headings", selectmode="browse")
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

        scrollbar = ttk.Scrollbar(table_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)

        self.tree.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        self.tree.bind("<<TreeviewSelect>>", self._on_tree_select)
        self.tree.bind("<Double-1>", lambda e: self._handle_confirm_selection())

        # Bottom action bar with target lock confirmation
        footer = ttk.Frame(self, style="TFrame")
        footer.pack(fill="x", padx=20, pady=(0, 15))

        self.lbl_selected = ttk.Label(
            footer,
            text="No peripheral locked. Select a device from the radar list above.",
            font=FONT_HEADING,
            foreground=TEXT_MUTED,
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
            foreground=OMNI_GREEN_GLOW,
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
            foreground=OMNI_GREEN if count > 0 else TEXT_MUTED,
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
                foreground=OMNI_CORE_GLOW,
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
