#!/usr/bin/env python

import tempfile
from datetime import datetime
from typing import IO, Any, List

from iteration_utilities import deepflatten  # type:ignore


def get_current_timestamp() -> str:
    """
    Get current timestamp

    Returns:
        current_timestamp - A formatted string of current time:
                            <month><day><year><hour><minutes><seconds>
    """
    current_timestamp = datetime.now().strftime("%m%d%Y%H%M%S")
    return current_timestamp


def write_content_to_tempfile(content: List[Any]) -> IO:
    """
    Write content to temporary file

    Arguments:
        content - Content to write

    Returns:
        temp_file - temporary file
    """
    # If we receive an output that contains a list
    # flatten it to a single list
    if isinstance(content, list):
        content = list(deepflatten(content, depth=1))
    # Create temporary file
    temp_file = tempfile.NamedTemporaryFile(
        prefix=f"jiav_{get_current_timestamp()}_", suffix=".txt", mode="w+t"
    )
    # Write content to temporary file
    temp_file.writelines(content)
    # Commit changes to file
    temp_file.seek(0)
    return temp_file
