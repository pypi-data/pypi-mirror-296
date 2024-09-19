#!/usr/bin/env python

from typing import List, Union

from jira import Issue
from jiav import logger
from jiav.backend import BaseBackend, Result
from jiav.jira import JiraConnection

jiav_logger = logger.subscribe_to_logger()


class JiraIssueBackend(BaseBackend):
    """
    JiraIssueBackend object

    Checks that a Jira issue is in a desired status

    Attributes:
        name   - Backend name
        schema - json_schema to be used to verify that the supplied step is
                 valid according to the backends's requirements
        step   - Backend excution instructions
    """

    MOCK_STEP = {"issue": "TEST-1", "status": "Done"}
    SCHEMA = {
        "type": "object",
        "required": ["issue", "status"],
        "properties": {"issue": {"type": "string"}, "status": {"type": "string"}},
        "additionalProperties": False,
    }

    def __init__(self) -> None:
        self.name = "jira_issue"
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
        issue: Union[Issue, str] = self.step["issue"]
        issue_status: str = self.step["status"]
        output: List = []
        errors: List = []
        successful: bool = False
        # Reusing the original JiraConnection object since the class is a singleton
        jira_connection: JiraConnection = JiraConnection()  # type: ignore
        remote_issue: Union[Issue, None] = None
        remote_issue_status: str = ""
        jiav_logger.debug(f"Issue: {issue}")
        jiav_logger.debug(f"Status: {issue_status}")
        try:
            remote_issue = jira_connection.jira.issue(id=issue)
            remote_issue_status = str(remote_issue.get_field("status"))
            if remote_issue_status != issue_status:
                jiav_logger.error(
                    " ".join(
                        [
                            f"Issue '{issue}' status '{remote_issue_status}' does",
                            f"not match the desired status '{issue_status}'",
                        ]
                    )
                )
                errors.append(
                    (
                        f"Issue '{issue}' status '{remote_issue_status}' does",
                        f"not match the desired status '{issue_status}'",
                    )
                )
            else:
                successful = True
                output.append(
                    f"Jira issue '{issue}' is in the desired status '{issue_status}'"
                )
        except Exception as e:
            jiav_logger.error(e.text)  # type: ignore # pyright: ignore # pylint: disable=E1101 # noqa: E501
            errors.append(e.text)  # type: ignore # pyright: ignore # pylint: disable=E1101 # noqa: E501
        self.result = Result(successful, output, errors)
