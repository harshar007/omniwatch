"""Read-only GATT service and characteristic inspector."""

from __future__ import annotations

import logging
from typing import Callable, Optional

from bleak import BleakClient
from bleak.backends.characteristic import BleakGATTCharacteristic
from bleak.exc import BleakError

from omnitrix_watch.ble.permissions import (
    can_read,
    resolve_characteristic_name,
    resolve_service_name,
)
from omnitrix_watch.models.device import (
    CharacteristicSummary,
    DeviceSummary,
    GattInventory,
)

logger = logging.getLogger(__name__)


def sanitize_raw_value(val_bytes: bytes) -> str:
    """Format characteristic value into a safe string representation.

    Redacts excessive lengths or unprintable payloads to prevent leakage.
    """
    if not val_bytes:
        return "<empty (0 bytes)>"

    # Try ASCII decode if clean printable text
    try:
        decoded = val_bytes.decode("utf-8")
        if decoded.isprintable() and len(decoded.strip()) > 0:
            return decoded.strip()
    except UnicodeDecodeError:
        pass

    # Fall back to formatted hex string
    hex_str = val_bytes.hex(" ").upper()
    if len(hex_str) > 64:
        return f"{hex_str[:64]}... ({len(val_bytes)} bytes total)"
    return hex_str


class GATTInspector:
    """Inspects services and characteristics on a connected BLE peripheral in read-only mode."""

    def __init__(self, client: BleakClient, device: DeviceSummary) -> None:
        self.client = client
        self.device = device

    async def inspect(
        self,
        progress_callback: Optional[Callable[[int, int, str], None]] = None,
    ) -> GattInventory:
        """Enumerate GATT services and read all readable characteristics safely."""
        if not self.client.is_connected:
            raise RuntimeError("Cannot inspect GATT: Peripheral is not connected.")

        logger.info("Beginning read-only GATT inspection for %s...", self.device.display_name)
        characteristics: list[CharacteristicSummary] = []

        services = list(self.client.services)
        all_chars: list[tuple[str, BleakGATTCharacteristic]] = []
        for service in services:
            for char in service.characteristics:
                all_chars.append((service.uuid, char))

        total_chars = len(all_chars)
        logger.info(
            "Found %d services and %d characteristics to inspect.",
            len(services),
            total_chars,
        )

        for idx, (service_uuid, char) in enumerate(all_chars, start=1):
            service_name = resolve_service_name(service_uuid)
            char_name = resolve_characteristic_name(char.uuid)
            props = list(char.properties)

            read_val: Optional[str] = None
            read_err: Optional[str] = None

            if can_read(props):
                if progress_callback:
                    progress_callback(idx, total_chars, f"Reading {char_name} ({char.uuid[:8]})...")
                try:
                    raw_bytes = await self.client.read_gatt_char(char)
                    read_val = sanitize_raw_value(raw_bytes)
                    logger.debug("Successfully read char %s: %s", char.uuid, read_val)
                except BleakError as be:
                    read_err = str(be)
                    logger.debug("Failed reading char %s: %s", char.uuid, be)
                except Exception as e:
                    read_err = f"Unexpected read failure: {e}"
                    logger.debug("Exception reading char %s: %s", char.uuid, e)
            else:
                if progress_callback:
                    progress_callback(idx, total_chars, f"Skipping non-readable {char_name}...")

            summary = CharacteristicSummary(
                service_uuid=service_uuid,
                characteristic_uuid=char.uuid,
                properties=props,
                service_name=service_name,
                characteristic_name=char_name,
                handle=char.handle,
                read_result=read_val,
                read_error=read_err,
            )
            characteristics.append(summary)

        inventory = GattInventory(
            device_name=self.device.display_name,
            device_model="Redmi Watch Move",
            characteristics=characteristics,
        )

        logger.info("GATT inspection finished successfully.")
        return inventory
