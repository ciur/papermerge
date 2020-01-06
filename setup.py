import os
from setuptools import setup, find_packages
from setuptools.command.egg_info import manifest_maker

with open(os.path.join(os.path.dirname(__file__), 'README.rst')) as readme:
    README = readme.read()

# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

setup(
    name='papermerge',
    version="1.0.0",
    packages=find_packages(),
    include_package_data=True,
    license='Proprietary License',  # example license
    description='Papermerge',
    long_description="Document Management System designed for scanned documents",
    url='https://www.papermerge.com/',
    author='Eugen Ciur',
    author_email='eugen@papermerge.com',
)
