"""BLE permissions, standard UUID mappings, and safety validations."""

from __future__ import annotations

from typing import Iterable, Optional

# Standard Bluetooth SIG 16-bit UUID definitions
KNOWN_SERVICES: dict[str, str] = {
    "1800": "Generic Access",
    "1801": "Generic Attribute",
    "180a": "Device Information",
    "180f": "Battery Service",
    "180d": "Heart Rate",
    "1812": "Human Interface Device",
    "1802": "Immediate Alert",
    "1803": "Link Loss",
    "1804": "Tx Power",
    "1805": "Current Time Service",
    "fee0": "Xiaomi / Huami Profile Service",
    "fee1": "Xiaomi / Huami Auth & Firmware Service",
    "fe95": "Xiaomi Inc. BLE Custom Service",
    "fdab": "Xiaomi Wear Companion Service",
}

KNOWN_CHARACTERISTICS: dict[str, str] = {
    "2a00": "Device Name",
    "2a01": "Appearance",
    "2a04": "Peripheral Preferred Connection Parameters",
    "2a05": "Service Changed",
    "2a19": "Battery Level",
    "2a24": "Model Number String",
    "2a25": "Serial Number String",
    "2a26": "Firmware Revision String",
    "2a27": "Hardware Revision String",
    "2a28": "Software Revision String",
    "2a29": "Manufacturer Name String",
    "2a37": "Heart Rate Measurement",
    "2a38": "Body Sensor Location",
    "2a2b": "Current Time",
}


def normalize_uuid(uuid_str: str) -> str:
    """Normalize UUID to lowercase standard format."""
    return uuid_str.lower().strip()


def resolve_service_name(uuid_str: str) -> str:
    """Resolve service UUID to a human-readable name if known."""
    norm = normalize_uuid(uuid_str)
    # Check 16-bit short UUID format: 0000xxxx-0000-1000-8000-00805f9b34fb
    if len(norm) == 36 and norm.startswith("0000") and norm.endswith("-0000-1000-8000-00805f9b34fb"):
        short_id = norm[4:8]
        if short_id in KNOWN_SERVICES:
            return KNOWN_SERVICES[short_id]
    elif len(norm) == 4 and norm in KNOWN_SERVICES:
        return KNOWN_SERVICES[norm]
    elif norm in KNOWN_SERVICES:
        return KNOWN_SERVICES[norm]
    return "Proprietary / Vendor Service"


def resolve_characteristic_name(uuid_str: str) -> str:
    """Resolve characteristic UUID to a human-readable name if known."""
    norm = normalize_uuid(uuid_str)
    if len(norm) == 36 and norm.startswith("0000") and norm.endswith("-0000-1000-8000-00805f9b34fb"):
        short_id = norm[4:8]
        if short_id in KNOWN_CHARACTERISTICS:
            return KNOWN_CHARACTERISTICS[short_id]
    elif len(norm) == 4 and norm in KNOWN_CHARACTERISTICS:
        return KNOWN_CHARACTERISTICS[norm]
    elif norm in KNOWN_CHARACTERISTICS:
        return KNOWN_CHARACTERISTICS[norm]
    return "Unknown Characteristic"


def can_read(properties: Iterable[str]) -> bool:
    """Verify if the characteristic properties allow standard read."""
    return any(p.lower() == "read" for p in properties)


def is_write_prohibited() -> bool:
    """Safety guard: The current research milestone strictly prohibits writes."""
    return True
