# setup.py

from setuptools import setup, find_packages

setup(
    name='datsci_library',
    version='0.1',
    description='A set of functions to help me on rutinary work tasks as data specialist, this is a beta phase as it is my first ever creation of a python library. Please don't judge :)',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author='Alvaro Castillejo',
    url='https://github.com/alvaroocaa/DatSci_library',
    packages=find_packages(),  
    install_requires=[
        'numpy',
        'pandas',
        'sys',
        'os'
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
