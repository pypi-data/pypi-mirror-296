from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(     
    name="betterprints",     
    version="0.1.1",
    python_requires=">=3.6",   
    packages=find_packages(),
    long_description=long_description,
    long_description_content_type="text/markdown",
)