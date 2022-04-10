#!/usr/bin/python3

import json

f = open('./config/settings.json', encoding='UTF-8')
SETTING = json.load(f)
f.close()


def get_gateway_id():
    return SETTING['gateway']['id']

def get_gateway_name():
    return SETTING['gateway']['name']

def get_gateway_host():
    return SETTING['gateway']['host']

def get_default_keys():
    return SETTING['generator']['default_keys']

def get_telemetry_keys():
    return SETTING['generator']['telemetry_keys']

def get_value_types():
    return SETTING['generator']['value_types']

def get_gateway_credentials():
    return SETTING['gateway']['security']

def get_gateway_certificates():
    return SETTING['gateway']['advanced_security']

# Protocols
def get_protocol_port(protocol):
    return SETTING['gateway']['protocols'][protocol]['port']

def get_protocol_topic(protocol):
    return SETTING['gateway']['protocols'][protocol]['topic_name']

def get_protocol_credentials(protocol):
    return SETTING['gateway']['protocols'][protocol]['security']

def get_protocol_certificates(protocol):
    return SETTING['gateway']['protocols'][protocol]['advanced_security']
    