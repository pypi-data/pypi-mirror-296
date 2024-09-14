import setuptools
from pathlib import Path

x = Path("README.md")
setuptools.setup(
    name="Test_Pkg_pub",
    version=1.0,
    long_description=x.read_text(),
    packages=setuptools.find_packages(exclude=["tests"])
)
