"""Device session coordinator managing BLE background event loop and state."""

from __future__ import annotations

import asyncio
from enum import Enum
import logging
from pathlib import Path
import queue
import threading
from typing import Any, List, Optional

from omnitrix_watch.ble.connection import BLEConnectionManager
from omnitrix_watch.ble.gatt_inspector import GATTInspector
from omnitrix_watch.ble.scanner import BLEScannerService
from omnitrix_watch.config import AppConfig
from omnitrix_watch.models.device import DeviceSummary, GattInventory

logger = logging.getLogger(__name__)


class SessionState(str, Enum):
    """Session connection and inspection state."""

    IDLE = "IDLE"
    SCANNING = "SCANNING"
    CONNECTING = "CONNECTING"
    CONNECTED = "CONNECTED"
    INSPECTING = "INSPECTING"
    DISCONNECTING = "DISCONNECTING"
    ERROR = "ERROR"


class SessionEvent:
    """Event emitted from the BLE worker thread to the UI."""

    def __init__(self, event_type: str, data: Any = None, message: str = "") -> None:
        self.type = event_type
        self.data = data
        self.message = message

    def __repr__(self) -> str:
        return f"<SessionEvent type={self.type} message='{self.message}'>"


class DeviceSession:
    """Coordinates BLE scanner, connection, and GATT inspector in a dedicated async thread."""

    def __init__(self, config: Optional[AppConfig] = None) -> None:
        self.config = config or AppConfig()
        self.state = SessionState.IDLE
        self.selected_device: Optional[DeviceSummary] = None
        self.latest_inventory: Optional[GattInventory] = None

        self._event_queue: queue.Queue[SessionEvent] = queue.Queue()
        self._loop: Optional[asyncio.AbstractEventLoop] = None
        self._thread: Optional[threading.Thread] = None
        self._stop_event = threading.Event()

        self._scanner: Optional[BLEScannerService] = None
        self._connection: Optional[BLEConnectionManager] = None

        self._start_worker_thread()

    def _start_worker_thread(self) -> None:
        """Start background thread running asyncio loop."""
        ready_event = threading.Event()

        def _run_loop() -> None:
            self._loop = asyncio.new_event_loop()
            asyncio.set_event_loop(self._loop)
            self._scanner = BLEScannerService(default_duration=self.config.ble.scan_duration)
            self._connection = BLEConnectionManager(timeout=self.config.ble.connect_timeout)
            ready_event.set()
            logger.debug("DeviceSession async event loop started.")
            self._loop.run_forever()
            logger.debug("DeviceSession async event loop stopped.")

        self._thread = threading.Thread(target=_run_loop, daemon=True, name="Omnitrix-BLE-Worker")
        self._thread.start()
        ready_event.wait()

    def _set_state(self, new_state: SessionState, message: str = "") -> None:
        """Update session state and enqueue notification."""
        self.state = new_state
        self._event_queue.put(SessionEvent("state_changed", new_state, message))

    def poll_events(self) -> List[SessionEvent]:
        """Retrieve all queued events for UI processing."""
        events = []
        while True:
            try:
                events.append(self._event_queue.get_nowait())
            except queue.Empty:
                break
        return events

    def start_scan(self, duration: Optional[float] = None, name_filter: Optional[str] = None) -> None:
        """Dispatch scan task to worker thread."""
        if self.state in (SessionState.SCANNING, SessionState.CONNECTING, SessionState.INSPECTING):
            logger.warning("Cannot start scan in state %s", self.state)
            return

        self._set_state(SessionState.SCANNING, "Scanning for BLE peripherals...")

        def _on_device(dev: DeviceSummary) -> None:
            self._event_queue.put(SessionEvent("device_found", dev))

        async def _scan_coro() -> None:
            try:
                assert self._scanner is not None
                devices = await self._scanner.scan(
                    duration=duration or self.config.ble.scan_duration,
                    name_filter=name_filter if name_filter is not None else self.config.ble.name_filter,
                    detection_callback=_on_device,
                )
                self._set_state(SessionState.IDLE, f"Scan finished. Found {len(devices)} devices.")
                self._event_queue.put(SessionEvent("scan_completed", devices))
            except Exception as e:
                self._set_state(SessionState.ERROR, f"Scan failed: {e}")
                self._event_queue.put(SessionEvent("error", str(e), "Scan error"))

        assert self._loop is not None
        asyncio.run_coroutine_threadsafe(_scan_coro(), self._loop)

    def cancel_scan(self) -> None:
        """Request immediate scan cancellation."""
        if self._scanner and self._scanner.is_scanning:
            self._scanner.cancel()

    def select_device(self, device: DeviceSummary) -> None:
        """Mark a device as explicitly chosen by the user."""
        device.selected_by_user = True
        self.selected_device = device
        self._event_queue.put(SessionEvent("device_selected", device, f"Selected {device.display_name}"))

    def connect_selected(self) -> None:
        """Connect to the selected device."""
        if not self.selected_device:
            self._event_queue.put(SessionEvent("error", None, "No device selected."))
            return

        self._set_state(SessionState.CONNECTING, f"Connecting to {self.selected_device.display_name}...")

        def _on_disconnect() -> None:
            self._set_state(SessionState.IDLE, "Disconnected from peripheral.")
            self._event_queue.put(SessionEvent("disconnected", None, "Device connection terminated."))

        async def _connect_coro() -> None:
            try:
                assert self._connection is not None
                assert self.selected_device is not None
                success = await self._connection.connect(self.selected_device, on_disconnect=_on_disconnect)
                if success:
                    self._set_state(SessionState.CONNECTED, f"Connected to {self.selected_device.display_name}")
                    self._event_queue.put(SessionEvent("connected", self.selected_device))
                else:
                    self._set_state(SessionState.ERROR, "Connection failed.")
                    self._event_queue.put(SessionEvent("error", None, "Connection failed"))
            except Exception as e:
                self._set_state(SessionState.ERROR, f"Connection error: {e}")
                self._event_queue.put(SessionEvent("error", str(e), "Connection failed"))

        assert self._loop is not None
        asyncio.run_coroutine_threadsafe(_connect_coro(), self._loop)

    def disconnect(self) -> None:
        """Disconnect active session safely."""
        self._set_state(SessionState.DISCONNECTING, "Disconnecting...")

        async def _disc_coro() -> None:
            try:
                if self._connection:
                    await self._connection.disconnect()
            finally:
                self._set_state(SessionState.IDLE, "Ready.")
                self._event_queue.put(SessionEvent("disconnected", None, "Cleanly disconnected."))

        assert self._loop is not None
        asyncio.run_coroutine_threadsafe(_disc_coro(), self._loop)

    def inspect_gatt(self) -> None:
        """Run read-only GATT inspection."""
        if self.state != SessionState.CONNECTED or not self._connection or not self._connection.is_connected:
            self._event_queue.put(SessionEvent("error", None, "Must be connected before GATT inspection."))
            return

        self._set_state(SessionState.INSPECTING, "Inspecting GATT services & characteristics (Read-only)...")

        def _progress(cur: int, tot: int, text: str) -> None:
            self._event_queue.put(SessionEvent("inspection_progress", {"current": cur, "total": tot}, text))

        async def _inspect_coro() -> None:
            try:
                assert self._connection is not None
                assert self._connection.client is not None
                assert self.selected_device is not None
                inspector = GATTInspector(self._connection.client, self.selected_device)
                inventory = await inspector.inspect(progress_callback=_progress)
                self.latest_inventory = inventory
                self._set_state(SessionState.CONNECTED, f"Inspection complete: {len(inventory.characteristics)} items.")
                self._event_queue.put(SessionEvent("inspection_completed", inventory))
            except Exception as e:
                self._set_state(SessionState.CONNECTED, f"GATT inspection failed: {e}")
                self._event_queue.put(SessionEvent("error", str(e), "Inspection error"))

        assert self._loop is not None
        asyncio.run_coroutine_threadsafe(_inspect_coro(), self._loop)

    def export_inventory_to_file(self, target_path: str = "docs/gatt-inventory.md") -> bool:
        """Export latest inventory to markdown file."""
        if not self.latest_inventory:
            return False
        try:
            p = Path(target_path)
            p.parent.mkdir(parents=True, exist_ok=True)
            p.write_text(self.latest_inventory.to_markdown(), encoding="utf-8")
            logger.info("Exported GATT inventory to %s", target_path)
            return True
        except Exception as e:
            logger.error("Failed to export inventory: %s", e)
            return False

    def shutdown(self) -> None:
        """Gracefully shut down connection, event loop, and worker thread."""
        logger.info("Shutting down DeviceSession...")
        if self._connection and self._connection.is_connected:
            future = asyncio.run_coroutine_threadsafe(self._connection.disconnect(), self._loop)
            try:
                future.result(timeout=3.0)
            except Exception:
                pass

        if self._loop and self._loop.is_running():
            self._loop.call_soon_threadsafe(self._loop.stop)

        if self._thread and self._thread.is_alive():
            self._thread.join(timeout=2.0)
        logger.info("DeviceSession shutdown complete.")
