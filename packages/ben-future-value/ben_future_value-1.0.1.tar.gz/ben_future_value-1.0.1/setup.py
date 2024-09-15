import setuptools

import pathlib

PROJECT_NAME = "ben_future_value"
VERSION = "1.0.1"
SHORT_DESCRIPTION = "A package to assist in calculating future value"
SOURCE_CODE_LINK= "https://github.com/Ben-Payton/ben_future_value"
DOCUMENTATION_LINK = "https://github.com/Ben-Payton/ben_future_value/blob/main/README.md" 
REQUIRED_DEPENDANCIES = ["matplotlib","seaborn"]


setuptools.setup(
    name = PROJECT_NAME,
    version = VERSION,
    description= SHORT_DESCRIPTION,
    long_description= pathlib.Path("README.md").read_text(),
    long_description_content_type="text/markdown",
    author = "Ben Payton",
    project_urls = {
        "Documentation" : DOCUMENTATION_LINK,
        "Source" : SOURCE_CODE_LINK
    },
    install_requires = REQUIRED_DEPENDANCIES,
    packages=setuptools.find_packages()
    )
