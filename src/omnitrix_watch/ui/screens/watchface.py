"""Omnitrix Watch Face Screen with Alien DNA selection and live timekeeper."""

from __future__ import annotations

import datetime
import math
from pathlib import Path
import tkinter as tk
from tkinter import messagebox, ttk
from typing import Optional

from omnitrix_watch.sound import sound_player
from omnitrix_watch.ui.theme import (
    BG_DARK,
    BG_PANEL,
    BG_SURFACE,
    BORDER_COLOR,
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


class WatchPreviewCanvas(tk.Canvas):
    """Visual preview of the watch face on the Redmi Watch Move 2 AMOLED display."""

    def __init__(self, parent: tk.Widget, width: int = 260, height: int = 300, **kwargs) -> None:
        super().__init__(
            parent,
            width=width,
            height=height,
            bg="#020503",
            highlightthickness=2,
            highlightbackground=BORDER_COLOR,
            **kwargs,
        )
        self.w = width
        self.h = height
        self.selected_alien: AlienProfile = DEFAULT_ALIEN_ROSTER[0]
        self.show_seconds = True
        self.format_24h = True
        self.pulse_phase = 0.0

        self.draw()

    def update_alien(self, alien: AlienProfile) -> None:
        """Switch current alien display."""
        self.selected_alien = alien
        self.draw()

    def tick_animation(self) -> None:
        """Advance time and pulsing glow."""
        self.pulse_phase = (self.pulse_phase + 0.1) % (2 * math.pi)
        self.draw()

    def draw(self) -> None:
        """Render watch face elements simulating Redmi Watch Move 2 screen."""
        self.delete("all")
        cx = self.w / 2
        cy = self.h / 2

        # 1. Bezel of Redmi Watch Move 2 (curved rectangular smartwatch frame)
        self.create_rectangle(
            6, 6, self.w - 6, self.h - 6,
            outline="#1e3828", width=3
        )

        # 2. Outer Omnitrix ring with pulsing glow
        glow_width = 2 + int(math.sin(self.pulse_phase) * 1.5 + 1.5)
        accent_color = self.selected_alien.signature_color
        dial_r = min(self.w, self.h) / 2 - 28

        self.create_oval(
            cx - dial_r, cy - dial_r, cx + dial_r, cy + dial_r,
            outline=OMNI_GREEN, width=glow_width
        )
        self.create_oval(
            cx - dial_r + 6, cy - dial_r + 6, cx + dial_r - 6, cy + dial_r - 6,
            outline=OMNI_GREEN_DARK, width=1
        )

        # 3. Timekeeper display (Top section of watch face)
        now = datetime.datetime.now()
        if self.format_24h:
            time_str = now.strftime("%H:%M:%S" if self.show_seconds else "%H:%M")
        else:
            time_str = now.strftime("%I:%M:%S" if self.show_seconds else "%I:%M")

        self.create_text(
            cx, cy - dial_r + 28,
            text=time_str,
            fill=OMNI_GREEN_GLOW,
            font=("Consolas", 16, "bold"),
        )

        # Date subtitle
        date_str = now.strftime("%a, %b %d").upper()
        self.create_text(
            cx, cy - dial_r + 48,
            text=date_str,
            fill="#a0e8b0",
            font=("Consolas", 8),
        )

        # 4. Omnitrix Hourglass motif in center
        tri_size = 40
        top_pts = [cx - tri_size, cy - 10, cx + tri_size, cy - 10, cx, cy + 20]
        bot_pts = [cx - tri_size, cy + 50, cx + tri_size, cy + 50, cx, cy + 20]
        self.create_polygon(top_pts, fill=accent_color, outline=OMNI_GREEN_DARK, width=1)
        self.create_polygon(bot_pts, fill=accent_color, outline=OMNI_GREEN_DARK, width=1)

        # 5. Alien Core Emblem & Name
        self.create_oval(cx - 18, cy + 18, cx + 18, cy + 54, fill=BG_DARK, outline=OMNI_GREEN_GLOW, width=2)
        self.create_text(
            cx, cy + 36,
            text=f"#{self.selected_alien.id:02d}",
            fill=OMNI_GREEN,
            font=("Consolas", 10, "bold"),
        )

        self.create_text(
            cx, cy + 76,
            text=self.selected_alien.name.upper(),
            fill=accent_color,
            font=("Consolas", 10, "bold"),
        )

        # 6. Complications at bottom (Battery & Pulse)
        self.create_text(
            35, self.h - 22,
            text="⚡ 98%",
            fill=OMNI_GREEN,
            font=("Consolas", 8, "bold"),
        )
        self.create_text(
            self.w - 38, self.h - 22,
            text="♥ 74 BPM",
            fill="#ff3355",
            font=("Consolas", 8, "bold"),
        )


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
        header = ttk.Frame(self, style="TFrame")
        header.pack(fill="x", padx=20, pady=(15, 10))

        title = ttk.Label(
            header,
            text="OMNITRIX WATCH FACE BUILDER",
            style="Header.Label",
            font=FONT_TITLE,
            foreground=OMNI_GREEN,
        )
        title.pack(side="left")

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
        body = ttk.Frame(self, style="TFrame")
        body.pack(fill="both", expand=True, padx=20, pady=10)

        # Left Column: Preview
        left_col = ttk.Frame(body, style="Panel.TFrame", padding=15)
        left_col.pack(side="left", fill="y", padx=(0, 15))

        preview_lbl = ttk.Label(
            left_col,
            text="WATCH DISPLAY PREVIEW",
            foreground=OMNI_GREEN,
            font=FONT_HEADING,
        )
        preview_lbl.pack(anchor="center", pady=(0, 10))

        self.preview_canvas = WatchPreviewCanvas(left_col, width=240, height=290)
        self.preview_canvas.pack(pady=5)

        note_lbl = ttk.Label(
            left_col,
            text="AMOLED 1.85\" | 390x450 px",
            style="Muted.TLabel",
            font=FONT_BADGE,
        )
        note_lbl.pack(pady=(6, 0))

        # Right Column: Alien DNA Matrix & Controls
        right_col = ttk.Frame(body, style="TFrame")
        right_col.pack(side="right", fill="both", expand=True)

        # Card 1: Alien DNA Profile Card
        alien_card = ttk.Frame(right_col, style="Surface.TFrame", padding=12)
        alien_card.pack(fill="x", pady=(0, 10))

        ttk.Label(
            alien_card,
            text="🧬 ACTIVE ALIEN DNA MATRIX",
            foreground=OMNI_GREEN,
            font=FONT_HEADING,
        ).pack(anchor="w", pady=(0, 8))

        self.lbl_alien_title = ttk.Label(
            alien_card,
            text="",
            foreground=OMNI_GREEN_GLOW,
            font=("Consolas", 13, "bold"),
        )
        self.lbl_alien_title.pack(anchor="w")

        self.lbl_alien_species = ttk.Label(
            alien_card,
            text="",
            foreground=TEXT_PRIMARY,
            font=FONT_BODY,
        )
        self.lbl_alien_species.pack(anchor="w", pady=(2, 2))

        self.lbl_alien_ability = ttk.Label(
            alien_card,
            text="",
            foreground=TEXT_MUTED,
            font=FONT_BODY,
        )
        self.lbl_alien_ability.pack(anchor="w")

        # Selector buttons
        btn_nav_frame = ttk.Frame(alien_card, style="Surface.TFrame")
        btn_nav_frame.pack(fill="x", pady=(10, 0))

        self.btn_prev = ttk.Button(
            btn_nav_frame,
            text="◀ PREVIOUS ALIEN",
            style="Omni.TButton",
            command=self._prev_alien,
        )
        self.btn_prev.pack(side="left", fill="x", expand=True, padx=(0, 5))

        self.btn_next = ttk.Button(
            btn_nav_frame,
            text="NEXT ALIEN ▶",
            style="Omni.TButton",
            command=self._next_alien,
        )
        self.btn_next.pack(side="right", fill="x", expand=True, padx=(5, 0))

        # Card 2: Watch Face Configuration Options
        opts_card = ttk.Frame(right_col, style="Surface.TFrame", padding=12)
        opts_card.pack(fill="x", pady=(0, 10))

        ttk.Label(
            opts_card,
            text="⚙️ WATCH FACE TIME & COMPLICATIONS",
            foreground=OMNI_GREEN,
            font=FONT_HEADING,
        ).pack(anchor="w", pady=(0, 8))

        self.var_24h = tk.BooleanVar(value=True)
        chk_24h = ttk.Checkbutton(
            opts_card,
            text="24-Hour Time Format (Military Clock)",
            variable=self.var_24h,
            command=self._update_opts,
        )
        chk_24h.pack(anchor="w", pady=2)

        self.var_seconds = tk.BooleanVar(value=True)
        chk_sec = ttk.Checkbutton(
            opts_card,
            text="Show Running Seconds Indicator",
            variable=self.var_seconds,
            command=self._update_opts,
        )
        chk_sec.pack(anchor="w", pady=2)

        # Card 3: Export & Installation Actions
        action_card = ttk.Frame(right_col, style="Surface.TFrame", padding=12)
        action_card.pack(fill="both", expand=True)

        ttk.Label(
            action_card,
            text="📦 PACKAGE FOR REDMI WATCH MOVE 2",
            foreground=OMNI_GREEN,
            font=FONT_HEADING,
        ).pack(anchor="w", pady=(0, 6))

        desc = ttk.Label(
            action_card,
            text="Generates watch face layout manifest and asset specification for compile into .bin/.zip format compatible with Redmi Watch Move 2.",
            foreground=TEXT_MUTED,
            font=FONT_BODY,
            wraplength=420,
        )
        desc.pack(anchor="w", pady=(0, 10))

        self.btn_export = ttk.Button(
            action_card,
            text="⚡ EXPORT WATCH FACE BUNDLE (.BIN/.JSON)",
            style="Omni.TButton",
            command=self._export_bundle,
        )
        self.btn_export.pack(fill="x", pady=5)

        self._update_alien_card()

    def _prev_alien(self) -> None:
        sound_player.play_dial_turn()
        self.current_alien_idx = (self.current_alien_idx - 1) % len(self.all_aliens)
        self._update_alien_card()

    def _next_alien(self) -> None:
        sound_player.play_dial_turn()
        self.current_alien_idx = (self.current_alien_idx + 1) % len(self.all_aliens)
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
            foreground=alien.signature_color,
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
