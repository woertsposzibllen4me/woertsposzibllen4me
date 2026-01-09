"""Manages the game state transitions and notifies via WebSocket."""

import asyncio
import time
from typing import final

from src.apps.pregamespy.core.constants import (
    DSLR_HIDE_VS_SCREEN,
    DSLR_MOVE_FOR_HERO_PICK,
    DSLR_MOVE_STARTING_BUY,
    SCENE_CHANGE_FOR_PREGAME,
    SCENE_CHANGE_IN_GAME,
)
from src.apps.pregamespy.core.image_processor import ImageProcessor
from src.apps.pregamespy.core.pick_phase import PickPhase
from src.apps.pregamespy.core.shared_events import mute_ssim_prints
from src.apps.pregamespy.core.tabbed import Tabbed
from src.connection.websocket_client import WebSocketClient


@final
class GameStateManager:
    """Manages the game state transitions and notifies via WebSocket."""

    def __init__(self, image_processor: ImageProcessor, ws: WebSocketClient) -> None:
        """Initialize the GameStateManager."""
        self.image_processor = image_processor
        self.ws = ws
        self.tabbed = Tabbed()
        self.game_phase = PickPhase()

    async def set_state_finding_game(self) -> None:
        """Set the state to finding a game."""
        self.game_phase.finding_game = True  # initial game phase
        print(
            "\n\n\n\n\n\n\nWaiting to find a game..."
        )  # to avoid forefront blocking secondary windows

    async def set_state_game_found(self) -> None:
        """Set the state to game found (hero pick)."""
        self.tabbed.in_game = True
        self.game_phase.hero_pick = True
        print("\nFound a game")
        await self.ws.send_json_requests(str(SCENE_CHANGE_FOR_PREGAME))

    async def set_back_state_hero_pick(self) -> None:
        """Set the state back to hero pick e.g. from starting buy."""
        self.tabbed.in_game = True
        self.game_phase.hero_pick = True
        print("\nBack to hero select")
        await self.ws.send_json_requests(str(DSLR_MOVE_FOR_HERO_PICK))

    async def set_state_starting_buy(self) -> None:
        """Set the state to starting buy phase."""
        self.tabbed.in_game = True
        self.game_phase.starting_buy = True
        print("\nStarting buy")
        await self.ws.send_json_requests(str(DSLR_MOVE_STARTING_BUY))

    async def set_state_vs_screen(self) -> None:
        """Set the state to versus screen cutscene."""
        self.tabbed.in_game = True
        self.game_phase.versus_screen = True
        await self.ws.send_json_requests(str(DSLR_HIDE_VS_SCREEN))
        print("\nWe are in vs screen")

    async def set_state_in_game(self) -> None:
        """Set the state to in-game."""
        self.tabbed.in_game = True
        self.game_phase.in_game = True
        await self.ws.send_json_requests(str(SCENE_CHANGE_IN_GAME))
        print("\nWe are in now game")

    async def set_state_dota_menu(self) -> None:
        """Set the state to tabbed out to Dota menus."""
        self.tabbed.to_dota_menu = True
        self.game_phase.unknown = True
        await self.ws.send_json_requests(str(DSLR_HIDE_VS_SCREEN))
        print("\nWe are in Dota Menus")

    async def set_state_desktop(self) -> None:
        """Set the state to tabbed to desktop."""
        self.tabbed.to_desktop = True
        self.game_phase.unknown = True
        print("\nWe are on desktop")

    async def set_state_settings_screen(self) -> None:
        """Set the state to in Dota settings screen."""
        self.tabbed.to_settings_screen = True
        self.game_phase.unknown = True
        await self.ws.send_json_requests(str(DSLR_HIDE_VS_SCREEN))
        print("\nWe are in settings")

    async def confirm_transition_to_vs_screen(self, target_value: float) -> None:
        """Try to confirm that we are in fact in the versus screen cutscene.

        Done by assuming that if no other screen matches for 0.5 seconds, we are in vs
        screen, not very accurate.
        """
        start_time = time.time()
        duration = 0.5
        print("\nNo matches detected")
        mute_ssim_prints.set()

        while time.time() - start_time < duration:
            print(
                f"Checking for vs screen... ({time.time() - start_time:.4f}s elapsed.)",
                end="\r",
            )
            ssim_matches = await self.image_processor.scan_screen_for_matches()

            if max(ssim_matches.values()) >= target_value:
                print("\nNot in vs screen")
                break
            if time.time() - start_time >= duration:
                # The condition was true for the entire 0.5 seconds
                await self.set_state_vs_screen()
                break
        mute_ssim_prints.clear()

    async def wait_for_settings_screen_exiting_fade_out(self):
        """Wait for the settings screen to finish its fade-out transition."""
        self.tabbed.to_settings_screen = False
        await asyncio.sleep(0.25)

    async def wait_for_starting_buy_screen_transition_out(self):
        """Wait for the slide transition animation back to hero picks screen."""
        self.game_phase.starting_buy = False
        await asyncio.sleep(0.6)
