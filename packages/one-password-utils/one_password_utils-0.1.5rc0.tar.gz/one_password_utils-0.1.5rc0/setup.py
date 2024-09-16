from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="one_password_utils",  # This is the name users will use with pip
    version="0.1.5c", 
    author="Jisnu Kalita",
    author_email="jisnukalita@outlook.com",
    description="1Password_Utility is a Python package providing utility functions for interacting with 1Password via the command-line interface (CLI). It simplifies the process of retrieving credentials from 1Password vaults within your Python scripts, making it easier to automate tasks and securely manage sensitive information.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/tuklu/1Password_Utility.git", 
    packages=find_packages(),  # Automatically find packages within your project
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6'
)