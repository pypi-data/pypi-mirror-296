"""
Created on 2020.07.30
:author: Felix Soubelet

High level object to handle operations.
"""

import sys
from pathlib import Path

from loguru import logger

from colorframe.border import add_colorframe_to_image, process_directory_of_images
from colorframe.utils import create_output_dir


class BorderCreator:
    """Simple class to handle all functionality."""

    def __init__(
        self,
        commandline_path: str,
        left_border: int,
        right_border: int,
        top_border: int,
        bottom_border: int,
        color: str = "white",
    ):
        self.target_path = Path(commandline_path)
        self.left_border = left_border
        self.right_border = right_border
        self.top_border = top_border
        self.bottom_border = bottom_border
        self.color = color
        logger.debug("BorderCreator instantiation successful")

    def execute_target(self) -> None:
        """Executes the whiteframe addition on the target."""
        create_output_dir()

        if self.target_path.is_dir():
            process_directory_of_images(
                directory_path=self.target_path,
                borders=(
                    self.left_border,
                    self.right_border,
                    self.top_border,
                    self.bottom_border,
                ),
                color=self.color,
            )
        elif self.target_path.is_file():
            add_colorframe_to_image(
                image_path=self.target_path,
                borders=(
                    self.left_border,
                    self.right_border,
                    self.top_border,
                    self.bottom_border,
                ),
                color=self.color,
            )
        else:
            logger.error(f"Invalid path provided: '{self.target_path}'")
            sys.exit()
        logger.info("The resulting images are in the 'outputs' directory")
