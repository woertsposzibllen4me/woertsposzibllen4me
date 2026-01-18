"""Constants for the pregamespy application."""

from src.config.settings import PROJECT_ROOT_PATH
from src.core.termwm import SecondaryWindow
from src.utils.helpers import load_grayscale_opencv_template

# Window config for TerminalWindowManager
SECONDARY_WINDOWS = [
    SecondaryWindow("hero_pick_scanner", 150, 80),
    SecondaryWindow("starting_buy_scanner", 150, 80),
    SecondaryWindow("dota_tab_scanner", 150, 80),
    SecondaryWindow("desktop_tab_scanner", 150, 80),
    SecondaryWindow("settings_scanner", 150, 80),
    SecondaryWindow("in_game_scanner", 150, 100),
]

_BASE_DIR = PROJECT_ROOT_PATH / "data" / "apps" / "pregamespy"
_OPENCV_DIR = _BASE_DIR / "opencv"
_WS_REQUESTS_DIR = _BASE_DIR / "ws_requests"

# Screen areas
DOTA_TAB_AREA = {"left": 1860, "top": 10, "width": 60, "height": 40}
STARTING_BUY_AREA = {"left": 860, "top": 120, "width": 400, "height": 30}
IN_GAME_AREA = {"left": 1820, "top": 1020, "width": 80, "height": 60}
PLAY_DOTA_BUTTON_AREA = {"left": 1525, "top": 1005, "width": 340, "height": 55}
DESKTOP_TAB_AREA = {"left": 1750, "top": 1040, "width": 50, "height": 40}
SETTINGS_AREA = {"left": 170, "top": 85, "width": 40, "height": 40}
HERO_PICK_AREA = {"left": 1658, "top": 1028, "width": 62, "height": 38}
NEW_CAPTURE_AREA = {"left": 0, "top": 0, "width": 0, "height": 0}

# Path to OpenCV templates
DOTA_TAB_TEMPLATE = load_grayscale_opencv_template(
    _OPENCV_DIR / "dota_menu_power_icon.jpg"
)
IN_GAME_TEMPLATE = load_grayscale_opencv_template(
    _OPENCV_DIR / "dota_courier_deliver_items_icon.jpg"
)
STARTING_BUY_TEMPLATE = load_grayscale_opencv_template(
    _OPENCV_DIR / "dota_strategy-load-out-world-guides.jpg"
)
PLAY_DOTA_BUTTON_TEMPLATE = load_grayscale_opencv_template(
    _OPENCV_DIR / "dota_play_dota_button.jpg"
)
DESKTOP_TAB_TEMPLATE = load_grayscale_opencv_template(
    _OPENCV_DIR / "windows_desktop_icons.jpg"
)
SETTINGS_TEMPLATE = load_grayscale_opencv_template(
    _OPENCV_DIR / "dota_settings_icon.jpg"
)
HERO_PICK_TEMPLATE = load_grayscale_opencv_template(
    _OPENCV_DIR / "dota_hero_select_chat_icons.jpg"
)

# Paths to JSON request files for scene changes
SCENE_CHANGE_IN_GAME = _WS_REQUESTS_DIR / "scene_change_for_in_game.json"
DSLR_MOVE_FOR_HERO_PICK = _WS_REQUESTS_DIR / "dslr_move_for_hero_pick.json"
SCENE_CHANGE_FOR_PREGAME = _WS_REQUESTS_DIR / "scene_change_for_pregame.json"
DSLR_MOVE_STARTING_BUY = _WS_REQUESTS_DIR / "dslr_move_for_starting_buy.json"
DSLR_HIDE_VS_SCREEN = _WS_REQUESTS_DIR / "dslr_hide_for_vs_screen.json"
