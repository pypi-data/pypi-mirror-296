from setuptools import find_packages, setup
from pathlib import Path
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()

setup(
    name='GDMO',
    packages=find_packages(),
    version='0.1.1',
    description='GDMO Library for standardized actions and routines. Current options / functions are Forecast.Forecast, API.APIRequest, Tables.Landing, and Tables.Delta',
    long_description=long_description,
    long_description_content_type='text/markdown',
    author='Stephan Kuiper',
    install_requires=['prophet','matplotlib','statsmodels'],
)