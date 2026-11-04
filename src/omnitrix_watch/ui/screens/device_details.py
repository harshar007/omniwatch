"""Omnitrix-themed GATT Inventory & Device Details Screen."""

from __future__ import annotations

import tkinter as tk
from tkinter import messagebox, ttk
from typing import Callable, Optional

from omnitrix_watch.models.device import CharacteristicSummary, GattInventory
from omnitrix_watch.sound import sound_player
from omnitrix_watch.ui.components.cards import CyberCard
from omnitrix_watch.ui.theme import (
    BG_DARK,
    BG_PANEL,
    BG_SURFACE,
    BORDER_COLOR,
    BORDER_BRIGHT,
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
        header = tk.Frame(self, bg=BG_DARK)
        header.pack(fill="x", padx=16, pady=(12, 8))

        title_box = tk.Frame(header, bg=BG_DARK)
        title_box.pack(side="left")

        tk.Label(
            title_box,
            text="🧬 GALVANIC GATT TELEMETRY DECODER",
            bg=BG_DARK,
            fg=OMNI_GREEN,
            font=FONT_TITLE,
        ).pack(anchor="w")

        tk.Label(
            title_box,
            text="READ-ONLY PROTOCOL CHARACTERISTIC AUDITOR // REDMI WATCH MOVE 2",
            bg=BG_DARK,
            fg=TEXT_MUTED,
            font=FONT_BADGE,
        ).pack(anchor="w", pady=(2, 0))

        # Action Buttons
        actions_bar = tk.Frame(header, bg=BG_DARK)
        actions_bar.pack(side="right")

        self.btn_inspect = ttk.Button(
            actions_bar,
            text="⚡ RUN GATT AUDIT",
            style="Accent.TButton",
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

        # Telemetry Metrics Banner Card
        card_metrics = CyberCard(self, title="Audit Metrics & Telemetry", subtitle="Sanctioned Scope")
        card_metrics.pack(fill="x", padx=16, pady=(0, 8))

        metric_row = tk.Frame(card_metrics.body, bg=BG_PANEL)
        metric_row.pack(fill="x")

        self.lbl_stat_services = tk.Label(
            metric_row,
            text="SERVICES: --",
            bg=BG_SURFACE,
            fg=OMNI_GREEN,
            font=FONT_BADGE,
            padx=10,
            pady=4,
            relief="solid",
            bd=1,
        )
        self.lbl_stat_services.pack(side="left", padx=(0, 8))

        self.lbl_stat_chars = tk.Label(
            metric_row,
            text="TOTAL ATTRIBUTES: --",
            bg=BG_SURFACE,
            fg=OMNI_GREEN_GLOW,
            font=FONT_BADGE,
            padx=10,
            pady=4,
            relief="solid",
            bd=1,
        )
        self.lbl_stat_chars.pack(side="left", padx=(0, 8))

        self.lbl_stat_readable = tk.Label(
            metric_row,
            text="READABLE ENDPOINTS: --",
            bg=BG_SURFACE,
            fg="#6ee7b7",
            font=FONT_BADGE,
            padx=10,
            pady=4,
            relief="solid",
            bd=1,
        )
        self.lbl_stat_readable.pack(side="left", padx=(0, 8))

        self.lbl_stat_security = tk.Label(
            metric_row,
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
        self.progress_frame = tk.Frame(self, bg=BG_DARK)
        self.progress_frame.pack(fill="x", padx=16, pady=(0, 6))

        self.lbl_progress = tk.Label(
            self.progress_frame,
            text="Awaiting GATT link connection to Redmi Watch Move 2.",
            bg=BG_DARK,
            fg=TEXT_MUTED,
            font=FONT_BODY,
            anchor="w",
        )
        self.lbl_progress.pack(fill="x")

        self.progressbar = ttk.Progressbar(
            self.progress_frame,
            style="Omni.Horizontal.TProgressbar",
            mode="determinate",
        )
        self.progressbar.pack(fill="x", pady=(4, 0))

        # Main Table Card
        card_table = CyberCard(self, title="GATT Service & Characteristic Registry", subtitle="Direct Memory Map")
        card_table.pack(fill="both", expand=True, padx=16, pady=(0, 12))

        # Quick Filter Row
        filter_bar = tk.Frame(card_table.body, bg=BG_PANEL)
        filter_bar.pack(fill="x", pady=(0, 6))

        tk.Label(filter_bar, text="FILTER ATTRIBUTES:", bg=BG_PANEL, fg=TEXT_MUTED, font=FONT_BADGE).pack(side="left", padx=(0, 6))

        self.var_table_filter = tk.StringVar(value="")
        self.ent_table_filter = tk.Entry(
            filter_bar,
            textvariable=self.var_table_filter,
            bg=BG_SURFACE,
            fg=OMNI_GREEN_GLOW,
            insertbackground=OMNI_GREEN,
            relief="solid",
            bd=1,
            font=FONT_MONO,
            width=24,
        )
        self.ent_table_filter.pack(side="left", padx=(0, 8))
        self.ent_table_filter.bind("<KeyRelease>", self._apply_table_filter)

        btn_clear = tk.Button(
            filter_bar,
            text="CLEAR FILTER",
            bg=BG_SURFACE,
            fg=TEXT_MUTED,
            font=("Consolas", 7, "bold"),
            padx=6,
            pady=1,
            relief="solid",
            bd=1,
            cursor="hand2",
            command=self._clear_table_filter,
        )
        btn_clear.pack(side="left")

        columns = ("service", "char_uuid", "name", "props", "readable", "value")
        self.tree = ttk.Treeview(card_table.body, columns=columns, show="headings")

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

        scrollbar_y = ttk.Scrollbar(card_table.body, orient="vertical", command=self.tree.yview)
        scrollbar_x = ttk.Scrollbar(card_table.body, orient="horizontal", command=self.tree.xview)
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
            fg=OMNI_GREEN_GLOW,
        )

    def display_inventory(self, inventory: GattInventory) -> None:
        """Populate the treeview with inspected GATT characteristics."""
        self.current_inventory = inventory
        self.all_characteristics = inventory.characteristics
        self._populate_rows(self.all_characteristics)

        services_set = {c.service_uuid for c in inventory.characteristics}
        readable_count = sum(1 for c in inventory.characteristics if c.is_readable)

        self.lbl_stat_services.config(text=f"SERVICES: {len(services_set)}")
        self.lbl_stat_chars.config(text=f"TOTAL ATTRIBUTES: {len(inventory.characteristics)}")
        self.lbl_stat_readable.config(text=f"READABLE ENDPOINTS: {readable_count}")

        self.btn_export.configure(state="normal")
        sound_player.play_alien_select()
        self.lbl_progress.configure(
            text=f"Audit complete: {len(inventory.characteristics)} attributes mapped across {len(services_set)} services.",
            fg=OMNI_GREEN,
        )

    def _populate_rows(self, char_list: list[CharacteristicSummary]) -> None:
        for item in self.tree.get_children():
            self.tree.delete(item)

        for char in char_list:
            props_str = ", ".join(char.properties)
            read_str = "🟢 READABLE" if char.is_readable else "🔒 WRITE/NOTIFY"

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

    def _apply_table_filter(self, _event: Optional[tk.Event] = None) -> None:
        q = self.var_table_filter.get().strip().lower()
        if not q:
            self._populate_rows(self.all_characteristics)
            return
        filtered = [
            c for c in self.all_characteristics
            if (q in c.characteristic_name.lower() or
                q in c.characteristic_uuid.lower() or
                q in c.service_name.lower())
        ]
        self._populate_rows(filtered)

    def _clear_table_filter(self) -> None:
        self.var_table_filter.set("")
        self._populate_rows(self.all_characteristics)

    def _handle_export_click(self) -> None:
        sound_player.play_beep()
        self.on_export()
