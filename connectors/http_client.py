#!/usr/bin/python3

import sys
import time
import json
import logging
import threading
import queue
import requests

from utils.data_generator import DataGenerator
from utils.setting import Setting
import utils.helper as Helper


class HTTP_Client:
    def __init__(self, host, sn, dataObj, protocol='http', requestMethod='POST'):

        self.host = host
        self.sn = sn
        self.dataObj = dataObj

        stg = Setting()
        self.protocol = protocol
        self.port = stg.getProtocolPort(self.protocol)
        self.endpoint = stg.getProtocolTopic(self.protocol)
        userData = stg.getProtocolCredentials(self.protocol)
        self.username = userData['usr']
        self.password = userData['passwd']
        self.method = requestMethod
        #self.clientID = stg.getBrokerID()
        self.clientID = 'client_' + sn
        self.headers = {'content-type': 'application/json'}
        self.url = url = f'{self.protocol}://{self.host}:{self.port}{self.endpoint}'

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
        self.session = requests.Session()
        self.session.auth = (self.username, self.password)

        msg = f'Session created [{self.protocol}]'
        self.logger.debug( msg )
        print(f'{self.sn} | {msg}')

        '''
        try:
            r = Requests.get(self.url) #### GET
            r.raise_for_status()
            s = requests.Session() #create sessions
        except Requests.exceptions.ConnectionError as err_c:
            print ("Error: " + err_c)
        return r
        '''

    def disconnect(self):
        try:
            #test
            self.logger.debug(f'Disconnect [{self.protocol}]')
        except:
            pass
            #self.logger.error(f'Error occured while disconnecting! [{self.protocol}]')
        
        '''
        try:
            print("disconnected!")
        except:
            print()
        '''

    def GET(self, body):
        print('GET')

        '''
        try:
            r = Requests.get(self.url) #### GET
            r.raise_for_status()
            s = requests.Session() #create sessions
        except Requests.exceptions.ConnectionError as err_c:
            print ("Error: " + err_c)
        return r
        '''
        

    def POST(self, body):
        try:
            response = self.session.post(self.url, json=body, headers=self.headers, auth=(self.username, self.password))
            response.raise_for_status()
            
            self.logger.debug(f'Response: {response}')
            #print(f'{self.sn} | POST - Status: {r.status_code} - Sent message: {body} to {self.endpoint}')
            self.logger.info(f'POST: Status: {response.status_code} | Publish message: {body} to [{self.endpoint}] endpoint successfully')
        except requests.exceptions.HTTPError as err_h:
            error_msg = f'Http Error: {err_h}'
            self.logger.error( error_msg )
            #raise Exception('')
        except requests.exceptions.ConnectionError as err_c:
            error_msg = f'Error Connecting: {err_c}'
            self.logger.error( error_msg )
        except requests.exceptions.Timeout as err_t:
            error_msg = f'Timeout Error: {err_t}'
            self.logger.error( error_msg )
        except requests.exceptions.RequestException as err:
            error_msg = f'Other Exception: {err}'
            self.logger.error( error_msg )

    def publish(self, body):
        newBody = json.loads(body)
        interval = self.dataObj['interval']
        keyValueList = self.dataObj['keyValue']

        #data = {}
        objects = []
        for keyValue in keyValueList:
            objects.append ( DataGenerator( keyValue['key'], keyValue['initValue'], keyValue['valueType'] ))

        if self.method == "POST":
            while not self.timeout:
                for obj in objects:
                    newBody[ obj.get_key() ] = obj.generate_data()
                    self.POST( newBody )
                    time.sleep(interval)

        elif self.method == "GET":
            self.GET( newBody )


    def run(self, body):
        self.logger.debug(f'Run [{self.protocol}]')
        self.connect()

        try:
            self.thread = threading.Thread(
                target = self.publish, 
                args = (body,), 
                name = "thread-client_"+self.sn
            )
            self.thread.setDaemon(True)
            self.thread.start()
            self.logger.debug(f'Create a thread [{self.protocol}]')
        except:
            err = f'An exception occurred while publishing data: [{self.host}:{self.port}]'
            self.logger.error( err )
            print(f'{self.sn} | {err}')


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
            self.logger.error(f'Thread cannot be stopped thread [{self.protocol}]')


    #def __call__(self):
        #print("tst-callback")
    #def __del__(self):
      #class_name = self.__class__.__name__
      #print class_name, "destroyed"
