"""Main Omnitrix Watch Desktop UI application."""

from __future__ import annotations

import logging
from pathlib import Path
import sys
import tkinter as tk
from tkinter import messagebox, ttk
from typing import Optional

from omnitrix_watch.config import AppConfig
from omnitrix_watch.models.device import DeviceSummary, GattInventory
from omnitrix_watch.services.device_session import DeviceSession, SessionEvent, SessionState
from omnitrix_watch.sound import sound_player
from omnitrix_watch.ui.components.footer_hud import FooterHUD
from omnitrix_watch.ui.components.header_bar import HeaderBar
from omnitrix_watch.ui.components.navbar import OmniNavBar
from omnitrix_watch.ui.screens.device_details import DeviceDetailsScreen
from omnitrix_watch.ui.screens.device_picker import DevicePickerScreen
from omnitrix_watch.ui.screens.donation import DonationScreen
from omnitrix_watch.ui.screens.home import HomeScreen
from omnitrix_watch.ui.screens.simulator import OmnitrixSimulatorScreen
from omnitrix_watch.ui.screens.watchface import WatchFaceScreen
from omnitrix_watch.ui.theme import (
    BG_DARK,
    BG_PANEL,
    BG_SURFACE,
    BORDER_COLOR,
    FONT_BADGE,
    OMNI_GREEN,
    OMNI_GREEN_DARK,
    OMNI_GREEN_GLOW,
    TEXT_MUTED,
    apply_theme,
)

logger = logging.getLogger(__name__)


class OmnitrixApp:
    """Omnitrix-themed desktop application for BLE discovery & GATT inspection."""

    def __init__(self, root: tk.Tk, config: Optional[AppConfig] = None) -> None:
        self.root = root
        self.config = config or AppConfig()
        self.session = DeviceSession(self.config)

        self.root.title("OMNITRIX - Watch Companion & Research Platform")
        self.root.geometry(f"{self.config.ui.window_width}x{self.config.ui.window_height}")
        self.root.minsize(800, 620)

        # Set Omnitrix App Icon if available
        self._set_app_icon()

        apply_theme(self.root)

        # 1. Top Cyber Header Bar
        self.header_bar = HeaderBar(self.root, on_audio_toggle=self._on_audio_toggled)
        self.header_bar.pack(fill="x", side="top")

        # 2. Segmented Cyber Navigation Bar
        nav_tabs = [
            ("simulator", "⚡ SIMULATOR"),
            ("home", "🌐 DASHBOARD"),
            ("watchface", "⌚ WATCH FACE"),
            ("picker", "📡 BLE SCANNER"),
            ("details", "🔍 GATT INVENTORY"),
            ("donation", "💖 GALVAN PRIME"),
        ]
        self.navbar = OmniNavBar(
            self.root,
            tabs=nav_tabs,
            on_select=self._on_navbar_select,
            initial_index=0,
        )
        self.navbar.pack(fill="x", side="top")

        # 3. Tab notebook for screen container
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill="both", expand=True)

        # Screen instances
        self.screen_simulator = OmnitrixSimulatorScreen(self.notebook)
        self.screen_watchface = WatchFaceScreen(self.notebook)
        self.screen_home = HomeScreen(
            self.notebook,
            on_scan=self._action_start_scan,
            on_connect=self._action_connect,
            on_disconnect=self._action_disconnect,
            on_inspect=self._action_inspect,
            on_open_picker=lambda: self.select_screen_by_index(3),
            on_open_inventory=lambda: self.select_screen_by_index(4),
            on_open_watchface=lambda: self.select_screen_by_index(2),
            on_open_simulator=lambda: self.select_screen_by_index(0),
        )
        self.screen_picker = DevicePickerScreen(
            self.notebook,
            on_start_scan=self.session.start_scan,
            on_cancel_scan=self.session.cancel_scan,
            on_device_selected=self._action_select_device,
        )
        self.screen_details = DeviceDetailsScreen(
            self.notebook,
            on_inspect=self._action_inspect,
            on_export=self._action_export_inventory,
        )
        self.screen_donation = DonationScreen(self.notebook)

        self.screens = [
            self.screen_simulator,
            self.screen_home,
            self.screen_watchface,
            self.screen_picker,
            self.screen_details,
            self.screen_donation,
        ]

        self.notebook.add(self.screen_simulator, text="  ⚡ SIMULATOR  ")
        self.notebook.add(self.screen_home, text="  DIAL DASHBOARD  ")
        self.notebook.add(self.screen_watchface, text="  WATCH FACE  ")
        self.notebook.add(self.screen_picker, text="  BLE SCANNER  ")
        self.notebook.add(self.screen_details, text="  GATT INVENTORY  ")
        self.notebook.add(self.screen_donation, text="  💖 DONATION  ")

        self.notebook.bind("<<NotebookTabChanged>>", self._on_notebook_tab_changed)

        # 4. Global HUD Telemetry Bar at bottom
        self.footer_hud = FooterHUD(self.root)
        self.footer_hud.pack(fill="x", side="bottom")

        # Global Hotkey navigation [1-6]
        self._bind_hotkeys()

        # Window closing handler
        self.root.protocol("WM_DELETE_WINDOW", self.on_close)

        # Start periodic event pump & dial tick
        self._schedule_event_pump()
        self._schedule_dial_tick()

        self.screen_home.append_log("Omnitrix Research Suite initialized.")
        self.screen_home.append_log("Safety Mode: Read-only active. No writes or firmware modifications permitted.")

    def _set_app_icon(self) -> None:
        """Load and set the Omnitrix window icon."""
        candidates = []
        base_dir = getattr(sys, "_MEIPASS", None)
        if base_dir:
            candidates.append(Path(base_dir) / "assets" / "icons" / "omnitrix.ico")
            candidates.append(Path(base_dir) / "assets" / "omnitrix.ico")
            candidates.append(Path(base_dir) / "assets" / "omnitrix.png")

        project_root = Path(__file__).resolve().parent.parent.parent.parent
        candidates.append(project_root / "assets" / "icons" / "omnitrix.ico")
        candidates.append(project_root / "assets" / "omnitrix.ico")
        candidates.append(project_root / "assets" / "omnitrix.png")
        candidates.append(Path("assets/icons/omnitrix.ico"))
        candidates.append(Path("assets/omnitrix.ico"))

        for path in candidates:
            if path.exists():
                try:
                    if path.suffix == ".ico":
                        self.root.iconbitmap(str(path))
                        return
                    elif path.suffix == ".png":
                        img = tk.PhotoImage(file=str(path))
                        self.root.iconphoto(True, img)
                        return
                except Exception as e:
                    logger.debug("Failed setting icon from %s: %s", path, e)

    def _bind_hotkeys(self) -> None:
        """Bind keys 1-6 for quick navigation between screens."""
        def handle_num_key(idx: int) -> None:
            # Check if focused widget is an Entry or Spinbox
            focus_widget = self.root.focus_get()
            if isinstance(focus_widget, (tk.Entry, ttk.Entry, tk.Spinbox)):
                return
            self.select_screen_by_index(idx)

        for i in range(len(self.screens)):
            key = str(i + 1)
            self.root.bind(f"<Key-{key}>", lambda e, idx=i: handle_num_key(idx))
            self.root.bind(f"<Alt-Key-{key}>", lambda e, idx=i: handle_num_key(idx))

    def _on_navbar_select(self, index: int, _tab_id: str) -> None:
        """Called when user clicks a button in OmniNavBar."""
        if 0 <= index < len(self.screens):
            self.notebook.select(self.screens[index])

    def _on_notebook_tab_changed(self, _event: tk.Event) -> None:
        """Synchronize navbar when notebook tab changes."""
        cur = self.notebook.index(self.notebook.select())
        if cur != self.navbar.current_index:
            self.navbar.select_tab(cur)

    def select_screen_by_index(self, index: int) -> None:
        """Select a screen by its index and synchronize navbar."""
        if 0 <= index < len(self.screens):
            self.notebook.select(self.screens[index])
            self.navbar.select_tab(index)

    def _on_audio_toggled(self, is_enabled: bool) -> None:
        """Audio state change handler."""
        status_text = "🔊 AUDIO ACTIVE" if is_enabled else "🔇 AUDIO MUTED"
        color = OMNI_GREEN_GLOW if is_enabled else TEXT_MUTED
        self.screen_home.btn_sound.config(
            text="🔊 AUDIO: ON" if is_enabled else "🔇 AUDIO: OFF",
            fg=OMNI_GREEN if is_enabled else TEXT_MUTED,
        )

    def _schedule_event_pump(self) -> None:
        """Poll the background session queue every 50ms."""
        self._process_session_events()
        self.root.after(50, self._schedule_event_pump)

    def _schedule_dial_tick(self) -> None:
        """Advance dial rotation animation frame."""
        self.screen_simulator.tick_animation()
        self.screen_home.tick_animation()
        self.screen_watchface.tick_animation()
        self.screen_picker.tick_animation()
        self.root.after(40, self._schedule_dial_tick)

    def _process_session_events(self) -> None:
        """Process all pending events from the BLE session worker thread."""
        events = self.session.poll_events()
        for ev in events:
            logger.debug("Received session event: %s", ev)
            if ev.type == "state_changed":
                new_state: SessionState = ev.data
                self.screen_home.set_status(ev.message or new_state.value, new_state)
                self.header_bar.set_status(new_state.value)
                if ev.message:
                    self.screen_home.append_log(ev.message)

            elif ev.type == "device_found":
                dev: DeviceSummary = ev.data
                self.screen_picker.add_or_update_device(dev)

            elif ev.type == "scan_completed":
                devices = ev.data
                self.screen_picker.set_scan_completed(devices)
                self.screen_home.append_log(f"Scan finished. {len(devices)} peripherals detected.")
                self.footer_hud.set_ble_status(f"📡 BLE SCAN: {len(devices)} FOUND")

            elif ev.type == "device_selected":
                dev = ev.data
                self.screen_home.set_device_info(dev)
                self.screen_home.append_log(f"Device targeted: {dev.display_name} ({dev.sanitized_address})")
                self.footer_hud.lbl_target.config(text=f"⌚ TARGET: {dev.display_name[:18]}")

            elif ev.type == "connected":
                dev = ev.data
                self.screen_home.set_device_info(dev)
                self.screen_home.append_log(f"GATT link established with {dev.display_name}.")
                self.header_bar.set_status("LINKED", color=OMNI_GREEN_GLOW, bg_color=OMNI_GREEN_DARK)
                self.footer_hud.set_ble_status("📡 GATT LINKED", color=OMNI_GREEN_GLOW)
                messagebox.showinfo(
                    "Connected",
                    f"Successfully established BLE link with {dev.display_name}!\n\n"
                    "You may now proceed to GATT Inspection.",
                )

            elif ev.type == "disconnected":
                self.screen_home.append_log("BLE link disconnected.")
                self.header_bar.set_status("STANDBY", color=TEXT_MUTED, bg_color=BG_SURFACE)
                self.footer_hud.set_ble_status("📡 BLE 5.0 ACTIVE", color=OMNI_GREEN)

            elif ev.type == "inspection_progress":
                info = ev.data
                self.screen_details.update_progress(info["current"], info["total"], ev.message)

            elif ev.type == "inspection_completed":
                inventory: GattInventory = ev.data
                self.screen_details.display_inventory(inventory)
                self.screen_home.append_log(
                    f"GATT inspection complete: {len(inventory.characteristics)} characteristics identified."
                )
                self.select_screen_by_index(4)
                messagebox.showinfo(
                    "Inspection Complete",
                    f"Successfully mapped {len(inventory.characteristics)} GATT characteristics.\n\n"
                    "Review them in the GATT Inventory tab or export to docs/gatt-inventory.md.",
                )

            elif ev.type == "error":
                self.screen_home.append_log(f"ERROR: {ev.message or ev.data}")
                self.header_bar.set_status("FAULT", color="#f87171", bg_color="#450a0a")
                messagebox.showerror("Omnitrix BLE Error", f"{ev.message or 'Operation failed'}\n\nDetails: {ev.data}")

    def _action_start_scan(self) -> None:
        self.select_screen_by_index(3)
        self.screen_picker._handle_scan_click()

    def _action_select_device(self, device: DeviceSummary) -> None:
        self.session.select_device(device)
        self.screen_home.set_device_info(device)
        self.select_screen_by_index(1)
        self.screen_home.append_log(f"Confirmed target selection: {device.display_name}")

    def _action_connect(self) -> None:
        if not self.session.selected_device:
            messagebox.showwarning("No Device Selected", "Please scan and select your watch first.")
            self.select_screen_by_index(3)
            return
        self.session.connect_selected()

    def _action_disconnect(self) -> None:
        self.session.disconnect()

    def _action_inspect(self) -> None:
        if self.session.state != SessionState.CONNECTED:
            messagebox.showwarning(
                "Not Connected",
                "You must connect to the watch before inspecting its GATT services.",
            )
            return
        self.select_screen_by_index(4)
        self.session.inspect_gatt()

    def _action_export_inventory(self) -> None:
        success = self.session.export_inventory_to_file("docs/gatt-inventory.md")
        if success:
            self.screen_home.append_log("GATT inventory exported to docs/gatt-inventory.md")
            messagebox.showinfo(
                "Export Complete",
                "Sanitized GATT inventory was saved to docs/gatt-inventory.md.",
            )
        else:
            messagebox.showerror(
                "Export Failed",
                "Failed to write GATT inventory to docs/gatt-inventory.md.",
            )

    def on_close(self) -> None:
        """Handle application exit gracefully."""
        self.session.shutdown()
        self.root.destroy()
