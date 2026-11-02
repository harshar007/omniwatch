# BLE Scan Findings

This document records the observed BLE advertising behavior of the Redmi Watch Move.

## Observation Log

### Scan Session: Initial Discovery Run
- **Date & Time:** *YYYY-MM-DD HH:MM:SS*
- **Host OS:** Windows 11
- **Discovery State:** Watch unpaired / paired
- **Observed Local Name:** e.g., `Redmi Watch Move` or unnamed advertisement
- **Advertised Service UUIDs:** (e.g. `0000fee0-...` or proprietary 128-bit UUIDs)
- **Manufacturer Specific Data Company ID:** (e.g. `0x038F` for Xiaomi Inc.)
- **RSSI Level:** (e.g., -65 dBm at 1 meter)
- **Connectable Flag:** True / False

## Notes on Device Identification
- Many modern wearable devices randomize their BLE MAC address (RPA - Resolvable Private Address) or rotate addresses periodically.
- Filter by local name prefix or specific manufacturer ID (`0x038F` Xiaomi) when scanning, but always allow manual user confirmation.
