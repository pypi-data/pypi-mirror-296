#!/usr/bin/env python

from abc import ABC, abstractmethod
from typing import Any, Dict, List, NamedTuple

import jsonschema
import jsonschema.exceptions
from importlib_metadata import entry_points
from referencing.jsonschema import Schema

from jiav import exceptions


class Result(NamedTuple):
    successful: bool
    output: List[str]
    errors: List[str]


class BaseBackend(ABC):
    """
    jiav base backend object

    All backends should inherit from this object

    Attributes:
        name   - Backend name
        valid  - Whether backend is valid
        schema - json_schema to be used to verify that the supplied setp
                 is valid according to the backends's requirments
        step   - Instructions to perform according to backend
    """

    # SCHEMA: Dict = {}

    def __init__(self, name: str, schema: Schema, step: Dict) -> None:
        self.name = name if name else "placeholder"
        self.schema = schema
        self.step = step
        self.result: Result

    def validate_schema(self) -> bool:
        """
        Validates that the verification step is obeying the required
        schema

        Returns True if backend schema is valid
        """
        try:
            jsonschema.validate(instance=self.step, schema=self.schema)
        except jsonschema.exceptions.ValidationError as e:
            raise exceptions.InvalidManifestException(e)
        return True

    @abstractmethod
    def execute_backend(self) -> None:
        """
        Executes backend

        This function should be overridden by each individual backend

        Returns False if this method is invoked directly and not overriden
        by backend
        """
        pass


def import_backends() -> Dict[str, Dict[str, Any]]:
    """
    Imports all valid backends from jiav/api/backends directory

    All valid backends are inherited from BaseBackend object

    Returns:
        exposed_backends - List of valid backend objects based on inherited
        from BaseBackend object
    """
    discovered_backends = entry_points(group="jiav.backend")
    exposed_backends: Dict[str, Dict[str, Any]] = {}
    for backend in discovered_backends:
        exposed_backends.update(
            {backend.name: {"version": backend.dist.version, "class": backend.value}}
        )
    return exposed_backends
