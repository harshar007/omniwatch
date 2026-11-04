"""Sci-Fi segmented cyber navigation bar for switching between Omnitrix screens."""

from __future__ import annotations

import tkinter as tk
from typing import Callable, List, Optional, Tuple

from omnitrix_watch.sound import sound_player
from omnitrix_watch.ui.theme import (
    BG_DARK,
    BG_PANEL,
    BG_SURFACE,
    BORDER_COLOR,
    BORDER_BRIGHT,
    FONT_BADGE,
    FONT_HEADING,
    OMNI_CORE_GLOW,
    OMNI_GREEN,
    OMNI_GREEN_DARK,
    OMNI_GREEN_GLOW,
    TEXT_DIM,
    TEXT_MUTED,
    TEXT_PRIMARY,
)


class OmniNavBar(tk.Frame):
    """Futuristic segmented navigation bar with animated glowing tabs and hotkey cues."""

    def __init__(
        self,
        parent: tk.Widget,
        tabs: List[Tuple[str, str]],  # List of (tab_id, title)
        on_select: Callable[[int, str], None],
        initial_index: int = 0,
        **kwargs,
    ) -> None:
        super().__init__(
            parent,
            bg=BG_DARK,
            padx=10,
            pady=4,
            **kwargs,
        )
        self.tabs = tabs
        self.on_select = on_select
        self.current_index = initial_index
        self.buttons: List[tk.Frame] = []
        self.label_widgets: List[tk.Label] = []
        self.indicator_bars: List[tk.Frame] = []

        self._build_bar()

    def _build_bar(self) -> None:
        """Construct segmented tab buttons."""
        container = tk.Frame(self, bg=BG_DARK)
        container.pack(fill="x")

        for idx, (tab_id, title) in enumerate(self.tabs):
            tab_frame = tk.Frame(
                container,
                bg=BG_PANEL if idx == self.current_index else BG_DARK,
                highlightthickness=1,
                highlightbackground=BORDER_BRIGHT if idx == self.current_index else BORDER_COLOR,
                cursor="hand2",
            )
            tab_frame.pack(side="left", padx=3, pady=2, fill="y")

            # Tab text
            hotkey_str = f"[{idx + 1}] "
            lbl = tk.Label(
                tab_frame,
                text=f"{hotkey_str}{title}",
                bg=BG_PANEL if idx == self.current_index else BG_DARK,
                fg=OMNI_GREEN_GLOW if idx == self.current_index else TEXT_MUTED,
                font=FONT_HEADING,
                padx=12,
                pady=6,
                cursor="hand2",
            )
            lbl.pack(fill="both", expand=True)

            # Bottom illuminated glow line indicator
            indicator = tk.Frame(
                tab_frame,
                bg=OMNI_GREEN if idx == self.current_index else BG_DARK,
                height=2,
            )
            indicator.pack(fill="x", side="bottom")

            # Bind events for clicks and hovers
            for widget in (tab_frame, lbl):
                widget.bind("<Button-1>", lambda e, i=idx: self._handle_click(i))
                widget.bind("<Enter>", lambda e, i=idx: self._handle_hover(i, True))
                widget.bind("<Leave>", lambda e, i=idx: self._handle_hover(i, False))

            self.buttons.append(tab_frame)
            self.label_widgets.append(lbl)
            self.indicator_bars.append(indicator)

    def _handle_click(self, index: int) -> None:
        """Process tab click."""
        if index == self.current_index:
            return
        sound_player.play_dial_turn()
        self.select_tab(index)

    def _handle_hover(self, index: int, is_entering: bool) -> None:
        """Subtle hover feedback."""
        if index == self.current_index:
            return
        if is_entering:
            self.buttons[index].config(bg=BG_SURFACE)
            self.label_widgets[index].config(bg=BG_SURFACE, fg=OMNI_GREEN)
        else:
            self.buttons[index].config(bg=BG_DARK)
            self.label_widgets[index].config(bg=BG_DARK, fg=TEXT_MUTED)

    def select_tab(self, index: int) -> None:
        """Activate the tab at specified index."""
        if index < 0 or index >= len(self.tabs):
            return

        old_idx = self.current_index
        self.current_index = index

        # Reset old tab
        self.buttons[old_idx].config(bg=BG_DARK, highlightbackground=BORDER_COLOR)
        self.label_widgets[old_idx].config(bg=BG_DARK, fg=TEXT_MUTED)
        self.indicator_bars[old_idx].config(bg=BG_DARK)

        # Highlight new tab
        self.buttons[index].config(bg=BG_PANEL, highlightbackground=BORDER_BRIGHT)
        self.label_widgets[index].config(bg=BG_PANEL, fg=OMNI_GREEN_GLOW)
        self.indicator_bars[index].config(bg=OMNI_GREEN)

        tab_id, _ = self.tabs[index]
        self.on_select(index, tab_id)
