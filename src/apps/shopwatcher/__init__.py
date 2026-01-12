"""ShopWatcher application package.

This app is used to monitor the shop interface appearance from Dota2, react when it
opens/closes and track the time spent in the shop.
"""

from .core.constants import SECONDARY_WINDOWS
from .core.shared_events import mute_ssim_prints, secondary_windows_spawned
from .core.shop_detector import ShopDetector
from .core.socket_handler import ShopWatcherHandler

__all__ = [
    "SECONDARY_WINDOWS",
    "ShopDetector",
    "ShopWatcherHandler",
    "mute_ssim_prints",
    "secondary_windows_spawned",
]
