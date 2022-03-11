from setuptools import setup
from os import path

long_description = ""
with open("README.md", 'r') as f:
    long_description = f.read()

VERSION = "1.0"

setup(
    version=VERSION,
    name="iot-data-generator",
    author="IoTeam",
    author_email="",
    description="IoTwin | Data Generator",
    url="",
    long_description=long_description,
    long_description_content_type="text/markdown",
    include_package_data=True,
    python_requires=">=3.6",
    packages=['iot-data-generator'],
    install_requires=[
        'numpy',
        'PyQt5',
        'paho-mqtt',
        'requests',
    ],
    scripts=[
        'main'
    ]