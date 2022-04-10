#!/usr/bin/python3

import utils.setting as Setting
import utils.helper as Helper


class Client:
    def __init__(self, sn, data_obj, protocol='mqtt'):
        self.host = Setting.get_gateway_host()
        self.gateway_id = Setting.get_gateway_id()
        
        self.sn = sn
        self.client_id = f'{self.gateway_id}_{sn}'
        self.data_obj = data_obj

        self.protocol = protocol
        self.port = Setting.get_protocol_port(self.protocol)
        self.topic = Setting.get_protocol_topic(self.protocol)
        self.security = Setting.get_protocol_credentials(self.protocol)
        self.adv_security =Setting.get_protocol_certificates(self.protocol)

        self.thread = None
        self.timeout = False

        logfile = Helper.get_device_log_file(self.sn)
        self.logger = Helper.create_logger(f'{self.protocol}-{self.client_id}', logfile)
        self.logger.debug(f'New device instance created: [{self.host}:{self.port} - {self.protocol}]')

    # def get(self):
    # def set(self, test):

    def get_host(self):
        return self.host
    
    def get_port(self):
        return self.port

    def get_gateway_id(self):
        return self.gateway_id

    def get_sn(self):
        return self.sn
    
    def get_client_id(self):
        return self.client_id

    def get_thread(self):
        return self.thread

    def check_thread(self):
        return self.thread.is_alive()

    # def run()
    # def get_thread()
    # def check_thread()



    # def __call__(self):
        # print("tst-callback")
    # def __del__(self):
      #class_name = self.__class__.__name__
      # print class_name, "destroyed"
