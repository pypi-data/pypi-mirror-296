import setuptools
from setuptools import setup, find_packages

setup(
    name="MLscannerSPheno",
    version="1",
    author="Ahmed Hammad",
    author_email="your.email@example.com",
    description="A simple package example",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
    ],
   # package_dir = {"": "src"},
    #packages = setuptools.find_packages(where="src"),
    python_requires = ">=3.7"
)
