#!/usr/bin/env python

from __future__ import annotations

from abc import ABC
from typing import Any, List, Union

from jira import JIRA, Issue, JIRAError
from requests.exceptions import ConnectionError

from jiav import exceptions, logger

jiav_logger = logger.subscribe_to_logger()


class JiraConnection(ABC):
    """
    Jira connection

    Attributes:
        jira - jira.JIRA object if authenticated successfully.
    """

    _instance = None

    def __new__(cls, *args: Any, **kwargs: Any) -> "JiraConnection":
        if not cls._instance:
            cls._instance = super(JiraConnection, cls).__new__(cls)
        return cls._instance

    def __init__(self, url: str, username: str, access_token: str):
        """
        Attempts to authenticate with Jira API

        Arguments:
            url           - Jira URL
            instance_type - Instance type (cloud or hosted)
            access_token  - Personal Access Token to authenticate with
        """
        # Initiall connection is used to discover details about the Jira instance
        if not hasattr(self, "jira"):
            try:
                self.jira = JIRA(server=url)
            except JIRAError as e:
                if "JiraError HTTP 404 url" in str(e):
                    raise exceptions.NoJiraRestAPIEndpoint(url) from None
                else:
                    raise exceptions.JiraUnhandledException()
            # NOTE: Failed to contact the server enitrely, perhaps should
            #       raise a unique exception for this case
            except ConnectionError:
                raise exceptions.NoJiraRestAPIEndpoint(url) from None
            instance_type = self.jira.deploymentType
            # Authenticate with a Jira cloud instance
            if instance_type == "Cloud":
                if not username:
                    raise exceptions.JiraMissingCredentials("Username") from None
                self.jira = JIRA(server=url, basic_auth=(username, access_token))
            # Authenticate with a self-hosted Jira instance
            elif instance_type == "Server":
                if username:
                    jiav_logger.warning(
                        "Username argument is omitted for self-hosted Jira instances"
                    )
                self.jira = JIRA(server=url, token_auth=access_token)
            # Check if authentication was successful
            try:
                self.jira.myself()
            except JIRAError as e:
                if "JiraError HTTP 401 url" in str(e):
                    raise exceptions.JiraAuthenticationFailed(url) from None
                else:
                    raise exceptions.JiraUnhandledException()
            jiav_logger.info(
                " ".join(
                    [
                        f"Successfully authenticated with Jira instance '{url}' of",
                        f"type '{instance_type}'",
                    ]
                )
            )

    def fetch_issues(self, issues: List[str], jql: str) -> List[Issue]:
        """
        Attempt to fetch issues from Jira
        Requires jira attribute to contain jira.JIRA
        (successful authentication using authenticate method)

        Arguments:
            issues - List of Jira issues
            jql    - Jira Query Language query

        Returns:
            remote_issues - Fetched Jira issues
        """
        remote_issues: List[Issue] = []

        # Iterate over provided issues
        if issues:
            for issue in issues:
                try:
                    remote_issue = self.jira.issue(issue)
                    remote_issues.append(remote_issue)
                except JIRAError as e:
                    if "You do not have the permission to see " in e.text:
                        jiav_logger.error(
                            f"You do not have permissions to view {issue}"
                        )
                    # NOTE: In Jira cloud instances, the returned output is
                    #       'Issue does not exist',
                    #       While self-hosted instances, the otuput is:
                    #       'Issue Does Not Exist'
                    elif "Issue does not exist".lower() in e.text.lower():
                        jiav_logger.error(f"Issue '{issue}' does not exist")
                    else:
                        raise exceptions.JiraUnhandledException()
        # Perform JQL query
        elif jql:
            try:
                remote_issues = self.jira.search_issues(jql, json_result=False)  # type: ignore # noqa: E501
            except JIRAError as e:
                if "Error in the JQL Query:" in e.text:
                    raise exceptions.JQLError(jql, e.text) from None
                elif "for field" and "is invalid" in e.text:
                    raise exceptions.InvalidKeyInJQL(jql, e.text) from None
                else:
                    raise exceptions.JiraUnhandledException()
            if not remote_issues:
                raise exceptions.JQLReturnedNothing(jql)

        if not remote_issues:
            raise exceptions.NoIssuesFound()
        else:
            jiav_logger.info(f"Discovered issues: {remote_issues}")
        return remote_issues

    def check_if_status_is_valid(
        self, issue: Issue, desired_status: str
    ) -> Union[None, str]:
        """
        Checks if desired status is a valid status for this issue

        Arguments:
            issue          - Jira issue
            desired_status - Desired status requested by jiav manifest

        Returns:
            transition_id - Workflow transition ID to use when updating
                            the status of the issue
        """
        transition_id: Union[None, str] = None
        issue_transitions = self.jira.transitions(issue)
        for status in issue_transitions:
            if desired_status == status["name"]:
                transition_id = status["id"]
        return transition_id

    def upload_attachment(self, issue: Issue, file_path: str) -> None:
        """
        Uploads an attachment to issue

        Arguments:
            issue    - Jira issue
            filename - Path of the file to add as an attachment
        """
        try:
            self.jira.add_attachment(issue=issue, attachment=file_path)
            jiav_logger.info(f"Uploaded attachment to issue '{issue}'")
        except JIRAError:
            raise exceptions.JiraUnhandledException()

    def update_issue_status(self, issue: Issue, transition_id: str) -> None:
        """
        Update issue status using transition ID discovered by
        jiav.utils.jira.JiraConnection.check_if_status_is_valid

        Arguments:
            issue         - Jira issue
            transition_id - Workflow transition ID to use when updating
                            the status of the issue
        """
        try:
            self.jira.transition_issue(issue, transition=transition_id)
            issue.update()
            jiav_logger.info(f"Updated status for '{issue}'")
        except JIRAError:
            raise exceptions.JiraUnhandledException()

    def post_comment(self, issue: Issue, comment: str) -> None:
        """
        Posts a comment with the result of verification process

        Arguments:
            issue   - Jira issue
            comment - Comment to post
        """
        try:
            self.jira.add_comment(issue, comment)
            jiav_logger.info(f"Posted a comment in '{issue}'")
        except JIRAError:
            raise exceptions.JiraUnhandledException()
