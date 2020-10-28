import os
from setuptools import setup, find_packages

with open("README.md", "r") as readme:
    README = readme.read()

# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

short_description = "Open source document management system (DMS)"

setup(
    name='papermerge',
    version="1.5.1",
    packages=find_packages(include=['papermerge.*']),
    include_package_data=True,
    license='Apache 2.0 License',
    description=short_description,
    long_description=README,
    long_description_content_type="text/markdown",
    url='https://papermerge.com/',
    author='Eugen Ciur',
    author_email='eugen@papermerge.com',
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.7',
)
