**TESTING DOCUMENTATION**

This directory contains an automated test suite written for the Python API client using the [Robot Framework](http://robotframework.org) (RF from now on).

Directory structure is as follows:

* libraries: Python 3 library files used in the tests
* output:    Default output directory for methods that download files (i.e. orderDataProduct())
* report:    Output directory for reports produced by RF
* resources: Robot generic scripts to be reused by tests
* suites:    Test suites

Read the test suites (.robot files) in "suites" to understand what exactly is being tested.
Test suites contain the test cases in the "Test Cases" section, and are written in a language similar to english.


**TESTING REQUIREMENTS**

1. Make sure Python 3 and pip are installed properly and can be run from any directory.
2. If required, install Robot Framework:
		pip3 install robotframework
		(or use "pip" depending on your system configuration)
3. Install pabot for test parallelization:
		pip3 install -U robotframework-pabot
4. Uninstall the onc package (pip3 uninstall onc) to make sure that the code tested is the one in this directory.
	WARNING: Failing to do this might cause tests to pass on an older version and a buggy new version might end up deployed.


**RUNNING THE TESTS**

In the terminal, go to the "tests" directory and run all tests from there.
After tests finish, review the summary and logs in the "output" directory.

*To run all the test suites (parallelized):*

	Execute the "runall" bash script.

*To run a single test suite:*

	robot --outputdir report --loglevel DEBUG suites/NAME_OF_THE_TEST_SUITE.robot

*To run a single test:*

Add a placeholder tag to the test code, for example:
	[Tags] runthis
Then use --include to set the tag to run:
	robot --outputdir report --loglevel DEBUG --include runthis suites/NAME_OF_THE_TEST_SUITE.robot


**DEVELOPING TESTS**

Tests are written in "almost" plain English. This is intentional to keep tests easy to read and maintain.

If its only required to modify a test parameter value, or just duplicating an existing test,
just make the required changes, no coding knowledge is required.

For anything more advanced than that, please read the Robot Framework Documentation and consider keeping
the directory structure relevant.


**CODE DOCUMENTATION**

Robot Framework promotes test cases written almost in plain english (if you need to document it, you're writing it wrong).
Still, code documentation is welcome if ever required.


**ACKNOWLEDGEMENTS**

Initial author: dcabrera@uvic.ca
Maintainers: 