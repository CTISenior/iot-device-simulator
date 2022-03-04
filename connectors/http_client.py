#!/usr/bin/python

import requests
import time
import json
import logging
import threading

from utils.simulator import Simulator
from utils.setting import Setting
import utils.helper as Helper


logging.basicConfig(filename="logs/http.log", level=logging.DEBUG)


class HTTP_Client:
    def __init__(self, sn, dataObj, protocol='http', requestMethod='POST'):
        stg = Setting()
        self.host = stg.getGatewayHost()
        self.protocol = protocol
        self.port = stg.getProtocolPort(self.protocol)
        self.endpoint = stg.getProtocolTopic(self.protocol)
        userData = stg.getProtocolCredentials(self.protocol)
        self.username= userData['usr']
        self.password = userData['passwd']
        self.method = requestMethod
        #self.clientID = stg.getBrokerID()
        self.clientID = 'client_' + sn
        self.headers = {'content-type': 'application/json'}
        self.url = url = f'{self.protocol}://{self.host}:{self.port}{self.endpoint}'
        
        self.sn = sn
        self.dataObj = dataObj
        self.thread = None
        self.timeout = False
        
        #logging.basicConfig(filename="logs/"+self.clientID, level=logging.DEBUG)
        logging.debug(f'New device instance created: {self.host}:{self.port} | {self.protocol} | {self.clientID}')
    
    '''
    def connect(self):
    if (
            response.status_code != 204 and
            response.headers["content-type"].strip().startswith("application/json")
        ):
        if status is 200 -> OK
        print r.status_code
        print r.headers['content-type']

        try:
            r = requests.get(self.url) #### GET
            r.raise_for_status()
        except requests.exceptions.HTTPError as e:
            print ("Error: " + str(e)) #log
        return r
    '''
    '''
    def disconnect(self):
        try:
            print("disconnected!")
        except:
            print()
    '''

    def GET(self, body):
        print("GET")

    def POST(self, body):
        try:
            r = requests.post(self.url, json=body, headers=self.headers, auth=(self.username, self.password))
            print(f'{str(r)}')
            logging.debug(f'{str(r)}')
            logging.debug(f'POST | Status: 200 OK | {self.clientID} | Send message: {self.protocol} to IoT Gateway successfully')
        except requests.exceptions.RequestException as e:
            print(str(e))
            logging.error(f'{str(e)} | {self.clientID}')
         
    def publish(self, body):
        print("12131")
        newBody = json.loads(body)
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

        if self.method == "POST":
            while self.timeout == False:
                newBody[key] = s1.simulate()
                if(key2 != ''):
                    newBody[key2] = s2.simulate()
                if(key3 != ''):
                    newBody[key3] = s3.simulate()

                self.POST( newBody )

                time.sleep(interval)

        elif self.method == "GET":
            self.GET( newBody )


    def run(self, body):
        self.thread = threading.Thread(target = self.publish, args = (body,), name = "thread-client_"+self.sn)
        self.thread.setDaemon(True) 
        self.thread.start()
   
    def get_client_ID(self):
        print(self.clientID)
        return self.clientID

    def stop_thread(self):
        print(self.thread.is_alive())

        self.timeout = True
        self.thread.join()

        print("Stop HTTP")
        #logging.debug("Disconnected result code: " + str(rc))

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
