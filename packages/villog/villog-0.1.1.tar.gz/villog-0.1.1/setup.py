'''setup'''

from pathlib import Path
from setuptools import setup, find_packages

this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()

setup(
    name = "villog",
    version = "0.1.1",
    description = "A simple python library for logging",
    author = "Krisztián Villers",
    packages = find_packages(),
    long_description = long_description,
    long_description_content_type = "text/markdown",
    install_requires=[
          'xlsxwriter'
    ]
)
