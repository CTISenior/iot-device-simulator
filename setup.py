from setuptools import setup
from os import path

long_description = ""
with open("README.md", 'r') as f:
    long_description = f.read()

VERSION = "1.2.0"

setup(
    version=VERSION,
    name="iotwin-data-generator",
    author="IoTeam",
    author_email="",
    description="IoTwin | Data Generator",
    url="https://github.com/CTISenior/iotwin-data-generator",
    long_description=long_description,
    long_description_content_type="text/markdown",
    include_package_data=True,
    python_requires=">=3.6",
    packages=['iotwin_data_generator'],
    install_requires=[
        'python3-pyqt5',
        'numpy',
        'paho-mqtt',
        'requests'
    ],
    scripts={
        'runners': [
            'iotwin-data-generator = iotwin_data_generator.main:daemon',
        ]
    })