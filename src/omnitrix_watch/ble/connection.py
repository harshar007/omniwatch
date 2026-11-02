"""BLE Connection Manager using bleak."""

from __future__ import annotations

import asyncio
import logging
from typing import Callable, Optional

from bleak import BleakClient
from bleak.exc import BleakError

from omnitrix_watch.models.device import DeviceSummary

logger = logging.getLogger(__name__)


class BLEConnectionManager:
    """Manages active BLE connection state with safety controls."""

    def __init__(self, timeout: float = 10.0) -> None:
        self.timeout = timeout
        self._client: Optional[BleakClient] = None
        self._connected_device: Optional[DeviceSummary] = None
        self._on_disconnect_callback: Optional[Callable[[], None]] = None

    @property
    def is_connected(self) -> bool:
        """True if actively connected to a BLE peripheral."""
        return self._client is not None and self._client.is_connected

    @property
    def current_device(self) -> Optional[DeviceSummary]:
        """Currently connected or target device."""
        return self._connected_device

    @property
    def client(self) -> Optional[BleakClient]:
        """Underlying BleakClient instance."""
        return self._client

    def _internal_disconnect_callback(self, _client: BleakClient) -> None:
        """Callback invoked by bleak when connection drops."""
        masked_addr = self._connected_device.sanitized_address if self._connected_device else "unknown"
        logger.warning("BLE peripheral disconnected unexpectedly: %s", masked_addr)
        if self._on_disconnect_callback:
            try:
                self._on_disconnect_callback()
            except Exception as e:
                logger.error("Error in on_disconnect_callback: %s", e)

    async def connect(
        self,
        device: DeviceSummary,
        on_disconnect: Optional[Callable[[], None]] = None,
    ) -> bool:
        """Connect to an explicitly selected device."""
        if not device.selected_by_user:
            raise PermissionError("Connection rejected: Device was not explicitly selected by user.")

        if self.is_connected:
            await self.disconnect()

        self._connected_device = device
        self._on_disconnect_callback = on_disconnect

        logger.info(
            "Connecting to %s (Address: %s) with timeout %.1fs...",
            device.display_name,
            device.sanitized_address,
            self.timeout,
        )

        try:
            self._client = BleakClient(
                device.address,
                disconnected_callback=self._internal_disconnect_callback,
                timeout=self.timeout,
            )
            connected = await self._client.connect()
            if connected:
                logger.info("Successfully established BLE connection to %s", device.display_name)
                return True
            else:
                logger.warning("Connection attempt returned False.")
                return False
        except BleakError as be:
            logger.error("BLE connection error: %s", be)
            await self.disconnect()
            raise RuntimeError(f"Could not connect to {device.display_name}: {be}") from be
        except asyncio.TimeoutError:
            logger.error("BLE connection timed out after %.1fs", self.timeout)
            await self.disconnect()
            raise TimeoutError(f"Connection to {device.display_name} timed out.")
        except Exception as e:
            logger.error("Unexpected error connecting to device: %s", e)
            await self.disconnect()
            raise

    async def disconnect(self) -> None:
        """Safely disconnect from the active device."""
        if self._client:
            logger.info("Disconnecting BLE client...")
            try:
                if self._client.is_connected:
                    await self._client.disconnect()
            except Exception as e:
                logger.warning("Error during BLE disconnect: %s", e)
            finally:
                self._client = None
                self._connected_device = None
                logger.info("BLE client disconnected cleanly.")
