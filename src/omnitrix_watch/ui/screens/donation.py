"""Omnitrix-themed Donation & Sponsorship Screen."""

from __future__ import annotations

import tkinter as tk
from tkinter import messagebox, ttk
import webbrowser

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

GITHUB_SPONSORS_URL = "https://github.com/sponsors/harshar007"
BUYMEACOFFEE_URL = "https://buymeacoffee.com/harshar007"
KOFI_URL = "https://ko-fi.com/harshar007"
PAYPAL_URL = "https://paypal.me/harshar007"


class DonationScreen(ttk.Frame):
    """Screen for supporting the project and viewing sponsorship tiers."""

    def __init__(self, parent: tk.Widget) -> None:
        super().__init__(parent, style="TFrame")
        self._build_ui()

    def _build_ui(self) -> None:
        # Title bar
        header = ttk.Frame(self, style="TFrame")
        header.pack(fill="x", padx=20, pady=(15, 8))

        title_box = ttk.Frame(header, style="TFrame")
        title_box.pack(side="left")

        ttk.Label(
            title_box,
            text="💖 GALVAN PRIME DONATION & SPONSOR HUB",
            foreground=OMNI_GREEN,
            font=FONT_TITLE,
        ).pack(anchor="w")

        ttk.Label(
            title_box,
            text="POWER AZMUTH'S WORKSHOP // 100% FREE & OPEN-SOURCE COMMUNITY PROJECT",
            foreground=TEXT_MUTED,
            font=FONT_BADGE,
        ).pack(anchor="w", pady=(2, 0))

        # Main Layout: 2 Columns
        body = ttk.Frame(self, style="TFrame")
        body.pack(fill="both", expand=True, padx=20, pady=10)

        # Left Column: Instant One-Click Donate Buttons & Perks
        left_col = ttk.Frame(body, style="Panel.TFrame", padding=15)
        left_col.pack(side="left", fill="both", expand=True, padx=(0, 10))

        ttk.Label(
            left_col,
            text="⚡ INSTANT DONATION CHANNELS",
            foreground=OMNI_GREEN,
            font=FONT_HEADING,
        ).pack(anchor="w", pady=(0, 10))

        # Button 1: GitHub Sponsors
        btn_gh = tk.Button(
            left_col,
            text="💖 SPONSOR ON GITHUB SPONSORS",
            bg="#24292e",
            fg="#ea4aaa",
            activebackground="#ea4aaa",
            activeforeground="#ffffff",
            font=("Consolas", 10, "bold"),
            relief="solid",
            bd=1,
            cursor="hand2",
            padx=12,
            pady=8,
            command=lambda: self._open_url(GITHUB_SPONSORS_URL),
        )
        btn_gh.pack(fill="x", pady=4)

        # Button 2: Buy Me A Coffee
        btn_bmc = tk.Button(
            left_col,
            text="☕ BUY ME A COFFEE ($3 / $5)",
            bg="#2a2510",
            fg="#ffdd00",
            activebackground="#ffdd00",
            activeforeground="#000000",
            font=("Consolas", 10, "bold"),
            relief="solid",
            bd=1,
            cursor="hand2",
            padx=12,
            pady=8,
            command=lambda: self._open_url(BUYMEACOFFEE_URL),
        )
        btn_bmc.pack(fill="x", pady=4)

        # Button 3: Ko-fi
        btn_kofi = tk.Button(
            left_col,
            text="🥤 TIP ON KO-FI (NO FEES)",
            bg="#2a1515",
            fg="#ff5e5b",
            activebackground="#ff5e5b",
            activeforeground="#ffffff",
            font=("Consolas", 10, "bold"),
            relief="solid",
            bd=1,
            cursor="hand2",
            padx=12,
            pady=8,
            command=lambda: self._open_url(KOFI_URL),
        )
        btn_kofi.pack(fill="x", pady=4)

        # Button 4: PayPal
        btn_pp = tk.Button(
            left_col,
            text="🅿️ SEND VIA PAYPAL",
            bg="#0d2038",
            fg="#38bdf8",
            activebackground="#0284c7",
            activeforeground="#ffffff",
            font=("Consolas", 10, "bold"),
            relief="solid",
            bd=1,
            cursor="hand2",
            padx=12,
            pady=8,
            command=lambda: self._open_url(PAYPAL_URL),
        )
        btn_pp.pack(fill="x", pady=4)

        # Perks & Transparency Card
        perks_box = ttk.Frame(left_col, style="Surface.TFrame", padding=10)
        perks_box.pack(fill="both", expand=True, pady=(15, 0))

        ttk.Label(
            perks_box,
            text="📊 WHERE YOUR DONATIONS GO",
            foreground=OMNI_GREEN,
            font=FONT_HEADING,
        ).pack(anchor="w", pady=(0, 6))

        breakdown = (
            "• 50% Hardware Lab: Purchasing smartwatches & BLE sniffers\n"
            "• 25% CI/CD Cloud: GitHub Actions runners & build hosting\n"
            "• 15% Audio/Vector Art: Synthesized sound & alien graphics\n"
            "• 10% Coffee & Fuel: Late night debugging sessions!"
        )
        ttk.Label(
            perks_box,
            text=breakdown,
            foreground=TEXT_PRIMARY,
            font=("Consolas", 9),
            justify="left",
        ).pack(anchor="w")

        # Right Column: Galactic Tiers & Crypto
        right_col = ttk.Frame(body, style="Panel.TFrame", padding=15)
        right_col.pack(side="right", fill="both", expand=True)

        ttk.Label(
            right_col,
            text="🪐 GALACTIC SPONSORSHIP TIERS",
            foreground=OMNI_GREEN,
            font=FONT_HEADING,
        ).pack(anchor="w", pady=(0, 8))

        tiers = [
            ("🟢 LEVEL 1: GALVANIC CADET ($3)", "Name permanently inscribed in README.md Hall of Fame!"),
            ("⚡ LEVEL 2: OMNITRIX BEARER ($10)", "Priority BLE hardware help + Vote on next Alien DNA profile!"),
            ("🧬 LEVEL 3: AZMUTH'S APPRENTICE ($25)", "Early beta access to new watch face .bin files + Logo in release notes!"),
            ("🌌 LEVEL 4: GALVAN HIGH COUNCIL ($100)", "Top sponsor banner + 1-on-1 BLE protocol consultation!"),
        ]

        for title, desc in tiers:
            t_frame = ttk.Frame(right_col, style="Surface.TFrame", padding=8)
            t_frame.pack(fill="x", pady=3)
            ttk.Label(t_frame, text=title, foreground=OMNI_GREEN_GLOW, font=("Consolas", 9, "bold")).pack(anchor="w")
            ttk.Label(t_frame, text=desc, foreground=TEXT_MUTED, font=("Consolas", 8)).pack(anchor="w")

        # Crypto Section
        crypto_box = ttk.Frame(right_col, style="Surface.TFrame", padding=10)
        crypto_box.pack(fill="x", pady=(12, 0))

        ttk.Label(
            crypto_box,
            text="💎 WEB3 CRYPTO DONATION",
            foreground=OMNI_GREEN,
            font=FONT_HEADING,
        ).pack(anchor="w", pady=(0, 4))

        ttk.Label(
            crypto_box,
            text="View full crypto wallet list (BTC, ETH, USDT, SOL) in DONATION.md or copy addresses directly from the project repository.",
            foreground=TEXT_MUTED,
            font=("Consolas", 8),
            wraplength=380,
        ).pack(anchor="w")

    def _open_url(self, url: str) -> None:
        sound_player.play_beep()
        try:
            webbrowser.open(url)
        except Exception as e:
            messagebox.showerror("Could not open browser", f"URL: {url}\n\nError: {e}")
