"""Watch Face generator and layout builder for Redmi Watch Move 2."""

from __future__ import annotations

import datetime
import json
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Any, Dict, Optional

from omnitrix_watch.watchface.aliens import (
    DEFAULT_ALIEN_ROSTER,
    AlienProfile,
    get_alien_by_id,
)


@dataclass
class WatchFaceConfig:
    """Configuration settings for generating a Redmi Watch Move 2 watch face."""

    target_device: str = "Redmi Watch Move 2"
    screen_width: int = 390
    screen_height: int = 450
    selected_alien_id: int = 1
    time_format_24h: bool = True
    show_seconds: bool = True
    show_date: bool = True
    show_battery: bool = True
    show_heart_rate: bool = True
    dial_glow_color: str = "#00ff55"
    dial_style: str = "omnitrix_classic"


@dataclass
class WatchFaceManifest:
    """Manifest describing all layout elements for the Redmi Watch Move 2 screen."""

    schema_version: str
    target_hardware: str
    created_at: str
    dimensions: Dict[str, int]
    selected_alien: Dict[str, Any]
    layout_elements: Dict[str, Any]
    color_palette: Dict[str, str]

    def to_json(self, indent: int = 2) -> str:
        """Serialize manifest to JSON string."""
        return json.dumps(asdict(self), indent=indent)


class WatchFaceGenerator:
    """Constructs and exports Omnitrix watch face bundles for the Redmi Watch Move 2."""

    def __init__(self, config: Optional[WatchFaceConfig] = None) -> None:
        self.config = config or WatchFaceConfig()

    def get_current_alien(self) -> AlienProfile:
        """Return the active alien profile for the watch face."""
        alien = get_alien_by_id(self.config.selected_alien_id)
        if not alien:
            alien = DEFAULT_ALIEN_ROSTER[0]
        return alien

    def format_time_preview(self, dt: Optional[datetime.datetime] = None) -> str:
        """Format a sample time string according to configuration."""
        now = dt or datetime.datetime.now()
        if self.config.time_format_24h:
            fmt = "%H:%M:%S" if self.config.show_seconds else "%H:%M"
        else:
            fmt = "%I:%M:%S %p" if self.config.show_seconds else "%I:%M %p"
        return now.strftime(fmt)

    def generate_manifest(self) -> WatchFaceManifest:
        """Generate structured manifest detailing coordinate layers for the watch display."""
        alien = self.get_current_alien()
        w = self.config.screen_width
        h = self.config.screen_height

        layout = {
            "background": {
                "type": "vector_dial",
                "center_x": w // 2,
                "center_y": h // 2,
                "radius": min(w, h) // 2 - 20,
                "primary_color": "#080c0a",
                "glow_color": self.config.dial_glow_color,
            },
            "time_display": {
                "type": "digital_clock",
                "pos_x": w // 2,
                "pos_y": (h // 2) - 85,
                "align": "center",
                "font": "Galvanic-Neon-Monospace",
                "color": "#00ff55",
                "format_24h": self.config.time_format_24h,
                "show_seconds": self.config.show_seconds,
            },
            "date_display": {
                "type": "calendar_date",
                "pos_x": w // 2,
                "pos_y": (h // 2) - 55,
                "align": "center",
                "color": "#a0e8b0",
                "enabled": self.config.show_date,
            },
            "alien_silhouette": {
                "type": "alien_matrix_emblem",
                "pos_x": w // 2,
                "pos_y": (h // 2) + 15,
                "diameter": 110,
                "alien_id": alien.id,
                "alien_name": alien.name,
                "signature_color": alien.signature_color,
                "dna_code": alien.dna_code,
            },
            "battery_meter": {
                "type": "arc_progress_bar",
                "pos_x": 45,
                "pos_y": h - 40,
                "color": "#00ff55",
                "label": "CORE_PWR",
                "enabled": self.config.show_battery,
            },
            "heart_rate_meter": {
                "type": "arc_progress_bar",
                "pos_x": w - 45,
                "pos_y": h - 40,
                "color": "#ff3355",
                "label": "PULSE_BPM",
                "enabled": self.config.show_heart_rate,
            },
        }

        palette = {
            "background": "#080c0a",
            "dial_glow": self.config.dial_glow_color,
            "alien_accent": alien.signature_color,
            "text_primary": "#00ff55",
            "text_secondary": "#a0e8b0",
            "status_bar": "#002b11",
        }

        return WatchFaceManifest(
            schema_version="1.0.0",
            target_hardware=self.config.target_device,
            created_at=datetime.datetime.now(datetime.timezone.utc).isoformat(),
            dimensions={"width": w, "height": h},
            selected_alien={
                "id": alien.id,
                "name": alien.name,
                "species": alien.species,
                "homeworld": alien.homeworld,
                "dna_code": alien.dna_code,
                "color": alien.signature_color,
            },
            layout_elements=layout,
            color_palette=palette,
        )

    def export_bundle(self, output_dir: Path) -> Path:
        """Export watch face manifest and source assets to directory."""
        output_dir.mkdir(parents=True, exist_ok=True)
        manifest = self.generate_manifest()
        
        manifest_path = output_dir / "watchface_manifest.json"
        manifest_path.write_text(manifest.to_json(), encoding="utf-8")

        # Generate human-readable spec sheet
        spec_sheet = output_dir / "WATCHFACE_SPEC.md"
        alien = self.get_current_alien()
        spec_content = (
            f"# Omnitrix Watch Face Specification\n\n"
            f"- **Target Peripheral:** {self.config.target_device}\n"
            f"- **Resolution:** {self.config.screen_width} x {self.config.screen_height} AMOLED\n"
            f"- **Active Alien DNA:** #{alien.id} {alien.name} ({alien.species} - {alien.homeworld})\n"
            f"- **DNA Code:** `{alien.dna_code}`\n"
            f"- **Time Display:** {'24-Hour' if self.config.time_format_24h else '12-Hour'} "
            f"({'with seconds' if self.config.show_seconds else 'HH:MM'})\n"
            f"- **Accent Color:** `{alien.signature_color}`\n\n"
            f"```ascii\n{alien.ascii_art}\n```\n\n"
            f"## Next Step for Device Deployment\n"
            f"Compile these coordinates and glyph assets into `.bin` using EasyFace / Mi Create "
            f"or upload via companion BLE transfer.\n"
        )
        spec_sheet.write_text(spec_content, encoding="utf-8")

        return manifest_path
