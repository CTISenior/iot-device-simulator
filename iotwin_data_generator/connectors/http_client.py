#!/usr/bin/python3

import time
import json
import threading
import requests
import ssl

import utils.setting as Setting
from utils.data_generator import DataGenerator
from connectors.client import Client


class HTTP_Client(Client):
    def __init__(self, sn, data_obj, protocol, request_method='POST'):
        super().__init__(sn, data_obj, protocol)
        self.headers = {'content-type': 'application/json'}
        self.endpoint = Setting.get_protocol_topic(self.protocol)
        self.method = request_method
        self.url = f'{self.protocol}://{self.host}:{self.port}{self.endpoint}'

    def get(self):
        print("get")
        # return self

    def set(self):
        print("set")

    def connect(self):
        '''
            try:
                r = Requests.get(self.url) #### GET
                r.raise_for_status()
                s = requests.Session() #create sessions
            except Requests.exceptions.ConnectionError as err_c:
                print ("Error: " + err_c)
            return r
        '''

        self.session = requests.Session()
        if self.adv_security['certificates']:
            self.session.cert = (self.adv_security['cert'], self.adv_security['key'])
        elif self.security['credentials']:
            self.session.auth = (self.security['username'], self.security['password'])

        log_msg = f'New session created [{self.protocol}]'
        self.logger.debug(log_msg)
        print(f'{self.sn} | {log_msg}')

    def disconnect(self):
        '''
            try:
                print("disconnected!")
            except:
                print()
        '''

        try:
            # test
            self.logger.debug(f'Disconnect [{self.protocol}]')
        except BaseException:
            pass
            #self.logger.error(f'Error occured while disconnecting! [{self.protocol}]')

    def GET(self, body):
        '''
            try:
                r = Requests.get(self.url) #### GET
                r.raise_for_status()
                s = requests.Session() #create sessions
            except Requests.exceptions.ConnectionError as err_c:
                print ("Error: " + err_c)
            return r
        '''

        print('GET')

    def POST(self, body):
        try:
            response = self.session.post(
                self.url, 
                json=body, 
                headers=self.headers
            )
            response.raise_for_status()
            #print(f'{self.sn} | POST - Status: {r.status_code} - Publish telemetry data: {body} to {self.endpoint}')
            self.logger.info(f'POST: Status: {response.status_code} | Publish telemetry data: {body} to [{self.endpoint}] endpoint successfully')
        except requests.exceptions.HTTPError as err_h:
            error_msg = f'HTTP Error: {err_h}'
            self.logger.error(error_msg)
            #raise Exception('')
        except requests.exceptions.ConnectionError as err_c:
            error_msg = f'Error Connecting: {err_c}'
            self.logger.error(error_msg)
        except requests.exceptions.Timeout as err_t:
            error_msg = f'Timeout Error: {err_t}'
            self.logger.error(error_msg)
        except requests.exceptions.RequestException as err:
            error_msg = f'Other Exception: {err}'
            self.logger.error(error_msg)

    def publish(self, body):
        '''Publish message to gateway'''

        new_body = json.loads(body)
        interval = self.data_obj['interval']
        keyvalue_list = self.data_obj['keyValue']

        #data = {}
        objects = []
        for key_value in keyvalue_list:
            objects.append(
                DataGenerator(
                    key_value['key'],
                    key_value['initValue'],
                    key_value['valueType']
                )
            )

        if self.method == "POST":
            while not self.timeout:
                for obj in objects:
                    new_body[obj.get_key()] = obj.generate_data()
                    self.POST(new_body)
                    time.sleep(interval)
        elif self.method == "GET":
            self.GET(new_body)

    def run(self, body):
        self.logger.debug(f'Run [{self.protocol}]')
        self.connect()

        try:
            self.thread = threading.Thread(
                target=self.publish,
                args=(body,),
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

    def stop_thread(self):
        self.disconnect()
        try:
            self.timeout = True
            self.thread.join()
            log_msg = f'Stop thread [{self.protocol}]'
            self.logger.debug(log_msg)
            print(f'{self.sn} | {log_msg}')
        except BaseException:
            self.logger.error(f'Thread cannot be stopped thread [{self.protocol}]')

    # def __call__(self):
        # print("tst-callback")
    # def __del__(self):
      #class_name = self.__class__.__name__
      # print class_name, "destroyed"
