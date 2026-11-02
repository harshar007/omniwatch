"""Device picker screen allowing user to search and explicitly select BLE devices."""

from __future__ import annotations

import tkinter as tk
from tkinter import ttk
from typing import Callable, Optional

from omnitrix_watch.models.device import DeviceSummary
from omnitrix_watch.ui.theme import (
    BG_DARK,
    BG_PANEL,
    BG_SURFACE,
    BORDER_COLOR,
    FONT_BADGE,
    FONT_BODY,
    FONT_HEADING,
    FONT_TITLE,
    OMNI_GREEN,
    OMNI_GREEN_DARK,
    TEXT_MUTED,
    TEXT_PRIMARY,
)


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
        self._build_ui()

    def _build_ui(self) -> None:
        # Title bar
        header = ttk.Frame(self, style="TFrame")
        header.pack(fill="x", padx=20, pady=(15, 10))

        ttk.Label(
            header,
            text="BLE DEVICE DISCOVERY & SELECTION",
            foreground=OMNI_GREEN,
            font=FONT_TITLE,
        ).pack(side="left")

        # Scan controls card
        filter_bar = ttk.Frame(self, style="Surface.TFrame", padding=10)
        filter_bar.pack(fill="x", padx=20, pady=(0, 10))

        ttk.Label(filter_bar, text="Filter:", font=FONT_BODY, foreground=TEXT_PRIMARY).pack(side="left", padx=(0, 6))

        self.var_filter = tk.StringVar(value="")
        self.ent_filter = tk.Entry(
            filter_bar,
            textvariable=self.var_filter,
            bg=BG_PANEL,
            fg=TEXT_PRIMARY,
            insertbackground=OMNI_GREEN,
            relief="solid",
            bd=1,
            font=FONT_BODY,
            width=18,
        )
        self.ent_filter.pack(side="left", padx=(0, 15))

        ttk.Label(filter_bar, text="Scan Time (s):", font=FONT_BODY, foreground=TEXT_PRIMARY).pack(side="left", padx=(0, 6))

        self.var_duration = tk.StringVar(value="5.0")
        self.spin_duration = tk.Spinbox(
            filter_bar,
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
            filter_bar,
            text="START SCAN",
            style="Omni.TButton",
            command=self._handle_scan_click,
        )
        self.btn_scan.pack(side="left", padx=4)

        self.btn_cancel = ttk.Button(
            filter_bar,
            text="CANCEL",
            style="Danger.TButton",
            command=self.on_cancel_scan,
        )
        self.btn_cancel.pack(side="left", padx=4)

        self.btn_quick_redmi = ttk.Button(
            filter_bar,
            text="Filter 'Redmi'",
            style="Omni.TButton",
            command=lambda: self.var_filter.set("Redmi"),
        )
        self.btn_quick_redmi.pack(side="right")

        # Devices Table
        table_frame = ttk.Frame(self, style="Surface.TFrame", padding=2)
        table_frame.pack(fill="both", expand=True, padx=20, pady=(0, 10))

        columns = ("name", "address", "rssi", "services")
        self.tree = ttk.Treeview(table_frame, columns=columns, show="headings", selectmode="browse")
        self.tree.heading("name", text="Device Name")
        self.tree.heading("address", text="Sanitized Address / MAC")
        self.tree.heading("rssi", text="RSSI (Signal)")
        self.tree.heading("services", text="Advertised Services")

        self.tree.column("name", width=220, anchor="w")
        self.tree.column("address", width=180, anchor="center")
        self.tree.column("rssi", width=100, anchor="center")
        self.tree.column("services", width=260, anchor="w")

        scrollbar = ttk.Scrollbar(table_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)

        self.tree.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        self.tree.bind("<<TreeviewSelect>>", self._on_tree_select)
        self.tree.bind("<Double-1>", lambda e: self._handle_confirm_selection())

        # Bottom action bar
        footer = ttk.Frame(self, style="TFrame")
        footer.pack(fill="x", padx=20, pady=(0, 15))

        self.lbl_selected = ttk.Label(
            footer,
            text="No device selected.",
            font=FONT_HEADING,
            foreground=TEXT_MUTED,
        )
        self.lbl_selected.pack(side="left")

        self.btn_confirm = ttk.Button(
            footer,
            text="CONFIRM TARGET SELECTION",
            style="Omni.TButton",
            state="disabled",
            command=self._handle_confirm_selection,
        )
        self.btn_confirm.pack(side="right")

    def _handle_scan_click(self) -> None:
        try:
            dur = float(self.var_duration.get())
        except ValueError:
            dur = 5.0
        filt = self.var_filter.get().strip()
        self.discovered_devices.clear()
        for item in self.tree.get_children():
            self.tree.delete(item)
        self.lbl_selected.configure(text="Scanning in progress...")
        self.btn_confirm.configure(state="disabled")
        self.on_start_scan(dur, filt)

    def add_or_update_device(self, device: DeviceSummary) -> None:
        """Add newly discovered device or update existing item in table."""
        self.discovered_devices[device.address] = device
        
        rssi_text = f"{device.rssi} dBm" if device.rssi is not None else "N/A"
        raw_services = device.details.get("service_uuids", [])
        services_text = ", ".join(s[:8] for s in raw_services) if raw_services else "None"

        # Check if item exists in tree
        if self.tree.exists(device.address):
            self.tree.item(
                device.address,
                values=(device.display_name, device.sanitized_address, rssi_text, services_text),
            )
        else:
            self.tree.insert(
                "",
                "end",
                iid=device.address,
                values=(device.display_name, device.sanitized_address, rssi_text, services_text),
            )

    def set_scan_completed(self, devices: list[DeviceSummary]) -> None:
        """Called when scan completes."""
        self.lbl_selected.configure(
            text=f"Scan complete. Found {len(devices)} device(s). Please select your watch."
        )

    def _on_tree_select(self, event: tk.Event) -> None:
        selected_items = self.tree.selection()
        if not selected_items:
            self.btn_confirm.configure(state="disabled")
            return
        addr = selected_items[0]
        if addr in self.discovered_devices:
            dev = self.discovered_devices[addr]
            self.lbl_selected.configure(
                text=f"Selected: {dev.display_name} ({dev.sanitized_address})"
            )
            self.btn_confirm.configure(state="normal")

    def _handle_confirm_selection(self) -> None:
        selected_items = self.tree.selection()
        if not selected_items:
            return
        addr = selected_items[0]
        if addr in self.discovered_devices:
            dev = self.discovered_devices[addr]
            self.on_device_selected(dev)
