# setup.py
from setuptools import setup, find_packages
from pathlib import Path

# Read the contents of your README file
this_directory = Path(__file__).parent
long_description = (this_directory / "README.rst").read_text()

setup(
    name='kpol',
    version='0.1',
    packages=find_packages(),
    description='Alacarte of python libraries for engineering research.',
    author='Dr. Polachan',
    author_email='kurian.polachan@iiitb.ac.in',
    url='https://sites.google.com/view/cdwl/professor',
    long_description=long_description,
    long_description_content_type='text/x-rst',
)
