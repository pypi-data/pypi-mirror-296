# jiav

> [!NOTE]
> This repository is a **Proof of Concept.**

> [!WARNING]
> Since this tool executes commands locally, we should avoid trusting public comments as much as possible.
>
> It will default to scanning only private comments (regardless of the visibility group). It is possible to read from public comments **if you understand the potential risk, this might cause to your systems**.
>
> The output of verification steps is also not uploaded as attachments by default because it is impossible to limit attachments' visibility, refer to [JRASERVER-3893](https://jira.atlassian.com/browse/JRASERVER-3893). It is possible to attach the output **if you understand the potential risk, this might expose sensitive information**.

<https://github.com/user-attachments/assets/1a9d5728-96e3-436a-9e0d-b31f74d5298b>

**J**ira **I**ssues **A**uto **V**erification.

`jiav` is a [Python](https://www.python.org) based auto verification
tool for [Jira](https://www.atlassian.com/software/jira).

The primary goal is to provide a robust auto-verification
workflow while focusing on ease of use and simplicity.
Users provide a YAML-formatted comment in Jira issues, and the tool will execute it.  
On successful execution, the issue will move to the desired status.

Both self-hosted and cloud Jira instances are supported.

## Backends

`jiav` allows developers to build custom backends; refer to the [development guide](docs/source/developing_backends.rst).

Built-in backends:

- `lineinfile` - looks for a line in file.
- `regexinfile` - looks for a regex in file.
- `jira_issue` - queries a Jira issue's status.

An example of a backends shipped externally:

- [`ansible`](https://github.com/vkhitrin/jiav-backend-ansible) - runs [Ansible](https://www.ansible.com) playbooks.  
  **This is a risky backend since it allows users to run arbitrary code. Be cautious when enabling it!**
- [`command`](https://github.com/vkhitrin/jiav-backend-command) - runs shell commands.  
  **This is a risky backend since it allows users to run arbitrary code. Be cautious when enabling it!**

## Requirements

`jiav` requires Python `>= 3.8`.

Self-hosted Jira instances require "Personal Access Tokens" (PAT) which are available starting from
[`>=8.14`](https://confluence.atlassian.com/enterprise/using-personal-access-tokens-1026032365.html).

Cloud Jira instances require a username + API tokens.

## Documentation

Visit <https://jiav.readthedocs.io>.

## Installation

### Remote

Install from remote using `pip3`:

```bash
pip3 install jiav
```

Install from remote using `pipx`:

```bash
pipx install jiav
```

### Local

Clone the local repository:

```bash
git clone https://github.com/vkhitrin/jiav.git
cd jiav
```

Install using `pip3`:

```bash
pip3 install .
```

Install using `pipx`:

```bash
pipx install .
```

## Usage

Please refer to the user guide:
<https://jiav.readthedocs.io/en/latest/user_guide.html>

If you do not have access to a Jira instance or wish to attempt this tool in an isolated environment, refer to
a ["Getting Started"](docs/source/getting_started.rst) on setting up a demo environment.

## Contributing

**All contributions are welcome!**

To install in development mode, use `poetry`:

```bash
poetry install --with=main,dev,types
```

If proposing new pull requests, please ensure that new/existing tests are passing:

```bash
pytest
```
