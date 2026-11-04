# Omnitrix Wearable Smartwatch Simulator (Web Edition)

A standalone, zero-dependency HTML5 / CSS3 / Web Audio API recreation of the Ben 10 Omnitrix Watch simulator, executable directly in any web browser (Chrome, Edge, Firefox, Safari) on both desktop and mobile devices.

---

## ⚡ How to Launch

### Option 1: Double-Click Launcher
Double-click [`Launch-Web-Simulator.bat`](../Launch-Web-Simulator.bat) or execute [`Launch-Web-Simulator.ps1`](../Launch-Web-Simulator.ps1) from the project root.

### Option 2: Direct File Open
Open [`web/index.html`](index.html) directly in any web browser.

### Option 3: Local HTTP Server (Python)
```bash
python -m http.server 8080 --directory web
```
Then visit `http://localhost:8080` in your browser.

---

## 🎮 Interactive Controls

| Input | Hardware Action |
|:---|:---|
| **Click Watch Core** or **`Space`** | **Pop-Up Core** (elevates dial) / **Slam Transform** |
| **Mouse Wheel** or **`A` / `D`** | **Rotate Outer Bezel** (cycles through 18 alien DNA profiles) |
| **Drag Bezel** or **Touch Swipe** | **Mechanical Bezel Rotation** with inertia and haptic clicks |
| **Double-Click Core** or **`R`** | **Emergency Quick Recharge** (bypasses cooldown lock) |
| **`M`** | **Master Control Mode** (infinite time + on-the-fly switching) |
| **`S`** | **Self-Destruct Mode (S.D.M.)** with emergency alarm klaxon |
| **`Esc`** | **Revert to Human Form** |

---

## 🧬 Features & Visuals

- **4 Generation Themes**:
  - *Prototype (Classic 2005)*: Galvanic neon green `#00ff55`
  - *Recalibrated (Alien Force)*: Aqua green `#00ff88`
  - *Omniverse*: High-energy green `#22ff66`
  - *Albedo*: Crimson red `#ff2233` rogue core
- **3D Pop-Up Elevation**: Dynamic mechanical depth rendering, shadow projection, and pneumatic audio hisses.
- **Pure Web Audio Synthesizer**: No external audio files required. All clicks, slams, energy hums, and alarms are generated mathematically in real time via the browser's `AudioContext`.
- **18 Alien DNA Profiles**: Heatblast, Diamondhead, XLR8, Four Arms, Grey Matter, Upgrade, Ripjaws, Stinkfly, Ghostfreak, Cannonbolt, Wildmutt, Swampfire, Humungousaur, Big Chill, Echo Echo, Chromastone, Way Big, and Alien X.
