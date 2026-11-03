"""Omnitrix Wearable Simulator Screen.

A faithful high-fidelity recreation of the iconic Ben 10 Omnitrix Watch simulator
(inspired by Andrej Vujic's Wear OS / Android Alien Watch Omnitrix Simulator).

Features:
- 4 Iconic Generations: Prototype (Classic 2005), Recalibrated (Alien Force), Omniverse, and Albedo (Red).
- Realistic Smartwatch-on-wrist rendering with straps, metallic bezel, screws, and side buttons.
- Interactive 3D Pop-Up Core with mechanical elevation shading.
- Interactive Rotating Bezel: Mouse scroll wheel, mouse drag, arrow keys (A/D or Left/Right), and touch buttons.
- Full 18-Alien DNA Roster with custom vector silhouettes, sound cues, power stats, and battle quotes.
- Dramatic Slam & Transformation Flash shockwave sequence.
- Transformed Hero View with chest Omnitrix badge, depleting energy ring, and live stats HUD.
- Timeout warning sequence with urgent alarms and reversion to human.
- Cooldown / Recharge mode with red energy gauge and double-tap quick recharge.
- Master Control Mode (Infinite transformation, instant on-the-fly switching, secret sequence L-R-L-R-L-R-L-R).
- Self-Destruct Mode (S.D.M.) with emergency klaxon and countdown timer (secret code L-R-L-L-L-R-L-L).
- DNA Scanner Mode with rotating extraterrestrial radar beam.
- Full audio engine with zero external dependencies.
"""

from __future__ import annotations

from enum import Enum
import math
import random
import time
import tkinter as tk
from tkinter import messagebox, ttk
from typing import Callable, List, Optional

from omnitrix_watch.sound import sound_player
from omnitrix_watch.ui.theme import (
    BG_DARK,
    BG_PANEL,
    BG_SURFACE,
    BORDER_COLOR,
    FONT_BADGE,
    FONT_BODY,
    FONT_DIAL,
    FONT_HEADING,
    FONT_MONO,
    FONT_TITLE,
    OMNI_CORE_GLOW,
    OMNI_GREEN,
    OMNI_GREEN_DARK,
    OMNI_GREEN_DIM,
    OMNI_GREEN_GLOW,
    TEXT_DIM,
    TEXT_MUTED,
    TEXT_PRIMARY,
)
from omnitrix_watch.watchface.aliens import (
    AlienProfile,
    get_alien_quote,
    get_alien_stats,
    get_simulator_aliens,
)


class SimulatorState(str, Enum):
    """Lifecycle states of the Omnitrix Simulator."""
    STANDBY = "STANDBY"              # Core flush/down, hourglass pulsing
    SELECTION = "SELECTION"          # Core popped up, bezel rotating
    TRANSFORMING = "TRANSFORMING"    # Explosive green/red energy flash
    TRANSFORMED = "TRANSFORMED"      # Hero active, alien displayed, timer ticking
    COOLDOWN = "COOLDOWN"            # Red recharge lock, energy filling up
    SELF_DESTRUCT = "SELF_DESTRUCT"  # Klaxon alarm, emergency countdown
    DNA_SCAN = "DNA_SCAN"            # Sci-fi yellow/orange radar sweep


class OmnitrixGen(str, Enum):
    """The four classic iterations of the Omnitrix."""
    PROTOTYPE = "PROTOTYPE"          # Classic 2005 original
    RECALIBRATED = "RECALIBRATED"    # Alien Force / Ultimatrix
    OMNIVERSE = "OMNIVERSE"          # Omniverse angular
    ALBEDO = "ALBEDO"                # Crimson Galvanic core


# Theme palette definitions per generation
GEN_THEMES = {
    OmnitrixGen.PROTOTYPE: {
        "accent": "#00ff41",
        "glow": "#80ff9f",
        "dark_accent": "#004d13",
        "case": "#141815",
        "case_rim": "#253028",
        "strap": "#0c100d",
        "dial_bg": "#050a06",
        "nodes": "#00ff41",
        "name": "PROTOTYPE (CLASSIC)",
    },
    OmnitrixGen.RECALIBRATED: {
        "accent": "#00ff88",
        "glow": "#94ffd0",
        "dark_accent": "#003b1e",
        "case": "#0e1310",
        "case_rim": "#1a241e",
        "strap": "#080b09",
        "dial_bg": "#020704",
        "nodes": "#00e5ff",
        "name": "RECALIBRATED (AF)",
    },
    OmnitrixGen.OMNIVERSE: {
        "accent": "#66ff00",
        "glow": "#b8ff66",
        "dark_accent": "#264a00",
        "case": "#e4eae5",
        "case_rim": "#a0ada3",
        "strap": "#141a15",
        "dial_bg": "#030a02",
        "nodes": "#66ff00",
        "name": "OMNIVERSE",
    },
    OmnitrixGen.ALBEDO: {
        "accent": "#ff1e2d",
        "glow": "#ff7580",
        "dark_accent": "#4d050a",
        "case": "#18080a",
        "case_rim": "#301216",
        "strap": "#0c0405",
        "dial_bg": "#0a0203",
        "nodes": "#ff1e2d",
        "name": "ALBEDO (CRIMSON)",
    },
}


class OmnitrixWatchCanvas(tk.Canvas):
    """Interactive circular Smartwatch on Wrist with 3D Pop-Up Omnitrix Core."""

    def __init__(self, parent: tk.Widget, size: int = 480, **kwargs) -> None:
        super().__init__(
            parent,
            width=size,
            height=size,
            bg=BG_DARK,
            highlightthickness=0,
            **kwargs,
        )
        self.size = size
        self.cx = size / 2
        self.cy = size / 2

        # Core simulator state
        self.generation = OmnitrixGen.PROTOTYPE
        self.state = SimulatorState.STANDBY
        self.master_control = False
        self.roster: List[AlienProfile] = get_simulator_aliens(include_unlocked=True)
        self.alien_index = 0

        # Physical dial kinematics & animation
        self.dial_angle = 0.0          # Current visual bezel angle (radians)
        self.target_angle = 0.0        # Smooth interpolation target
        self.pulse_phase = 0.0         # Breathing glow phase
        self.pop_height = 0.0          # 0.0 = flush, 1.0 = fully elevated
        self.target_pop_height = 0.0   # Target pop height

        # Shockwave & Flash fx
        self.flash_alpha = 0.0         # Transformation screen flash intensity (0..1)
        self.shockwave_r = 0.0         # Radial shockwave ring

        # Timers
        self.transform_time_remaining = 20.0
        self.max_transform_time = 20.0
        self.cooldown_progress = 0.0   # 0.0 to 1.0
        self.self_destruct_seconds = 30.0

        # DNA Scanner beam
        self.scan_beam_angle = 0.0
        self.scan_pulse = 0.0

        # Secret sequence buffer for L/R turns
        self.turn_sequence: List[str] = []
        self.last_turn_time = 0.0

        # Drag tracking
        self.drag_start_angle = 0.0
        self.is_dragging = False

        # Status text feedback
        self.hud_message = "OMNITRIX STANDBY - PUSH CORE"

        # Bindings
        self.bind("<Button-1>", self._on_click)
        self.bind("<Double-Button-1>", self._on_double_click)
        self.bind("<ButtonPress-1>", self._on_drag_start, add="+")
        self.bind("<B1-Motion>", self._on_drag_motion)
        self.bind("<ButtonRelease-1>", self._on_drag_end)
        self.bind("<MouseWheel>", self._on_mouse_wheel)

        self.draw()

    @property
    def current_alien(self) -> AlienProfile:
        """Currently selected alien DNA profile."""
        return self.roster[self.alien_index % len(self.roster)]

    @property
    def theme(self) -> dict:
        """Current color theme based on Omnitrix generation."""
        return GEN_THEMES[self.generation]

    # -------------------------------------------------------------------------
    # State Transitions & Actions
    # -------------------------------------------------------------------------

    def set_generation(self, gen: OmnitrixGen) -> None:
        """Switch the Omnitrix generation model."""
        self.generation = gen
        sound_player.play_beep()
        self.hud_message = f"ACTIVE MODEL: {self.theme['name']}"
        self.draw()

    def toggle_master_control(self) -> bool:
        """Toggle Master Control on/off."""
        self.master_control = not self.master_control
        if self.master_control:
            sound_player.play_master_control()
            self.hud_message = "⚡ MASTER CONTROL UNLOCKED: INFINITE ENERGY"
        else:
            sound_player.play_beep()
            self.hud_message = "MASTER CONTROL DISENGAGED"
        self.draw()
        return self.master_control

    def pop_up_core(self) -> None:
        """Pop up the Omnitrix core into alien selection mode."""
        if self.state == SimulatorState.COOLDOWN:
            sound_player.play_error()
            self.hud_message = "ENERGY DEPLETED - RECHARGE REQUIRED"
            return

        if self.state in (SimulatorState.STANDBY, SimulatorState.TRANSFORMED):
            self.state = SimulatorState.SELECTION
            self.target_pop_height = 1.0
            sound_player.play_popup()
            self.hud_message = f"SELECT DNA: {self.current_alien.name.upper()}"
            self.draw()

    def slam_core(self) -> None:
        """Slam down the core to transform into currently dialed alien."""
        if self.state == SimulatorState.SELECTION:
            # Trigger transformation
            self.target_pop_height = 0.0
            self.state = SimulatorState.TRANSFORMING
            self.flash_alpha = 1.0
            self.shockwave_r = 10.0
            sound_player.play_transform()
            self.hud_message = f"TRANSFORMING INTO {self.current_alien.name.upper()}!"
            self.transform_time_remaining = 25.0
            self.draw()

        elif self.state == SimulatorState.STANDBY:
            # If popped down, first pop up
            self.pop_up_core()

        elif self.state == SimulatorState.TRANSFORMED:
            # If already transformed, revert to human
            self.revert_to_human()

    def revert_to_human(self) -> None:
        """Revert from alien form back to human form."""
        if self.state == SimulatorState.TRANSFORMED:
            sound_player.play_shockwave()
            self.flash_alpha = 0.6
            if self.master_control:
                self.state = SimulatorState.STANDBY
                self.hud_message = "REVERTED TO HUMAN (MASTER CONTROL STANDBY)"
            else:
                self.state = SimulatorState.COOLDOWN
                self.cooldown_progress = 0.0
                self.hud_message = "TIMEOUT REVERT: COOLDOWN RECHARGING..."
            self.draw()

    def quick_recharge(self) -> None:
        """Instantly recharge Omnitrix back to full ready state."""
        sound_player.play_recharge()
        self.state = SimulatorState.STANDBY
        self.cooldown_progress = 1.0
        self.hud_message = "⚡ 100% RECHARGED - CORE NOMINAL"
        self.draw()

    def trigger_self_destruct(self) -> None:
        """Toggle Self-Destruct Mode (S.D.M.)."""
        if self.state == SimulatorState.SELF_DESTRUCT:
            # Abort
            sound_player.play_beep()
            self.state = SimulatorState.STANDBY
            self.hud_message = "SELF-DESTRUCT ABORTED - FAILSAFE ENGAGED"
        else:
            sound_player.play_self_destruct()
            self.state = SimulatorState.SELF_DESTRUCT
            self.self_destruct_seconds = 30.0
            self.hud_message = "⚠️ WARNING: SELF-DESTRUCT INITIATED (00:30)"
        self.draw()

    def trigger_dna_scan(self) -> None:
        """Toggle extraterrestrial DNA Scanner Mode."""
        if self.state == SimulatorState.DNA_SCAN:
            self.state = SimulatorState.STANDBY
            self.hud_message = "DNA SCANNER DISENGAGED"
        else:
            sound_player.play_dna_scan()
            self.state = SimulatorState.DNA_SCAN
            self.hud_message = "🔬 SCANNING EXTRATERRESTRIAL DNA SIGNATURE..."
        self.draw()

    def rotate_dial(self, direction: int) -> None:
        """Rotate dial bezel (-1 for Left/CCW, +1 for Right/CW)."""
        now = time.time()
        if now - self.last_turn_time > 3.0:
            self.turn_sequence.clear()
        self.last_turn_time = now

        step_code = "R" if direction > 0 else "L"
        self.turn_sequence.append(step_code)

        # Check secret codes from Andrej's Alien Watch simulator
        seq_str = ",".join(self.turn_sequence[-8:])
        if seq_str == "L,R,L,R,L,R,L,R":
            self.toggle_master_control()
            self.turn_sequence.clear()
            return
        elif seq_str == "L,R,L,L,L,R,L,L":
            self.trigger_self_destruct()
            self.turn_sequence.clear()
            return

        sound_player.play_dial_turn()

        # Advance alien index
        self.alien_index = (self.alien_index + direction) % len(self.roster)
        angle_step = (2 * math.pi) / len(self.roster)
        self.target_angle += direction * angle_step

        if self.state == SimulatorState.TRANSFORMED and self.master_control:
            # In Master Control, instantly morph mid-transformation on turn!
            sound_player.play_transform()
            self.hud_message = f"INSTANT MORPH: {self.current_alien.name.upper()}!"
        else:
            self.hud_message = f"DIAL: [{self.alien_index + 1}/{len(self.roster)}] {self.current_alien.name.upper()}"

        self.draw()

    # -------------------------------------------------------------------------
    # Input Event Handlers
    # -------------------------------------------------------------------------

    def _on_click(self, event: tk.Event) -> None:
        """Handle tap on dial / watch."""
        dx = event.x - self.cx
        dy = event.y - self.cy
        dist = math.hypot(dx, dy)

        # Click inside core dial (radius ~ 130)
        if dist <= 140:
            if self.state == SimulatorState.STANDBY:
                self.pop_up_core()
            elif self.state == SimulatorState.SELECTION:
                self.slam_core()
            elif self.state == SimulatorState.TRANSFORMED:
                self.revert_to_human()
            elif self.state == SimulatorState.COOLDOWN:
                # Prompt user about recharge
                sound_player.play_error()
                self.hud_message = "DOUBLE-CLICK TO QUICK RECHARGE"
            elif self.state == SimulatorState.SELF_DESTRUCT:
                self.trigger_self_destruct()
            elif self.state == SimulatorState.DNA_SCAN:
                # Lock onto alien
                sound_player.play_alien_select()
                self.hud_message = f"DNA SAMPLE REGISTERED: {self.current_alien.name.upper()}"
                self.state = SimulatorState.SELECTION
                self.pop_up_core()

    def _on_double_click(self, event: tk.Event) -> None:
        """Double click anywhere on the core triggers Quick Recharge (Andrej feature!)."""
        if self.state == SimulatorState.COOLDOWN:
            self.quick_recharge()

    def _on_mouse_wheel(self, event: tk.Event) -> None:
        """Scroll wheel spins the bezel."""
        if event.delta > 0:
            self.rotate_dial(-1)
        else:
            self.rotate_dial(1)

    def _on_drag_start(self, event: tk.Event) -> None:
        """Start tracking drag around dial."""
        dx = event.x - self.cx
        dy = event.y - self.cy
        if 40 < math.hypot(dx, dy) < 170:
            self.is_dragging = True
            self.drag_start_angle = math.atan2(dy, dx)

    def _on_drag_motion(self, event: tk.Event) -> None:
        """Spin dial according to circular drag motion."""
        if not self.is_dragging:
            return
        dx = event.x - self.cx
        dy = event.y - self.cy
        current_angle = math.atan2(dy, dx)
        delta_angle = current_angle - self.drag_start_angle

        # Normalize delta
        while delta_angle > math.pi:
            delta_angle -= 2 * math.pi
        while delta_angle < -math.pi:
            delta_angle += 2 * math.pi

        threshold = 0.35  # ~20 degrees
        if abs(delta_angle) > threshold:
            direction = 1 if delta_angle > 0 else -1
            self.rotate_dial(direction)
            self.drag_start_angle = current_angle

    def _on_drag_end(self, _event: tk.Event) -> None:
        """Release dial drag."""
        self.is_dragging = False

    # -------------------------------------------------------------------------
    # Animation Tick Loop (Called at ~40ms / 25 FPS)
    # -------------------------------------------------------------------------

    def tick_animation(self) -> None:
        """Advance physics, animation interpolations, and countdown timers."""
        # Breathing pulse
        self.pulse_phase = (self.pulse_phase + 0.08) % (2 * math.pi)

        # Smooth dial angle interpolation
        self.dial_angle += (self.target_angle - self.dial_angle) * 0.35

        # Smooth pop-up elevation
        self.pop_height += (self.target_pop_height - self.pop_height) * 0.25

        # Flash alpha decay
        if self.flash_alpha > 0.0:
            self.flash_alpha = max(0.0, self.flash_alpha - 0.06)

        # Shockwave expansion
        if self.shockwave_r > 0:
            self.shockwave_r += 10.0
            if self.shockwave_r > self.size * 0.7:
                self.shockwave_r = 0.0

        # State-specific timing logic
        if self.state == SimulatorState.TRANSFORMING:
            if self.flash_alpha <= 0.4:
                self.state = SimulatorState.TRANSFORMED

        elif self.state == SimulatorState.TRANSFORMED:
            if not self.master_control:
                self.transform_time_remaining -= 0.06
                # Warning beeps when under 5s
                if 4.9 < self.transform_time_remaining < 5.1:
                    sound_player.play_timeout()
                    self.hud_message = "⚠️ WARNING: ENERGY DEPLETION IMMINENT"
                elif 0.0 < self.transform_time_remaining <= 0.08:
                    self.revert_to_human()

        elif self.state == SimulatorState.COOLDOWN:
            self.cooldown_progress += 0.006
            if self.cooldown_progress >= 1.0:
                self.quick_recharge()

        elif self.state == SimulatorState.SELF_DESTRUCT:
            self.self_destruct_seconds -= 0.06
            if int(self.self_destruct_seconds * 10) % 15 == 0:
                sound_player.play_self_destruct()
            if self.self_destruct_seconds <= 0.0:
                # Detonation / reset
                self.self_destruct_seconds = 0.0
                self.flash_alpha = 1.0
                self.state = SimulatorState.COOLDOWN
                self.cooldown_progress = 0.0
                self.hud_message = "DETONATION DISCHARGED - SYSTEM IN RECOVERY"

        elif self.state == SimulatorState.DNA_SCAN:
            self.scan_beam_angle = (self.scan_beam_angle + 0.12) % (2 * math.pi)

        self.draw()

    # -------------------------------------------------------------------------
    # Canvas Drawing Engine
    # -------------------------------------------------------------------------

    def draw(self) -> None:
        """Render all visual layers of the Wearable Omnitrix Smartwatch."""
        self.delete("all")
        cx, cy = self.cx, self.cy
        th = self.theme

        # 1. Background Smartwatch Straps (Top and Bottom)
        strap_w = 150
        strap_col = th["strap"]
        strap_border = "#1a221d"
        # Top strap
        self.create_rectangle(
            cx - strap_w / 2, 0, cx + strap_w / 2, cy - 130,
            fill=strap_col, outline=strap_border, width=2,
        )
        # Top strap ribbed texture
        for y_strap in range(20, int(cy - 140), 22):
            self.create_line(
                cx - strap_w / 2 + 10, y_strap, cx + strap_w / 2 - 10, y_strap,
                fill="#162019", width=3,
            )
        # Bottom strap
        self.create_rectangle(
            cx - strap_w / 2, cy + 130, cx + strap_w / 2, self.size,
            fill=strap_col, outline=strap_border, width=2,
        )
        # Bottom strap ribbed texture
        for y_strap in range(int(cy + 150), self.size - 10, 22):
            self.create_line(
                cx - strap_w / 2 + 10, y_strap, cx + strap_w / 2 - 10, y_strap,
                fill="#162019", width=3,
            )

        # 2. Watch Lugs (connecting case to strap)
        lug_pts_tl = [cx - strap_w / 2 - 10, cy - 110, cx - strap_w / 2 + 14, cy - 150, cx - strap_w / 2 + 35, cy - 120]
        self.create_polygon(lug_pts_tl, fill=th["case_rim"], outline=strap_border)
        lug_pts_tr = [cx + strap_w / 2 + 10, cy - 110, cx + strap_w / 2 - 14, cy - 150, cx + strap_w / 2 - 35, cy - 120]
        self.create_polygon(lug_pts_tr, fill=th["case_rim"], outline=strap_border)
        lug_pts_bl = [cx - strap_w / 2 - 10, cy + 110, cx - strap_w / 2 + 14, cy + 150, cx - strap_w / 2 + 35, cy + 120]
        self.create_polygon(lug_pts_bl, fill=th["case_rim"], outline=strap_border)
        lug_pts_br = [cx + strap_w / 2 + 10, cy + 110, cx + strap_w / 2 - 14, cy + 150, cx + strap_w / 2 - 35, cy + 120]
        self.create_polygon(lug_pts_br, fill=th["case_rim"], outline=strap_border)

        # 3. Side Crown Activator Button on right
        crown_w, crown_h = 24, 46
        self.create_rectangle(
            cx + 158, cy - crown_h / 2, cx + 158 + crown_w, cy + crown_h / 2,
            fill="#2c3a31", outline="#475e4f", width=2,
        )
        # Ridge notches on button
        for by in range(int(cy - crown_h / 2 + 6), int(cy + crown_h / 2 - 4), 8):
            self.create_line(cx + 162, by, cx + 158 + crown_w - 4, by, fill="#5d7a67", width=2)

        # 4. Main Smartwatch Chassis (Round Bezel)
        case_r = 165
        self.create_oval(
            cx - case_r, cy - case_r, cx + case_r, cy + case_r,
            fill=th["case"], outline=th["case_rim"], width=6,
        )

        # Outer metallic bevel groove
        self.create_oval(
            cx - case_r + 8, cy - case_r + 8, cx + case_r - 8, cy + case_r - 8,
            outline="#1c2820", width=3,
        )

        # 5. Bezel Node Screws / Classic 4 Nodes (at 12, 3, 6, 9 o'clock)
        node_dist = case_r - 14
        node_r = 7
        for angle_deg in [0, 90, 180, 270]:
            rad = math.radians(angle_deg)
            nx = cx + node_dist * math.cos(rad)
            ny = cy + node_dist * math.sin(rad)
            node_fill = th["nodes"] if (self.generation == OmnitrixGen.PROTOTYPE or self.state == SimulatorState.TRANSFORMED) else "#2d3d32"
            self.create_oval(
                nx - node_r, ny - node_r, nx + node_r, ny + node_r,
                fill=node_fill, outline="#08140c", width=2,
            )

        # 6. Master Control Radiant Aura (When Active)
        if self.master_control:
            pulse_rad = 148 + 4 * math.sin(self.pulse_phase * 2)
            self.create_oval(
                cx - pulse_rad, cy - pulse_rad, cx + pulse_rad, cy + pulse_rad,
                outline="#ffd700", width=3,
            )

        # 7. Pop-Up 3D Elevation Depth Ring
        elev_px = int(self.pop_height * 18)
        dial_r = 132

        if elev_px > 2:
            # 3D Depth Shadow/Cylinder beneath the popped-up core
            self.create_oval(
                cx - dial_r, cy - dial_r + elev_px, cx + dial_r, cy + dial_r + elev_px,
                fill="#0a120d", outline="#1b281f", width=2,
            )
            # Vertical side ribs showing mechanical pop-up shaft
            for rib_x in [-80, -40, 0, 40, 80]:
                self.create_line(
                    cx + rib_x, cy + dial_r - 10, cx + rib_x, cy + dial_r + elev_px,
                    fill="#3b5242", width=3,
                )

        # 8. Inner Rotating Bezel Faceplate
        core_cy = cy - (elev_px // 2)
        self.create_oval(
            cx - dial_r, core_cy - dial_r, cx + dial_r, core_cy + dial_r,
            fill=th["dial_bg"], outline="#1e2c22", width=4,
        )

        # 9. Bezel Notches & Alien Markers (Rotate with dial_angle)
        num_bezel_ticks = len(self.roster)
        for i in range(num_bezel_ticks):
            b_angle = self.dial_angle + (i * 2 * math.pi / num_bezel_ticks)
            tx1 = cx + (dial_r - 3) * math.cos(b_angle)
            ty1 = core_cy + (dial_r - 3) * math.sin(b_angle)
            tx2 = cx + (dial_r - 12) * math.cos(b_angle)
            ty2 = core_cy + (dial_r - 12) * math.sin(b_angle)
            is_active = (i == self.alien_index)
            tick_color = th["accent"] if is_active else "#264230"
            tick_width = 3 if is_active else 1
            self.create_line(tx1, ty1, tx2, ty2, fill=tick_color, width=tick_width)

        # 10. Render Mode Content Based on SimulatorState
        if self.state == SimulatorState.STANDBY:
            self._draw_standby_mode(cx, core_cy, dial_r, th)

        elif self.state == SimulatorState.SELECTION:
            self._draw_selection_mode(cx, core_cy, dial_r, th)

        elif self.state in (SimulatorState.TRANSFORMING, SimulatorState.TRANSFORMED):
            self._draw_transformed_mode(cx, core_cy, dial_r, th)

        elif self.state == SimulatorState.COOLDOWN:
            self._draw_cooldown_mode(cx, core_cy, dial_r, th)

        elif self.state == SimulatorState.SELF_DESTRUCT:
            self._draw_self_destruct_mode(cx, core_cy, dial_r, th)

        elif self.state == SimulatorState.DNA_SCAN:
            self._draw_dna_scan_mode(cx, core_cy, dial_r, th)

        # 11. Shockwave Ripple
        if self.shockwave_r > 0:
            self.create_oval(
                cx - self.shockwave_r, core_cy - self.shockwave_r,
                cx + self.shockwave_r, core_cy + self.shockwave_r,
                outline=th["glow"], width=3,
            )

        # 12. Fullscreen Energy Flash on Slam/Transform
        if self.flash_alpha > 0.05:
            flash_color = th["accent"] if self.generation != OmnitrixGen.ALBEDO else "#ff2233"
            # Draw semi-transparent energy flash stippling / radial burst
            burst_r = self.size * self.flash_alpha
            self.create_oval(
                cx - burst_r, cy - burst_r, cx + burst_r, cy + burst_r,
                fill=flash_color, outline="#ffffff", width=4,
            )

        # 13. Top HUD Banner (Status & Generation)
        self.create_text(
            cx, 16,
            text=f"[{self.theme['name']}]  •  {self.state.value}",
            fill=th["accent"],
            font=("Consolas", 9, "bold"),
        )

        # 14. Bottom HUD Message
        self.create_text(
            cx, self.size - 14,
            text=self.hud_message,
            fill=th["glow"] if self.state != SimulatorState.COOLDOWN else "#ff5555",
            font=("Consolas", 9, "bold"),
        )

    # -------------------------------------------------------------------------
    # Mode-Specific Sub-Renderers
    # -------------------------------------------------------------------------

    def _draw_standby_mode(self, cx: float, cy: float, r: float, th: dict) -> None:
        """Render the classic pulsating Hourglass emblem."""
        pulse_val = 0.5 + 0.5 * math.sin(self.pulse_phase)
        glow_color = th["glow"] if pulse_val > 0.5 else th["accent"]

        # Inner dark core
        inner_r = r - 20
        self.create_oval(
            cx - inner_r, cy - inner_r, cx + inner_r, cy + inner_r,
            fill="#030804", outline=th["dark_accent"], width=2,
        )

        # Classic Omnitrix Hourglass: Opposing top & bottom triangles
        tri_size = inner_r * 0.76
        top_tri = [cx - tri_size, cy - tri_size, cx + tri_size, cy - tri_size, cx, cy]
        bot_tri = [cx - tri_size, cy + tri_size, cx + tri_size, cy + tri_size, cx, cy]

        self.create_polygon(top_tri, fill=glow_color, outline=th["accent"], width=2)
        self.create_polygon(bot_tri, fill=glow_color, outline=th["accent"], width=2)

        # Central core circle
        center_r = 26
        self.create_oval(
            cx - center_r, cy - center_r, cx + center_r, cy + center_r,
            fill="#060f08", outline=glow_color, width=3,
        )

        # Glass glare reflection arc
        self.create_arc(
            cx - inner_r + 14, cy - inner_r + 14, cx + inner_r - 14, cy + inner_r - 14,
            start=45, extent=90, style="arc", outline="#ffffff", width=2,
        )

        # Text prompt
        self.create_text(
            cx, cy,
            text="READY",
            fill=glow_color,
            font=("Consolas", 10, "bold"),
        )

    def _draw_selection_mode(self, cx: float, cy: float, r: float, th: dict) -> None:
        """Render popped-up core with active alien vector silhouette."""
        inner_r = r - 16
        alien = self.current_alien

        # Popped-up illuminated inner ring
        self.create_oval(
            cx - inner_r, cy - inner_r, cx + inner_r, cy + inner_r,
            fill="#020804", outline=th["accent"], width=3,
        )

        # Left / Right Rotation Indicator Arrows on rim
        self.create_text(cx - inner_r + 16, cy, text="◀", fill=th["accent"], font=("Consolas", 14, "bold"))
        self.create_text(cx + inner_r - 16, cy, text="▶", fill=th["accent"], font=("Consolas", 14, "bold"))

        # Holographic radar background grid
        for grid_r in [30, 60, 90]:
            self.create_oval(
                cx - grid_r, cy - grid_r, cx + grid_r, cy + grid_r,
                outline=th["dark_accent"], width=1, dash=(2, 4),
            )

        # Draw the alien's custom vector silhouette!
        self._render_alien_silhouette(cx, cy - 4, alien, size=65, color=th["accent"])

        # Alien Name Banner (Above and Below)
        self.create_text(
            cx, cy - inner_r + 26,
            text=f"[{alien.id:02d}] {alien.name.upper()}",
            fill=th["glow"],
            font=("Consolas", 11, "bold"),
        )

        self.create_text(
            cx, cy + inner_r - 26,
            text="PUSH CORE TO SLAM",
            fill=th["accent"],
            font=("Consolas", 9, "bold"),
        )

    def _draw_transformed_mode(self, cx: float, cy: float, r: float, th: dict) -> None:
        """Render transformed hero mode with live countdown and alien art."""
        inner_r = r - 12
        alien = self.current_alien

        # Transformed energetic core background
        self.create_oval(
            cx - inner_r, cy - inner_r, cx + inner_r, cy + inner_r,
            fill="#030c06", outline=alien.signature_color, width=3,
        )

        # Circular Depleting Transformation Energy Ring
        if not self.master_control and self.max_transform_time > 0:
            fraction = max(0.0, self.transform_time_remaining / self.max_transform_time)
            extent = int(fraction * 360)
            meter_col = th["accent"] if self.transform_time_remaining > 5 else "#ff3344"
            self.create_arc(
                cx - inner_r + 6, cy - inner_r + 6, cx + inner_r - 6, cy + inner_r - 6,
                start=90, extent=-extent, style="arc", outline=meter_col, width=5,
            )
        elif self.master_control:
            # Infinite pulsing gold ring
            self.create_oval(
                cx - inner_r + 6, cy - inner_r + 6, cx + inner_r - 6, cy + inner_r - 6,
                outline="#ffd700", width=4,
            )

        # Render Alien Vector Silhouette (Full Hero Stance)
        self._render_alien_silhouette(cx, cy - 12, alien, size=75, color=alien.signature_color)

        # Chest Omnitrix Badge (Clickable to revert)
        badge_y = cy + 42
        badge_r = 16
        self.create_oval(
            cx - badge_r, badge_y - badge_r, cx + badge_r, badge_y + badge_r,
            fill="#051009", outline=th["accent"], width=2,
        )
        # Hourglass on badge
        b_tri = badge_r * 0.7
        self.create_polygon(
            [cx - b_tri, badge_y - b_tri, cx + b_tri, badge_y - b_tri, cx, badge_y],
            fill=th["accent"], outline=th["accent"],
        )
        self.create_polygon(
            [cx - b_tri, badge_y + b_tri, cx + b_tri, badge_y + b_tri, cx, badge_y],
            fill=th["accent"], outline=th["accent"],
        )

        # Alien Name Title
        self.create_text(
            cx, cy - inner_r + 24,
            text=alien.name.upper(),
            fill="#ffffff",
            font=("Consolas", 12, "bold"),
        )

        # Time remaining text
        time_str = "∞ MASTER" if self.master_control else f"{max(0.0, self.transform_time_remaining):.1f}s"
        time_col = th["glow"] if (self.master_control or self.transform_time_remaining > 5) else "#ff4444"
        self.create_text(
            cx, cy + inner_r - 18,
            text=f"REMAINING: {time_str}",
            fill=time_col,
            font=("Consolas", 9, "bold"),
        )

    def _draw_cooldown_mode(self, cx: float, cy: float, r: float, th: dict) -> None:
        """Render red recharge cooldown mode with energy gauge."""
        inner_r = r - 20
        red_core = "#ff1e2d"
        red_dim = "#590a10"

        # Red pulsing glow
        self.create_oval(
            cx - inner_r, cy - inner_r, cx + inner_r, cy + inner_r,
            fill="#0a0203", outline=red_dim, width=3,
        )

        # Red Hourglass
        tri_size = inner_r * 0.72
        top_tri = [cx - tri_size, cy - tri_size, cx + tri_size, cy - tri_size, cx, cy]
        bot_tri = [cx - tri_size, cy + tri_size, cx + tri_size, cy + tri_size, cx, cy]
        self.create_polygon(top_tri, fill=red_core, outline=red_dim, width=2)
        self.create_polygon(bot_tri, fill=red_core, outline=red_dim, width=2)

        # Circular recharge energy progress arc
        recharge_extent = int(self.cooldown_progress * 360)
        self.create_arc(
            cx - inner_r + 6, cy - inner_r + 6, cx + inner_r - 6, cy + inner_r - 6,
            start=90, extent=-recharge_extent, style="arc", outline="#ff5555", width=6,
        )

        # Center indicator
        center_r = 24
        self.create_oval(
            cx - center_r, cy - center_r, cx + center_r, cy + center_r,
            fill="#120405", outline=red_core, width=2,
        )

        pct = int(self.cooldown_progress * 100)
        self.create_text(
            cx, cy - 2,
            text=f"{pct}%",
            fill="#ffffff",
            font=("Consolas", 9, "bold"),
        )

        self.create_text(
            cx, cy + inner_r - 18,
            text="RECHARGING...",
            fill="#ff7777",
            font=("Consolas", 8, "bold"),
        )

    def _draw_self_destruct_mode(self, cx: float, cy: float, r: float, th: dict) -> None:
        """Render S.D.M. Emergency Warning klaxon faceplate."""
        inner_r = r - 16
        is_flash_step = int(self.self_destruct_seconds * 4) % 2 == 0
        alert_col = "#ff1122" if is_flash_step else "#ffaa00"

        self.create_oval(
            cx - inner_r, cy - inner_r, cx + inner_r, cy + inner_r,
            fill="#1a0406", outline=alert_col, width=4,
        )

        # Warning triangles
        tri_size = inner_r * 0.70
        self.create_polygon(
            [cx - tri_size, cy - tri_size, cx + tri_size, cy - tri_size, cx, cy],
            fill=alert_col, outline="#ffffff", width=2,
        )
        self.create_polygon(
            [cx - tri_size, cy + tri_size, cx + tri_size, cy + tri_size, cx, cy],
            fill=alert_col, outline="#ffffff", width=2,
        )

        self.create_text(
            cx, cy - 8,
            text="⚠️ S.D.M. ACTIVE",
            fill="#ffffff",
            font=("Consolas", 11, "bold"),
        )

        self.create_text(
            cx, cy + 14,
            text=f"00:{int(self.self_destruct_seconds):02d}",
            fill="#ffffff",
            font=("Consolas", 16, "bold"),
        )

    def _draw_dna_scan_mode(self, cx: float, cy: float, r: float, th: dict) -> None:
        """Render extraterrestrial DNA Scanner radar sweep."""
        inner_r = r - 16
        scan_col = "#ffcc00"
        dark_scan = "#554400"

        self.create_oval(
            cx - inner_r, cy - inner_r, cx + inner_r, cy + inner_r,
            fill="#0d0a02", outline=scan_col, width=3,
        )

        # Concentric radar rings
        for ring_r in [30, 60, 90]:
            self.create_oval(
                cx - ring_r, cy - ring_r, cx + ring_r, cy + ring_r,
                outline=dark_scan, width=1, dash=(3, 3),
            )

        # Rotating radar sweep line
        beam_x = cx + inner_r * math.cos(self.scan_beam_angle)
        beam_y = cy + inner_r * math.sin(self.scan_beam_angle)
        self.create_line(cx, cy, beam_x, beam_y, fill=scan_col, width=3)

        # Scanning wedge
        deg_start = -math.degrees(self.scan_beam_angle)
        self.create_arc(
            cx - inner_r, cy - inner_r, cx + inner_r, cy + inner_r,
            start=deg_start, extent=45, fill="#332800", outline="",
        )

        # Center lock reticle
        self.create_text(
            cx, cy,
            text="🔬 SCANNING",
            fill=scan_col,
            font=("Consolas", 10, "bold"),
        )

    # -------------------------------------------------------------------------
    # Alien Vector Silhouette Renderer
    # -------------------------------------------------------------------------

    def _render_alien_silhouette(self, cx: float, cy: float, alien: AlienProfile, size: float, color: str) -> None:
        """Render iconic procedural vector silhouettes for all aliens."""
        name = alien.name.lower()

        if "heatblast" in name:
            # Fiery horned crest & magma torso
            pts = [
                cx, cy - size * 0.7,
                cx + size * 0.35, cy - size * 0.25,
                cx + size * 0.2, cy - size * 0.1,
                cx + size * 0.5, cy + size * 0.45,
                cx + size * 0.15, cy + size * 0.3,
                cx, cy + size * 0.6,
                cx - size * 0.15, cy + size * 0.3,
                cx - size * 0.5, cy + size * 0.45,
                cx - size * 0.2, cy - size * 0.1,
                cx - size * 0.35, cy - size * 0.25,
            ]
            self.create_polygon(pts, fill=color, outline="#ffffff", width=1)
            # Glowing core eyes
            self.create_oval(cx - 8, cy - size * 0.35, cx - 2, cy - size * 0.25, fill="#ffffff")
            self.create_oval(cx + 2, cy - size * 0.35, cx + 8, cy - size * 0.25, fill="#ffffff")

        elif "diamondhead" in name:
            # Sharp crystalline back shards & angular prism crown
            pts = [
                cx, cy - size * 0.75,
                cx + size * 0.25, cy - size * 0.45,
                cx + size * 0.55, cy - size * 0.55,
                cx + size * 0.35, cy - size * 0.15,
                cx + size * 0.45, cy + size * 0.55,
                cx, cy + size * 0.35,
                cx - size * 0.45, cy + size * 0.55,
                cx - size * 0.35, cy - size * 0.15,
                cx - size * 0.55, cy - size * 0.55,
                cx - size * 0.25, cy - size * 0.45,
            ]
            self.create_polygon(pts, fill=color, outline="#ffffff", width=1)
            # Crystal facet line
            self.create_line(cx, cy - size * 0.75, cx, cy + size * 0.35, fill="#ffffff", width=2)

        elif "xlr8" in name:
            # Sleek pointed racing helmet & aerodynamic visor
            pts = [
                cx - size * 0.3, cy + size * 0.5,
                cx, cy + size * 0.2,
                cx + size * 0.65, cy - size * 0.2,
                cx + size * 0.1, cy - size * 0.65,
                cx - size * 0.45, cy - size * 0.15,
            ]
            self.create_polygon(pts, fill=color, outline="#ffffff", width=1)
            # Speed visor slit
            self.create_line(cx - size * 0.15, cy - size * 0.2, cx + size * 0.35, cy - size * 0.2, fill="#ffffff", width=3)

        elif "four arms" in name:
            # 4 muscular raised arms & brawny shoulders
            pts = [
                cx, cy - size * 0.55,
                cx + size * 0.2, cy - size * 0.35,
                cx + size * 0.65, cy - size * 0.6,    # Upper right arm
                cx + size * 0.55, cy - size * 0.15,
                cx + size * 0.75, cy + size * 0.1,     # Lower right arm
                cx + size * 0.35, cy + size * 0.25,
                cx + size * 0.3, cy + size * 0.6,
                cx - size * 0.3, cy + size * 0.6,
                cx - size * 0.35, cy + size * 0.25,
                cx - size * 0.75, cy + size * 0.1,     # Lower left arm
                cx - size * 0.55, cy - size * 0.15,
                cx - size * 0.65, cy - size * 0.6,    # Upper left arm
                cx - size * 0.2, cy - size * 0.35,
            ]
            self.create_polygon(pts, fill=color, outline="#ffffff", width=1)

        elif "grey matter" in name:
            # Oversized Galvan cranium & wide eyes
            self.create_oval(cx - size * 0.45, cy - size * 0.65, cx + size * 0.45, cy + size * 0.1, fill=color, outline="#ffffff")
            # Slim body
            self.create_rectangle(cx - size * 0.15, cy + size * 0.05, cx + size * 0.15, cy + size * 0.55, fill=color)
            # Big oval eyes
            self.create_oval(cx - size * 0.32, cy - size * 0.45, cx - size * 0.08, cy - size * 0.15, fill="#000000", outline="#ffffff")
            self.create_oval(cx + size * 0.08, cy - size * 0.45, cx + size * 0.32, cy - size * 0.15, fill="#000000", outline="#ffffff")

        elif "upgrade" in name:
            # Galvanic Mechamorph circuit optic lens & nanotech body
            pts = [
                cx - size * 0.35, cy - size * 0.45,
                cx + size * 0.35, cy - size * 0.45,
                cx + size * 0.45, cy + size * 0.55,
                cx - size * 0.45, cy + size * 0.55,
            ]
            self.create_polygon(pts, fill=color, outline="#ffffff", width=1)
            # Cyclops optical sensor ring
            self.create_oval(cx - 14, cy - size * 0.15, cx + 14, cy + size * 0.15, fill="#000000", outline="#ffffff", width=2)
            self.create_oval(cx - 6, cy - size * 0.05, cx + 6, cy + size * 0.05, fill=color)

        elif "ripjaws" in name:
            # Angler fish light bulb & vicious steel jaws
            # Jaw
            self.create_polygon(
                [cx - size * 0.4, cy - size * 0.2, cx + size * 0.4, cy - size * 0.2, cx + size * 0.2, cy + size * 0.55, cx - size * 0.2, cy + size * 0.55],
                fill=color, outline="#ffffff",
            )
            # Angler lure
            self.create_line(cx, cy - size * 0.2, cx + size * 0.3, cy - size * 0.65, fill=color, width=2)
            self.create_oval(cx + size * 0.25, cy - size * 0.72, cx + size * 0.38, cy - size * 0.58, fill="#ffffff")

        elif "ghostfreak" in name:
            # Ethereal wispy ghost tail & hooded phantom
            pts = [
                cx, cy - size * 0.65,
                cx + size * 0.4, cy - size * 0.25,
                cx + size * 0.25, cy + size * 0.2,
                cx + size * 0.45, cy + size * 0.55,
                cx + size * 0.1, cy + size * 0.4,
                cx - size * 0.2, cy + size * 0.65,
                cx - size * 0.4, cy - size * 0.25,
            ]
            self.create_polygon(pts, fill=color, outline="#ffffff", width=1, smooth=True)
            # Single eye track slit
            self.create_line(cx - 12, cy - size * 0.25, cx + 6, cy - size * 0.15, fill="#ffffff", width=3)

        elif "stinkfly" in name:
            # 4 stalk eyes & dragonfly wings
            # Wings
            self.create_oval(cx - size * 0.65, cy - size * 0.35, cx - size * 0.1, cy + size * 0.1, fill=color)
            self.create_oval(cx + size * 0.1, cy - size * 0.35, cx + size * 0.65, cy + size * 0.1, fill=color)
            # Body & tail
            self.create_polygon([cx - 8, cy - size * 0.4, cx + 8, cy - size * 0.4, cx, cy + size * 0.65], fill=color, outline="#ffffff")
            # 4 eye stalks
            for ex in [-16, -6, 6, 16]:
                self.create_oval(cx + ex - 3, cy - size * 0.55, cx + ex + 3, cy - size * 0.42, fill="#ffffff")

        elif "cannonbolt" in name:
            # Spherical armored shell plates
            self.create_oval(cx - size * 0.52, cy - size * 0.52, cx + size * 0.52, cy + size * 0.52, fill=color, outline="#ffffff", width=2)
            # Armor shell segments
            self.create_arc(cx - size * 0.4, cy - size * 0.4, cx + size * 0.4, cy + size * 0.4, start=30, extent=120, outline="#000000", width=3, style="arc")
            self.create_arc(cx - size * 0.4, cy - size * 0.4, cx + size * 0.4, cy + size * 0.4, start=210, extent=120, outline="#000000", width=3, style="arc")

        elif "wildmutt" in name:
            # Feral quadruped hunter
            pts = [
                cx - size * 0.55, cy + size * 0.45,
                cx - size * 0.4, cy - size * 0.1,
                cx + size * 0.45, cy - size * 0.2,
                cx + size * 0.6, cy + size * 0.4,
                cx + size * 0.3, cy + size * 0.3,
                cx, cy + size * 0.15,
                cx - size * 0.3, cy + size * 0.3,
            ]
            self.create_polygon(pts, fill=color, outline="#ffffff", width=1)
            # Sensory gills
            for gx in [-10, 0, 10]:
                self.create_line(cx + gx, cy - size * 0.05, cx + gx + 4, cy + size * 0.05, fill="#000000", width=2)

        elif "swampfire" in name:
            # Fire petal head crown & vine torso
            pts = [
                cx, cy - size * 0.7,
                cx + size * 0.25, cy - size * 0.35,
                cx + size * 0.45, cy - size * 0.45,
                cx + size * 0.3, cy + size * 0.5,
                cx - size * 0.3, cy + size * 0.5,
                cx - size * 0.45, cy - size * 0.45,
                cx - size * 0.25, cy - size * 0.35,
            ]
            self.create_polygon(pts, fill=color, outline="#ffffff", width=1)
            # Petal lines
            self.create_line(cx, cy - size * 0.7, cx, cy + size * 0.1, fill="#ffffff", width=2)

        elif "humungousaur" in name:
            # Massive titan dinosaur snout & dorsal ridges
            pts = [
                cx - size * 0.45, cy + size * 0.55,
                cx - size * 0.5, cy - size * 0.2,
                cx - size * 0.2, cy - size * 0.6,
                cx + size * 0.2, cy - size * 0.6,
                cx + size * 0.5, cy - size * 0.2,
                cx + size * 0.45, cy + size * 0.55,
            ]
            self.create_polygon(pts, fill=color, outline="#ffffff", width=2)
            # Dinosaur jaw
            self.create_rectangle(cx - size * 0.25, cy - size * 0.35, cx + size * 0.25, cy - size * 0.15, fill="#000000")

        elif "big chill" in name:
            # Folded moth-wing phantom cloak & antennae
            pts = [
                cx, cy - size * 0.45,
                cx + size * 0.5, cy + size * 0.55,
                cx, cy + size * 0.3,
                cx - size * 0.5, cy + size * 0.55,
            ]
            self.create_polygon(pts, fill=color, outline="#ffffff", width=1)
            # Antennae
            self.create_line(cx - 6, cy - size * 0.45, cx - size * 0.25, cy - size * 0.75, fill=color, width=2)
            self.create_line(cx + 6, cy - size * 0.45, cx + size * 0.25, cy - size * 0.75, fill=color, width=2)

        elif "echo echo" in name:
            # Silicon amplifier body & headphone speaker bells
            self.create_oval(cx - size * 0.35, cy - size * 0.4, cx + size * 0.35, cy + size * 0.45, fill=color, outline="#ffffff")
            # Speaker ear cups
            self.create_oval(cx - size * 0.5, cy - size * 0.15, cx - size * 0.3, cy + size * 0.15, fill="#000000", outline="#ffffff")
            self.create_oval(cx + size * 0.3, cy - size * 0.15, cx + size * 0.5, cy + size * 0.15, fill="#000000", outline="#ffffff")

        elif "chromastone" in name:
            # Monolithic crystal head horn
            pts = [
                cx, cy - size * 0.75,
                cx + size * 0.3, cy - size * 0.25,
                cx + size * 0.35, cy + size * 0.5,
                cx - size * 0.35, cy + size * 0.5,
                cx - size * 0.3, cy - size * 0.25,
            ]
            self.create_polygon(pts, fill=color, outline="#ffffff", width=1)
            # Radiant horn shard
            self.create_line(cx, cy - size * 0.75, cx, cy + size * 0.2, fill="#ffffff", width=2)

        elif "alien x" in name:
            # Celestialsapien 3-horned cosmic starfield
            pts = [
                cx, cy - size * 0.7,
                cx + size * 0.15, cy - size * 0.35,
                cx + size * 0.35, cy - size * 0.6,
                cx + size * 0.35, cy + size * 0.55,
                cx - size * 0.35, cy + size * 0.55,
                cx - size * 0.35, cy - size * 0.6,
                cx - size * 0.15, cy - size * 0.35,
            ]
            self.create_polygon(pts, fill="#05070f", outline="#ffffff", width=2)
            # Twinkling star field
            random.seed(42)
            for _ in range(12):
                sx = cx + random.uniform(-size * 0.22, size * 0.22)
                sy = cy + random.uniform(-size * 0.25, size * 0.4)
                self.create_oval(sx - 1.5, sy - 1.5, sx + 1.5, sy + 1.5, fill="#ffffff")

        else:
            # Default heroic crest
            self.create_oval(cx - size * 0.4, cy - size * 0.4, cx + size * 0.4, cy + size * 0.4, fill=color, outline="#ffffff", width=2)
            self.create_text(cx, cy, text="DNA", fill="#ffffff", font=("Consolas", 12, "bold"))


class OmnitrixSimulatorScreen(ttk.Frame):
    """Primary user-facing screen integrating the Omnitrix Simulator with HUD controls."""

    def __init__(self, parent: tk.Widget) -> None:
        super().__init__(parent, style="Panel.TFrame")

        # Two-column layout: Left = Interactive Watch Canvas, Right = Control & Stats HUD
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)
        self.rowconfigure(0, weight=1)

        # ---------------- Left Column: Watch Display ----------------
        canvas_container = tk.Frame(self, bg=BG_DARK, bd=2, relief="solid")
        canvas_container.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)

        # Title bar above watch
        watch_hdr = tk.Frame(canvas_container, bg=BG_PANEL)
        watch_hdr.pack(fill="x", padx=4, pady=4)

        tk.Label(
            watch_hdr,
            text="⚡ WEARABLE OMNITRIX SIMULATOR",
            bg=BG_PANEL,
            fg=OMNI_GREEN,
            font=("Consolas", 11, "bold"),
        ).pack(side="left", padx=8)

        self.btn_mute = tk.Button(
            watch_hdr,
            text="🔊 SOUND ON",
            bg="#182c1f",
            fg=OMNI_GREEN_GLOW,
            activebackground=OMNI_GREEN,
            activeforeground="#000000",
            font=("Consolas", 8, "bold"),
            relief="flat",
            command=self._toggle_sound,
        )
        self.btn_mute.pack(side="right", padx=6)

        # Interactive Canvas
        self.canvas = OmnitrixWatchCanvas(canvas_container, size=480)
        self.canvas.pack(fill="both", expand=True, padx=6, pady=6)

        # Quick Dial Turn Touch Buttons beneath the watch
        dial_bar = tk.Frame(canvas_container, bg=BG_DARK)
        dial_bar.pack(fill="x", pady=6)

        tk.Button(
            dial_bar,
            text="◀ ROTATE LEFT [A]",
            bg="#142419",
            fg=OMNI_GREEN,
            activebackground=OMNI_GREEN,
            font=("Consolas", 9, "bold"),
            relief="groove",
            command=lambda: self.canvas.rotate_dial(-1),
        ).pack(side="left", expand=True, fill="x", padx=4)

        tk.Button(
            dial_bar,
            text="💥 SLAM CORE / TRANSFORM [SPACE]",
            bg="#0c3d18",
            fg="#ffffff",
            activebackground=OMNI_GREEN,
            font=("Consolas", 9, "bold"),
            relief="raised",
            command=self.canvas.slam_core,
        ).pack(side="left", expand=True, fill="x", padx=4)

        tk.Button(
            dial_bar,
            text="ROTATE RIGHT ▶ [D]",
            bg="#142419",
            fg=OMNI_GREEN,
            activebackground=OMNI_GREEN,
            font=("Consolas", 9, "bold"),
            relief="groove",
            command=lambda: self.canvas.rotate_dial(1),
        ).pack(side="left", expand=True, fill="x", padx=4)

        # ---------------- Right Column: Controls & Alien Stats HUD ----------------
        hud_container = tk.Frame(self, bg=BG_PANEL, bd=2, relief="solid")
        hud_container.grid(row=0, column=1, sticky="nsew", padx=10, pady=10)

        # 1. Model Selector Section
        model_sec = tk.LabelFrame(
            hud_container,
            text=" ⌚ OMNITRIX GENERATION SELECTOR ",
            bg=BG_PANEL,
            fg=OMNI_GREEN,
            font=("Consolas", 9, "bold"),
            bd=1,
        )
        model_sec.pack(fill="x", padx=10, pady=6)

        gen_btn_frame = tk.Frame(model_sec, bg=BG_PANEL)
        gen_btn_frame.pack(fill="x", padx=4, pady=4)

        for gen in OmnitrixGen:
            name_label = gen.value[:5]
            tk.Button(
                gen_btn_frame,
                text=name_label,
                bg="#1a2b20",
                fg=TEXT_PRIMARY,
                activebackground=OMNI_GREEN,
                font=("Consolas", 8, "bold"),
                relief="flat",
                command=lambda g=gen: self._on_switch_gen(g),
            ).pack(side="left", expand=True, fill="x", padx=2)

        # 2. Master Control & Sub-Modes
        submodes_sec = tk.LabelFrame(
            hud_container,
            text=" ⚙️ SPECIAL SUBSYSTEMS & CHEATS ",
            bg=BG_PANEL,
            fg=OMNI_GREEN,
            font=("Consolas", 9, "bold"),
            bd=1,
        )
        submodes_sec.pack(fill="x", padx=10, pady=6)

        sub_btns = tk.Frame(submodes_sec, bg=BG_PANEL)
        sub_btns.pack(fill="x", padx=4, pady=4)

        self.btn_master = tk.Button(
            sub_btns,
            text="👑 MASTER CONTROL [M]",
            bg="#2c2a0d",
            fg="#ffd700",
            activebackground="#ffd700",
            font=("Consolas", 8, "bold"),
            relief="groove",
            command=self._on_toggle_master,
        )
        self.btn_master.pack(side="left", expand=True, fill="x", padx=2)

        tk.Button(
            sub_btns,
            text="🔬 DNA SCAN [D]",
            bg="#262208",
            fg="#ffcc00",
            activebackground="#ffcc00",
            font=("Consolas", 8, "bold"),
            relief="groove",
            command=self.canvas.trigger_dna_scan,
        ).pack(side="left", expand=True, fill="x", padx=2)

        tk.Button(
            sub_btns,
            text="⚠️ S.D.M. [S]",
            bg="#380e12",
            fg="#ff5555",
            activebackground="#ff3333",
            font=("Consolas", 8, "bold"),
            relief="groove",
            command=self.canvas.trigger_self_destruct,
        ).pack(side="left", expand=True, fill="x", padx=2)

        tk.Button(
            sub_btns,
            text="⚡ RECHARGE [R]",
            bg="#102e1b",
            fg=OMNI_GREEN_GLOW,
            activebackground=OMNI_GREEN,
            font=("Consolas", 8, "bold"),
            relief="groove",
            command=self.canvas.quick_recharge,
        ).pack(side="left", expand=True, fill="x", padx=2)

        # 3. Selected Alien Dossier & Battle Cry Banner
        self.alien_sec = tk.LabelFrame(
            hud_container,
            text=" 🧬 ALIEN DNA PROFILE & BATTLE STATS ",
            bg=BG_PANEL,
            fg=OMNI_GREEN,
            font=("Consolas", 9, "bold"),
            bd=1,
        )
        self.alien_sec.pack(fill="both", expand=True, padx=10, pady=6)

        self.lbl_alien_title = tk.Label(
            self.alien_sec,
            text="[ALIEN-01] HEATBLAST",
            bg=BG_PANEL,
            fg="#ff6600",
            font=("Consolas", 14, "bold"),
        )
        self.lbl_alien_title.pack(anchor="w", padx=10, pady=(6, 2))

        self.lbl_alien_quote = tk.Label(
            self.alien_sec,
            text='"Let\'s turn up the heat!"',
            bg=BG_PANEL,
            fg="#ffffff",
            font=("Consolas", 9, "italic"),
        )
        self.lbl_alien_quote.pack(anchor="w", padx=10, pady=(0, 6))

        self.lbl_alien_species = tk.Label(
            self.alien_sec,
            text="Species: Pyronite  •  Homeworld: Pyros",
            bg=BG_PANEL,
            fg=TEXT_MUTED,
            font=("Consolas", 8),
        )
        self.lbl_alien_species.pack(anchor="w", padx=10, pady=1)

        self.lbl_alien_ability = tk.Label(
            self.alien_sec,
            text="Ability: Pyrokinesis & Heat Generation",
            bg=BG_PANEL,
            fg=OMNI_GREEN,
            font=("Consolas", 8),
        )
        self.lbl_alien_ability.pack(anchor="w", padx=10, pady=1)

        # Live Stat Bars
        self.stats_frame = tk.Frame(self.alien_sec, bg=BG_PANEL)
        self.stats_frame.pack(fill="both", expand=True, padx=10, pady=8)

        self.stat_bars = {}
        for stat in ["Strength", "Speed", "Defense", "Energy", "Intellect"]:
            row = tk.Frame(self.stats_frame, bg=BG_PANEL)
            row.pack(fill="x", pady=2)
            tk.Label(row, text=f"{stat:<10}", bg=BG_PANEL, fg=TEXT_PRIMARY, font=("Consolas", 8)).pack(side="left")
            bar = ttk.Progressbar(row, orient="horizontal", mode="determinate", length=180)
            bar.pack(side="right", fill="x", expand=True, padx=4)
            self.stat_bars[stat] = bar

        # 4. Controls Cheatsheet
        cheat_sec = tk.LabelFrame(
            hud_container,
            text=" 🎮 WEAR OS & KEYBOARD SHORTCUTS ",
            bg=BG_PANEL,
            fg=TEXT_MUTED,
            font=("Consolas", 8, "bold"),
            bd=1,
        )
        cheat_sec.pack(fill="x", padx=10, pady=(4, 10))

        help_text = (
            "• Mouse Scroll / Drag Bezel  : Spin Alien Wheel\n"
            "• Spacebar / Click Core       : Pop-Up / Slam Transform\n"
            "• Double-Click Core / [R]     : Instant Recharge\n"
            "• Secret Master Sequence      : L, R, L, R, L, R, L, R\n"
            "• Secret Self-Destruct Code   : L, R, L, L, L, R, L, L"
        )
        tk.Label(
            cheat_sec,
            text=help_text,
            bg=BG_PANEL,
            fg="#7da08a",
            font=("Consolas", 8),
            justify="left",
        ).pack(anchor="w", padx=8, pady=4)

        # Bind Global Keyboard Shortcuts to Root Window
        self.bind("<Visibility>", self._on_screen_visible)
        self._update_alien_hud()

    def _on_screen_visible(self, _event: tk.Event) -> None:
        """Bind keyboard accelerators when screen is viewed."""
        root = self.winfo_toplevel()
        root.bind("<space>", lambda e: self.canvas.slam_core())
        root.bind("<Left>", lambda e: self.canvas.rotate_dial(-1))
        root.bind("<Right>", lambda e: self.canvas.rotate_dial(1))
        root.bind("a", lambda e: self.canvas.rotate_dial(-1))
        root.bind("d", lambda e: self.canvas.rotate_dial(1))
        root.bind("m", lambda e: self._on_toggle_master())
        root.bind("s", lambda e: self.canvas.trigger_self_destruct())
        root.bind("r", lambda e: self.canvas.quick_recharge())

    def _toggle_sound(self) -> None:
        """Toggle audio SFX."""
        new_state = sound_player.toggle()
        self.btn_mute.configure(text="🔊 SOUND ON" if new_state else "🔇 SOUND MUTED")

    def _on_switch_gen(self, gen: OmnitrixGen) -> None:
        """Switch generation from button."""
        self.canvas.set_generation(gen)

    def _on_toggle_master(self) -> None:
        """Toggle master control and update button style."""
        is_on = self.canvas.toggle_master_control()
        if is_on:
            self.btn_master.configure(bg="#ffd700", fg="#000000", text="👑 MASTER CONTROL: ON")
        else:
            self.btn_master.configure(bg="#2c2a0d", fg="#ffd700", text="👑 MASTER CONTROL [M]")

    def tick_animation(self) -> None:
        """Advance dial physics and refresh HUD details."""
        self.canvas.tick_animation()
        self._update_alien_hud()

    def _update_alien_hud(self) -> None:
        """Update alien dossier text and progress bars."""
        alien = self.canvas.current_alien
        self.lbl_alien_title.configure(
            text=f"[{alien.id:02d}] {alien.name.upper()}",
            fg=alien.signature_color,
        )
        self.lbl_alien_quote.configure(text=f'"{get_alien_quote(alien.id)}"')
        self.lbl_alien_species.configure(text=f"Species: {alien.species}  •  Homeworld: {alien.homeworld}")
        self.lbl_alien_ability.configure(text=f"Ability: {alien.primary_ability}")

        stats = get_alien_stats(alien.id)
        for stat_name, bar in self.stat_bars.items():
            bar["value"] = stats.get(stat_name, 50)
