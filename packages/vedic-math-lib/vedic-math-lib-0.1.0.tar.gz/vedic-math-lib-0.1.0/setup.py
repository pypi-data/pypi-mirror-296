# setup.py

from setuptools import setup, find_packages

setup(
    name="vedic-math-lib",
    version="0.1.0",
    description="A Python library implementing Vedic Mathematics Sutras",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/knarsing/vedic-math-lib/tree/main/vedic-math-lib",
    author="knarsing",
    author_email="narsing.pimple@gmail.com",
    license="MIT",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
