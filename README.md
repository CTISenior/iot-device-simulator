# IoTwin | Data Generator

[![Python](https://badgen.net/pypi/python/black)](https://www.python.org/downloads/)
[![Linux](https://svgshare.com/i/Zhy.svg)](https://svgshare.com/i/Zhy.svg)
[![CodeQL](https://github.com/CTISenior/iot-device-simulator/actions/workflows/codeql-analysis.yml/badge.svg)](https://github.com/CTISenior/iot-device-simulator/actions/workflows/codeql-analysis.yml)

> It is developed and designed for developers. (Tested on Ubuntu 20.04)

## Installation

```
>_ sudo apt install -y python3-dev python3-pip git libglib2.0-dev
>_ git clone https://github.com/CTISenior/iotwin-data-generator.git
>_ cd iotwin-data-generator
>_ python3 setup.py install
>_ python3 ./iotwin_data_generator/main.py
```


### default "config/settings.json" file

```
{
    "gateway": {
        "name": "Test Broker",
        "client_id" : "test_id",
        "host": "127.0.0.1",
        "default_keys": ["temp", "hum", "custom"],
        "security": {
            "isSecure": false,
            "username": "username",
            "password": "password"
        },
        "ssl": {
            "certificates": false,
            "cert": "~/ssl/cert.pem",
            "key": "~/ssl/key.pem"
        },
        "protocols": {
            "mqtt": {
                "name": "mqtt",
                "port": 1883,
                "topic_name": "/sensor/data",
                "method": null,
                "security": {
                    "isSecure": false,
                    "username": "username",
                    "password": "password"
                },
                "ssl": {
                    "certificates": false,
                    "cert": "~/ssl/cert.pem",
                    "key": "~/ssl/key.pem"
                }
            },
            "http": {
                "name": "http",
                "port": 5000,
                "topic_name": "/device",
                "method": "post",
                "security": {
                    "isSecure": false,
                    "username": "username",
                    "password": "password"
                },
                "ssl": {
                    "certificates": false,
                    "cert": "~/ssl/cert.pem",
                    "key": "~/ssl/key.pem"
                }
            },
            "": {

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