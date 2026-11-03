"""UI Screens package."""

from omnitrix_watch.ui.screens.device_details import DeviceDetailsScreen
from omnitrix_watch.ui.screens.device_picker import DevicePickerScreen
from omnitrix_watch.ui.screens.donation import DonationScreen
from omnitrix_watch.ui.screens.home import HomeScreen
from omnitrix_watch.ui.screens.simulator import OmnitrixSimulatorScreen
from omnitrix_watch.ui.screens.watchface import WatchFaceScreen

__all__ = [
    "OmnitrixSimulatorScreen",
    "HomeScreen",
    "DevicePickerScreen",
    "DeviceDetailsScreen",
    "WatchFaceScreen",
    "DonationScreen",
]
