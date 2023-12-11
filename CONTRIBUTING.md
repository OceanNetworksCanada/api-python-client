# Contributing

All contributions are welcome and appreciated! Credits will be given in the changelog file.

## Types of Contributions

### Report Bugs

Bugs can come from Oceans 3.0 API (backend) or the onc library. When reporting an issue, please include some descriptions (code snippet, expected behavior, actual behavior, etc.) to help us reproduce the bug.

Bugs from the backend can also be reported at [Oceans 3.0 Data Portal](https://data.oceannetworks.ca/DataPreview) from the request support form located in the top-right corner.

### Fix Bugs / Implement Features

These are issues labeled with "bug" / "enhancement". Any issue that has no assignee is open to whoever wants to implement it.

### Write Documentation

Documentations are important for users to understand the library. You are welcome to raise an issue if you find something that is outdated or can be improved.

For docstring, [numpy style](https://numpydoc.readthedocs.io/en/latest/format.html) is used.

### Commit

We use [conventional commits](https://www.conventionalcommits.org/) for commit messages. Most of the time it is as simple as adding a type before the message.

The general format is as follows:

```text
<type>[optional scope]: short description

[optional body: long description]

[optional footer]
```

Types can be _fix, feat (short for feature), refactor, style, docs, test, etc_. Some examples are:

```text
feat: allow users to cancel a running data product

test: add tests for cancelling a running data product

docs: add docstrings for discovery methods
```

Check [py-pkgs open source book](https://py-pkgs.org/07-releasing-versioning#automatic-version-bumping) for an introduction.

---

## Set up a development environment

Here is a setup for the local development.

### Creating a virtual environment

Make sure the python version meets the minimum version requirement defined in pyproject.toml. This step can be simplified if you are using [VS Code](https://code.visualstudio.com/docs/python/environments) or [PyCharm](https://www.jetbrains.com/help/pycharm/creating-virtual-environment.html#python_create_virtual_env).

```shell
# Create a virtual environment
$ python -m venv .venv

# Activate the venv
$ source .venv/bin/activate
# For Windows, use .venv\Scripts\activate

# Install onc library and dev dependencies in editable mode
$ pip install -e .[dev]
```

### Running the test

See README.md in the tests folder.

Or use tox

```shell
$ tox -e py310 # py38, py39, py311, py312. Make sure the specified python version is installed.
```

### Formatter

Code is formatted using [black](https://black.readthedocs.io/en/stable/) and [isort](https://pycqa.github.io/isort/).

```shell
$ black src tests
$ isort src tests
```

Or use tox

```shell
$ tox -e format
```

### Linter

[Ruff](https://docs.astral.sh/ruff/) is used for linting.

```shell
$ ruff check src tests
```

Or use tox

```shell
$ tox -e lint
```

Sometimes ruff can fix the error.

```shell
$ ruff check --fix src tests
```

Or use tox (check [tox positional arguments](https://tox.wiki/en/latest/config.html#substitutions-for-positional-arguments-in-commands) for more information)

```shell
$ tox -e lint -- --fix src tests
```

## Set up a development environment for documentation

WIP.

## Make a pull request

The GitHub Actions services will automatically run formatter, linter and test suite (_ci.yml_) after you make a pull request. If you are an outside contributor, a maintainer will review and approve the GitHub checks.

The actual tox environments to run are specified in the [[gh]](https://github.com/tox-dev/tox-gh#basic-example) section of _tox.ini_.

```
[gh]
python =
    3.8 = py38
    3.9 = py39
    3.10 = py310, format-check, lint
    3.11 = py311
    3.12 = py312
```

In the config above, tox will run different set of tox environments on different python versions.

- on Python 3.8 job, tox runs `py38` environment,
- on Python 3.9 job, tox runs `py39` environment,
- on Python 3.10 job, tox runs `py310`, `format-check` and `lint` environments,
- on Python 3.11 job, tox runs `py311` environment,
- on Python 3.12 job, tox runs `py312` environment.

_ci.yml_ uses a matrix strategy for operating systems, so for each python version, it will run three times for Windows, Ubuntu and Mac OS.

### Before making a pull request

It is recommended to

1. Incorporate other people's changes from main.

```shell
# Sync the main first if you are on a fork.
$ git fetch
$ git rebase origin/main
```

2. Install the minimum python version specified in _pyproject.toml_ and run `tox`. This will run environments defined in `env_list` in _tox.ini_.

```shell
$ tox
```

### After making the pull request

If you find that some GitHub checks failed, you can check the log in the Actions tab to see what went wrong.

Since a successful test run relies on both the backend and the client library, if your local `tox` run passed but GitHub Action checks failed, it's probably because some temporary issues have happened to our backend server. You can have confidence in your commit and rerun the failed jobs.
