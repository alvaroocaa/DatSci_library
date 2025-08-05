from setuptools import setup, find_packages
import os

# Get the long description from the root-level README
this_dir = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(this_dir, "README.md"), encoding="utf-8") as f:
    long_description = f.read()

setup(
    name='datsci',
    version='2.7.1',
    description="A set of functions to help me on rutinary work tasks as data specialist, this is a beta phase as it is my first ever creation of a python library. Please don't judge :)",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author='Alvaro Castillejo',
    url='https://github.com/alvaroocaa/DatSci_library',
    packages=find_packages(),
    include_package_data=True,  
    package_data={
        'datsci': ['README.md'],   
    },
    install_requires=[
        'numpy',
        'pandas',
        'openpyxl',
        'xlsxwriter',
        'chardet'
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
