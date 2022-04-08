#!/usr/bin/python3

import json


class Setting:
    def __init__(self):
        f = open('./config/settings.json')
        self.data = json.load(f)
        f.close()

    def get_gateway_name(self):
        return self.data['gateway']['name']

    def get_client_id(self):
        return self.data['gateway']['client_id']

    def get_gateway_host(self):
        return self.data['gateway']['host']

    def get_default_keys(self):
        return self.data['gateway']['default_keys']

    def get_gateway_credentials(self):
        user_data = dict()
        user_data['usr'] = ""
        user_data['passwd'] = ""

        if self.is_secure():
            user_data['usr'] = self.data['gateway']['security']['username']
            user_data['passwd'] = self.data['gateway']['security']['password']
        return user_data

    def is_secure(self):
        return self.data['gateway']['security']['isSecure']

    def get_ssl_status(self):
        return self.data['gateway']['ssl']['certificates']

    def get_protocol_port(self, protocol):
        return self.data['gateway']['protocols'][protocol]['port']

    def get_protocol_topic(self, protocol):
        return self.data['gateway']['protocols'][protocol]['topic_name']

    def get_protocol_credentials(self, protocol):
        user_data = dict()
        user_data['usr'] = ""
        user_data['passwd'] = ""

        security_obj = self.data['gateway']['protocols'][protocol]['security']

        if self.is_protocol_secure(protocol):
            user_data['usr'] = security_obj['username']
            user_data['passwd'] = security_obj['password']

        return user_data

    def is_protocol_secure(self, protocol):
        return self.data['gateway']['protocols'][protocol]['security']['isSecure']

    def get_certificates(self):
        if self.get_ssl_status():
            ca_cert = self.data['gateway']['ssl']['caCert']
            cert = self.data['gateway']['ssl']['cert']

            return ca_cert, cert

        return None

        