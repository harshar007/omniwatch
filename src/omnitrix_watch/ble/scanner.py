"""BLE Scanner implementation using bleak."""

from __future__ import annotations

import asyncio
import logging
from typing import Callable, List, Optional

from bleak import BleakScanner
from bleak.backends.device import BLEDevice
from bleak.backends.scanner import AdvertisementData
from bleak.exc import BleakError

from omnitrix_watch.models.device import DeviceSummary

logger = logging.getLogger(__name__)


class BLEScannerService:
    """Handles scanning for nearby Bluetooth Low Energy peripherals."""

    def __init__(self, default_duration: float = 5.0) -> None:
        self.default_duration = default_duration
        self._is_scanning = False
        self._cancel_requested = False

    @property
    def is_scanning(self) -> bool:
        """True if a scan is currently active."""
        return self._is_scanning

    def cancel(self) -> None:
        """Request cancellation of an in-progress scan."""
        if self._is_scanning:
            logger.info("BLE scan cancellation requested.")
            self._cancel_requested = True

    async def scan(
        self,
        duration: Optional[float] = None,
        name_filter: Optional[str] = None,
        detection_callback: Optional[Callable[[DeviceSummary], None]] = None,
    ) -> List[DeviceSummary]:
        """Scan for nearby BLE devices for the specified duration in seconds.

        Returns a list of discovered DeviceSummary instances.
        """
        scan_time = duration if duration is not None else self.default_duration
        self._is_scanning = True
        self._cancel_requested = False
        discovered: dict[str, DeviceSummary] = {}

        def _on_advertisement(device: BLEDevice, adv_data: AdvertisementData) -> None:
            raw_name = adv_data.local_name or device.name
            name = raw_name.strip() if raw_name else None

            # Apply name filter if requested
            if name_filter and name:
                if name_filter.lower() not in name.lower():
                    return

            summary = DeviceSummary(
                address=device.address,
                name=name,
                rssi=adv_data.rssi if adv_data.rssi is not None else getattr(device, "rssi", None),
                details={
                    "service_uuids": list(adv_data.service_uuids or []),
                    "tx_power": adv_data.tx_power,
                    "manufacturer_data": {
                        f"0x{k:04X}": v.hex() for k, v in (adv_data.manufacturer_data or {}).items()
                    },
                },
            )
            discovered[device.address] = summary
            if detection_callback:
                try:
                    detection_callback(summary)
                except Exception as cb_err:
                    logger.debug("Error in discovery callback: %s", cb_err)

        logger.info("Starting BLE discovery scan for %.1f seconds...", scan_time)
        try:
            scanner = BleakScanner(detection_callback=_on_advertisement)
            await scanner.start()

            # Poll for cancellation or timeout
            step = 0.25
            elapsed = 0.0
            while elapsed < scan_time and not self._cancel_requested:
                await asyncio.sleep(step)
                elapsed += step

            await scanner.stop()
            logger.info("BLE scan completed. Found %d devices.", len(discovered))
        except BleakError as be:
            logger.error("Bluetooth adapter error during scan: %s", be)
            raise RuntimeError(f"Bluetooth scan failed: {be}") from be
        except asyncio.CancelledError:
            logger.info("BLE scan was cancelled via asyncio.")
        except Exception as ex:
            logger.error("Unexpected error during BLE scan: %s", ex)
            raise
        finally:
            self._is_scanning = False
            self._cancel_requested = False

        return list(discovered.values())
