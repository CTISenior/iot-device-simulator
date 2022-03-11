#!/usr/bin/python3

import sys
import time
import json
import threading
import queue
import logging

from paho.mqtt import client as mqtt_client

from utils.data_generator import DataGenerator
from utils.setting import Setting
import utils.helper as Helper


class MQTT_Client:
    def __init__(self, host, sn, dataObj, protocol='mqtt',):
        
        self.host = host
        self.sn = sn
        self.dataObj = dataObj

        stg = Setting()
        self.protocol = protocol
        self.port = stg.getProtocolPort(self.protocol)
        self.topic = stg.getProtocolTopic(self.protocol)
        userData = stg.getProtocolCredentials(self.protocol)
        self.username= userData['usr']
        self.password = userData['passwd']
        #self.clientID = stg.getBrokerID()
        self.clientID = 'client_' + sn

        self.thread = None
        self.timeout = False


        logfile = Helper.get_device_log_file(self.sn)
        self.logger = Helper.create_logger(f'{self.protocol}-{self.clientID}', logfile)
        self.logger.debug(f'New device instance created: [{self.host}:{self.port} - {self.protocol}]')

    def get(self):
        print("get")
        #return self

    def set(self):
        print("set")

    def connect(self):
        def on_connect(client, userdata, flags, rc):
            if rc == 0:
                msg = f'Connected to MQTT Broker: [{self.host}:{self.port}]'
                print(f'[{self.sn}] | {msg}')
                self.logger.debug( msg )
            else:
                err = f'Failed to connect to the MQTT Broker, return code: {str(rc)}'
                self.logger.error( err )
                print(f'[{self.sn}] | {err}')
                
        client = mqtt_client.Client(self.clientID)
        client.username_pw_set(self.username, self.password)
        #client.tls_set('ca.crt',tls_version=2)
        client.on_connect = on_connect
        client.connect(self.host, self.port)
        return client

    def disconnect(self):

        try:
            self.client.disconnect()
            #self.client.loop_stop()
            self.logger.debug(f'Disconnect [{self.protocol}]')
        except:
            pass
            #self.logger.error(f'Error occured while disconnecting! [{self.protocol}]')

    def publish(self, client, msg):
        newMsg = json.loads(msg)
        interval = self.dataObj['interval']
        keyValueList = self.dataObj['keyValue']

        #data = {}
        objects = []
        for keyValue in keyValueList:
            objects.append ( DataGenerator( keyValue['key'], keyValue['initValue'], keyValue['valueType'] ))

        while not self.timeout:
            for obj in objects:
                newMsg[ obj.get_key() ] = obj.generate_data()

            result = client.publish(self.topic, json.dumps(newMsg))

            if result[0] == 0:  #[0, 1]
                self.logger.info(f'Publish {newMsg} to [{self.topic}] topic successfully')
                #print(f'Sent {newMsg} to topic {self.topic} successfully')
            else:
                self.logger.error(f'Failed to publish message to topic: {self.topic}')
            
            time.sleep(interval)

    def run(self, msg):
        self.logger.debug(f'Run [{self.protocol}]')

        self.client = self.connect()
        #self.client.loop_start()
        
        try:
            self.thread = threading.Thread(
                target = self.publish, 
                args = (self.client, msg,), 
                name = "thread-client_"+self.sn
            )
            self.thread.setDaemon(True) 
            self.thread.start()
            self.logger.debug(f'Create thread [{self.protocol}]')
        except:
            err = f'An exception occurred while publishing data: [{self.host}:{self.port}]'
            self.logger.error( err )
            print(f'{self.sn} | {err}')
            #raise Exception('')
    

    def get_client_ID(self):
        return self.clientID

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
            self.logger.debug( msg )
            print(f'{self.sn} | {msg}')
        except:
            self.logger.error(f'Thread could not be stopped! [{self.protocol}]')

    #def __call__(self):
        #print("tst-callback")
    #def __del__(self):
      #class_name = self.__class__.__name__
      #print class_name, "destroyed"
