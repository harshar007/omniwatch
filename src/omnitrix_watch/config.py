"""Application configuration management."""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
import tomllib
from typing import Optional


@dataclass
class BLEConfig:
    """BLE connection and scanning settings."""

    scan_duration: float = 5.0
    name_filter: str = ""
    connect_timeout: float = 10.0


@dataclass
class UIConfig:
    """User interface appearance and behavior settings."""

    theme: str = "omnitrix_classic"
    window_width: int = 860
    window_height: int = 700


@dataclass
class LoggingConfig:
    """Logging settings."""

    level: str = "INFO"
    log_to_file: bool = True
    log_file: str = "logs/omnitrix_watch.log"


@dataclass
class AppConfig:
    """Top-level configuration object."""

    ble: BLEConfig = field(default_factory=BLEConfig)
    ui: UIConfig = field(default_factory=UIConfig)
    logging: LoggingConfig = field(default_factory=LoggingConfig)

    @classmethod
    def load(cls, config_path: Optional[str | Path] = None) -> AppConfig:
        """Load configuration from a TOML file if present, else use defaults."""
        path_to_try = None
        if config_path:
            path_to_try = Path(config_path)
        else:
            default_config = Path("config/app.toml")
            if default_config.exists():
                path_to_try = default_config
            else:
                example_config = Path("config/app.example.toml")
                if example_config.exists():
                    path_to_try = example_config

        if not path_to_try or not path_to_try.exists():
            return cls()

        try:
            with open(path_to_try, "rb") as f:
                data = tomllib.load(f)

            ble_data = data.get("ble", {})
            ui_data = data.get("ui", {})
            log_data = data.get("logging", {})

            return cls(
                ble=BLEConfig(
                    scan_duration=float(ble_data.get("scan_duration", 5.0)),
                    name_filter=str(ble_data.get("name_filter", "")),
                    connect_timeout=float(ble_data.get("connect_timeout", 10.0)),
                ),
                ui=UIConfig(
                    theme=str(ui_data.get("theme", "omnitrix_classic")),
                    window_width=int(ui_data.get("window_width", 860)),
                    window_height=int(ui_data.get("window_height", 700)),
                ),
                logging=LoggingConfig(
                    level=str(log_data.get("level", "INFO")),
                    log_to_file=bool(log_data.get("log_to_file", True)),
                    log_file=str(log_data.get("log_file", "logs/omnitrix_watch.log")),
                ),
            )
        except Exception:
            return cls()
