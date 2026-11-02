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
from omnitrix_watch.ui.screens.device_details import DeviceDetailsScreen
from omnitrix_watch.ui.screens.device_picker import DevicePickerScreen
from omnitrix_watch.ui.screens.home import HomeScreen
from omnitrix_watch.ui.theme import apply_theme

logger = logging.getLogger(__name__)


class OmnitrixApp:
    """Omnitrix-themed desktop application for BLE discovery & GATT inspection."""

    def __init__(self, root: tk.Tk, config: Optional[AppConfig] = None) -> None:
        self.root = root
        self.config = config or AppConfig()
        self.session = DeviceSession(self.config)

        self.root.title("OMNITRIX - Watch Companion & Research Platform")
        self.root.geometry(f"{self.config.ui.window_width}x{self.config.ui.window_height}")
        self.root.minsize(780, 600)

        # Set Omnitrix App Icon if available
        self._set_app_icon()

        apply_theme(self.root)

        # Tab notebook for screens
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill="both", expand=True)

        # Screen instances
        self.screen_home = HomeScreen(
            self.notebook,
            on_scan=self._action_start_scan,
            on_connect=self._action_connect,
            on_disconnect=self._action_disconnect,
            on_inspect=self._action_inspect,
            on_open_picker=lambda: self.notebook.select(self.screen_picker),
            on_open_inventory=lambda: self.notebook.select(self.screen_details),
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

        self.notebook.add(self.screen_home, text="  DIAL DASHBOARD  ")
        self.notebook.add(self.screen_picker, text="  BLE SCANNER  ")
        self.notebook.add(self.screen_details, text="  GATT INVENTORY  ")

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
            candidates.append(Path(base_dir) / "assets" / "omnitrix.ico")
            candidates.append(Path(base_dir) / "assets" / "omnitrix.png")

        # Project tree locations
        project_root = Path(__file__).resolve().parent.parent.parent.parent
        candidates.append(project_root / "assets" / "omnitrix.ico")
        candidates.append(project_root / "assets" / "omnitrix.png")
        candidates.append(Path("assets") / "omnitrix.ico")

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

    def _schedule_event_pump(self) -> None:
        """Poll the background session queue every 50ms."""
        self._process_session_events()
        self.root.after(50, self._schedule_event_pump)

    def _schedule_dial_tick(self) -> None:
        """Advance dial rotation animation frame."""
        self.screen_home.tick_animation()
        self.root.after(60, self._schedule_dial_tick)

    def _process_session_events(self) -> None:
        """Process all pending events from the BLE session worker thread."""
        events = self.session.poll_events()
        for ev in events:
            logger.debug("Received session event: %s", ev)
            if ev.type == "state_changed":
                new_state: SessionState = ev.data
                self.screen_home.set_status(ev.message or new_state.value, new_state)
                if ev.message:
                    self.screen_home.append_log(ev.message)

            elif ev.type == "device_found":
                dev: DeviceSummary = ev.data
                self.screen_picker.add_or_update_device(dev)

            elif ev.type == "scan_completed":
                devices = ev.data
                self.screen_picker.set_scan_completed(devices)
                self.screen_home.append_log(f"Scan finished. {len(devices)} peripherals detected.")

            elif ev.type == "device_selected":
                dev = ev.data
                self.screen_home.set_device_info(dev)
                self.screen_home.append_log(f"Device targeted: {dev.display_name} ({dev.sanitized_address})")

            elif ev.type == "connected":
                dev = ev.data
                self.screen_home.set_device_info(dev)
                self.screen_home.append_log(f"GATT link established with {dev.display_name}.")
                messagebox.showinfo(
                    "Connected",
                    f"Successfully established BLE link with {dev.display_name}!\n\n"
                    "You may now proceed to GATT Inspection.",
                )

            elif ev.type == "disconnected":
                self.screen_home.append_log("BLE link disconnected.")

            elif ev.type == "inspection_progress":
                info = ev.data
                self.screen_details.update_progress(info["current"], info["total"], ev.message)

            elif ev.type == "inspection_completed":
                inventory: GattInventory = ev.data
                self.screen_details.display_inventory(inventory)
                self.screen_home.append_log(
                    f"GATT inspection complete: {len(inventory.characteristics)} characteristics identified."
                )
                self.notebook.select(self.screen_details)
                messagebox.showinfo(
                    "Inspection Complete",
                    f"Successfully mapped {len(inventory.characteristics)} GATT characteristics.\n\n"
                    "Review them in the GATT Inventory tab or export to docs/gatt-inventory.md.",
                )

            elif ev.type == "error":
                self.screen_home.append_log(f"ERROR: {ev.message or ev.data}")
                messagebox.showerror("Omnitrix BLE Error", f"{ev.message or 'Operation failed'}\n\nDetails: {ev.data}")

    def _action_start_scan(self) -> None:
        self.notebook.select(self.screen_picker)
        self.screen_picker._handle_scan_click()

    def _action_select_device(self, device: DeviceSummary) -> None:
        self.session.select_device(device)
        self.screen_home.set_device_info(device)
        self.notebook.select(self.screen_home)
        self.screen_home.append_log(f"Confirmed target selection: {device.display_name}")

    def _action_connect(self) -> None:
        if not self.session.selected_device:
            messagebox.showwarning("No Device Selected", "Please scan and select your watch first.")
            self.notebook.select(self.screen_picker)
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
        self.notebook.select(self.screen_details)
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
