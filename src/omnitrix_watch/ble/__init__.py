"""BLE package."""

from omnitrix_watch.ble.connection import BLEConnectionManager
from omnitrix_watch.ble.gatt_inspector import GATTInspector
from omnitrix_watch.ble.permissions import (
    can_read,
    is_write_prohibited,
    resolve_characteristic_name,
    resolve_service_name,
)
from omnitrix_watch.ble.scanner import BLEScannerService

__all__ = [
    "BLEScannerService",
    "BLEConnectionManager",
    "GATTInspector",
    "resolve_service_name",
    "resolve_characteristic_name",
    "can_read",
    "is_write_prohibited",
]
