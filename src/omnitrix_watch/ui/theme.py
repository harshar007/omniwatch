"""Omnitrix-inspired visual theme palette and Tkinter styling."""

from __future__ import annotations

import tkinter as tk
from tkinter import ttk

# Omnitrix color palette
BG_VOID = "#030604"
BG_DARK = "#080c0a"
BG_PANEL = "#101813"
BG_SURFACE = "#17231c"
BG_HIGHLIGHT = "#203328"
BORDER_COLOR = "#264a34"
BORDER_BRIGHT = "#3f7a55"

OMNI_GREEN = "#00ff55"
OMNI_GREEN_GLOW = "#70ff94"
OMNI_CORE_GLOW = "#a7f3d0"
OMNI_GREEN_DIM = "#0e853f"
OMNI_GREEN_DARK = "#07381b"

TEXT_PRIMARY = "#e6f8ee"
TEXT_MUTED = "#779e85"
TEXT_DIM = "#476352"

COLOR_WARNING = "#fbbf24"
COLOR_ERROR = "#f87171"
COLOR_INFO = "#38bdf8"
COLOR_CYAN = "#00f0ff"
COLOR_PURPLE = "#c084fc"

FONT_TITLE = ("Consolas", 15, "bold")
FONT_HEADING = ("Consolas", 11, "bold")
FONT_BODY = ("Consolas", 10)
FONT_MONO = ("Consolas", 9)
FONT_DIAL = ("Consolas", 11, "bold")
FONT_BADGE = ("Consolas", 8, "bold")
FONT_SUBTITLE = ("Consolas", 9, "normal")


def apply_theme(root: tk.Tk) -> None:
    """Apply Omnitrix dark styling to ttk widgets."""
    root.configure(bg=BG_DARK)

    style = ttk.Style(root)
    # Use clam or default engine that supports extensive color overrides
    try:
        style.theme_use("clam")
    except Exception:
        pass

    style.configure(
        "TFrame",
        background=BG_DARK,
    )
    style.configure(
        "Panel.TFrame",
        background=BG_PANEL,
        relief="flat",
    )
    style.configure(
        "Surface.TFrame",
        background=BG_SURFACE,
        relief="solid",
        borderwidth=1,
    )
    style.configure(
        "Card.TFrame",
        background=BG_PANEL,
        relief="solid",
        borderwidth=1,
    )

    style.configure(
        "TLabel",
        background=BG_DARK,
        foreground=TEXT_PRIMARY,
        font=FONT_BODY,
    )
    style.configure(
        "Panel.TLabel",
        background=BG_PANEL,
        foreground=TEXT_PRIMARY,
        font=FONT_BODY,
    )
    style.configure(
        "Muted.TLabel",
        background=BG_DARK,
        foreground=TEXT_MUTED,
        font=FONT_BODY,
    )
    style.configure(
        "Header.TLabel",
        background=BG_DARK,
        foreground=OMNI_GREEN,
        font=FONT_TITLE,
    )
    style.configure(
        "Subheader.TLabel",
        background=BG_DARK,
        foreground=OMNI_GREEN_GLOW,
        font=FONT_HEADING,
    )
    style.configure(
        "Value.TLabel",
        background=BG_PANEL,
        foreground=OMNI_GREEN_GLOW,
        font=("Consolas", 12, "bold"),
    )
    style.configure(
        "Badge.TLabel",
        background=OMNI_GREEN_DARK,
        foreground=OMNI_GREEN_GLOW,
        font=FONT_BADGE,
        padding=(6, 2),
    )

    # Omnitrix primary buttons
    style.configure(
        "Omni.TButton",
        background=BG_SURFACE,
        foreground=OMNI_GREEN,
        font=FONT_HEADING,
        borderwidth=1,
        bordercolor=OMNI_GREEN_DIM,
        focuscolor="none",
        padding=(10, 6),
    )
    style.map(
        "Omni.TButton",
        background=[("active", BG_HIGHLIGHT), ("disabled", BG_DARK)],
        foreground=[("active", OMNI_GREEN_GLOW), ("disabled", TEXT_DIM)],
        bordercolor=[("active", OMNI_GREEN), ("disabled", BG_PANEL)],
    )

    # Accent button (Vibrant illuminated green)
    style.configure(
        "Accent.TButton",
        background=OMNI_GREEN_DARK,
        foreground=OMNI_GREEN_GLOW,
        font=FONT_HEADING,
        borderwidth=1,
        bordercolor=OMNI_GREEN,
        focuscolor="none",
        padding=(12, 6),
    )
    style.map(
        "Accent.TButton",
        background=[("active", OMNI_GREEN_DIM), ("disabled", BG_DARK)],
        foreground=[("active", "#ffffff"), ("disabled", TEXT_DIM)],
        bordercolor=[("active", OMNI_CORE_GLOW), ("disabled", BG_PANEL)],
    )

    # Danger / disconnect button
    style.configure(
        "Danger.TButton",
        background=BG_SURFACE,
        foreground=COLOR_ERROR,
        font=FONT_HEADING,
        borderwidth=1,
        bordercolor="#7f1d1d",
        padding=(10, 6),
    )
    style.map(
        "Danger.TButton",
        background=[("active", "#450a0a"), ("disabled", BG_DARK)],
        foreground=[("active", "#fca5a5"), ("disabled", TEXT_DIM)],
    )

    # Treeview (Data tables for BLE devices & GATT attributes)
    style.configure(
        "Treeview",
        background=BG_PANEL,
        fieldbackground=BG_PANEL,
        foreground=TEXT_PRIMARY,
        font=FONT_MONO,
        rowheight=26,
        borderwidth=1,
    )
    style.configure(
        "Treeview.Heading",
        background=BG_SURFACE,
        foreground=OMNI_GREEN,
        font=FONT_HEADING,
        relief="flat",
    )
    style.map(
        "Treeview",
        background=[("selected", BG_HIGHLIGHT)],
        foreground=[("selected", OMNI_GREEN_GLOW)],
    )

    # Notebook (Tab switcher)
    style.configure(
        "TNotebook",
        background=BG_DARK,
        borderwidth=0,
    )
    style.configure(
        "TNotebook.Tab",
        background=BG_PANEL,
        foreground=TEXT_MUTED,
        font=FONT_HEADING,
        padding=(14, 6),
    )
    style.map(
        "TNotebook.Tab",
        background=[("selected", BG_SURFACE)],
        foreground=[("selected", OMNI_GREEN)],
    )

    # Progress bar
    style.configure(
        "Omni.Horizontal.TProgressbar",
        troughcolor=BG_PANEL,
        background=OMNI_GREEN,
        bordercolor=BORDER_COLOR,
        lightcolor=OMNI_GREEN_GLOW,
        darkcolor=OMNI_GREEN_DIM,
    )

    # Custom Entry fields
    style.configure(
        "TEntry",
        fieldbackground=BG_PANEL,
        foreground=TEXT_PRIMARY,
        insertcolor=OMNI_GREEN,
        bordercolor=BORDER_COLOR,
        lightcolor=BORDER_COLOR,
        darkcolor=BORDER_COLOR,
    )
