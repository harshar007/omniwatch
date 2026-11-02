"""Main entrypoint for Omnitrix Watch Companion & Research Platform."""

from __future__ import annotations

import argparse
import asyncio
import logging
import sys
import tkinter as tk
from typing import Optional

from omnitrix_watch.ble.scanner import BLEScannerService
from omnitrix_watch.config import AppConfig
from omnitrix_watch.logging_setup import setup_logging
from omnitrix_watch.models.device import DeviceSummary

logger = logging.getLogger(__name__)


def run_cli_scan(duration: float, name_filter: Optional[str]) -> int:
    """Perform a headless BLE scan from the console."""
    print("=" * 65)
    print("OMNITRIX RESEARCH PROTOCOL: BLE SCANNER (HEADLESS CLI)")
    print("=" * 65)
    print(f"Scanning for {duration:.1f}s (Filter: '{name_filter or 'None'}')...\n")

    scanner = BLEScannerService(default_duration=duration)

    def _on_device(dev: DeviceSummary) -> None:
        rssi = f"{dev.rssi} dBm" if dev.rssi is not None else "N/A"
        print(f"[*] Found: {dev.display_name:<28} | MAC: {dev.sanitized_address:<18} | RSSI: {rssi}")

    try:
        devices = asyncio.run(scanner.scan(duration=duration, name_filter=name_filter, detection_callback=_on_device))
        print(f"\n[+] Scan finished. Total devices detected: {len(devices)}")
        return 0
    except Exception as e:
        print(f"\n[-] Error running BLE scan: {e}", file=sys.stderr)
        return 1


def run_gui(config: AppConfig) -> int:
    """Launch the Omnitrix graphical user interface."""
    try:
        from omnitrix_watch.ui.app import OmnitrixApp
    except ImportError as e:
        logger.error("Failed to import UI components: %s", e)
        return 1

    try:
        root = tk.Tk()
        _app = OmnitrixApp(root, config)
        root.mainloop()
        return 0
    except Exception as e:
        logger.error("Error executing Omnitrix GUI: %s", e)
        return 1


def main() -> int:
    """Parse arguments and start application."""
    parser = argparse.ArgumentParser(
        description="Omnitrix Watch Companion & Research Platform (Target: Redmi Watch Move)",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    parser.add_argument(
        "--config",
        "-c",
        type=str,
        default=None,
        help="Path to custom TOML configuration file",
    )
    parser.add_argument(
        "--cli-scan",
        action="store_true",
        help="Run headless command-line BLE scan without opening GUI",
    )
    parser.add_argument(
        "--duration",
        "-d",
        type=float,
        default=5.0,
        help="Duration in seconds for BLE scan (used with --cli-scan)",
    )
    parser.add_argument(
        "--filter",
        "-f",
        type=str,
        default=None,
        help="Device name filter substring (case-insensitive)",
    )
    parser.add_argument(
        "--log-level",
        type=str,
        default=None,
        choices=["DEBUG", "INFO", "WARNING", "ERROR"],
        help="Override logging verbosity",
    )

    args = parser.parse_args()

    config = AppConfig.load(args.config)
    if args.log_level:
        config.logging.level = args.log_level

    setup_logging(config.logging)

    if args.cli_scan:
        filt = args.filter if args.filter is not None else (config.ble.name_filter or None)
        return run_cli_scan(args.duration or config.ble.scan_duration, filt)

    return run_gui(config)


if __name__ == "__main__":
    sys.exit(main())
