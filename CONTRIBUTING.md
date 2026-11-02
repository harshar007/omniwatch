# Contributing to Omnitrix Watch

First off, thank you for considering contributing to **Omnitrix Watch**! Projects like this rely on community collaboration, transparent documentation, and rigorous safety practices.

---

## 🌌 The Prime Directives (Safety First)

This project explores the **Redmi Watch Move** through safe Bluetooth Low Energy (BLE) discovery and read-only GATT inspection. Because this involves physical embedded hardware, all contributors **must** adhere to the following safety constraints:

1. **Read-Only by Default:** Never introduce write operations, write-without-response bursts, or fuzzing payloads into the codebase without documented, verified protocol semantics and maintainer sign-off.
2. **No Brick Attempts:** Do not submit pull requests that attempt firmware patching, bootloader exploits, unauthorized over-the-air (OTA) flashing, or undocumented memory manipulation.
3. **Privacy First:** Never commit real Bluetooth MAC addresses, private device keys, auth tokens, or personal health telemetry to Git. Use the built-in `sanitized_address` model helper (`XX:XX:**:**:**:XX`).
4. **Reproducible Documentation:** Every protocol hypothesis or discovered GATT UUID must be backed by documented observations in `docs/`.

---

## 🛠️ Getting Started

### 1. Prerequisites
- **Python 3.11+**
- A Bluetooth 4.0+ BLE adapter (host machine with Windows 10/11 or modern Linux with BlueZ)
- Git

### 2. Fork & Clone
```bash
git clone https://github.com/<your-username>/omnitrix-watch.git
cd omnitrix-watch
```

### 3. Virtual Environment Setup

**Windows PowerShell:**
```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy RemoteSigned
& .\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -e ".[dev]"
```

**Linux / macOS:**
```bash
python3 -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
pip install -e ".[dev]"
```

---

## 🔄 Development Process & Workflow

We follow a structured branch-and-PR workflow:

1. **Check Issues / Discussions:** Look through existing issues or open a new one to propose a feature or research finding.
2. **Create a Feature Branch:**
   ```bash
   git checkout -b feature/omnitrix-enhancement
   # or
   git checkout -b docs/gatt-uuid-findings
   ```
3. **Implement Changes:** Write clean, modular Python code adhering to PEP 8, full type annotations (`mypy` compatible), and docstrings.
4. **Write Tests:** Add unit tests under `tests/` covering new models, parsers, or UI callbacks.
5. **Run the Test Suite:**
   ```bash
   pytest
   ```
6. **Commit with Conventional Messages:**
   - `feat: add alien selection dial animation`
   - `fix: resolve BleakError during scan cancellation`
   - `docs: update gatt-inventory with battery service characteristics`
   - `test: add unit tests for DeviceSummary address sanitization`
7. **Submit a Pull Request:** Fill in the PR template explaining the changes, hardware tested on (firmware revision), and safety verification.

---

## 📂 Repository Organization

| Path | Purpose |
|---|---|
| `src/omnitrix_watch/` | Core package source code |
| `src/omnitrix_watch/ble/` | Bleak async scanner, connection manager, GATT inspector |
| `src/omnitrix_watch/models/` | Data classes (`DeviceSummary`, `GattInventory`) |
| `src/omnitrix_watch/services/` | `DeviceSession` async worker coordinator |
| `src/omnitrix_watch/ui/` | Omnitrix-themed Tkinter UI |
| `docs/` | Research findings, GATT inventories, protocol notes |
| `config/` | TOML configuration templates |
| `tests/` | Pytest test suite with mocks |

---

## 📜 Code of Conduct

Participation in this project is governed by our [Code of Conduct](CODE_OF_CONDUCT.md). Please ensure you treat all members with respect and curiosity.
