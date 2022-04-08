#!/usr/bin/python3

import time
import json
import threading

from paho.mqtt import client as mqtt_client

from utils.data_generator import DataGenerator
from utils.setting import Setting
import utils.helper as Helper


class MQTT_Client:
    def __init__(self, host, sn, data_obj, protocol='mqtt'):

        self.host = host
        self.sn = sn
        self.data_obj = data_obj

        stg = Setting()
        self.protocol = protocol
        self.port = stg.get_protocol_port(self.protocol)
        self.topic = stg.get_protocol_topic(self.protocol)
        user_data = stg.get_protocol_credentials(self.protocol)
        self.username = user_data['usr']
        self.password = user_data['passwd']
        #self.client_id = stg.get_broker_id()
        self.client_id = 'client_' + sn

        self.thread = None
        self.timeout = False

        logfile = Helper.get_device_log_file(self.sn)
        self.logger = Helper.create_logger(
            f'{self.protocol}-{self.client_id}', logfile)
        self.logger.debug(
            f'New device instance created: [{self.host}:{self.port} - {self.protocol}]')

    def get(self):
        print("get")
        # return self

    def set(self):
        print("set")

    def connect(self):
        def on_connect(client, userdata, flags, rc):
            if rc == 0:
                msg = f'Connected to MQTT Broker: [{self.host}:{self.port}]'
                print(f'[{self.sn}] | {msg}')
                self.logger.debug(msg)
            else:
                err = f'Failed to connect to the MQTT Broker, return code: {str(rc)}'
                self.logger.error(err)
                print(f'[{self.sn}] | {err}')

        client = mqtt_client.Client(self.client_id)
        client.username_pw_set(self.username, self.password)
        # client.tls_set('ca.crt',tls_version=2)
        client.on_connect = on_connect
        client.connect(self.host, self.port)
        return client

    def disconnect(self):

        try:
            self.client.disconnect()
            # self.client.loop_stop()
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
                    keyvalue['valueType']))

        while not self.timeout:
            for obj in objects:
                new_msg[obj.get_key()] = obj.generate_data()

            result = client.publish(self.topic, json.dumps(new_msg))

            if result[0] == 0:  # [0, 1]
                self.logger.info(
                    f'Publish telemetry data: {new_msg} to [{self.topic}] topic successfully')
                #print(f'Sent {new_msg} to topic {self.topic} successfully')
            else:
                self.logger.error(
                    f'Failed to publish telemetry data to topic: {self.topic}')

            time.sleep(interval)

    def run(self, msg):
        self.logger.debug(f'Run [{self.protocol}]')

        self.client = self.connect()
        # self.client.loop_start()

        try:
            self.thread = threading.Thread(
                target=self.publish,
                args=(self.client, msg,),
                name="thread-client_" + self.sn
            )
            self.thread.setDaemon(True)
            self.thread.start()
            self.logger.debug(f'Create thread [{self.protocol}]')
        except BaseException:
            err = f'An exception occurred while publishing telemetry data: [{self.host}:{self.port}]'
            self.logger.error(err)
            print(f'{self.sn} | {err}')
            #raise Exception('')

    def get_client_ID(self):
        return self.client_id

    def get_thread(self):
        return self.thread

    def check_thread(self):
        return self.thread.is_alive()

    def stop_thread(self):
        self.disconnect()
        try:
            self.timeout = True
            self.thread.join()
            msg = f'Stop thread [{self.protocol}]'
            self.logger.debug(msg)
            print(f'{self.sn} | {msg}')
        except BaseException:
            self.logger.error(
                f'Thread could not be stopped! [{self.protocol}]')

    # def __call__(self):
        # print("tst-callback")
    # def __del__(self):
      #class_name = self.__class__.__name__
      # print class_name, "destroyed"
