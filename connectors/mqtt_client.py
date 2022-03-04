#!/usr/bin/python

import time
import json
import threading
import logging

from paho.mqtt import client as mqtt_client

from utils.simulator import Simulator
from utils.setting import Setting
import utils.helper as Helper



class MQTT_Client:
    def __init__(self, sn, dataObj, protocol='mqtt',):
        
        stg = Setting()
        self.host = stg.getGatewayHost()
        self.protocol = protocol
        self.port = stg.getProtocolPort(self.protocol)
        self.topic = stg.getProtocolTopic(self.protocol)
        userData = stg.getProtocolCredentials(self.protocol)
        self.username= userData['usr']
        self.password = userData['passwd']
        #self.clientID = stg.getBrokerID()
        self.clientID = 'client_' + sn

        self.sn = sn
        self.dataObj = dataObj
        self.thread = None
        self.timeout = False
        
        #logging.basicConfig(filename="logs/"+self.clientID, level=logging.DEBUG)
        logging.debug(f'New device instance created: {self.host}:{self.port} | {self.protocol} | {self.clientID}')

    def get(self):
        print("get")

    def set(self):
        print("set")

    def connect_mqtt(self):
        def on_connect(client, userdata, flags, rc):
            if rc == 0:            
                logging.debug(f'Connected to MQTT Broker {self.host}:{self.port} {self.clientID}')
                print(f'Connected to MQTT Broker {self.host}:{self.port} {self.clientID}')
            else:
                logging.error(f'Failed to connect, return code {str(rc)} | {self.clientID}')
                print(f'Failed to connect, return code {str(rc)} | {self.clientID}')
                
        client = mqtt_client.Client(self.clientID)
        client.username_pw_set(self.username, self.password)
        #client.tls_set('ca.crt',tls_version=2)
        client.on_connect = on_connect
        client.connect(self.host, self.port)
        return client

    def publish(self, client, msg):
        newMsg = json.loads(msg)
        interval = self.dataObj['interval']
        keyValue = self.dataObj['keyValue']

        key = keyValue[0]['key']
        s1 = Simulator(keyValue[0]['initValue'])
       
        key2 = keyValue[1]['key']
        if(key2 != ''):
            s2 = Simulator(keyValue[1]['initValue'])
        
        key3 = keyValue[2]['key']
        if(key3 != ''):
            s3 = Simulator(keyValue[2]['initValue'])
        

        Helper.update_json(self.dataObj)
        
        while self.timeout == False:
            newMsg[key] = s1.simulate()
            if(key2 != ''):
                newMsg[key2] = s2.simulate()
            if(key3 != ''):
                newMsg[key3] = s3.simulate()

            result = client.publish(self.topic, json.dumps(newMsg))

            if result[0] == 0:  #[0, 1]
                logging.debug(f'Send {newMsg} to topic {self.topic} | {self.clientID}')
                print(f'Send {newMsg} to topic {self.topic} | {self.clientID}')
            else:
                logging.error(f'Failed to send message to topic {self.topic} | {self.clientID}')
            
            time.sleep(interval)

    def run(self, msg):
        self.client = self.connect_mqtt()
        print("CLIENT-------")
        print(self.client)
        self.client.loop_start()
        print("Run MQTT") #log
        #logging.debug(f'Run MQTT {self.topic} | {self.clientID}')
        
        try:
            self.thread = threading.Thread(target = self.publish, args = (self.client, msg,), name = "thread-client_"+self.sn)
            self.thread.setDaemon(True) 
            self.thread.start()
        except:
            #print("An exception occurred 2")
            raise Exception("An exception occurred")
            logging.error(f'Disconnected result code: {self.host}:{self.port} | {self.clientID}')
        
    def stop_mqtt(self):
        def on_disconnect(client, userdata, rc=0):
            print("Stop MQTT")
            
            logging.debug(f'Disconnected result code: {str(rc)}')
            client.loop_stop()
   
    #@classmethod
    def get_client_ID(self):
        print(self.clientID)
        return self.clientID

    def stop_thread(self):
        print(self.thread.is_alive())

        self.client.loop_stop()  #stop loop 
        self.client.disconnect() #disconnect

        self.timeout = True
        self.thread.join()

    def get_thread(self):
        return self.thread
    
    def check_thread(self):
        return self.thread.is_alive()

    def connect2():
        print("connect")

    def disconnect2():
        print("disconnect")  

    #def __call__(self):
        #print("tst-callback")
    #def __del__(self):
      #class_name = self.__class__.__name__
      #print class_name, "destroyed"
