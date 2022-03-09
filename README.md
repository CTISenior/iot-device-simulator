# Iotwin | IoT Data Generator

[![CodeQL](https://github.com/CTISenior/iot-device-simulator/actions/workflows/codeql-analysis.yml/badge.svg)](https://github.com/CTISenior/iot-device-simulator/actions/workflows/codeql-analysis.yml)

> It is developed and designed for developers. (Tested on Ubuntu 20.04)

**Requirements** = [ 'python3', 'pip3', 'numpy', 'PyQt5', 'paho-mqtt', 'requests' ]

### default "conf/settings.json" file

```
{
    "gateway": {
        "name": "Test Broker",
        "client_id" : "test_id",
        "host": "127.0.0.1",
        "default_keys": ["temp", "hum", "custom"],
        "security": {
            "isSecure": false,
            "username": "",
            "password": ""
        },
        "ssl": {
            "certificates": false,
            "caCert": "",
            "cert": ""
        },
        "protocols": {
            "mqtt": {
                "name": "mqtt",
                "port": 1883,
                "topic_name": "/sensor/data",
                "method": null,
                "security": {
                    "isSecure": false,
                    "username": "",
                    "password": ""
                },
                "ssl": {
                    "certificates": false,
                    "caCert": "",
                    "cert": ""
                }
            },
            "http": {
                "name": "http",
                "port": 5000,
                "topic_name": "/device",
                "method": "post",
                "security": {
                    "isSecure": false,
                    "username": "",
                    "password": ""
                },
                "ssl": {
                    "certificates": false,
                    "caCert": "",
                    "cert": ""
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