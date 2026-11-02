# 🌌 Omnitrix Watch v0.1.0 — Initial Research Release

> **Codename:** Galvan Prime Protocol  
> **Target Peripheral:** Redmi Watch Move  
> **Release Date:** November 2, 2026  

---

## ⚡ What's New in v0.1.0

We are thrilled to announce the inaugural open-source release of **Omnitrix Watch**! This release establishes a secure, non-destructive Bluetooth Low Energy (BLE) research platform paired with a Ben 10 / Omnitrix-themed cyberpunk companion interface.

### 🌟 Highlights & Capabilities
- **🟢 Omnitrix Alien UI:** Full-screen dark dashboard (`#080c0a`) with glowing neon dial canvas, live mode status indicators, and sound-wave styled terminal logs.
- **📡 Asynchronous BLE Engine:** Multi-threaded architecture combining Python `asyncio` and `bleak` in a background worker thread, ensuring the GUI never freezes.
- **🔍 Safe GATT Inspector:** Automatically detects Bluetooth SIG Standard Services (Battery, Device Info, Heart Rate) and Xiaomi/Huami vendor services (`0xFEE0`, `0xFE95`, `0xFDAB`).
- **🛡️ Dynamic Address Masking:** Anonymizes peripheral MAC addresses in real-time across UI tables, logs, and exports (`XX:XX:**:**:**:XX`).
- **📑 One-Click Markdown Exporter:** Automatically compiles discovered services and readable characteristics into formatted tables at `docs/gatt-inventory.md`.
- **💻 One-Click Windows Launchers:** 
  - `Launch-Omnitrix.bat`: Double-click to automatically activate venv, verify packages, and launch.
  - `Create-Desktop-Shortcut.bat`: Creates a desktop shortcut directly on your Windows desktop.
  - Standalone portable Windows x64 binary (zero Python required).

---

## 📦 Release Artifacts

| File | Description | SHA-256 Checksum |
|---|---|---|
| `OmnitrixWatch-v0.1.0-windows-x64.zip` | Standalone portable Windows executable bundle (no Python installation required) | `130f977446f0d5f6acc5d296cb87fb919913f476fb80c9b65475cc738c51532d` |
| `OmnitrixWatch-v0.1.0-windows-x64.zip.sha256` | SHA-256 verification hash | — |

---

## 🛡️ Prime Directives & Safety Notice
Omnitrix Watch strictly operates in read-only mode during this phase. No firmware modifications or arbitrary GATT writes are performed.
