#!/usr/bin/env python3
"""
Setup script for OpenClaw Scrapling Integration
"""

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="openclaw-scrapling",
    version="0.1.0",
    author="OpenClaw Team",
    author_email="",
    description="AI-powered web scraping integration for OpenClaw",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/openclaw/openclaw",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "License :: OSI Approved :: BSD License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
    ],
    python_requires=">=3.8",
    install_requires=[
        "scrapling[ai]>=0.4",
        "httpx>=0.24.0",
        "orjson>=3.9.0",
        "lxml>=6.0.0",
        "cssselect>=1.2.0",
        "beautifulsoup4>=4.12.0",
        "playwright>=1.40.0",
    ],
    extras_require={
        "dev": [
            "pytest>=7.0.0",
            "pytest-asyncio>=0.21.0",
            "black>=23.0.0",
            "mypy>=1.0.0",
        ],
        "cli": [
            "click>=8.0.0",
            "rich>=13.0.0",
        ],
    },
    entry_points={
        "console_scripts": [
            "scrapling-cli=scrapling_cli:main",
            "openclaw-scrape=scrapling_cli:main",
        ],
    },
    include_package_data=True,
    package_data={
        "openclaw_scrapling": [
            "examples/*.py",
            "config/*.json",
            "templates/*.json",
        ],
    },
)