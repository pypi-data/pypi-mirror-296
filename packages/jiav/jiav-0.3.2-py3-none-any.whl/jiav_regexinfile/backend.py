#!/usr/bin/env python

import os
import re

from jiav import logger
from jiav.backend import BaseBackend, Result

MOCK_STEP = {"path": "/path/to/file", "regex": r"^.*$"}
SCHEMA = {
    "type": "object",
    "required": ["path", "regex"],
    "properties": {"path": {"type": "string"}, "regex": {"type": "string"}},
    "additionalProperties": False,
}

# Subscribe to logger
jiav_logger = logger.subscribe_to_logger()


class RegexInFileBackend(BaseBackend):
    """
    RegexInFile backend object

    Checks if regex is in file

    Attributes:
        name   - Backend name
        schema - json_schema to be used to verify that the supplied step is
        valid according to the backends's requirements
        step   - Backend excution instructions
    """

    def __init__(self) -> None:
        self.name = "regexinfile"
        self.schema = SCHEMA
        self.step = MOCK_STEP
        super().__init__(name=self.name, schema=self.schema, step=self.step)

    # Override method of BaseBackend
    def execute_backend(self) -> None:
        """
        Execute backend

        Returns a namedtuple describing the jiav manifest execution
        """
        # Parse required arugments
        file = self.step["path"]
        regex = self.step["regex"]
        output = list()
        errors = list()
        successful = False
        compiled_regex = re.compile(rf"{regex}")
        if not os.path.exists(file):
            errors.append(f"File {file} does not exist")
        else:
            try:
                with open(file) as f:
                    file_content = f.read()
                    if not compiled_regex.search(file_content):
                        errors.append(
                            f"Regex '{regex}' is not present in file '{file}'"
                        )
                        jiav_logger.error(
                            f"Regex '{regex}' is not present in file '{file}'"
                        )
                    else:
                        successful = True
                        output.append(f"Regex '{regex}' found in '{file}'")
                        jiav_logger.debug(f"Regex '{regex}' found in '{file}'")
            except Exception as e:
                errors.append(f"OS exception: {str(e)}")
        self.result = Result(successful, output, errors)
