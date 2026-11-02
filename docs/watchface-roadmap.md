# 🌌 Omnitrix Watch Face Roadmap — Redmi Watch Move 2

> **Target Peripheral:** Redmi Watch Move 2 (Redmi Move 2 / Redmi Watch 2 Series)  
> **Display Specification:** 1.85-inch AMOLED Display (~390 x 450 resolution)  
> **Theme Objective:** Full Omnitrix Alien DNA Matrix & Galvanic Timekeeper on physical watch hardware.

---

## ⚡ Overview & Vision

The Omnitrix Watch project is designed exclusively for the **Redmi Watch Move 2**. While the companion OS provides desktop BLE discovery, GATT telemetry auditing, and simulation, this roadmap defines the architecture for running the **Omnitrix Theme directly on the Redmi Watch Move 2 display**, featuring:
1. **Live Galvanic Timekeeper:** Glowing digital/analog clock showing the live hour, minute, and seconds.
2. **Interactive Alien DNA Matrix:** Displaying alien silhouettes, names, and signature colors for all 10 classic aliens.
3. **Alien Health & Energy Complications:** Core Power (Battery Level) and Alien Pulse (Heart Rate BPM).

---

## 🧬 The 10 Omnitrix Alien DNA Profiles

The watch face features 10 selectable alien DNA presets formatted for the watch display:

| ID | Codename | Alien Name | Species | Homeworld | Signature Accent | Primary Ability |
|---|---|---|---|---|---|---|
| `#01` | `ALIEN-01` | **Heatblast** | Pyronite | Pyros | `#FF5500` (Flame Orange) | Pyrokinesis & Heat Generation |
| `#02` | `ALIEN-02` | **Diamondhead** | Petrosapien | Petropia | `#00FFFF` (Crystal Cyan) | Crystalline Construct & Armor |
| `#03` | `ALIEN-03` | **XLR8** | Kineceleran | Kinet | `#00AAFF` (Speed Blue) | Hypersonic Velocity & Reflexes |
| `#04` | `ALIEN-04` | **Four Arms** | Tetramand | Khoros | `#FF1133` (Crimson Red) | Superhuman Force & Shockwave |
| `#05` | `ALIEN-05` | **Grey Matter** | Galvan | Galvan Prime | `#00FF66` (Galvanic Green) | Super-Genius Intellect & Tech |
| `#06` | `ALIEN-06` | **Upgrade** | Galvanic Mechamorph | Galvan B | `#00FF88` (Circuit Emerald) | Technological Assimilation |
| `#07` | `ALIEN-07` | **Ripjaws** | Piscciss Volann | Piscciss | `#00E5FF` (Ocean Azure) | Aquatic Agility & Crushing Jaws |
| `#08` | `ALIEN-08` | **Ghostfreak** | Ectonurite | Anur Phaetos | `#9966FF` (Phantom Violet) | Intangibility & Telekinesis |
| `#09` | `ALIEN-09` | **Stinkfly** | Lepidopterran | Lepidopterra | `#AACC00` (Insectoid Lime) | 360° Flight & Viscous Slime |
| `#10` | `ALIEN-10` | **Cannonbolt** | Arburian Pelarota | Arburia | `#FFCC00` (Kinetic Gold) | Armored Sphere Roll & Ricochet |

---

## ⌚ Watch Display Layout Coordinates (390 x 450 AMOLED)

```
+---------------------------------------------------+
|  [CORE: ⚡ 98%]                  [PULSE: ♥ 74]     |
|                                                   |
|             // OMNITRIX TIMEKEEPER //             |
|                    10:10:45                       |
|                 MON, NOV 02 2026                  |
|                                                   |
|                  .-------------.                  |
|                 /   \       /   \                 |
|                |     \     /     |                |
|                |      \===/      |                |
|                |     #01 HEATBLAST|                |
|                |      /===\      |                |
|                |     /     \     |                |
|                 \   /       \   /                 |
|                  '-------------'                  |
|               PYRONITE // PYROS                   |
+---------------------------------------------------+
```

- **Time Display:** Centered at `X: 195, Y: 140` using glowing Galvanic Monospace numerals.
- **Date String:** Centered at `X: 195, Y: 170` in muted green text.
- **Hourglass Bezel & Alien Avatar:** Centered at `X: 195, Y: 260` with a 110px radius dial circle.
- **Battery & Heart Rate Complications:** Positioned at `X: 35, Y: 410` and `X: 355, Y: 410`.

---

## 📦 Watch Face Resource Format (`.bin` / `.zip`)

Xiaomi / Redmi smartwatches use a compiled binary resource archive containing:
1. `watchface_manifest.json`: Coordinate definitions, data source bindings (time, battery, heart rate), and layer order.
2. `digits_*.png`: Sprite sheet containing numerals `0` through `9` in Galvanic neon green font.
3. `dial_bg.png`: Background dial frame rendered at 390x450 resolution.
4. `alien_silhouette_*.png`: Alien DNA vector images for the 10 aliens.

Use the built-in generator via CLI or Desktop GUI:
```powershell
# Export watch face manifest and specification
python -c "from omnitrix_watch.watchface import WatchFaceGenerator, WatchFaceConfig; from pathlib import Path; WatchFaceGenerator(WatchFaceConfig(target_device='Redmi Watch Move 2', selected_alien_id=1)).export_bundle(Path('release/watchface'))"
```

---

## 🚀 Sideloading & Installation Methods

1. **Companion App Cache Replace (Mi Fitness):**
   - Download any free official watch face in the Mi Fitness app.
   - Locate the cached `.bin` file in your phone's Android directory (`Android/data/com.xiaomi.wearable/files/...`).
   - Replace the `.bin` with `OmnitrixWatch_RedmiMove2.bin` while keeping the original file name.
   - Tap "Apply" in the companion app.
2. **Gadgetbridge Watch Face Installer:**
   - Connect the Redmi Watch Move 2 to Gadgetbridge on Android.
   - Tap the `.bin` / `.zip` file in your Android file manager and choose "Install with Gadgetbridge".
3. **Direct BLE GATT Transfer (Future Milestone):**
   - Direct transfer via the watch's over-the-air file transfer characteristic once the authentication handshake is established.
