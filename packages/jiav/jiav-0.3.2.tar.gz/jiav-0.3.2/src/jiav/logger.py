#!/usr/bin/env python

import logging
from logging import Logger

from rich.console import Console
from rich.logging import RichHandler


def subscribe_to_logger() -> Logger:
    """
    Subscribes module to general logger

    Returns:
        logger - Logger object for that module
    """
    logger = logging.getLogger(__name__)
    return logger


def configure_logger(debug: bool = False) -> Logger:
    """
    Initializes a logger handler to log events

    Arguments:
        debug - Enable debug mode during invocation

    Returns:
        logger - Logger handler
    """
    logging.basicConfig(
        level=logging.INFO,
        format="%(message)s",
        datefmt="[%X]",
        handlers=[
            RichHandler(
                omit_repeated_times=False,
                console=Console(stderr=True),
            )
        ],
    )
    logger = subscribe_to_logger()
    if debug:
        logger.setLevel(logging.DEBUG)
    return logger
