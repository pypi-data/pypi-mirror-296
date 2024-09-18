# setup.py
from setuptools import setup, find_packages

setup(
    name="databricksPackageVTR",  # Your package name
    version="0.12",
    packages=find_packages(),
    install_requires=[
        "pandas",
    ],
    author="Shashank",
    author_email="shashank.b@hoonartek.com",
    description="A package to load and display CSV data",
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
