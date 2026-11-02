"""Unit tests for DeviceSummary and CharacteristicSummary models."""

from omnitrix_watch.models.device import CharacteristicSummary, DeviceSummary


def test_device_summary_sanitized_address() -> None:
    """Verify MAC addresses are properly masked to protect user privacy."""
    dev = DeviceSummary(address="AA:BB:CC:DD:EE:FF", name="Redmi Watch Move 2", rssi=-60)
    assert dev.display_name == "Redmi Watch Move 2"
    assert dev.sanitized_address == "AA:BB:**:**:**:FF"


def test_device_summary_unknown_name() -> None:
    """Verify missing device name is formatted gracefully."""
    dev = DeviceSummary(address="11:22:33:44:55:66", name=None)
    assert dev.display_name == "Unknown Device"


def test_characteristic_summary_properties() -> None:
    """Verify capability checks for read, write, notify."""
    char_read_only = CharacteristicSummary(
        service_uuid="0000180a-0000-1000-8000-00805f9b34fb",
        characteristic_uuid="00002a24-0000-1000-8000-00805f9b34fb",
        properties=["read"],
    )
    assert char_read_only.is_readable is True
    assert char_read_only.is_writable is False
    assert char_read_only.is_notifiable is False

    char_write_notify = CharacteristicSummary(
        service_uuid="fee0",
        characteristic_uuid="fee1",
        properties=["write-without-response", "notify"],
    )
    assert char_write_notify.is_readable is False
    assert char_write_notify.is_writable is True
    assert char_write_notify.is_notifiable is True
