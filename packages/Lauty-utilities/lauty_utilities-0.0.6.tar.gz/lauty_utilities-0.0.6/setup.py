from docutils.nodes import description
from setuptools import setup, find_packages
with open("README.md","r") as f:
    pdesc = f.read()


setup(
    name = 'Lauty_utilities',
    version = '0.0.6',
    author = 'LautyGameplaysYT',
    packages= find_packages(),
    long_description=pdesc,
    long_description_content_type = "text/markdown",
)
#just some notes to myself, ignore the following 2 lines
# build command: python setup.py sdist bdist_wheel
# upload command: twine upload dist/*