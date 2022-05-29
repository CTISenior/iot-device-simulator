# IoTwin | Data Generator

[![Python](https://badgen.net/pypi/python/black)](https://www.python.org/downloads/)
[![Linux](https://svgshare.com/i/Zhy.svg)](https://svgshare.com/i/Zhy.svg)
[![CodeQL](https://github.com/CTISenior/iot-device-simulator/actions/workflows/codeql-analysis.yml/badge.svg)](https://github.com/CTISenior/iot-device-simulator/actions/workflows/codeql-analysis.yml)
[![linting: pylint](https://img.shields.io/badge/linting-pylint-yellowgreen)](https://github.com/PyCQA/pylint)
[![MIT license](https://img.shields.io/badge/License-MIT-blue.svg)](https://lbesson.mit-license.org/)

> It was developed and designed for developers. (Tested on Ubuntu Desktop 20.04)

## Installation

```
>_ sudo apt update -y
>_ sudo apt install -y python3-dev python3-pip git libglib2.0-dev libxkbcommon-x11-0 libqt5x11extras5
>_ git clone https://github.com/CTISenior/iotwin-data-generator.git
>_ cd iotwin-data-generator
>_ sudo python3 setup.py install
>_ sudo python3 ./iotwin_data_generator/main.py
```


### default "config/settings.json" file

```
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

### default "data/devices.json" file

```
{
    "devices": [
 
    ]
}
```

# Screenshots

![Main01](/assets/main_window.png)

![Main01](/assets/add_window.png)
