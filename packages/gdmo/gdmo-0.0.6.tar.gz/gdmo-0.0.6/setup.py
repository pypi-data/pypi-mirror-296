from setuptools import find_packages, setup
from pathlib import Path
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()

setup(
    name='gdmo',
    packages=find_packages(include=['Forecast']),
    version='0.0.5',
    description='GDMO Library for standardized actions and routines. Current option is Forecast',
    long_description=long_description,
    long_description_content_type='text/markdown',
    author='Stephan Kuiper',
    install_requires=[
        'pandas',
        'numpy',
        'matplotlib',
        'prophet',
        'scipy',
        'pyspark',
        'delta-spark'
    ],
)