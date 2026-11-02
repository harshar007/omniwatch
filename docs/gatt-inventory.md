# GATT Service & Characteristic Inventory

> [!NOTE]
> This inventory contains only sanitized, read-only GATT inspection results. No private addresses, encryption keys, or sensitive telemetry payloads are included.

## Target Device
- **Device Model:** Redmi Watch Move
- **Firmware:** *Unverified*
- **Date Inspected:** *Pending first live connection*

## Standard BLE Services (Adopted by Bluetooth SIG)
*(Populated during GATT inspection if present, e.g., Device Information Service 0x180A, Battery Service 0x180F)*

| Service Name | Service UUID | Characteristic UUID | Properties | Readable | Value / Note |
|---|---|---|---|---|---|
| *Awaiting scan* | | | | | |

## Vendor-Specific / Proprietary Services
*(Xiaomi / Huami / Wearable vendor proprietary services)*

| Service UUID | Characteristic UUID | Properties | Readable | Value (Sanitized Hex / ASCII) | Hypothesized Purpose |
|---|---|---|---|---|---|
| *Awaiting scan* | | | | | |

## Permission & Read Behavior Notes
- Unauthenticated reads: Which characteristics succeed without active pairing/bonding.
- Insufficient Authorization: Characteristics returning `ATT_ERR_INSUFFICIENT_AUTHENTICATION` (0x05) or `ATT_ERR_READ_NOT_PERMITTED` (0x02).
