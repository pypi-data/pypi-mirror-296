# setup.py
from setuptools import setup, find_packages

setup(
    name="databricksPackageVT",  # Your package name
    version="0.7",
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
