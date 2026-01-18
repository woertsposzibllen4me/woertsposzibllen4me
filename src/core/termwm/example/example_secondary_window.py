"""Example of a secondary window with customizable title and size."""

import argparse
import tkinter as tk
from pathlib import Path
from typing import Protocol, cast

TMW_EXAMPLE_SECOND_WIN_FILEPATH = Path(__file__)
# Default values
DEFAULT_TITLE = "Default Title"
DEFAULT_WIDTH = "200"
DEFAULT_HEIGHT = "200"


class Args(Protocol):
    """Protocol for command-line arguments."""

    title: str
    width: str
    height: str


def main() -> None:
    """Create and display a tkinter window with customizable properties."""
    parser = argparse.ArgumentParser(description="Create a secondary window")
    parser.add_argument("title", nargs="?", default=DEFAULT_TITLE, help="Window title")
    parser.add_argument("width", nargs="?", default=DEFAULT_WIDTH, help="Window width")
    parser.add_argument(
        "height", nargs="?", default=DEFAULT_HEIGHT, help="Window height"
    )

    args = cast("Args", cast("object", parser.parse_args()))

    root = tk.Tk()
    root.title(args.title)
    root.geometry(f"{args.width}x{args.height}")
    root.mainloop()


if __name__ == "__main__":
    main()
