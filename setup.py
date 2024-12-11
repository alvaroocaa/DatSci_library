# setup.py

from setuptools import setup, find_packages

setup(
    name='my-python-library',
    version='0.1.0',
    description='A short description of my library',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author='Your Name',
    author_email='your.email@example.com',
    url='https://github.com/alvaroocaa/DatSci_library',
    packages=find_packages(),  # This will automatically discover all packages
    install_requires=[
        # List any dependencies here, e.g.:
        # 'numpy',
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
