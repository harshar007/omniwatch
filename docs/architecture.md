# Omnitrix Watch System Architecture & Folder Structure

This document outlines the architectural hierarchy, UI design system, component model, and directory structure of the **Omnitrix Watch Companion & Research Platform** (Target: **Redmi Watch Move 2**).

---

## 1. Directory Tree & Module Boundaries

```text
omniwatch/
├── .github/
│   ├── FUNDING.yml                         # Sponsorship configuration (GitHub Sponsors, Ko-fi, etc.)
│   └── workflows/
│       └── release.yml                     # Multi-platform CI/CD automated build pipeline
├── assets/                                 # Static assets & media
│   ├── icons/                              # Multi-resolution icons & vector art
│   │   ├── omnitrix.ico                    # Windows application icon
│   │   └── omnitrix.png                    # Brand emblem
│   ├── sounds/                             # Synthesized mathematical WAV audio effects (< 40 KB total)
│   ├── omnitrix.ico                        # Root asset alias for packaging compatibility
│   └── omnitrix.png                        # Root asset alias
├── config/                                 # Configuration profiles
│   ├── app.example.toml                    # TOML configuration template
│   └── watchface.example.json              # Watch face manifest template
├── docs/                                   # Research findings, specs, & architectural guides
│   ├── architecture.md                     # System architecture & UI folder layout
│   ├── ble-scan-findings.md                # Bluetooth Low Energy discovery logs
│   ├── device-notes.md                     # Target device tracking & hardware revisions
│   ├── firmware-research.md                # Non-destructive container & package inspection
│   ├── gatt-inventory.md                   # Sanitized read-only GATT characteristic map
│   ├── protocol-hypotheses.md              # Extrapolated protocol definitions
│   ├── release-guide.md                    # PyInstaller & binary distribution guide
│   └── watchface-roadmap.md                # AMOLED layout coordinates & alien profiles
├── logs/
│   └── .gitkeep                            # Runtime debug logs directory
├── scripts/                                # Build automation & asset synthesis
│   ├── build_release.py                    # PyInstaller standalone packager
│   ├── generate_icon.py                    # Multi-layer .ico / .png generator
│   ├── generate_sounds.py                  # Pure standard library audio synthesizer
│   └── launchers/                          # Dedicated launcher scripts
│       ├── launch_gui.bat                  # Batch GUI companion launcher
│       ├── launch_gui.ps1                  # PowerShell GUI companion launcher
│       ├── launch_simulator.bat            # Direct 3D Omnitrix simulator launcher (CMD)
│       ├── launch_simulator.ps1            # Direct 3D Omnitrix simulator launcher (PS)
│       ├── create_desktop_shortcut.bat     # Windows shortcut generator (CMD)
│       └── create_desktop_shortcut.ps1     # Windows shortcut generator (PS)
├── src/omnitrix_watch/                     # Core Python source package
│   ├── __init__.py
│   ├── config.py                           # Strongly typed TOML configuration parser
│   ├── logging_setup.py                    # Colored terminal & rotating file logging
│   ├── main.py                             # CLI argument parsing & GUI entry point
│   ├── sound.py                            # Non-blocking audio manager with mute control
│   ├── ble/                                # Bluetooth Low Energy Layer
│   │   ├── __init__.py
│   │   ├── connection.py                   # Async BleakClient lifecycle management
│   │   ├── gatt_inspector.py               # Read-only service & characteristic scanner
│   │   ├── permissions.py                  # Zero-write safety guardrails
│   │   └── scanner.py                      # BleakScanner service with name/RSSI filters
│   ├── models/                             # Domain data models & dataclasses
│   │   ├── __init__.py
│   │   └── device.py                       # DeviceSummary, GattInventory, CharacteristicSummary
│   ├── services/                           # Background worker threads & queues
│   │   ├── __init__.py
│   │   └── device_session.py               # Asyncio worker thread & UI event queue
│   ├── ui/                                 # Modern Galvanic Cyber UI Layer
│   │   ├── __init__.py
│   │   ├── app.py                          # OmnitrixApp window coordinator
│   │   ├── theme.py                        # Cyber palette, TTK styling & typography
│   │   ├── components/                     # Reusable UI widgets & canvases
│   │   │   ├── __init__.py                 # Clean component exports
│   │   │   ├── header_bar.py               # Top brand bar, live clock, audio toggle
│   │   │   ├── navbar.py                   # Segmented cyber tabs with glowing active state
│   │   │   ├── footer_hud.py               # Bottom telemetry bar with status pills
│   │   │   ├── cards.py                    # CyberCard, StatBadge, and SignalMeter
│   │   │   ├── dial.py                     # Vector Omnitrix circular dial & radar sweep
│   │   │   ├── radar.py                    # 360-degree BLE scanner radar
│   │   │   └── watch_preview.py            # AMOLED smartwatch display preview
│   │   └── screens/                        # Full-screen view pages
│   │       ├── __init__.py
│   │       ├── simulator.py                # 3D Wearable Omnitrix simulator
│   │       ├── home.py                     # Dial dashboard & command center
│   │       ├── watchface.py                # Watchface studio & alien roster
│   │       ├── device_picker.py            # BLE scanner & target locking
│   │       ├── device_details.py           # GATT characteristic decoder
│   │       └── donation.py                 # Galvan Prime community sponsorship hub
│   └── watchface/                          # Watch face generator & DNA catalog
│       ├── __init__.py
│       ├── aliens.py                       # 18 alien DNA profiles, quotes, & stats
│       └── builder.py                      # Manifest compiler & asset packager
├── tests/                                  # Pytest automated test suite
│   ├── test_build_release.py
│   ├── test_components.py                  # UI components unit tests
│   ├── test_config.py
│   ├── test_device_models.py
│   ├── test_gatt_inventory_format.py
│   ├── test_simulator.py
│   ├── test_sound.py
│   └── test_watchface.py
├── Launch-Omnitrix.bat                     # Root launcher redirect
├── Launch-Omnitrix.ps1                     # Root launcher redirect
├── Launch-Simulator.bat                    # Direct simulator launcher
├── Launch-Simulator.ps1                    # Direct simulator launcher
├── Create-Desktop-Shortcut.bat             # Shortcut utility redirect
├── Create-Desktop-Shortcut.ps1             # Shortcut utility redirect
└── pyproject.toml                          # Project configuration & dependencies
```

---

## 2. Layer Separation & Data Flow

```text
       ┌────────────────────────────────────────────────────────┐
       │                   Desktop GUI Window                   │
       │  [HeaderBar] ➔ [OmniNavBar] ➔ [Screen View] ➔ [HUD]    │
       └───────────────────────────┬────────────────────────────┘
                                   │
                           Tkinter UI Thread
                                   │  Session Events (Thread-safe Queue)
                                   ▼
       ┌────────────────────────────────────────────────────────┐
       │                    DeviceSession                       │
       │    Background Daemon Thread running asyncio Loop        │
       └───────────────────────────┬────────────────────────────┘
                                   │
                    Bleak Asynchronous Coroutines
                                   ▼
       ┌────────────────────────────────────────────────────────┐
       │             BLE Subsystem (bleak / winrt)              │
       │     Scanner  •  Connection  •  GATT Inspector          │
       └───────────────────────────┬────────────────────────────┘
                                   │
                      Read-Only Bluetooth Radio
                                   ▼
       ┌────────────────────────────────────────────────────────┐
       │         Target: Redmi Watch Move 2 (GATT)              │
       └────────────────────────────────────────────────────────┘
```

---

## 3. UI Component System

All reusable visual elements are modularized in `src/omnitrix_watch/ui/components/`:

1. **`HeaderBar`**:
   - Animated vector Galvanic Core logo.
   - Live system digital clock.
   - Global sound mute/unmute button with audio feedback.
   - Dynamic connection status pill (`STANDBY`, `SCANNING`, `LINKED`, `FAULT`).

2. **`OmniNavBar`**:
   - Sci-fi segmented navigation buttons with hover glow.
   - Hotkey cues (`[1]` to `[6]`).
   - Active neon underline indicator.
   - Synchronized with `ttk.Notebook`.

3. **`FooterHUD`**:
   - Telemetry pills showing core condition (`CORE: 100% NOMINAL`), BLE radio status (`BLE 5.0 ACTIVE`), and safety guardrail (`ZERO-WRITE SANCTIONED`).
   - Keyboard navigation cheat sheet.

4. **`CyberCard`**:
   - Clean container panel with illuminated title accent, subtitle, and responsive body.

5. **`SignalMeter`**:
   - 5-bar RSSI signal strength graphic with color grading (Peak, Good, Fair, Weak).

6. **`StatBadge`**:
   - Telemetry chip displaying label and active value.

7. **`OmnitrixDial`**:
   - Custom vector canvas with rotating outer bezel notches, interactive shockwave ripples, and scanning radar sweep.

8. **`OmnitrixRadarCanvas`**:
   - 360-degree radar matrix displaying discovered Bluetooth peripherals as plotted blips.

9. **`WatchPreviewCanvas`**:
   - Simulated 390x450 AMOLED display of the Redmi Watch Move 2 with active alien DNA avatar, live clock, date, battery, and pulse complications.

---

## 4. Keyboard Shortcuts

| Shortcut | Action |
|:---|:---|
| **`1`** | Switch to **⚡ Simulator** |
| **`2`** | Switch to **🌐 Dial Dashboard** |
| **`3`** | Switch to **⌚ Watch Face Builder** |
| **`4`** | Switch to **📡 BLE Scanner** |
| **`5`** | Switch to **🔍 GATT Inventory** |
| **`6`** | Switch to **💖 Galvan Prime Sponsor Hub** |
| **`Space`** | Pop-Up Core / Slam Transform (Simulator) |
| **`A` / `Left`** | Rotate Bezel Counter-Clockwise |
| **`D` / `Right`** | Rotate Bezel Clockwise |
| **`M`** | Toggle Master Control Mode |
| **`S`** | Activate Self-Destruct Mode (S.D.M.) |
| **`R`** | Quick Recharge Core |
| **`Esc`** | Revert from Alien Transformation |
