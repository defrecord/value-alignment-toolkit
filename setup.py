#!/usr/bin/env python
"""
Setup script for Value Alignment Toolkit.
"""
from setuptools import setup, find_packages

with open("README.org", "r") as fh:
    long_description = fh.read()

setup(
    name="value_alignment_toolkit",
    version="0.1.0",
    author="Aidan Pace",
    author_email="apace@defrecord.com",
    description="Tools for implementing, analyzing, and validating AI value alignment",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/aygp-dr/value-alignment-toolkit",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
    ],
    python_requires=">=3.8",
    install_requires=[
        "numpy>=1.24.0",
        "pandas>=2.0.0",
        "scikit-learn>=1.2.0",
        "matplotlib>=3.7.0",
        "seaborn>=0.12.0",
        "transformers>=4.30.0",
        "sentence-transformers>=2.2.2",
    ],
)
