"""Python setup.py for oligopipe package"""
import io
import os
from setuptools import find_packages, setup


def read(*paths, **kwargs):
    """Read the contents of a text file safely.
    >>> read("VERSION")
    '0.1.0'
    >>> read("README.md")
    ...
    """

    content = ""
    with io.open(
        os.path.join(os.path.dirname(__file__), *paths),
        encoding=kwargs.get("encoding", "utf8"),
    ) as open_file:
        content = open_file.read().strip()
    return content


def read_requirements(path):
    return [
        line.strip()
        for line in read(path).split("\n")
        if not line.startswith(('"', "#", "-", "git+"))
    ]


setup(
    name="oligopipe",
    version=read("VERSION"),
    description="Python package for Oligogenic Variant Analysis pipelines",
    url="https://oligogenic.github.io/oligopipe-docs/",
    long_description=read("README.md"),
    long_description_content_type="text/markdown",
    author="Interuniversity Institute of Bioinformatics Brussels",
    author_email="oligopipe@ibsquare.be",
    maintainer="Emma Verkinderen",
    maintainer_email="oligopipe@ibsquare.be",
    license="MIT",
    packages=find_packages(exclude=["tests", ".github"]),
    include_package_data=True,
    install_requires=read_requirements("requirements.txt"),
    entry_points={
        "console_scripts": ["oligopipe = oligopipe.__main__:main"]
    },
    classifiers=[
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "License :: OSI Approved :: MIT License",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Intended Audience :: Science/Research",
        "Topic :: Scientific/Engineering :: Bio-Informatics",
    ],
    test_suite="tests"
)
