#!/usr/bin/python3

from connectors.mqtt_client import MQTT_Client
from connectors.http_client import HTTP_Client
from utils.setting import Setting


class Client:
    def __init__(self):
        stg = Setting()
        self.host = stg.get_gateway_host()  # same host for protocols

        '''
        #Common Variables

        self.name = ""
        self.id = ""
        self.security = ""
        self.credentials = ""
        self.certicates = ""
        self.thread = None
        self.timeout = False
        self.mqtt_clients = []
        self.http_clients = []

        self.logger = logging.getLogger(f'{self.id}')
        self.logger.setLevel(logging.INFO)
        '''

    def run(self, sn, deviceObj, msg, protocol):
        device_instance = None

        if protocol == 'mqtt':
            device_instance = MQTT_Client(self.host, sn, deviceObj)
            device_instance.run(msg)
        elif protocol == "http":
            device_instance = HTTP_Client(self.host, sn, deviceObj)
            device_instance.run(msg)

        return device_instance

    def get_host(self):
        return self.host

    '''
    mqtt.Client.connected_flag=False
    for i  in range(15):
        cname="Client"+str(i)
    client= mqtt.Client(cname)
    clients.append(client)

    for client in clients:
    '''

    # common classes..
