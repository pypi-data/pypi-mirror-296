#!/usr/bin/env python

import json
from typing import Any, Dict, List

import yaml
from jira import Issue
from rich import box, print_json
from rich.console import Console
from rich.table import Table


def prepare_summary(issues: List[Issue] = [], format: str = "table") -> None:
    """
    Prepares a summary or verified issues

    Arguments:
        issues - Jira issues

        format - Output format
    """
    if format == "json":
        format_json("verified_issues", issues)
    elif format == "yaml":
        format_yaml("verified_issues", issues)
    else:
        format_table("Verified Issues", issues)


def construct_dict(title: str, issues: List[Issue]) -> Dict[Any, Any]:
    """
    Constructs a dictionary from received items

    Arguments:
        title - Name of the key

        issues - Jira issues that will populate the value
    """
    dictionary: dict = dict({title.lower(): list()})
    for issue in issues:
        issue_assignee = (
            issue.fields.assignee.displayName if issue.fields.assignee else "Unassigned"
        )
        dictionary[title].append(
            dict(
                {
                    "issue": issue.key,
                    "summary": issue.fields.summary,
                    "status": issue.fields.status.name,
                    "assignee": issue_assignee,
                    "reporter": issue.fields.reporter.displayName,
                    "comments": issue.fields.comment.total,  # type: ignore
                }
            )
        )
    return dictionary


def format_json(title: str, issues: List[Issue]) -> None:
    """
    Prints a JSON of issues

    Arguments:
        title  - Name of the key

        issues - List of issues
    """
    j = json.dumps(construct_dict(title, issues))
    print_json(json=j)


def format_yaml(title: str, issues: list) -> None:
    """
    Prints a YAML of issues

    Arguments:
        title  - Name of the key

        issues - List of issues
    """
    print(
        yaml.dump(
            construct_dict(title, issues),
            explicit_start=False,
            default_flow_style=False,
        )
    )


def format_table(title: str, issues: List[Issue]) -> None:
    """
    Prints a table of issues

    Arguments:
        title  - Title of the table

        issues - List of issues
    """
    table_columns: List[str] = [
        "Issue",
        "Summary",
        "Status",
        "Assignee",
        "Reporter",
        "Comments",
    ]
    table = Table(title=title, box=box.SIMPLE_HEAD, *table_columns)
    for issue in issues:
        issue_assignee = (
            issue.fields.assignee.displayName if issue.fields.assignee else "Unassigned"
        )
        table.add_row(
            str(issue),
            issue.fields.summary,
            str(issue.fields.status),
            (f"{issue_assignee} "),
            (f"{issue.fields.reporter.displayName} "),
            str(issue.fields.comment.total),  # type: ignore
        )
    Console().print(table)
