"""Run from demonstrator.py to simulate an app using the terminal window manager."""

import argparse
import asyncio
from pathlib import Path
from random import randint
from typing import Protocol, cast

import src.core.termwm.slots_db_handler as sdh
from src.config.settings import PROJECT_ROOT_PATH
from src.core.termwm import (
    TERMINAL_WINDOW_SLOTS_DB_FILE_PATH,
    SecondaryWindow,
    TerminalWindowManager,
    WinType,
)
from src.core.termwm.example.example_secondary_window import (
    TMW_EXAMPLE_SECOND_WIN_FILEPATH,
)

TMW_EXAMPLE_SCRIPT_FILEPATH = Path(__file__)


class Args(Protocol):
    """Protocol for command-line arguments."""

    clear_slots: bool


async def main(*, clear_db_slots: bool = False) -> None:
    """Simulate the main script of an app using the terminal window manager at startup.

    Args:
        clear_db_slots: Whether to free all DB slots after adjusting.

    Usage:
        This script is meant to be run from the demonstrator.py script and will
        simulate the cli window of a script being repositioned and resized.

    """

    async def spawn_secondary_window(
        title: str = "Secondary Window", width: str = "200", height: str = "200"
    ) -> None:
        await asyncio.create_subprocess_exec(
            "python",
            str(script_file),
            title,
            width,
            height,
            cwd=str(PROJECT_ROOT_PATH),
        )

    script_file = TMW_EXAMPLE_SECOND_WIN_FILEPATH

    conn = await sdh.create_connection(TERMINAL_WINDOW_SLOTS_DB_FILE_PATH)
    if not conn:
        print("Connection with DB failed to be established.")
        return

    if clear_db_slots:
        await sdh.free_all_slots(conn)
        print("Freed slots.")

    main_manager = TerminalWindowManager()
    slot, _ = await main_manager.adjust_terminal_window(
        conn, WinType.ACCEPTED, "Example Script"
    )

    if slot is None:
        print("No slot in DB available/error occured.")
        return

    secondary_windows = [
        SecondaryWindow(name="Secondary Window 1", width=150, height=150),
        SecondaryWindow(
            name="Secondary Window 2",
            width=randint(120, 200),  # noqa: S311
            height=randint(120, 200),  # noqa: S311
        ),
    ]

    tasks = [
        spawn_secondary_window(window.name, str(window.width), str(window.height))
        for window in secondary_windows
    ]

    await asyncio.gather(*tasks)
    await asyncio.sleep(1)  # Give some time for the windows to appear
    await main_manager.adjust_secondary_windows(conn, slot, secondary_windows)
    print("Adjusted.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Launch the main script with an option to clear database slots."
    )
    parser.add_argument(
        "--clear-slots",
        action="store_true",
        help="Clear all slots in the database after adjusting",
    )
    args = cast("Args", cast("object", parser.parse_args()))
    print(f"Clear slots: {args.clear_slots}")
    asyncio.run(main(clear_db_slots=args.clear_slots))
