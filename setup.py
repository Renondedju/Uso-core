import os
from setuptools import setup, find_packages

# Utility function to read the README file.
# Used for the long_description.  It's nice, because now 1) we have a top level
# README file and 2) it's easier to type in the README file than to put a raw
# string in below ...
def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
    name     = "uso-core",
    version  = "0.1.0-dev",
    author   = "Renondedju",
    description = ("The main logic of Uso!bot"),
    license = "MIT",
    url = "https://github.com/Renondedju/Uso-core",
    packages=find_packages(),
    long_description=read('README.md'),
    classifiers=[
        "Development Status :: 1 - Planning",
        "Programming Language :: Python :: 3.6",
    ],
)