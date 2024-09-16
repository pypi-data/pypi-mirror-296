from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="onepassword_utils",  # Choose a unique name
    version="0.0.1",  # Start with a version number
    author="Jisnu Kalita",
    author_email="jisnukalita@outlook.com",
    description="A collection of utility functions for interacting with 1Password",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/tuklu/Onepassword_Utils.git",  # Replace with your project's URL
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',  # Specify minimum Python version required
    install_requires=[
        'op'  # List any dependencies your package needs
    ]
)