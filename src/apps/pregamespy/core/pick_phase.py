"""Module to store the pick phase states in a game start."""

from typing import final


@final
class PickPhase:
    """Class to store and ensure only one state is active at a time."""

    def __init__(self) -> None:
        """Initialize all states to False."""
        self._finding_game = False
        self._hero_pick = False
        self._starting_buy = False
        self._versus_screen = False
        self._in_game = False
        self._unknown = False

    @property
    def finding_game(self) -> bool:
        """Searching for a game."""
        return self._finding_game

    @finding_game.setter
    def finding_game(self, value: bool) -> None:
        if value:
            self._set_all_false()
        self._finding_game = value

    @property
    def hero_pick(self) -> bool:
        """In hero selection phase."""
        return self._hero_pick

    @hero_pick.setter
    def hero_pick(self, value: bool) -> None:
        if value:
            self._set_all_false()
        self._hero_pick = value

    @property
    def starting_buy(self) -> bool:
        """In starting buy phase."""
        return self._starting_buy

    @starting_buy.setter
    def starting_buy(self, value: bool) -> None:
        if value:
            self._set_all_false()
        self._starting_buy = value

    @property
    def versus_screen(self) -> bool:
        """In versus screen cutscene."""
        return self._versus_screen

    @versus_screen.setter
    def versus_screen(self, value: bool) -> None:
        if value:
            self._set_all_false()
        self._versus_screen = value

    @property
    def in_game(self) -> bool:
        """In actual game."""
        return self._in_game

    @in_game.setter
    def in_game(self, value: bool) -> None:
        if value:
            self._set_all_false()
        self._in_game = value

    @property
    def unknown(self) -> bool:
        """Unknown state (e.g., tabbed out)."""
        return self._unknown

    @unknown.setter
    def unknown(self, value: bool) -> None:
        if value:
            self._set_all_false()
        self._unknown = value

    def _set_all_false(self) -> None:
        for attr in self.__dict__:
            self.__dict__[attr] = False
