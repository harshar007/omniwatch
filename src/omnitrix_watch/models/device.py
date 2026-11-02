"""Data models for BLE devices and GATT inspection."""

from __future__ import annotations

import datetime
from dataclasses import dataclass, field
from typing import Any, List, Optional


@dataclass
class DeviceSummary:
    """Summary of an advertised BLE device."""

    address: str
    name: Optional[str] = None
    rssi: Optional[int] = None
    selected_by_user: bool = False
    details: dict[str, Any] = field(default_factory=dict)

    @property
    def display_name(self) -> str:
        """Friendly name for display, defaulting to 'Unknown Device'."""
        if self.name and self.name.strip():
            return self.name.strip()
        return "Unknown Device"

    @property
    def sanitized_address(self) -> str:
        """Return a masked address to prevent publishing private MACs."""
        if not self.address:
            return "N/A"
        parts = self.address.split(":")
        if len(parts) == 6:
            # Mask middle 3 octets: XX:XX:XX:XX:XX:XX -> XX:XX:**:**:**:XX
            return f"{parts[0]}:{parts[1]}:**:**:**:{parts[5]}"
        parts_dash = self.address.split("-")
        if len(parts_dash) == 6:
            return f"{parts_dash[0]}-{parts_dash[1]}-**-**-**-{parts_dash[5]}"
        # If it's a UUID string (macOS/iOS style)
        if len(self.address) > 12:
            return f"{self.address[:8]}...{self.address[-4:]}"
        return self.address


@dataclass
class CharacteristicSummary:
    """Summary of an inspected GATT characteristic."""

    service_uuid: str
    characteristic_uuid: str
    properties: List[str]
    service_name: str = "Unknown Service"
    characteristic_name: str = "Unknown Characteristic"
    handle: Optional[int] = None
    read_result: Optional[str] = None
    read_error: Optional[str] = None

    @property
    def is_readable(self) -> bool:
        """Check if characteristic advertises read permission."""
        return "read" in [p.lower() for p in self.properties]

    @property
    def is_writable(self) -> bool:
        """Check if characteristic advertises write permission."""
        props = [p.lower() for p in self.properties]
        return any("write" in p for p in props)

    @property
    def is_notifiable(self) -> bool:
        """Check if characteristic advertises notify or indicate permission."""
        props = [p.lower() for p in self.properties]
        return "notify" in props or "indicate" in props


@dataclass
class GattInventory:
    """Sanitized collection of inspected services and characteristics."""

    device_name: str
    device_model: str = "Redmi Watch Move 2"
    timestamp: str = field(
        default_factory=lambda: datetime.datetime.now(datetime.timezone.utc).isoformat()
    )
    characteristics: List[CharacteristicSummary] = field(default_factory=list)

    def to_markdown(self) -> str:
        """Format inventory as a sanitized Markdown report matching docs/gatt-inventory.md."""
        lines = [
            "# GATT Service & Characteristic Inventory",
            "",
            "> [!NOTE]",
            "> This inventory contains only sanitized, read-only GATT inspection results. "
            "No private addresses, encryption keys, or sensitive telemetry payloads are included.",
            "",
            "## Target Device",
            f"- **Device Name:** {self.device_name}",
            f"- **Device Model:** {self.device_model}",
            f"- **Inspection Timestamp:** {self.timestamp}",
            f"- **Total Characteristics Inspected:** {len(self.characteristics)}",
            "",
            "## GATT Service & Characteristic Table",
            "",
            "| Service UUID | Service Name | Characteristic UUID | Characteristic Name | Properties | Readable | Read Result / Note |",
            "|---|---|---|---|---|---|---|",
        ]

        for char in self.characteristics:
            props = ", ".join(char.properties) if char.properties else "none"
            readable_str = "Yes" if char.is_readable else "No"
            
            if char.read_error:
                result_str = f"Read error: {char.read_error}"
            elif char.read_result is not None:
                # Sanitize newlines or pipe characters that would break table markdown
                sanitized_val = char.read_result.replace("\n", " ").replace("|", "\\|")
                result_str = f"`{sanitized_val}`"
            elif not char.is_readable:
                result_str = "*Not readable*"
            else:
                result_str = "*Not attempted*"

            lines.append(
                f"| `{char.service_uuid}` | {char.service_name} | `{char.characteristic_uuid}` | {char.characteristic_name} | {props} | {readable_str} | {result_str} |"
            )

        lines.extend([
            "",
            "## Security & Safety Notice",
            "- All reads performed were non-destructive standard GATT read operations.",
            "- No writes or configuration updates were executed.",
            "- In accordance with project policy, no firmware modifications were attempted.",
        ])

        return "\n".join(lines) + "\n"
