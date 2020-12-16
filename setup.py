""" setup module to install the httpy package.
"""

from os import path
from setuptools import setup, find_packages

import httpy

# Current directory
DIRNAME = path.dirname(__file__)


def readme(filename="README.md"):
    """This function is used to read the README file.
    """
    with open(path.join(DIRNAME, filename)) as _file:
        return _file.read()


def requirements():
    """Returns the libraries required for the project to operate
    """
    with open(path.join(DIRNAME, "requirements.txt")) as _file:
        return _file.read().splitlines()


def main():
    """Main function
    """
    setup(
        # The name of library
        name=httpy.__name__,
        # The code version
        version=httpy.__version__,
        # Author info
        author=httpy.__author__,
        author_email=httpy.__email__,
        # An url that points to the official page of your lib
        url=httpy.__url__,
        # Licence used
        license=httpy.__license__,
        # A short description
        description=httpy.__title__,
        # A long description will be displayed to present the lib
        long_description=readme(),
        # List the packages to insert in the distribution
        packages=find_packages(),
        # A list of strings or a comma-separated string providing
        # descriptive meta-data
        keywords="httpy, http, request, httpclient, httpserver, requests, python",
        # Libraries (packages) required for the project to operate
        install_requires=requirements(),
        classifiers=[
            "Programming Language :: Python :: 3",
            "License :: OSI Approved",
            "Natural Language :: English",
            "Operating System :: OS Independent",
        ],
        python_requires='>=3.6',
    )


if __name__ == "__main__":
    main()
