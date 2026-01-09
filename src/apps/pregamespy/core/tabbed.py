"""Module for managing mutually exclusive tabbed states."""

from typing import final


@final
class Tabbed:
    """Class to manage mutually exclusive tabbed states."""

    def __init__(self) -> None:
        """Initialize all states to False."""
        self._to_desktop = False
        self._to_dota_menu = False
        self._to_settings_screen = False
        self._in_game = False

    @property
    def to_desktop(self) -> bool:
        """Tabbed out to Windows desktop."""
        return self._to_desktop

    @to_desktop.setter
    def to_desktop(self, value: bool) -> None:
        if value:
            self._set_all_false()
        self._to_desktop = value

    @property
    def to_dota_menu(self) -> bool:
        """Tabbed out to Dota 2 game menus (armory, heroes, etc.)."""
        return self._to_dota_menu

    @to_dota_menu.setter
    def to_dota_menu(self, value: bool) -> None:
        if value:
            self._set_all_false()
        self._to_dota_menu = value

    @property
    def to_settings_screen(self) -> bool:
        """In the Dota2 floating window settings screen."""
        return self._to_settings_screen

    @to_settings_screen.setter
    def to_settings_screen(self, value: bool) -> None:
        if value:
            self._set_all_false()
        self._to_settings_screen = value

    @property
    def in_game(self) -> bool:
        """In a live game."""
        return self._in_game

    @in_game.setter
    def in_game(self, value: bool) -> None:
        if value:
            self._set_all_false()
        self._in_game = value

    def _set_all_false(self) -> None:
        for attr in self.__dict__:
            self.__dict__[attr] = False
