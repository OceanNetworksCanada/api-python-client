# Testing Documentation

This directory contains an automated test suite written for the Python API client using the [Robot Framework](http://robotframework.org) (RF from now on).

Directory structure is as follows:

* libraries: Python 3 library files used in the tests
* output:    Default output directory for methods that download files (i.e. orderDataProduct())
* resources: Robot generic scripts to be reused by tests
* suites:    Test suites

Read the test suites (.robot files) in "suites" to understand what exactly is being tested.
Test suites contain the test cases in the "Test Cases" section, and are written in a language similar to english.


## Testing Requirements

1. Make sure Python 3 and pip are installed properly. It is highly suggested to use a virtual environment.
2. Install [Robot Framework](https://robotframework.org/)
```commandline
pip install robotframework
```
(or use "pip3" depending on your system configuration)

3. Optional: install [pabot](https://pabot.org/) for test parallelization:
```commandline
pip install -U robotframework-pabot
```
4. Install this project in editable mode (assume the current directory is the root)
```commandline
pip install -e .
```


## Running the Tests

In the terminal, go to the "tests" directory and run all tests from there.
```commandline
cd tests
```
After tests finish, review the summary and logs in the current directory.

*To run all the test suites (parallelized):*
```commandline
pabot --testlevelsplit --variable token:${YOUR_TOKEN} suites
```

*To run a single test suite (replace 0X with the prefix of the test file name, e.g., 01):*
```commandline
robot --variable token:${YOUR_TOKEN} suites/0X*
```

*To run a single test (replace Y with the prefix of the test name, e.g., 1):*
```commandline
robot --test Y* --variable token:${YOUR_TOKEN} suites/0X*
```
Additionally, You can check the three bash files (testall, testcoverage and testsuite) for running the test suites.

## Developing Tests

Tests are written in "almost" plain English. This is intentional to keep tests easy to read and maintain.

If its only required to modify a test parameter value, or just duplicating an existing test,
just make the required changes, no coding knowledge is required.

For anything more advanced than that, please read the Robot Framework Documentation and consider keeping
the directory structure relevant.


## Code Documentation

Robot Framework promotes test cases written almost in plain english (if you need to document it, you're writing it wrong).
Still, code documentation is welcome if ever required. 
If you are an internal user of Ocean Networks Canada, please refer to the [internal documentation page](https://internal.oceannetworks.ca/display/ONCData/11+-+Automated+User+Tests+for+API+Client+Libraries).


## Acknowledgements

Initial author: dcabrera@uvic.ca

Maintainers: Kan Fu