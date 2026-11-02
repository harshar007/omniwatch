# AGENT.md --- Omnitrix Watch Project

## 1. Mission

Build a safe, research-first companion project for a **Redmi Watch
Move** with a **Ben 10 / Omnitrix-inspired visual experience**.

Initial milestone: discover the watch over Bluetooth Low Energy (BLE),
document what is observable, and build a desktop Python prototype for
device discovery and read-only GATT inspection. Do not assume the watch
supports custom firmware, sideloaded apps, or a replacement operating
system.

## 2. Project goals

1.  Identify the watch and its BLE advertising behavior.
2.  Scan for nearby BLE devices and let the user explicitly select their
    own watch.
3.  Connect using supported BLE APIs and inspect exposed GATT services
    and characteristics.
4.  Read only characteristics that advertise read permission.
5.  Log connection state, service UUIDs, characteristic UUIDs, and
    errors without collecting unrelated nearby-device data.
6.  Build a Python-based Omnitrix-themed companion UI prototype.
7.  Keep all device-specific protocol findings documented and
    reproducible.
8.  Investigate firmware-update support only through official
    documentation, documented update flows, or firmware files the user
    is authorized to examine.

## 3. Non-goals and safety constraints

-   Do not claim that BLE access enables firmware flashing.
-   Do not attempt undocumented firmware writes, bootloader bypasses,
    exploit chains, authentication bypasses, or destructive commands.
-   Do not write to unknown GATT characteristics.
-   Do not replay captured packets or impersonate the official phone
    app.
-   Do not downgrade, overwrite, or patch firmware unless the
    manufacturer provides a supported method and the user has confirmed
    the exact device and recovery procedure.
-   Do not collect, decode, or retain data from other people's devices.
-   Do not store Bluetooth addresses, pairing secrets, tokens, or
    personal health data in source control.
-   If the watch is not discoverable or services are protected, document
    the limitation instead of attempting to bypass protections.

## 4. Initial technical assumptions

-   Target: Redmi Watch Move; exact hardware revision and firmware
    version must be recorded by the user.
-   Host: Windows or Linux desktop.
-   Language: Python 3.11 or later.
-   BLE library: `bleak`.
-   UI: start with a simple Python UI using `tkinter`; keep UI and BLE
    logic separated.
-   Theme: dark green/black Omnitrix-inspired styling, circular dial
    motif, alien selection screen, status indicators, and original
    placeholder artwork. Do not use copyrighted game assets unless the
    user supplies assets they have rights to use.
-   The watch may use a proprietary protocol. Treat all service and
    characteristic meanings as unknown until verified.

## 5. Proposed repository structure

``` text
omnitrix-watch/
├── AGENT.md
├── README.md
├── pyproject.toml
├── .gitignore
├── docs/
│   ├── device-notes.md
│   ├── ble-scan-findings.md
│   ├── gatt-inventory.md
│   ├── protocol-hypotheses.md
│   └── firmware-research.md
├── config/
│   └── app.example.toml
├── src/
│   └── omnitrix_watch/
│       ├── __init__.py
│       ├── main.py
│       ├── config.py
│       ├── logging_setup.py
│       ├── models/
│       │   ├── __init__.py
│       │   └── device.py
│       ├── ble/
│       │   ├── __init__.py
│       │   ├── scanner.py
│       │   ├── connection.py
│       │   ├── gatt_inspector.py
│       │   └── permissions.py
│       ├── services/
│       │   ├── __init__.py
│       │   └── device_session.py
│       └── ui/
│           ├── __init__.py
│           ├── app.py
│           ├── theme.py
│           └── screens/
│               ├── __init__.py
│               ├── home.py
│               ├── device_picker.py
│               └── device_details.py
├── tests/
│   ├── test_config.py
│   ├── test_device_models.py
│   └── test_gatt_inventory_format.py
└── logs/
    └── .gitkeep
```

## 6. Development phases

### Phase 0 --- Record device details

Before scanning, document: - Exact product name shown in the companion
app. - Hardware/model identifier if visible. - Firmware version. - Phone
OS and companion app version. - Whether the watch is paired to the
phone. - Whether the user can unpair it temporarily without losing
important data.

Do not publish personal identifiers or Bluetooth addresses in public
logs.

### Phase 1 --- Environment setup

Create a virtual environment and install only the initial dependency:

``` bash
python -m venv .venv
```

Windows PowerShell:

``` powershell
.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install bleak
```

Linux:

``` bash
source .venv/bin/activate
python -m pip install --upgrade pip
pip install bleak
```

Add a `pyproject.toml` with project metadata and dependencies. Keep
dependencies minimal until the BLE prototype works.

### Phase 2 --- BLE discovery

Implement `ble/scanner.py` to: - Scan for a short, configurable
duration. - Display device name when available, signal strength when
supported, and an ephemeral address for selection. - Allow the user to
select the intended watch. - Avoid automatically connecting to every
device. - Handle permission errors, unavailable adapters, timeouts, and
cancellation. - Never assume the device name alone proves identity.

Acceptance criteria: - The scan completes without crashing when no
devices are found. - The user can select or cancel. - Results are not
uploaded or sent to a server. - Logs omit stable device identifiers by
default.

### Phase 3 --- Read-only GATT inspection

Implement `ble/gatt_inspector.py` to: - Connect only after explicit user
selection. - Enumerate services and characteristics. - Record UUIDs and
supported properties. - Read only characteristics that explicitly
support reads. - Do not subscribe to notifications by default. - Do not
call write or write-without-response operations. - Save a sanitized
inventory to `docs/gatt-inventory.md` only after the user confirms the
selected device is their watch.

Acceptance criteria: - The tool disconnects cleanly. - Unknown services
are labeled unknown rather than guessed. - Failed reads are reported and
do not stop the entire inspection. - No write operation exists in the
initial prototype.

### Phase 4 --- Omnitrix desktop UI

Implement a Python UI with: - Dark background and green accent colors. -
A circular Omnitrix-inspired status dial drawn from original shapes. -
Scan, connect, disconnect, and inspect buttons. - Device name,
connection state, and scan progress. - A service/characteristic
inventory view. - A clear "Read-only research mode" indicator. - A
status area for errors and user guidance.

Keep BLE operations out of the UI thread. Use an appropriate
asynchronous integration or a worker thread with a thread-safe UI update
queue. Ensure disconnect and application shutdown are handled cleanly.

### Phase 5 --- Watch interaction feasibility study

After the read-only inventory: 1. Identify documented standard BLE
services, if any. 2. Compare UUIDs against reliable public
documentation. 3. Record which capabilities are confirmed, unknown, or
unsupported. 4. Determine whether the watch exposes any documented
customization interface. 5. Investigate official companion-app settings
and manufacturer-supported update mechanisms. 6. Do not infer that a
characteristic controls the display, vibration, sensors, or firmware
just from its UUID or data shape.

Any future write-capable feature requires a separately reviewed plan,
verified characteristic semantics, user confirmation, and a safe
recovery path.

### Phase 6 --- Firmware research decision

Do not begin flashing until all of the following are established: - A
firmware image is obtained from an authorized, trustworthy source. - The
exact hardware revision and firmware compatibility are verified. - The
manufacturer-supported update method or a well-documented recovery
method is known. - The bootloader/update mechanism is understood from
legitimate documentation. - A recovery plan exists for power loss or a
failed update. - The user explicitly approves the risks.

If these requirements cannot be met, keep the project as a companion UI
and read-only BLE research tool.

## 7. Data model

Create a `DeviceSummary` model with fields such as: -
`name: str | None` - `address: str` (runtime-only by default) -
`rssi: int | None` - `selected_by_user: bool`

Create a `CharacteristicSummary` model with: - `service_uuid: str` -
`characteristic_uuid: str` - `properties: list[str]` -
`read_result: str | None` - `read_error: str | None`

Do not store raw health records, authentication secrets, or full packet
captures. Hex output should be limited to explicitly authorized,
read-only characteristic values and should be redacted if it may contain
personal data.

## 8. Logging and documentation

-   Use Python's standard `logging` module.
-   Default log level: `INFO`.
-   Do not log pairing keys, tokens, personal health information, or
    unrelated device identifiers.
-   Include timestamps and operation outcomes.
-   Keep hypotheses separate from confirmed observations.
-   For each finding, record test conditions, device firmware version,
    and reproducibility.
-   Never describe an unverified UUID as a display, vibration, or
    firmware-control endpoint.

## 9. Testing strategy

-   Unit-test data models and GATT inventory formatting without
    requiring a real watch.
-   Mock BLE scanner and client behavior for error handling.
-   Test no-device, cancellation, connection failure, permission
    failure, read failure, and clean disconnect paths.
-   Keep hardware tests manual and clearly labeled.
-   Do not run destructive tests against the watch.

## 10. Agent execution instructions

Work in small, reviewable steps. Start by creating the repository
structure, packaging metadata, device notes template, and a read-only
BLE scanner. Then implement GATT inventory. Do not implement speculative
write commands or firmware flashing.

Before adding a dependency, explain why it is required. Before changing
the project architecture, update this file. Keep the app runnable after
every phase and provide exact commands to launch it.

When reporting progress, separate: - **Confirmed:** directly observed or
documented. - **Hypothesis:** plausible but unverified. - **Blocked:**
unavailable due to device, permission, or protocol restrictions. -
**Next step:** one concrete, safe action.

## 11. Definition of done for the first milestone

The first milestone is complete when: - The Python app launches. - It
scans nearby BLE devices. - The user can select the Redmi Watch Move
manually. - The app connects if the operating system and watch permit
it. - The app lists readable GATT services and characteristics without
writing to the device. - Results can be exported as a sanitized Markdown
inventory. - The UI has the initial Omnitrix-inspired theme. - README
instructions explain setup, limitations, and safe disconnect. - No
firmware flashing or undocumented write operations are present.
