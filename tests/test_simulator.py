"""Unit tests for the Omnitrix Simulator screen and state engine."""

import tkinter as tk

from omnitrix_watch.ui.screens.simulator import (
    GEN_THEMES,
    OmnitrixGen,
    OmnitrixSimulatorScreen,
    OmnitrixWatchCanvas,
    SimulatorState,
)
from omnitrix_watch.watchface.aliens import get_simulator_aliens


def test_simulator_generations_and_roster() -> None:
    """Verify all 4 generations exist and simulator roster has 18 aliens."""
    roster = get_simulator_aliens(include_unlocked=True)
    assert len(roster) == 18
    assert len(GEN_THEMES) == 4
    for gen in OmnitrixGen:
        assert gen in GEN_THEMES
        assert "accent" in GEN_THEMES[gen]
        assert "glow" in GEN_THEMES[gen]


def test_simulator_canvas_state_machine() -> None:
    """Test full cycle of states: Standby -> Selection -> Transform -> Transformed -> Revert -> Cooldown -> Quick Recharge."""
    root = tk.Tk()
    try:
        canvas = OmnitrixWatchCanvas(root, size=400)
        assert canvas.state == SimulatorState.STANDBY

        # 1. Pop-Up Core
        canvas.pop_up_core()
        assert canvas.state == SimulatorState.SELECTION
        assert canvas.target_pop_height == 1.0

        # 2. Rotate Dial
        initial_idx = canvas.alien_index
        canvas.rotate_dial(1)
        assert canvas.alien_index == (initial_idx + 1) % len(canvas.roster)
        canvas.rotate_dial(-1)
        assert canvas.alien_index == initial_idx

        # 3. Slam / Transform
        canvas.slam_core()
        assert canvas.state == SimulatorState.TRANSFORMING
        assert canvas.flash_alpha == 1.0

        # Simulate flash decay to reach TRANSFORMED state
        canvas.flash_alpha = 0.3
        canvas.tick_animation()
        assert canvas.state == SimulatorState.TRANSFORMED

        # 4. Revert to human
        canvas.revert_to_human()
        assert canvas.state == SimulatorState.COOLDOWN
        assert canvas.cooldown_progress == 0.0

        # 5. Quick Recharge
        canvas.quick_recharge()
        assert canvas.state == SimulatorState.STANDBY
        assert canvas.cooldown_progress == 1.0

    finally:
        root.destroy()


def test_master_control_and_secret_sequences() -> None:
    """Verify Master Control toggle and secret sequence decoding."""
    root = tk.Tk()
    try:
        canvas = OmnitrixWatchCanvas(root, size=400)
        assert canvas.master_control is False

        # Toggle master control directly
        is_active = canvas.toggle_master_control()
        assert is_active is True
        assert canvas.master_control is True

        # Test secret code execution: L, R, L, R, L, R, L, R
        canvas.master_control = False
        canvas.turn_sequence.clear()
        for d in [-1, 1, -1, 1, -1, 1, -1, 1]:
            canvas.rotate_dial(d)

        # After sequence completes, master control should be engaged
        assert canvas.master_control is True

        # Test Self-Destruct secret sequence: L, R, L, L, L, R, L, L
        canvas.state = SimulatorState.STANDBY
        canvas.turn_sequence.clear()
        for d in [-1, 1, -1, -1, -1, 1, -1, -1]:
            canvas.rotate_dial(d)

        assert canvas.state == SimulatorState.SELF_DESTRUCT
        assert canvas.self_destruct_seconds == 30.0

        # Abort self-destruct
        canvas.trigger_self_destruct()
        assert canvas.state == SimulatorState.STANDBY

    finally:
        root.destroy()


def test_simulator_screen_initialization() -> None:
    """Verify OmnitrixSimulatorScreen mounts properly with all HUD widgets."""
    root = tk.Tk()
    try:
        screen = OmnitrixSimulatorScreen(root)
        screen.pack(fill="both", expand=True)
        root.update()

        # Advance tick animation
        screen.tick_animation()
        assert screen.canvas.state == SimulatorState.STANDBY

        # Test generation switch
        screen._on_switch_gen(OmnitrixGen.RECALIBRATED)
        assert screen.canvas.generation == OmnitrixGen.RECALIBRATED

        screen._on_switch_gen(OmnitrixGen.ALBEDO)
        assert screen.canvas.generation == OmnitrixGen.ALBEDO

    finally:
        root.destroy()
