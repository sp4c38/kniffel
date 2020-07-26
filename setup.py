import os
import shutil

from setuptools import setup, find_packages

with open("README.md", "r") as read_me:
    long_description = read_me.read()

def parse_requirements(filename):
    # Returns the required packages from the parsed file
    return [requirement.replace("\n", "") for requirement in open(filename) if requirement and not requirement.startswith("#")]


setup(
    name="kniffel",
    version="0.0.3",

    author="sp4c38",
    author_email="lb@alien8.de",

    description="Play Kniffel on your computer!",
    long_description = long_description,
    long_description_content_type="text/markdown",

    install_requires = parse_requirements("requirements.txt"),
    url = "https://github.com/sp4c38/kniffel",

    package_dir = {"": "src"},
    packages = find_packages(
        where="src"
    ),
    include_package_data = True,

    #scripts = ["kniffel"],


    classifiers = [
        "Development Status :: 3 - Alpha",

        "Intended Audience :: Developers",
        "Topic :: Games/Entertainment :: Arcade",

        "License :: OSI Approved :: MIT License",

        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",

    ],
)
