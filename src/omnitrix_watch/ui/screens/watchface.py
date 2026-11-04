"""Omnitrix Watch Face Screen with Alien DNA selection and live timekeeper."""

from __future__ import annotations

import datetime
import math
from pathlib import Path
import tkinter as tk
from tkinter import messagebox, ttk
from typing import Optional

from omnitrix_watch.sound import sound_player
from omnitrix_watch.ui.components.cards import CyberCard
from omnitrix_watch.ui.components.watch_preview import WatchPreviewCanvas
from omnitrix_watch.ui.theme import (
    BG_DARK,
    BG_PANEL,
    BG_SURFACE,
    BORDER_COLOR,
    BORDER_BRIGHT,
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
from omnitrix_watch.watchface.aliens import (
    DEFAULT_ALIEN_ROSTER,
    AlienProfile,
    get_alien_by_id,
    get_all_aliens,
)
from omnitrix_watch.watchface.builder import WatchFaceConfig, WatchFaceGenerator

# Re-export WatchPreviewCanvas for backward compatibility
__all__ = ["WatchFaceScreen", "WatchPreviewCanvas"]


class WatchFaceScreen(ttk.Frame):
    """Screen for configuring and exporting Omnitrix watch faces for Redmi Watch Move 2."""

    def __init__(self, parent: tk.Widget) -> None:
        super().__init__(parent, style="TFrame")
        self.all_aliens = get_all_aliens()
        self.current_alien_idx = 0
        self.config = WatchFaceConfig()

        self._build_ui()

    def _build_ui(self) -> None:
        # Header banner
        header = tk.Frame(self, bg=BG_DARK)
        header.pack(fill="x", padx=16, pady=(12, 8))

        title_box = tk.Frame(header, bg=BG_DARK)
        title_box.pack(side="left")

        tk.Label(
            title_box,
            text="OMNITRIX WATCH FACE BUILDER",
            bg=BG_DARK,
            fg=OMNI_GREEN,
            font=FONT_TITLE,
        ).pack(anchor="w")

        tk.Label(
            title_box,
            text="AMOLED WATCHFACE GENERATOR & ALIEN DNA INTEGRATION",
            bg=BG_DARK,
            fg=TEXT_MUTED,
            font=FONT_BADGE,
        ).pack(anchor="w", pady=(2, 0))

        # Target peripheral badge
        target_badge = tk.Label(
            header,
            text="TARGET: REDMI WATCH MOVE 2 (390x450 AMOLED)",
            bg=OMNI_GREEN_DARK,
            fg=OMNI_GREEN,
            font=FONT_BADGE,
            padx=10,
            pady=4,
            relief="solid",
            bd=1,
        )
        target_badge.pack(side="right")

        # Main Layout: Watch Preview on left, Customizer on right
        body = tk.Frame(self, bg=BG_DARK)
        body.pack(fill="both", expand=True, padx=16, pady=6)

        # Left Column: Preview in CyberCard
        card_preview = CyberCard(body, title="Hardware Display Preview", subtitle="1.85\" AMOLED")
        card_preview.pack(side="left", fill="y", padx=(0, 12))

        self.preview_canvas = WatchPreviewCanvas(card_preview.body, width=240, height=290)
        self.preview_canvas.pack(pady=4)

        tk.Label(
            card_preview.body,
            text="NATIVE RESOLUTION: 390 x 450 px",
            bg=BG_PANEL,
            fg=TEXT_MUTED,
            font=FONT_BADGE,
        ).pack(pady=(4, 0))

        # Right Column: Alien DNA Matrix & Controls
        right_col = tk.Frame(body, bg=BG_DARK)
        right_col.pack(side="right", fill="both", expand=True)

        # Card 1: Alien DNA Profile Card
        card_dna = CyberCard(right_col, title="Active Alien DNA Matrix", subtitle="Extraterrestrial Profile")
        card_dna.pack(fill="x", pady=(0, 8))

        # Dropdown quick jump selector
        jump_row = tk.Frame(card_dna.body, bg=BG_PANEL)
        jump_row.pack(fill="x", pady=(0, 6))

        tk.Label(jump_row, text="JUMP TO ALIEN:", bg=BG_PANEL, fg=TEXT_MUTED, font=FONT_BADGE).pack(side="left", padx=(0, 6))

        alien_names = [f"#{a.id:02d} {a.name} ({a.species})" for a in self.all_aliens]
        self.combo_var = tk.StringVar(value=alien_names[0])
        self.combo_alien = ttk.Combobox(
            jump_row,
            textvariable=self.combo_var,
            values=alien_names,
            state="readonly",
            width=28,
        )
        self.combo_alien.pack(side="left")
        self.combo_alien.bind("<<ComboboxSelected>>", self._on_combo_select)

        self.lbl_alien_title = tk.Label(
            card_dna.body,
            text="",
            bg=BG_PANEL,
            fg=OMNI_GREEN_GLOW,
            font=("Consolas", 13, "bold"),
            anchor="w",
        )
        self.lbl_alien_title.pack(fill="x")

        self.lbl_alien_species = tk.Label(
            card_dna.body,
            text="",
            bg=BG_PANEL,
            fg=TEXT_PRIMARY,
            font=FONT_BODY,
            anchor="w",
        )
        self.lbl_alien_species.pack(fill="x", pady=(2, 1))

        self.lbl_alien_ability = tk.Label(
            card_dna.body,
            text="",
            bg=BG_PANEL,
            fg=TEXT_MUTED,
            font=FONT_BODY,
            anchor="w",
        )
        self.lbl_alien_ability.pack(fill="x")

        # Selector buttons
        btn_nav_frame = tk.Frame(card_dna.body, bg=BG_PANEL)
        btn_nav_frame.pack(fill="x", pady=(8, 0))

        self.btn_prev = ttk.Button(
            btn_nav_frame,
            text="◀ PREVIOUS ALIEN",
            style="Omni.TButton",
            command=self._prev_alien,
        )
        self.btn_prev.pack(side="left", fill="x", expand=True, padx=(0, 4))

        self.btn_next = ttk.Button(
            btn_nav_frame,
            text="NEXT ALIEN ▶",
            style="Omni.TButton",
            command=self._next_alien,
        )
        self.btn_next.pack(side="right", fill="x", expand=True, padx=(4, 0))

        # Card 2: Watch Face Configuration Options
        card_opts = CyberCard(right_col, title="Timekeeper Complications", subtitle="Display Settings")
        card_opts.pack(fill="x", pady=(0, 8))

        opts_inner = tk.Frame(card_opts.body, bg=BG_PANEL)
        opts_inner.pack(fill="x")

        self.var_24h = tk.BooleanVar(value=True)
        chk_24h = ttk.Checkbutton(
            opts_inner,
            text="24-Hour Military Time Format",
            variable=self.var_24h,
            command=self._update_opts,
        )
        chk_24h.pack(anchor="w", pady=2)

        self.var_seconds = tk.BooleanVar(value=True)
        chk_sec = ttk.Checkbutton(
            opts_inner,
            text="Live Seconds Indicator",
            variable=self.var_seconds,
            command=self._update_opts,
        )
        chk_sec.pack(anchor="w", pady=2)

        # Card 3: Export & Installation Actions
        card_action = CyberCard(right_col, title="Package for Redmi Watch Move 2", subtitle="Build Artifact")
        card_action.pack(fill="both", expand=True)

        desc = tk.Label(
            card_action.body,
            text="Generates complete watch face layout manifest and asset specification for compile into .bin/.zip format compatible with Redmi Watch Move 2.",
            bg=BG_PANEL,
            fg=TEXT_MUTED,
            font=FONT_BODY,
            wraplength=440,
            justify="left",
            anchor="w",
        )
        desc.pack(fill="x", pady=(0, 8))

        self.btn_export = ttk.Button(
            card_action.body,
            text="⚡ EXPORT WATCH FACE BUNDLE (.BIN/.JSON)",
            style="Accent.TButton",
            command=self._export_bundle,
        )
        self.btn_export.pack(fill="x", pady=2)

        self._update_alien_card()

    def _on_combo_select(self, _event: tk.Event) -> None:
        idx = self.combo_alien.current()
        if 0 <= idx < len(self.all_aliens):
            sound_player.play_alien_select()
            self.current_alien_idx = idx
            self._update_alien_card()

    def _prev_alien(self) -> None:
        sound_player.play_dial_turn()
        self.current_alien_idx = (self.current_alien_idx - 1) % len(self.all_aliens)
        self.combo_alien.current(self.current_alien_idx)
        self._update_alien_card()

    def _next_alien(self) -> None:
        sound_player.play_dial_turn()
        self.current_alien_idx = (self.current_alien_idx + 1) % len(self.all_aliens)
        self.combo_alien.current(self.current_alien_idx)
        self._update_alien_card()

    def _update_opts(self) -> None:
        self.preview_canvas.format_24h = self.var_24h.get()
        self.preview_canvas.show_seconds = self.var_seconds.get()
        self.preview_canvas.draw()

    def _update_alien_card(self) -> None:
        alien = self.all_aliens[self.current_alien_idx]
        self.config.selected_alien_id = alien.id
        self.preview_canvas.update_alien(alien)

        self.lbl_alien_title.config(
            text=f"[{alien.codename}] #{alien.id:02d} {alien.name.upper()}",
            fg=alien.signature_color,
        )
        self.lbl_alien_species.config(
            text=f"Species: {alien.species}  |  Homeworld: {alien.homeworld}"
        )
        self.lbl_alien_ability.config(
            text=f"Ability: {alien.primary_ability}  |  DNA: {alien.dna_code}"
        )

    def _export_bundle(self) -> None:
        sound_player.play_beep()
        out_dir = Path("dist/watchface")
        generator = WatchFaceGenerator(
            WatchFaceConfig(
                target_device="Redmi Watch Move 2",
                selected_alien_id=self.all_aliens[self.current_alien_idx].id,
                time_format_24h=self.var_24h.get(),
                show_seconds=self.var_seconds.get(),
            )
        )
        try:
            manifest_path = generator.export_bundle(out_dir)
            alien = self.all_aliens[self.current_alien_idx]
            messagebox.showinfo(
                "Watch Face Export Complete",
                f"Successfully exported Omnitrix Watch Face for Redmi Watch Move 2!\n\n"
                f"Selected Alien: #{alien.id} {alien.name}\n"
                f"Destination: {manifest_path.parent.resolve()}\n\n"
                f"Files created:\n"
                f"• watchface_manifest.json\n"
                f"• WATCHFACE_SPEC.md",
            )
        except Exception as ex:
            messagebox.showerror("Export Failed", f"Could not export watch face bundle:\n{ex}")

    def tick_animation(self) -> None:
        """Advance time display and pulsing glow in preview."""
        self.preview_canvas.tick_animation()
