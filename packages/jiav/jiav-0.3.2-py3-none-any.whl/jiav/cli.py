#!/usr/bin/env python

import importlib.metadata
from logging import Logger
from typing import Any, List, Tuple

import rich_click as click
from jira import Issue

from jiav import exceptions, logger, summary, verification
from jiav.backend import import_backends
from jiav.jira import JiraConnection
from jiav.manifest import Manifest

click.rich_click.COLOR_SYSTEM = "truecolor"
click.rich_click.SHOW_METAVARS_COLUMN = False
click.rich_click.APPEND_METAVARS_HELP = True
click.rich_click.OPTION_GROUPS = {
    "jiav verify": [
        {
            "name": "Main options",
            "options": ["--jira", "--access-token", "--username"],
        },
        {
            "name": "Issue options",
            "options": ["--issue", "--query"],
        },
        {
            "name": "Dangerous options",
            "options": ["--upload-attachment", "--allow-public-comments"],
        },
    ]
}

jiav_logger: Logger = logger.configure_logger()


class MutuallyExclusiveOption(click.Option):
    def __init__(self, *args: Any, **kwargs: Any):
        self.mutually_exclusive = set(kwargs.pop("mutually_exclusive", []))
        help = kwargs.get("help", "")
        if self.mutually_exclusive:
            opt = ", ".join(self.mutually_exclusive)
            kwargs["help"] = help + (
                " NOTE: This argument is mutually exclusive with"
                " arguments: [" + opt + "]."
            )
        super(MutuallyExclusiveOption, self).__init__(*args, **kwargs)

    def handle_parse_result(
        self, ctx: click.Context, opts: Any, args: Any
    ) -> Tuple[Any, Any]:
        if self.mutually_exclusive.intersection(opts) and self.name in opts:
            raise click.UsageError(
                "Illegal usage: `{}` is mutually exclusive with "
                "arguments `{}`.".format(self.name, ", ".join(self.mutually_exclusive))
            )

        return super(MutuallyExclusiveOption, self).handle_parse_result(ctx, opts, args)


def _version_option() -> str:
    """
    Build the string printed by jiav --version
    """
    jiav_version = importlib.metadata.version("jiav")
    backend_output = "\n".join(
        [
            f"  - {name}, version {version}"
            for name, version in import_backends().items()
        ]
    )

    output = (
        f"jiav, version {jiav_version}\n\n" "Installed Backends:\n" f"{backend_output}"
    )

    return output


@click.group(context_settings={"auto_envvar_prefix": "JIAV"})
@click.version_option(package_name="jiav", message=_version_option())
def jiav() -> None:
    pass


@click.command()
@click.option(
    "-f",
    "--from-file",
    type=click.File("r"),
    help="Path to local file to validate.",
    required=True,
)
def validate_manifest(from_file: click.File) -> None:
    """Validate manifest locally."""
    content = from_file.read()  # type: ignore
    jiav_logger.info(f"File content:\n{content}")
    try:
        Manifest(manifest_text=content)
        jiav_logger.info("Provided YAML is valid")
    except Exception as e:
        jiav_logger.error(e)
        jiav_logger.error("Provided manifest is not valid")
        raise SystemExit(5)


@click.command()
@click.option("-j", "--jira", type=str, help="Jira URL.", required=True)
@click.option(
    "-a",
    "--access-token",
    type=str,
    help=(
        " ".join(
            [
                "Personal Access Token (PAT) for self-hosted instances or ",
                "an API token for cloud instances.",
            ]
        )
    ),
    required=True,
)
@click.option(
    "-u",
    "--username",
    type=str,
    help="Cloud Jira username NOTE: Not required for self-hosted instances.",
)
@click.option(
    "-i",
    "--issue",
    help="Issue to verify.",
    multiple=True,
    type=str,
    cls=MutuallyExclusiveOption,
    mutually_exclusive=["query"],
)
@click.option(
    "-q",
    "--query",
    help="JQL query.",
    cls=MutuallyExclusiveOption,
    mutually_exclusive=["issue"],
)
@click.option(
    "--upload-attachment",
    help=(
        " ".join(
            [
                "Uploads attachment of execution, this is not safe since all",
                "users who can access the ticket will be able to view it;",
                "refer to https://jira.atlassian.com/browse/JRASERVER-3893",
            ]
        )
    ),
    flag_value=True,
)
@click.option(
    "--allow-public-comments",
    help=(
        " ".join(
            [
                "Allows to read manifest from non-private comments; this is",
                "potentially dangerous since unexpected users will be able to",
                "provide a manifest.",
            ]
        )
    ),
    flag_value=True,
)
@click.option(
    "--no-comment-on-failure",
    help="Do not post a comment on failed manifest execution.",
    flag_value=True,
)
@click.option(
    "--dry-run",
    help="Execute manifest without updating issues.",
    flag_value=True,
)
@click.option(
    "--debug",
    help="Enable debug logging.",
    flag_value=True,
)
@click.option(
    "--format",
    type=click.Choice(["table", "json", "yaml"], case_sensitive=False),
    help="Output format.",
)
def verify(
    jira: str,
    access_token: str,
    username: str,
    issue: List[str],
    query: str,
    upload_attachment: bool,
    allow_public_comments: bool,
    no_comment_on_failure: bool,
    dry_run: bool,
    debug: bool,
    format: str,
) -> None:
    """Verifies issues in Jira."""
    issues: List[Issue] = []
    verifeid_issues: List[Issue] = []
    jiav_logger: Logger = logger.configure_logger(debug)
    # If user requested to upload attachment, warn them
    if upload_attachment:
        jiav_logger.warn(
            "".join(
                [
                    "Will upload attachment of the execution, this might leak ",
                    "sensetive information, "
                    "refer to: https://jira.atlassian.com/browse/JRASERVER-3893",
                ]
            )
        )
    # If user requested to include public comments, warn them
    if allow_public_comments:
        jiav_logger.warn("Will include public comments in search!")
    if no_comment_on_failure:
        jiav_logger.warn("Comment will not be posted of failed manifest execution")
    if dry_run:
        jiav_logger.info("Will not update issues, running as a dry run")
    try:
        jira_connection: JiraConnection = JiraConnection(
            url=jira,
            username=username,
            access_token=access_token,
        )
    except exceptions.NoJiraRestAPIEndpoint as e:
        jiav_logger.exception(e)
        jiav_logger.critical("Provided URL does not contain a valid JIRA endpoint")
        raise SystemExit(1)
    except exceptions.JiraUnhandledException as e:
        jiav_logger.exception(e)
        jiav_logger.critical(
            "An unhandled exception occurred while trying to connect to Jira"
        )
        raise SystemExit(1)
    except exceptions.JiraAuthenticationFailed as e:
        jiav_logger.exception(e)
        jiav_logger.critical(
            " ".join(
                [
                    "Authentication with the Jira insatance failed,",
                    "please check your credentials",
                ]
            )
        )
        raise SystemExit(2)
    except exceptions.JiraMissingCredentials as e:
        jiav_logger.exception(e)
        jiav_logger.critical(
            "Missing username, please provide a username to a Jira cloud instance"
        )
        raise SystemExit(2)
    # Fetch issues from authenticated Jira instance
    try:
        issues = jira_connection.fetch_issues(issues=issue, jql=query)
    except exceptions.JiraMissingCredentials:
        pass
    except exceptions.JiraUnhandledException as e:
        jiav_logger.exception(e)
        jiav_logger.critical(
            "An unhandled exception occurred while trying to fetch issues"
        )
        raise SystemExit(2)
    except exceptions.InvalidKeyInJQL:
        jiav_logger.critical("Invalid key in JQL")
        raise SystemExit(3)
    except exceptions.JQLReturnedNothing as e:
        jiav_logger.exception(e)
        jiav_logger.critical("Query returned no issues")
        raise SystemExit(3)
    except exceptions.JQLError as e:
        jiav_logger.exception(e)
        jiav_logger.critical("Query returned an error")
        raise SystemExit(3)
    except exceptions.NoIssuesFound:
        jiav_logger.critical("No issues found")
        raise SystemExit(4)
    # Iterate over valid issues and attempt to update and verify them
    verifeid_issues = verification.verify_issues(
        issues=issues,
        jira_connection=jira_connection,
        upload_attachment=upload_attachment,
        allow_public_comments=allow_public_comments,
        no_comment_on_failure=no_comment_on_failure,
        dry_run=dry_run,
    )
    # Print summary if issues were verified
    if verifeid_issues:
        summary.prepare_summary(issues=verifeid_issues, format=format)
    else:
        jiav_logger.info("No issues were verified")
        raise SystemExit(6)


jiav.add_command(validate_manifest)
jiav.add_command(verify)

if __name__ == "__main__":
    jiav()
