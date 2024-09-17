from setuptools import setup, find_packages
from typing import List

with open('README.md', 'r', encoding='utf-8') as f:
    long_description = f.read()     
   

__version__ = "0.0.8"
REPO_NAME = "DB-connector"  #github repo name
PKG_NAME= "hemant-193-database_setup"   # by this name pavkage will be visible in PyPi 
AUTHOR_USER_NAME = "hemant-193"
AUTHOR_EMAIL = "hemantb8160@gmail.com"

setup(
    name=PKG_NAME,
    version=__version__,
    author=AUTHOR_USER_NAME,
    author_email=AUTHOR_EMAIL,
    description="A python package for connecting with database.",
    long_description=long_description,
    long_description_content="text/markdown",
    url=f"https://github.com/{AUTHOR_USER_NAME}/{REPO_NAME}",
    project_urls={
        "Bug Tracker": f"https://github.com/{AUTHOR_USER_NAME}/{REPO_NAME}/issues",
    },
    package_dir={"": "src"},
    packages=find_packages(where="src"),
    install_requires=["pymongo","pymongo[srv]","dnspython","pandas","numpy","ensure","pytest"]
    )



