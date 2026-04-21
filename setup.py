#!/usr/bin/env python3
"""
Calculator Hub - Setup Script
Install with: pip install -e .
"""

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

with open("requirements.txt", "r", encoding="utf-8") as fh:
    requirements = [line.strip() for line in fh if line.strip() and not line.startswith("#")]

setup(
    name="calculator-hub",
    version="1.0.0",
    author="Calculator Hub Team",
    description="A comprehensive web-based calculator application with multiple calculation tools",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/calculator-hub",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
    ],
    python_requires=">=3.8",
    install_requires=requirements,
    entry_points={
        "console_scripts": [
            "calculator-hub=app.main:main",
        ],
    },
    include_package_data=True,
    package_data={
        "app": [
            "templates/*.html",
            "static/css/*.css",
            "static/js/*.js",
        ],
    },
)
