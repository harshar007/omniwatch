"""GATT Inventory & Device Details Screen."""

from __future__ import annotations

import tkinter as tk
from tkinter import messagebox, ttk
from typing import Callable, Optional

from omnitrix_watch.models.device import CharacteristicSummary, GattInventory
from omnitrix_watch.ui.theme import (
    BG_DARK,
    BG_PANEL,
    BG_SURFACE,
    BORDER_COLOR,
    COLOR_INFO,
    FONT_BADGE,
    FONT_BODY,
    FONT_HEADING,
    FONT_MONO,
    FONT_TITLE,
    OMNI_GREEN,
    OMNI_GREEN_DARK,
    OMNI_GREEN_GLOW,
    TEXT_MUTED,
    TEXT_PRIMARY,
)


class DeviceDetailsScreen(ttk.Frame):
    """Screen for viewing inspected GATT services, characteristics, and exporting reports."""

    def __init__(
        self,
        parent: tk.Widget,
        on_inspect: Callable[[], None],
        on_export: Callable[[], None],
    ) -> None:
        super().__init__(parent, style="TFrame")
        self.on_inspect = on_inspect
        self.on_export = on_export
        self.current_inventory: Optional[GattInventory] = None

        self._build_ui()

    def _build_ui(self) -> None:
        # Title bar
        header = ttk.Frame(self, style="TFrame")
        header.pack(fill="x", padx=20, pady=(15, 10))

        ttk.Label(
            header,
            text="GATT SERVICES & CHARACTERISTICS INVENTORY",
            foreground=OMNI_GREEN,
            font=FONT_TITLE,
        ).pack(side="left")

        # Action Buttons
        actions_bar = ttk.Frame(header, style="TFrame")
        actions_bar.pack(side="right")

        self.btn_inspect = ttk.Button(
            actions_bar,
            text="RUN GATT INSPECTION",
            style="Omni.TButton",
            command=self.on_inspect,
        )
        self.btn_inspect.pack(side="left", padx=(0, 8))

        self.btn_export = ttk.Button(
            actions_bar,
            text="EXPORT TO docs/gatt-inventory.md",
            style="Omni.TButton",
            command=self._handle_export_click,
            state="disabled",
        )
        self.btn_export.pack(side="left")

        # Progress bar
        self.progress_frame = ttk.Frame(self, style="TFrame")
        self.progress_frame.pack(fill="x", padx=20, pady=(0, 8))

        self.lbl_progress = ttk.Label(
            self.progress_frame,
            text="Ready to inspect GATT profile.",
            foreground=TEXT_MUTED,
            font=FONT_BODY,
        )
        self.lbl_progress.pack(anchor="w")

        self.progressbar = ttk.Progressbar(
            self.progress_frame,
            style="Omni.Horizontal.TProgressbar",
            mode="determinate",
        )
        self.progressbar.pack(fill="x", pady=(4, 0))

        # Main table
        table_frame = ttk.Frame(self, style="Surface.TFrame", padding=2)
        table_frame.pack(fill="both", expand=True, padx=20, pady=(0, 15))

        columns = ("service", "char_uuid", "name", "props", "readable", "value")
        self.tree = ttk.Treeview(table_frame, columns=columns, show="headings")

        self.tree.heading("service", text="Service")
        self.tree.heading("char_uuid", text="Characteristic UUID")
        self.tree.heading("name", text="Resolved Name")
        self.tree.heading("props", text="Properties")
        self.tree.heading("readable", text="Read")
        self.tree.heading("value", text="Read Value / Diagnostic")

        self.tree.column("service", width=160, anchor="w")
        self.tree.column("char_uuid", width=220, anchor="w")
        self.tree.column("name", width=170, anchor="w")
        self.tree.column("props", width=120, anchor="center")
        self.tree.column("readable", width=60, anchor="center")
        self.tree.column("value", width=200, anchor="w")

        scrollbar_y = ttk.Scrollbar(table_frame, orient="vertical", command=self.tree.yview)
        scrollbar_x = ttk.Scrollbar(table_frame, orient="horizontal", command=self.tree.xview)
        self.tree.configure(yscrollcommand=scrollbar_y.set, xscrollcommand=scrollbar_x.set)

        self.tree.pack(side="left", fill="both", expand=True)
        scrollbar_y.pack(side="right", fill="y")

    def update_progress(self, current: int, total: int, status_text: str) -> None:
        """Update inspection progress indicator."""
        if total > 0:
            pct = int((current / total) * 100)
            self.progressbar["value"] = pct
        self.lbl_progress.configure(text=f"[{current}/{total}] {status_text}")

    def display_inventory(self, inventory: GattInventory) -> None:
        """Populate the treeview with inspected GATT characteristics."""
        self.current_inventory = inventory
        for item in self.tree.get_children():
            self.tree.delete(item)

        for char in inventory.characteristics:
            props_str = ", ".join(char.properties)
            read_str = "YES" if char.is_readable else "NO"
            
            if char.read_error:
                val_str = f"ERR: {char.read_error}"
            elif char.read_result is not None:
                val_str = char.read_result
            elif not char.is_readable:
                val_str = "<write/notify only>"
            else:
                val_str = "<unread>"

            self.tree.insert(
                "",
                "end",
                values=(
                    char.service_name,
                    char.characteristic_uuid,
                    char.characteristic_name,
                    props_str,
                    read_str,
                    val_str,
                ),
            )

        self.lbl_progress.configure(
            text=f"Inspection complete. {len(inventory.characteristics)} characteristics listed for {inventory.device_name}."
        )
        self.progressbar["value"] = 100
        self.btn_export.configure(state="normal")

    def _handle_export_click(self) -> None:
        if not self.current_inventory:
            return
        confirm = messagebox.askyesno(
            "Confirm Inventory Export",
            "Are you sure you want to export this sanitized GATT inventory to 'docs/gatt-inventory.md'?\n\n"
            "This will document observable characteristics without private identifiers.",
        )
        if confirm:
            self.on_export()
