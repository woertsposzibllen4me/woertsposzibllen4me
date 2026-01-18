"""Demonstrate what happens when launching an app using the terminal window manager."""

import argparse
import shutil
import subprocess
from typing import Protocol, cast

from src.config.settings import PROJECT_ROOT_PATH
from src.core.termwm.example.example_script import TMW_EXAMPLE_SCRIPT_FILEPATH


class Args(Protocol):
    """Protocol for command-line arguments."""

    clear_slots: bool


def launch_main_script(*, clear_slots: bool = False) -> None:
    """Simulate the launching of an application using the terminal window manager.

    Args:
        clear_slots: Whether to clear all slots in the database before adjusting.

    """
    example_script_filename = TMW_EXAMPLE_SCRIPT_FILEPATH

    commands = [
        f"cd /d {PROJECT_ROOT_PATH}",
        f"set PYTHONPATH={PROJECT_ROOT_PATH}",
        ".\\.venv\\Scripts\\activate",
        f"py {example_script_filename}" + (" --clear-slots" if clear_slots else ""),
    ]

    cmd_path = shutil.which("cmd")
    if not cmd_path:
        e = "Could not find cmd.exe in PATH."
        raise RuntimeError(e)

    # Use /k to keep parent window open after executing start command
    command_string = " && ".join(commands)
    subprocess.run(  # noqa: S603  # Intentional: controlled input only
        [cmd_path, "/c", "start", "cmd", "/k", command_string],
        check=True,
        cwd=PROJECT_ROOT_PATH,
    )


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
    launch_main_script(clear_slots=args.clear_slots)
