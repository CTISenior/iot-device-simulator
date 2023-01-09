from setuptools import setup
from os import path

long_description = ""
with open("README.md", 'r', encoding='UTF-8') as f:
    long_description = f.read()

required = []
with open('requirements.txt', encoding='UTF-8') as f:
    required = f.read().splitlines()

VERSION = "1.2.0"

setup(
    version=VERSION,
    name="iotwin-data-generator",
    author="IoTeam",
    author_email="",
    description="IoTwin | Data Generator",
    url="https://github.com/muratalkan/iotwin-data-generator",
    long_description=long_description,
    long_description_content_type="text/markdown",
    include_package_data=True,
    python_requires=">=3.6",
    packages=['iotwin_data_generator'],
    install_requires=required,
    entry_points={
        'gui_scripts': [
            'iotwin-data-generator = iotwin_data_generator.__main__:main'
        ]
    }
)
