#!/usr/bin/python3

import time
import json
import threading
import ssl


import paho.mqtt.client as mqtt

from utils.data_generator import DataGenerator
from connectors.client import Client


class MQTT_Client(Client):
    def __init__(self, sn, data_obj, protocol):
        super().__init__(sn, data_obj, protocol)

    def get(self):
        print("get")
        # return self

    def set(self):
        print("set")

    def connect(self):
        def on_connect(client, userdata, flags, rc):
            if rc == 0:
                log_msg = f'Connected to MQTT Broker: [{self.host}:{self.port}]'
                print(f'[{self.sn}] | {log_msg}')
                self.logger.debug(log_msg)
            else:
                err = f'Failed to connect to the MQTT Broker, return code: {str(rc)}'
                self.logger.error(err)
                print(f'[{self.sn}] | {err}')

        client = mqtt.Client(self.client_id)
        if self.adv_security['certificates']:
            client.tls_set(self.adv_security['ca_cert'], tls_version=2)
            #client.tls_insecure_set(True)
        elif self.security['credentials']:
            client.username_pw_set(self.security['username'], self.security['password'])
        
        client.on_connect = on_connect
        client.connect(self.host, self.port)
        client.loop_start()
        return client

    def disconnect(self):
        try:
            self.client.disconnect()
            self.client.loop_stop()
            self.logger.debug(f'Disconnect [{self.protocol}]')
        except BaseException:
            pass
            #self.logger.error(f'Error occured while disconnecting! [{self.protocol}]')

    def publish(self, client, msg):
        """Publish message to gateway"""

        new_msg = json.loads(msg)
        interval = self.data_obj['interval']
        keyvalue_list = self.data_obj['keyValue']

        #data = {}
        objects = []
        for keyvalue in keyvalue_list:
            objects.append(
                DataGenerator(
                    keyvalue['key'],
                    keyvalue['initValue'],
                    keyvalue['valueType']
                )
            )

        while not self.timeout:
            for obj in objects:
                new_msg[obj.get_key()] = obj.generate_data()

            result = client.publish(self.topic, json.dumps(new_msg))

            if result[0] == 0:  # [0, 1]
                self.logger.info(f'Publish telemetry data: {new_msg} to [{self.topic}] topic successfully')
                #print(f'Sent {new_msg} to topic {self.topic} successfully')
            else:
                self.logger.error(f'Failed to publish telemetry data to topic: {self.topic}')

            time.sleep(interval)

    def run(self, msg):
        self.logger.debug(f'Run [{self.protocol}]')

        self.client = self.connect()
        # self.client.loop_start()

        log_msg = f'New client created [{self.protocol}]'
        self.logger.debug(log_msg)
        print(f'{self.sn} | {log_msg}')

        try:
            self.thread = threading.Thread(
                target=self.publish,
                args=(self.client, msg,),
                name=self.client_id
            )
            self.thread.setDaemon(True)
            self.thread.start()
            log_msg = f'Start thread [{self.protocol}]'
            self.logger.debug(log_msg)
            print(f'{self.sn} | {log_msg}')
        except BaseException:
            err = f'An exception occurred while publishing telemetry data: [{self.host}:{self.port}]'
            self.logger.error(err)
            print(f'{self.sn} | {err}')
            #raise Exception('')

    def stop_thread(self):
        self.disconnect()
        try:
            self.timeout = True
            self.thread.join()
            log_msg = f'Stop thread [{self.protocol}]'
            self.logger.debug(log_msg)
            print(f'{self.sn} | {log_msg}')
        except BaseException:
            self.logger.error(f'Thread could not be stopped! [{self.protocol}]')

    # def __call__(self):
        # print("tst-callback")
    # def __del__(self):
      #class_name = self.__class__.__name__
      # print class_name, "destroyed"
