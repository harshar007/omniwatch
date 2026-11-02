# Protocol Hypotheses & Analysis

## Context
Xiaomi/Redmi wearable devices historically use proprietary protocols over BLE. These protocols often feature:
1. **Cryptographic Authentication Handshake:**
   - Generation of random challenge by the peripheral.
   - Response signed or encrypted using an Auth Key established during pairing with Mi Fitness / Xiaomi Wear.
2. **Framing & Packet Serialization:**
   - Multi-packet chunking with header bytes (opcode, sequence number, payload length, CRC).
3. **Notification-Driven Data Transfer:**
   - Health metrics (heart rate, step counts, sleep stages) are rarely exposed directly via standard GATT characteristic reads; instead, an encrypted command requests data, which is streamed via notifications.

## Safety Principles
- **No Speculative Replay:** Under no circumstances should captured packets or arbitrary bytes be blindly written to unknown characteristics. Doing so could corrupt flash settings or cause watch bootloops.
- **Hypothesis Labeling:** All claims regarding service function or characteristic role must be explicitly tagged as `[Hypothesis - Unverified]` until proven by standard GATT definitions or official vendor documentation.
