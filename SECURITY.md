# Security Policy

## 🛡️ Supported Versions

The following versions of Omnitrix Watch currently receive security and safety updates:

| Version | Supported          |
| ------- | ------------------ |
| 0.1.x   | :white_check_mark: |

---

## 🔒 Safety & Hardware Research Policy

Omnitrix Watch is strictly a **companion research tool** operating under a **zero-harm / read-only hardware policy**:

1. **Non-Destructive Operations:** The codebase deliberately avoids sending raw write packets, firmware flash commands, or proprietary bootloader handshakes to external BLE devices.
2. **Safe Privacy:** Bluetooth addresses, session tokens, and pairing keys must never be logged or stored. Discovered MAC addresses must always be masked (`XX:XX:**:**:**:XX`).
3. **No Bricking Risk:** We do not publish or endorse unverified firmware flashers, brick-risk scripts, or unauthenticated writes.

---

## 🚨 Reporting a Vulnerability

If you discover a security concern (such as an inadvertent packet injection path, data leak, or privacy flaw):

1. **Do not create a public GitHub issue.**
2. Send an email to the research maintainers or open a confidential GitHub Security Advisory.
3. Provide detailed steps to reproduce, the platform/OS, and any relevant logs (with MAC addresses redacted).
4. We aim to acknowledge receipt within 48 hours and provide a fix or safety patch promptly.
