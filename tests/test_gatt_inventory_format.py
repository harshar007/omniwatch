"""Unit tests for GATT Inventory Markdown export and formatting."""

from omnitrix_watch.models.device import CharacteristicSummary, GattInventory


def test_gatt_inventory_markdown_format() -> None:
    """Verify inventory generates compliant, sanitized Markdown tables."""
    chars = [
        CharacteristicSummary(
            service_uuid="0000180a-0000-1000-8000-00805f9b34fb",
            service_name="Device Information",
            characteristic_uuid="00002a24-0000-1000-8000-00805f9b34fb",
            characteristic_name="Model Number String",
            properties=["read"],
            read_result="M2345W1",
        ),
        CharacteristicSummary(
            service_uuid="0000fee0-0000-1000-8000-00805f9b34fb",
            service_name="Xiaomi Profile Service",
            characteristic_uuid="00000001-0000-1000-8000-00805f9b34fb",
            characteristic_name="Unknown Characteristic",
            properties=["write", "notify"],
            read_result=None,
        ),
        CharacteristicSummary(
            service_uuid="0000fee1-0000-1000-8000-00805f9b34fb",
            service_name="Xiaomi Auth Service",
            characteristic_uuid="00000002-0000-1000-8000-00805f9b34fb",
            characteristic_name="Unknown Characteristic",
            properties=["read"],
            read_error="ATT_ERR_INSUFFICIENT_AUTHENTICATION",
        ),
    ]

    inventory = GattInventory(
        device_name="Redmi Watch Move",
        device_model="Redmi Watch Move",
        timestamp="2026-11-02T12:00:00Z",
        characteristics=chars,
    )

    md = inventory.to_markdown()

    # Check headers and markdown formatting
    assert "# GATT Service & Characteristic Inventory" in md
    assert "Redmi Watch Move" in md
    assert "| `0000180a-0000-1000-8000-00805f9b34fb` | Device Information | `00002a24-0000-1000-8000-00805f9b34fb` | Model Number String | read | Yes | `M2345W1` |" in md
    assert "*Not readable*" in md
    assert "Read error: ATT_ERR_INSUFFICIENT_AUTHENTICATION" in md
    assert "Security & Safety Notice" in md
