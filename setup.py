import setuptools
from setuptools import setup

setup(
    name="easy-upbit",
    version="0.1.0",
    description="Upbit Rest Ap & Socket Client",
    packages=setuptools.find_packages(),
    install_requires=[
        "attrs>=19.3.0",
        "pytz>=2020.1",
        "requests>=2.25.1",
        "requests-toolbelt>=0.9.1",
    ],
)
