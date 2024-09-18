import os

from setuptools import find_packages, setup

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

_commitTag = os.environ.get("CI_COMMIT_TAG")

setup(
    name="pyqrbtf",
    version=_commitTag or "0.0.0",
    author="Yorsh Siarhei",
    author_email="myrik260138@gmail.com",
    description="A project for generating a QR codes in SVG format",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://gitlab.com/Myrik/pyqrbtf",
    # packages=find_packages("src"),
    package_dir={"pyqrbtf": "pyqrbtf"},
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
    ],
    python_requires=">=3.8",
    install_requires=[
        "qrcode",
    ],
)
