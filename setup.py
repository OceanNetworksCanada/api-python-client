import setuptools

# Modify this version before publishing a new release
buildVersion = "2.3.1"

print('setup.py has build version: ' + buildVersion + '. Make sure this is the version you want to upload.')

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="onc",
    version=buildVersion,

    # Original author, emails go to generic data team address
    author="ONC Data Team",
    author_email="data@oceannetworks.ca",
    
    # Current maintainer here, all previous maintainers to be acknowledged in README.md
    maintainer="Dany Cabrera",
    maintainer_email="dcabrera@uvic.ca",

    description="Ocean 2.0 API Python Client Library",
    license="Apache 2.0",
    keywords="ONC Ocean API",
    long_description=long_description,
    long_description_content_type="text/markdown",
	url='https://wiki.oceannetworks.ca/display/O2A/Python+Client+Library',
    
    packages=setuptools.find_packages(),
	install_requires=[
        'requests',
        'python-dateutil',
        'numpy',
        'humanize',
        'urllib3'
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
    ],
)