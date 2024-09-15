"""
Setup script for packaging and distribution of the 'colorty' library.
"""

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="colorty",
    version="0.1.6",
    packages=find_packages(exclude=["tests*"]),  # Exclude test packages
    install_requires=[],
    author="Vivek",
    author_email="xsvk@gmx.com",
    description="A simple library for handling colored text in terminal environments.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/dynstat/colorty",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
    include_package_data=True,  # Include non-Python files specified in MANIFEST.in
    entry_points={
        "console_scripts": [
            "colorty=colorty.cli:main",  # If you have a CLI, add this line
        ],
    },
)
