import os
import shutil

from setuptools import setup, find_packages

with open("README.md", "r") as read_me:
    long_description = read_me.read()

def parse_requirements(filename):
    # Returns the required packages from the parsed file
    return [requirement.replace("\n", "") for requirement in open(filename) if requirement and not requirement.startswith("#")]


setup(
    name="kniffelGame", # name of distribution
    version="1.0.6", # version of distribution

    author="sp4c38", # authors name
    author_email="lb@alien8.de", # authors email

    description="Play Kniffel on your computer!", # short distribution description
    long_description = long_description, # long distribution description
    long_description_content_type="text/markdown", # content type of the long description

    install_requires = parse_requirements("requirements.txt"), # requirements parsed from requirements.txt file
    url = "https://github.com/sp4c38/kniffel", # main project url

    package_dir = {"": "src"},
    packages = find_packages(
        where="src"
    ),

    entry_points = { # Make kniffel executable through the console
        "console_scripts": ["kniffel=kniffelGame.kniffel:main"],
    },

    include_package_data = True,

    classifiers = [
        "Development Status :: 3 - Alpha",

        "Intended Audience :: Developers",
        "Topic :: Games/Entertainment :: Arcade",

        "License :: OSI Approved :: MIT License",

        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",

    ],
)
