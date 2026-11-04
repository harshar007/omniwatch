"""Unit tests for the modularized Omnitrix UI components."""

from __future__ import annotations

import tkinter as tk

from omnitrix_watch.models.device import DeviceSummary
from omnitrix_watch.services.device_session import SessionState
from omnitrix_watch.ui.components.cards import CyberCard, SignalMeter, StatBadge
from omnitrix_watch.ui.components.dial import OmnitrixDial
from omnitrix_watch.ui.components.footer_hud import FooterHUD
from omnitrix_watch.ui.components.header_bar import HeaderBar
from omnitrix_watch.ui.components.navbar import OmniNavBar
from omnitrix_watch.ui.components.radar import OmnitrixRadarCanvas
from omnitrix_watch.ui.components.watch_preview import WatchPreviewCanvas
from omnitrix_watch.watchface.aliens import DEFAULT_ALIEN_ROSTER


def test_dial_component() -> None:
    """Test Omnitrix circular dial states and animation ticks."""
    root = tk.Tk()
    root.withdraw()
    try:
        dial = OmnitrixDial(root, size=200)
        assert dial.current_state == SessionState.IDLE
        assert dial.state_label == "STANDBY"

        # Update state to scanning
        dial.update_state(SessionState.SCANNING)
        assert dial.current_state == SessionState.SCANNING
        assert dial.is_animating is True

        # Tick animation
        dial.tick_animation()

        # Simulate click shockwave
        dial._on_dial_click(None)
        assert dial.shockwave_radius > 0
    finally:
        root.destroy()


def test_radar_component() -> None:
    """Test Omnitrix BLE radar blip plotting and scanning sweep."""
    root = tk.Tk()
    root.withdraw()
    try:
        radar = OmnitrixRadarCanvas(root, size=150)
        assert radar.is_scanning is False

        radar.update_scan_state(True)
        assert radar.is_scanning is True
        radar.tick_animation()

        dev = DeviceSummary(name="Redmi Watch Move 2", address="AA:BB:CC:DD:EE:FF", rssi=-62)
        radar.update_devices([dev], selected_addr=dev.address)
        assert len(radar.devices) == 1
    finally:
        root.destroy()


def test_watch_preview_component() -> None:
    """Test watch preview canvas drawing and alien profile switching."""
    root = tk.Tk()
    root.withdraw()
    try:
        preview = WatchPreviewCanvas(root, width=200, height=250)
        assert preview.selected_alien.id == DEFAULT_ALIEN_ROSTER[0].id

        if len(DEFAULT_ALIEN_ROSTER) > 1:
            preview.update_alien(DEFAULT_ALIEN_ROSTER[1])
            assert preview.selected_alien.id == DEFAULT_ALIEN_ROSTER[1].id

        preview.tick_animation()
    finally:
        root.destroy()


def test_header_and_navbar_components() -> None:
    """Test HeaderBar, OmniNavBar, and FooterHUD components."""
    root = tk.Tk()
    root.withdraw()
    try:
        header = HeaderBar(root)
        header.set_status("CONNECTED")
        assert header.lbl_status_pill.cget("text") == "CONNECTED"

        selected_tabs = []
        navbar = OmniNavBar(
            root,
            tabs=[("t1", "Tab 1"), ("t2", "Tab 2")],
            on_select=lambda idx, tid: selected_tabs.append((idx, tid)),
        )
        assert navbar.current_index == 0
        navbar.select_tab(1)
        assert navbar.current_index == 1
        assert selected_tabs[-1] == (1, "t2")

        footer = FooterHUD(root)
        footer.set_ble_status("CONNECTED")
        footer.set_core_status("99% OPTIMAL")
    finally:
        root.destroy()


def test_cards_and_stat_badges() -> None:
    """Test CyberCard, StatBadge, and SignalMeter."""
    root = tk.Tk()
    root.withdraw()
    try:
        card = CyberCard(root, title="Telemetry", subtitle="Real-time")
        badge = StatBadge(card.body, label="Battery", value="98%")
        assert badge.lbl_val.cget("text") == "98%"
        badge.set_value("100%")
        assert badge.lbl_val.cget("text") == "100%"

        meter = SignalMeter(card.body)
        meter.set_rssi(-50)
        assert meter.rssi == -50
    finally:
        root.destroy()
