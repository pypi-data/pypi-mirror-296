#!/usr/bin/env python

import os
from typing import List

from jiav import logger
from jiav.backend import BaseBackend, Result

# Subscribe to logger
jiav_logger = logger.subscribe_to_logger()


class LineInFileBackend(BaseBackend):
    """
    LineInFile backend object

    Checks if line is in file

    Attributes:
        name   - Backend name
        schema - json_schema to be used to verify that the supplied step is
        valid according to the backends's requirements
        step   - Backend excution instructions
    """

    MOCK_STEP = {"path": "/path/to/file", "line": "line_in_file"}
    SCHEMA = {
        "type": "object",
        "required": ["path", "line"],
        "properties": {"path": {"type": "string"}, "line": {"type": "string"}},
        "additionalProperties": False,
    }

    def __init__(self) -> None:
        self.name = "lineinfile"
        self.schema = self.SCHEMA
        self.step = self.MOCK_STEP
        super().__init__(name=self.name, schema=self.schema, step=self.step)

    # Overrdie method of BaseBackend
    def execute_backend(self) -> None:
        """
        Execute backend

        Returns a namedtuple describing the jiav manifest execution
        """
        # Parse required arugments
        file: str = self.step["path"]
        line: str = self.step["line"]
        output: List[str] = []
        errors: List[str] = []
        successful = False
        jiav_logger.debug(f"File: '{file}'")
        jiav_logger.debug(f"Line: '{line}'")
        # Check if file exits
        if not os.path.exists(file):
            errors.append(f"File '{file}' does not exist")
            jiav_logger.error(f"File '{file}' does not exist")
        else:
            try:
                with open(file) as f:
                    file_content = f.read()
                    if line not in file_content:
                        errors.append(f"Line '{line}' is not present in file '{file}'")
                        jiav_logger.error(
                            f"Line '{line}' is not present in file '{file}'"
                        )
                    else:
                        successful = True
                        output.append(f"Line '{line}' found in '{file}'")
                        jiav_logger.debug(f"Line '{line}' found in '{file}'")
            except Exception as e:
                errors.append(f"OS exception: {str(e)}")
        self.result = Result(successful, output, errors)
