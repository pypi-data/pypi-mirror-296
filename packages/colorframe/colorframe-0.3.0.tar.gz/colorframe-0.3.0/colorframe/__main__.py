"""
Created on 2020.07.30
:author: Felix Soubelet

High level object to handle operations.
"""

import sys

import typer
from loguru import logger

from colorframe.api import BorderCreator
from colorframe.utils import set_logger_level

app = typer.Typer()


@app.command()
def create(
    path: str = typer.Argument(
        None,
        help="Location, relative or absolute, to the file or directory of files to add a "
        "colored border to.",
    ),
    left: int = typer.Option(0, help="Width of the frame to add on the left image edge."),
    right: int = typer.Option(0, help="Width of the frame to add on the right image edge."),
    top: int = typer.Option(0, help="Height of the frame to add on the top image edge."),
    bottom: int = typer.Option(0, help="Height of the frame to add on the bottom image edge."),
    color: str = typer.Option(
        "white",
        help="The desired color of the added border. Should be a keyword recognized by Pillow.",
    ),
    log_level: str = typer.Option(
        "info",
        help="The base console logging level. Can be 'debug', 'info', 'warning' and 'error'.",
    ),
) -> None:
    """Add colored borders on pictures, easily."""
    set_logger_level(log_level)

    if all(side == 0 for side in (left, right, top, bottom)):
        logger.error("Provide at least one side to add a border to.")
        sys.exit(1)

    border_api = BorderCreator(path, left, top, right, bottom, color)
    border_api.execute_target()


if __name__ == "__main__":
    app()
