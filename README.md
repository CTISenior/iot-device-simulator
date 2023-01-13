# IoTwin | Data Generator

[![Python](https://badgen.net/pypi/python/black)](https://www.python.org/downloads/)
[![Linux](https://svgshare.com/i/Zhy.svg)](https://www.linux.org/pages/download/)
[![CI](https://github.com/muratalkan/iotwin-data-generator/actions/workflows/main.yml/badge.svg)](https://github.com/muratalkan/iotwin-data-generator/actions/workflows/main.yml)
[![CodeQL](https://github.com/muratalkan/iotwin-data-generator/actions/workflows/codeql-analysis.yml/badge.svg)](https://github.com/muratalkan/iotwin-data-generator/actions/workflows/codeql-analysis.yml)
[![linting: pylint](https://img.shields.io/badge/linting-pylint-yellowgreen)](https://pypi.org/project/pylint/)
[![MIT license](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE.md)

> IoTwin Data Generator helps developers create virtual devices without the need to configure physical devices.

## Table of Contents
- [Installation](#installation)
- [Usage](#usage)
- [Configuration](#configuration)
- [Screenshots](#screenshots)
- [Roadmap](#roadmap)
- [License](#license)

-------

## Installation

```bash
sudo apt update -y
sudo apt install python3-dev python3-pip git libglib2.0-dev libxkbcommon-x11-0 libqt5x11extras5 -y 
git clone https://github.com/muratalkan/iotwin-data-generator.git
sudo python3 ./iotwin-data-generator/setup.py install
sudo python3 ./iotwin_data_generator/main.py
```

## Usage
* Double click > device log
* Right click > context-menu

## Configuration

#### default "config/settings.json" file

```JSON
{
    "gateway": {
        "id" : "test_id",
        "name": "Test Broker",
        "host": "127.0.0.1",
        "security": {
            "credentials": false,
            "username": "username",
            "password": "password"
        },
        "advanced_security": {
            "certificates": false,
            "ca_cert": "~/ssl/ca.pem",
            "private_key": "~/ssl/privateKey.pem",
            "cert": "~/ssl/certificate.pem"
        },
        "protocols": {
            "mqtt": {
                "name": "mqtt",
                "port": 1883,
                "topic_name": "/sensor/data",
                "method": null,
                "telemetry_keys":["serialNumber", "deviceName", "deviceType", "deviceModel"],
                "security": {
                    "credentials": false,
                    "username": "username",
                    "password": "password"
                },
                "advanced_security": {
                    "certificates": false,
                    "ca_cert": "~/ssl/cert.pem"
                }
            },
            "http": {
                "name": "http",
                "port": 5000,
                "topic_name": "/devices",
                "method": "post",
                "telemetry_keys":["serialNumber", "deviceName", "deviceType", "deviceModel"],
                "security": {
                    "credentials": false,
                    "username": "username",
                    "password": "password"
                },
                "advanced_security": {
                    "certificates": false,
                    "cert": "~/ssl/cert.pem",
                    "key": "~/ssl/key.pem"
                }
            },
            "modbus": {
                
            }
        }
    },
    "generator": {
        "default_keys": ["temp", "hum", "custom"],
        "telemetry_keys":["serialNumber", "deviceName", "deviceType", "deviceModel"],
        "value_types": {
            "RFN-1": {
                "value_list":  [-0.01, 0, 0.01],
                "format": "{0:.3f}"
            },
            "RFN-2": {
                "value_list":  [-0.05, 0, 0.05],
                "format": "{0:.3f}"
            },
            "RFN-3": {
                "value_list":  [-0.1, 0, 0.1],
                "format": "{0:.2f}"
            },
            "RFN-4": {
                "value_list":  [-0.5, 0, 0.5],
                "format": "{0:.2f}"
            },
            "RN": {
                "value_list":  [-1, 0, 1],
                "format": "{0:.0f}"
            },
            "CN": {
                "value_list":  [0],
                "format": "{0:.0f}"
            }
        }
    }
}
```

#### default "data/devices.json" file

```JSON
{
    "devices": [
 
    ]
}
```
## Screenshots
Main Window </br>
<kbd>
 ![main_window](/assets/main_window.jpg)
</kbd>

"Add New Device" Dialog </br>
<kbd>
  ![add_dialog](/assets/addnewdevice_dialog.jpg)
</kbd>

## Roadmap
- Code Revision and Optimization
- Advanced Security
- More Protocol Support
- Command Dialog
- Testing

## License
Licensed under the [MIT License](LICENSE) 2022 - [Murat Alkan](https://github.com/muratalkan)

[[Back to top]](#table-of-contents)
