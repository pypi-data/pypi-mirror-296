import os
from setuptools import find_packages, setup

# Read the dependencies from requirements.txt
def parse_requirements(filename):
    with open(os.path.join(os.path.dirname(__file__), filename), "r") as file:
        return [line.strip() for line in file if line.strip() and not line.startswith('#')]

setup(
    name="pySidraData",
    version="0.1.0",
    description="A Python client for interacting with IBGE API for aggregate data.",
    author="Fernando Barbosa",
    author_email="fernando.liaison@gmail.com",
    license="MIT",
    packages=find_packages(where="pySidraData"),
    package_dir={"": "pySidraData"},
    install_requires=parse_requirements("requirements.txt"),
    extras_require={
        "dev": ["pre-commit", "flake8", "black", "isort"],
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    project_urls={
        "Homepage": "https://github.com/nandevers/pySidraData",
        "Repository": "https://github.com/nandevers/pySidraData",
    },
)
