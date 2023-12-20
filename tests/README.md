# Testing Documentation

This directory contains an automated test suite written for the Python API client using
the [Robot Framework](http://robotframework.org) (RF from now on) as well as pytest.

Directory structure is as follows:

- libraries: Python 3 library files used in the tests
- output: Default output directory for methods that download files (i.e. orderDataProduct())
- pytests: Tests converted from RF to pytest format
- resources: Robot generic scripts to be reused by tests
- suites: Test suites

Read the test suites (.robot files) in "suites" to understand what exactly is being tested.
Test suites contain the test cases in the "Test Cases" section, and are written in a language similar to english.

## Testing Requirements

1. Make sure Python 3 and pip are installed properly. It is highly suggested to use a virtual environment.
2. Install [Robot Framework](https://robotframework.org/) and [python-dotenv](https://saurabh-kumar.com/python-dotenv/)

```shell
pip install robotframework python-dotenv
```

(or use "pip3" depending on your system configuration)

3. Optional: install [pabot](https://pabot.org/) for test parallelization:

```shell
pip install -U robotframework-pabot
```

4. Install this project in editable mode (assume the current directory is the root)

```shell
pip install -e .
```

## Running the Tests

In the terminal, run all tests from the root directory.
Tests can also be run from a different folder. Just change the relative path of the test suites.

Create a `.env` file under tests folder and put TOKEN variable in the file.
If you are on Windows, make sure the encoding of `.env` file is UTF-8 after using the command below.

```shell
echo TOKEN=${YOUR_TOKEN} > .env
```

The default testing environment is PROD. If you are an internal developer, add the following line to .env so that the tests are running against QA.

```shell
echo ONC_ENV=QA >> .env
```

Change ONC_ENV value from QA to PROD if testing in PROD is needed. Removing the line also does the trick.

_To run all the RF test suites (parallelized):_

```shell
pabot --testlevelsplit tests/robot/suites
```

_To run a single RF test suite (replace 0X with the prefix of the test file name, e.g., 01):_

```shell
robot tests/suites/01*    # robot tests/suites/0X*
```

_To run a single RF test in a test suite (replace Y with the prefix of the test name, e.g., 01):_

```shell
robot --test "01*" tests/suites/01*  # robot --test "Y*" tests/suites/0X*
```

_To run pytest_

```shell
pytest
```

_`--variable TOKEN:${YOUR_TOKEN}` can be used if no `.env` file is present_

```shell
robot --variable TOKEN:${YOUR_TOKEN} tests/suites/01*
```

Additionally, You can check the three bash files (testall, testcoverage and testsuite) for running the test suites.
Robot Framework also has plugins for IDEs like VS Code and Pycharm that makes running tests easier.

After tests finish, review the summary and logs in the root directory.

## Developing Tests

Tests are written in "almost" plain English. This is intentional to keep tests easy to read and maintain.

If it's only required to modify a test parameter value, or just duplicating an existing test,
just make the required changes, no coding knowledge is required.

For anything more advanced than that, please read the Robot Framework Documentation and consider keeping
the directory structure relevant.

## Code Documentation

Robot Framework promotes test cases written almost in plain english (if you need to document it, you're writing it wrong).
Still, code documentation is welcome if ever required.
If you are an internal user of Ocean Networks Canada, please refer to the [internal documentation page](https://internal.oceannetworks.ca/display/ONCData/11+-+Automated+User+Tests+for+API+Client+Libraries).

## Acknowledgements

Initial author: Dany Cabrera

Maintainers: Kan Fu

Previous maintainers: Dany Cabrera
