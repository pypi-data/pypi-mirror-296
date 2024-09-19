#!/usr/bin/env python

from jsonschema.exceptions import ValidationError


class jiavException(Exception):
    """
    Base jiav exception
    """

    def __init__(self, message: str) -> None:
        self.message = message

    def __str__(self) -> str:
        return self.message


class NoJiraRestAPIEndpoint(jiavException):
    """
    Raised when the provided URL is not a valid Jira Rest API endpoint
    """

    def __init__(self, url: str) -> None:
        message = f"Provided url '{url}' does not expose a Jira Rest API endpoint"
        super().__init__(message)


class JiraMissingCredentials(jiavException):
    """
    Raised when user did not provide all required credentials
    """

    def __init__(self, missing_credentials: str) -> None:
        message = f"{missing_credentials} is required for this instance"
        super().__init__(message)


class JiraAuthenticationFailed(jiavException):
    """
    Raised when user did not authenticate correctly with Jira instance
    """

    def __init__(self, url: str) -> None:
        message = (
            f"Failed to authenticate with instance {url}, please check your credentials"
        )
        super().__init__(message)


class PermissionsError(jiavException):
    """
    Raised when failed to fetch content because of permissions
    """

    def __init__(self, issue: str) -> None:
        message = (
            f"You do not have permissions to view {issue}, "
            "please ensure you are using the correct token."
        )
        super().__init__(message)


class IssueNotExists(jiavException):
    """
    Raised when no valid issues were found
    """

    def __init__(self, issue: str) -> None:
        message = f"Issue {issue} does not exist."
        super().__init__(message)


class JQLError(jiavException):
    """
    Raised when JQL error occurs
    """

    def __init__(self, jql: str, err: str) -> None:
        message = f"{err}.\nQuery: {jql}"
        super().__init__(message)


class JQLReturnedNothing(jiavException):
    """
    Raised when JQL returns no issues
    """

    def __init__(self, jql: str) -> None:
        message = (
            "No issues returned by query, please ensure your query is valid"
            f"\nQuery: {jql}"
        )
        super().__init__(message)


class InvalidKeyInJQL(jiavException):
    """
    Raised when an invalid key in JQL
    """

    def __init__(self, jql: str, err: str) -> None:
        message = f"{err}.\nQuery: {jql}"
        super().__init__(message)


class NoIssuesFound(jiavException):
    """
    Raised when no issues were found
    """

    def __init__(self) -> None:
        message = "No issues were found"
        super().__init__(message)


class JiraUnhandledException(jiavException):
    """
    Raised when an unhandled exception is raised by
    requests.exceptions.HTTPError
    """

    def __init__(self) -> None:
        message = "Unhandled excpetion was raised, please report it"
        super().__init__(message)


class InvalidManifestException(jiavException):
    """
    Raised when an invalid manifest is supplied
    """

    def __init__(self, py_err: ValidationError) -> None:
        super().__init__(str(py_err))


class InvalidBackend(jiavException):
    """
    Raised when an unsupported backend is requested
    """

    def __init__(self, backend: str) -> None:
        message = f"'{backend}' is not a supported backend"
        super().__init__(message)


class BackendExecutionFailed(jiavException):
    """
    Raised when an unexxpected error occurs during backend execution
    """

    def __init__(self, backend: str) -> None:
        message = f"'{backend}' execution failed"
        super().__init__(message)
