#!/usr/bin/python

from connectors.mqtt_client import MQTT_Client
from connectors.http_client import HTTP_Client
from utils.setting import Setting

class Client:
    def __init__(self):
        stg = Setting()
        self.host = stg.getGatewayHost()
        
    def run(self, sn, deviceObj, msg, protocol):
        device_instance = None

        if protocol=='mqtt':
            device_instance = MQTT_Client(sn, deviceObj)
            device_instance.run(msg)
        elif protocol=="http":
            device_instance = HTTP_Client(sn, deviceObj)
            device_instance.run(msg)

        return device_instance

    def getHost(self):
        return self.host
