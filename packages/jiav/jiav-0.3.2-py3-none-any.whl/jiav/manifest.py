#!/usr/bin/env python

import importlib
from abc import ABC
from typing import Any, Dict, List, Type, Union

import jsonschema
import jsonschema.exceptions
import yaml
import yaml.composer
import yaml.parser
import yaml.scanner

from jiav import exceptions, logger
from jiav.backend import BaseBackend, import_backends

jiav_logger = logger.subscribe_to_logger()


class Manifest(ABC):
    """
    A jiav Manifest

    Attributes:
        manifest_text      - Manifest text fetched from comment
        successful         - Result of manifest execution
        verified_status    - Jira status to transition to
        verification_steps - Verification steps to perform
        backend_steps      - Parsed backend steps to execute
    """

    # A JSON schema for jiav manifest
    ROOT_JIAV_SCHEMA = {
        "type": "object",
        "required": ["jiav"],
        "properties": {
            "jiav": {
                "type": "object",
                "required": ["verified_status", "verification_steps"],
                "properties": {
                    "verification_steps": {"type": "array"},
                    "verified_status": {"type": "string"},
                },
            }
        },
    }
    # A JSON schema for individual steps
    STEP_SCHEMA = {
        "type": "object",
        "required": ["name", "backend"],
        "properties": {"name": {"type": "string"}, "backend": {"type": "string"}},
    }

    def __init__(self, manifest_text: str) -> None:
        self.manifest: Dict = self.validiate_text_contains_manifest(manifest_text)
        self.successful: bool = False
        self.verified_status: str = self.manifest["jiav"]["verified_status"]
        self.verification_steps: List[Dict[str, str]] = self.manifest["jiav"][
            "verification_steps"
        ]
        self.backend_steps: List[BaseBackend] = []
        self.validate_verifications_steps()

    def validiate_text_contains_manifest(self, text: str) -> Dict[Any, Any]:
        """
        Performs an initial validation of text, checks if text is a valid
        manifest
        """
        # Attempt to parse YAML from comment
        m: Dict[Any, Any] = {}
        try:
            m = yaml.safe_load(text)
        except yaml.scanner.ScannerError:
            jiav_logger.debug("Comment can not be parsed as YAML")
        except yaml.parser.ParserError:
            jiav_logger.debug("Comment can not be parsed as YAML")
        except yaml.composer.ComposerError:
            jiav_logger.debug("Comment can not be parsed as YAML")
        # Attempt to validate YAML according to schema
        try:
            jsonschema.validate(instance=m, schema=self.ROOT_JIAV_SCHEMA)
        except jsonschema.exceptions.ValidationError as e:
            raise exceptions.InvalidManifestException(e) from None
        return m

    def backend_is_valid(self, backend: str) -> bool:
        """
        Validates requested backend

        Params:
            backend - Requested backend

        Returns a boolean value if the requested backed is installed
        """
        return backend in import_backends().keys()

    def validate_verification_step(self, step: Dict[str, Any]) -> bool:
        """
        Validates a verification step

        Arguments:
            step - Verification step

        Returns True if successfully validated verification step
        """
        backend_name: str = step["backend"]
        backend_class_name: str = import_backends()[backend_name]["class"]
        backend_module = importlib.import_module(backend_class_name.split(".")[0])
        backend_module_class: str = backend_class_name.split(".")[1]
        backend_class: Type[BaseBackend] = getattr(backend_module, backend_module_class)
        # Construct initial class
        backend_instance = backend_class()  # type: ignore
        # Remove unnecessary keys for schema validation
        del step["backend"]
        del step["name"]
        backend_instance.step = step
        # Validate backend schema
        backend_instance.validate_schema()
        self.backend_steps.append(backend_instance)
        return True

    def execute_manifest(self) -> None:
        """
        Executes manifest

        Returns:
            execution_output - jiav manifest execution output
        """
        # Init variables
        execution_output: List[Union[str, List[str]]] = []
        # Iterate over steps in manifest
        for step in self.backend_steps:
            jiav_logger.debug("Executing backend '{}'".format(step.name))
            execution_output.append("Output of backend '{}':\n".format(step.name))
            try:
                step.execute_backend()
            except Exception:
                raise exceptions.BackendExecutionFailed(step.name)
            if step.result.successful:
                execution_output.append(step.result.output)
            # If one of the steps failed, immediately fail and don't continue
            else:
                # If stderr contains output, log it
                if step.result.errors:
                    execution_output.append(step.result.errors)
                else:
                    execution_output.append(step.result.output)
                break
            self.successful = True
        self.execution_output = execution_output
        if self.successful:
            jiav_logger.info("Manifest was executed successfully")
        else:
            jiav_logger.error("Manifest has failed to execute")

    def validate_verifications_steps(self) -> None:
        """
        Validates verification_steps from jiav manifest
        """
        steps = self.verification_steps
        # Iterate over steps in manifest
        for step in steps:
            step_backend = step.get("backend")
            # Attempt to validate step according to schema
            try:
                jsonschema.validate(instance=step, schema=self.STEP_SCHEMA)
            except jsonschema.exceptions.ValidationError as e:
                raise exceptions.InvalidManifestException(e)

            if not self.backend_is_valid(str(step_backend)):
                raise exceptions.InvalidBackend(str(step_backend))
            self.validate_verification_step(step)
