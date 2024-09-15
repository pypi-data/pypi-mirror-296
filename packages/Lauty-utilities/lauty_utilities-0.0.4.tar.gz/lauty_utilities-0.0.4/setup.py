from docutils.nodes import description
from setuptools import setup, find_packages
with open("README.md","r") as f:
    pdesc = f.read()


setup(
    name = 'Lauty_utilities',
    version = '0.0.4',
    author = 'LautyGameplaysYT',
    packages= find_packages(),
    long_description=pdesc,
    long_description_content_type = "text/markdown",
)