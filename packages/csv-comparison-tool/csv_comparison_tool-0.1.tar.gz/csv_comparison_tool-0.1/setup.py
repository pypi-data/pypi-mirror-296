# setup.py
from setuptools import setup, find_packages

setup(
    name='csv_comparison_tool',  # Name of your package
    version='0.1',
    packages=find_packages(),  # Automatically discover all packages in the directory
    install_requires=[
        'pandas',  # This package needs pandas installed
    ],
    entry_points={
        'console_scripts': [
            'csvcompare=csv_comparison_tool.compare:main',  # Command-line entry point
        ],
    },
    description='A simple tool to compare CSV/XLSX files using pandas and tkinter.',
    author='Dee Cuaresma',
    author_email='dustin.cuaresma@lattice.com',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
)