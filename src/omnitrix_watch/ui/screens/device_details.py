"""Omnitrix-themed GATT Inventory & Device Details Screen."""

from __future__ import annotations

import tkinter as tk
from tkinter import messagebox, ttk
from typing import Callable, Optional

from omnitrix_watch.models.device import CharacteristicSummary, GattInventory
from omnitrix_watch.sound import sound_player
from omnitrix_watch.ui.theme import (
    BG_DARK,
    BG_PANEL,
    BG_SURFACE,
    BORDER_COLOR,
    COLOR_ERROR,
    COLOR_INFO,
    COLOR_WARNING,
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
        self.all_characteristics: list[CharacteristicSummary] = []

        self._build_ui()

    def _build_ui(self) -> None:
        # Title bar
        header = ttk.Frame(self, style="TFrame")
        header.pack(fill="x", padx=20, pady=(15, 8))

        title_box = ttk.Frame(header, style="TFrame")
        title_box.pack(side="left")

        ttk.Label(
            title_box,
            text="🧬 GALVANIC GATT TELEMETRY DECODER",
            foreground=OMNI_GREEN,
            font=FONT_TITLE,
        ).pack(anchor="w")

        ttk.Label(
            title_box,
            text="NON-DESTRUCTIVE READ-ONLY CHARACTERISTIC AUDITOR // REDMI WATCH MOVE 2",
            foreground=TEXT_MUTED,
            font=FONT_BADGE,
        ).pack(anchor="w", pady=(2, 0))

        # Action Buttons
        actions_bar = ttk.Frame(header, style="TFrame")
        actions_bar.pack(side="right")

        self.btn_inspect = ttk.Button(
            actions_bar,
            text="⚡ RUN GATT AUDIT",
            style="Omni.TButton",
            command=self._handle_inspect_click,
        )
        self.btn_inspect.pack(side="left", padx=(0, 8))

        self.btn_export = ttk.Button(
            actions_bar,
            text="📑 EXPORT INVENTORY (.MD)",
            style="Omni.TButton",
            command=self._handle_export_click,
            state="disabled",
        )
        self.btn_export.pack(side="left")

        # Telemetry Cartridges Metric Banner
        metric_bar = ttk.Frame(self, style="Surface.TFrame", padding=10)
        metric_bar.pack(fill="x", padx=20, pady=(0, 10))

        self.lbl_stat_services = tk.Label(
            metric_bar,
            text="SERVICES: --",
            bg=BG_PANEL,
            fg=OMNI_GREEN,
            font=FONT_BADGE,
            padx=10,
            pady=4,
            relief="solid",
            bd=1,
        )
        self.lbl_stat_services.pack(side="left", padx=(0, 8))

        self.lbl_stat_chars = tk.Label(
            metric_bar,
            text="TOTAL ATTRIBUTES: --",
            bg=BG_PANEL,
            fg=OMNI_GREEN_GLOW,
            font=FONT_BADGE,
            padx=10,
            pady=4,
            relief="solid",
            bd=1,
        )
        self.lbl_stat_chars.pack(side="left", padx=(0, 8))

        self.lbl_stat_readable = tk.Label(
            metric_bar,
            text="READABLE ENDPOINTS: --",
            bg=BG_PANEL,
            fg="#6ee7b7",
            font=FONT_BADGE,
            padx=10,
            pady=4,
            relief="solid",
            bd=1,
        )
        self.lbl_stat_readable.pack(side="left", padx=(0, 8))

        self.lbl_stat_security = tk.Label(
            metric_bar,
            text="SECURITY: 🛡️ ZERO-WRITE ENFORCED",
            bg=OMNI_GREEN_DARK,
            fg=OMNI_GREEN,
            font=FONT_BADGE,
            padx=10,
            pady=4,
            relief="solid",
            bd=1,
        )
        self.lbl_stat_security.pack(side="right")

        # Progress bar
        self.progress_frame = ttk.Frame(self, style="TFrame")
        self.progress_frame.pack(fill="x", padx=20, pady=(0, 8))

        self.lbl_progress = ttk.Label(
            self.progress_frame,
            text="Awaiting GATT link connection to Redmi Watch Move 2.",
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

        self.tree.heading("service", text="GATT Service Profile")
        self.tree.heading("char_uuid", text="Characteristic UUID")
        self.tree.heading("name", text="Resolved Attribute Name")
        self.tree.heading("props", text="Properties")
        self.tree.heading("readable", text="Permission")
        self.tree.heading("value", text="Telemetry Payload / Diagnostic Status")

        self.tree.column("service", width=180, anchor="w")
        self.tree.column("char_uuid", width=220, anchor="w")
        self.tree.column("name", width=180, anchor="w")
        self.tree.column("props", width=120, anchor="center")
        self.tree.column("readable", width=90, anchor="center")
        self.tree.column("value", width=220, anchor="w")

        scrollbar_y = ttk.Scrollbar(table_frame, orient="vertical", command=self.tree.yview)
        scrollbar_x = ttk.Scrollbar(table_frame, orient="horizontal", command=self.tree.xview)
        self.tree.configure(yscrollcommand=scrollbar_y.set, xscrollcommand=scrollbar_x.set)

        self.tree.pack(side="left", fill="both", expand=True)
        scrollbar_y.pack(side="right", fill="y")

    def _handle_inspect_click(self) -> None:
        sound_player.play_radar_ping()
        self.on_inspect()

    def update_progress(self, current: int, total: int, status_text: str) -> None:
        """Update inspection progress indicator."""
        if total > 0:
            pct = int((current / total) * 100)
            self.progressbar["value"] = pct
        self.lbl_progress.configure(
            text=f"[{current}/{total}] {status_text}",
            foreground=OMNI_GREEN_GLOW,
        )

    def display_inventory(self, inventory: GattInventory) -> None:
        """Populate the treeview with inspected GATT characteristics."""
        self.current_inventory = inventory
        self.all_characteristics = inventory.characteristics
        for item in self.tree.get_children():
            self.tree.delete(item)

        services_set = set()
        readable_count = 0

        for char in inventory.characteristics:
            services_set.add(char.service_uuid)
            props_str = ", ".join(char.properties)
            read_str = "🟢 READABLE" if char.is_readable else "🔒 WRITE/NOTIFY"
            if char.is_readable:
                readable_count += 1
            
            if char.read_error:
                val_str = f"⚠️ {char.read_error}"
            elif char.read_result is not None:
                val_str = f"HEX: {char.read_result}"
            elif not char.is_readable:
                val_str = "<write/notify permission only>"
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

        # Update metric stats
        self.lbl_stat_services.config(text=f"SERVICES: {len(services_set)}")
        self.lbl_stat_chars.config(text=f"TOTAL ATTRIBUTES: {len(inventory.characteristics)}")
        self.lbl_stat_readable.config(text=f"READABLE ENDPOINTS: {readable_count}")

        self.btn_export.configure(state="normal")
        sound_player.play_alien_select()
        self.lbl_progress.configure(
            text=f"Audit complete: {len(inventory.characteristics)} attributes mapped across {len(services_set)} services.",
            foreground=OMNI_GREEN,
        )

    def _handle_export_click(self) -> None:
        sound_player.play_beep()
        self.on_export()
