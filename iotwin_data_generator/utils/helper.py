#!/usr/bin/python3

import os
import json
#import glob
#import yaml
import threading
import logging
import html

devices_json_file = 'data/devices.json'
device_log_directory = './logs/deviceLogs'


def get_device_log_file(sn):
    return f'{device_log_directory}/{sn}.log'

def create_directory(filename):
    try:
        os.makedirs(filename)
    except FileExistsError:
        err = 'file exists'

def init():
    create_directory(device_log_directory)

def read_json():
    with open(devices_json_file, 'r', encoding='UTF-8') as file:
        file_data = json.load(file)
    return file_data

def check_device_exist(sn):
    devices = read_json()['devices']
    for i, dev in enumerate(devices):
        if sn == dev['serialNumber']:
            return dev, i  # obj, #position
    return None

def update_json(new_data):
    status = check_device_exist(new_data['serialNumber'])
    if status is None:
        with open(devices_json_file, 'r+', encoding='UTF-8') as file:
            file_data = json.load(file)
            file_data["devices"].append(new_data)
            file.seek(0)
            json.dump(file_data, file, indent=4)

def delete_json(sn):
    data = read_json()
    device_data, position = check_device_exist(sn)
    data['devices'].pop(position)

    with open(devices_json_file, 'w', encoding='UTF-8') as json_file_modified:
        json.dump(data, json_file_modified, indent=4)

def get_device_data(sn):
    device_data, pos = check_device_exist(sn)
    return device_data

def get_device_instance(device_instance_list, sn):
    if bool(device_instance_list):
        #gateway_id = Setting.get_gateway_id()
        for instance in device_instance_list:
            if instance.sn == sn:
                return instance
    return None

def check_thread_status(thread1):
    if thread1.is_alive():
        return "Running"
    return "Stopped!"
    # return t1.is_alive()

def get_running_device_count():
    return threading.active_count() - 1  # exclude main thread

def read_log_file(logfile):
    if os.path.isfile(logfile):
        with open(logfile, encoding='UTF-8') as f:
            f = f.readlines()
        return f
    return None

def remove_device_log_files():
    '''
        files = glob.glob(f'{device_log_directory}}/*')
        for f in files:
            os.remove(f)
    '''
    for file in os.scandir(device_log_directory):
        os.remove(file.path)

def validate_field(inp):
    if inp != '' and len(inp) >= 3 and len(inp) <= 30:
        return True
    return False

def check_duplicated_keys(key_list):
    return any(key_list.count(element) > 1 for element in key_list)

def sanitize(input):
    return html.escape(input)

def create_logger(name, log_file):
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)
    fh = logging.FileHandler(log_file)
    fh.setFormatter(
        logging.Formatter(
            '%(asctime)s | %(levelname)s | %(name)s | %(message)s',
            "%m/%d/%Y %H:%M:%S"))
    logger.addHandler(fh)
    return logger

def prepare_telemetry_data(data_obj):
    msg = {
        "serialNumber": data_obj['serialNumber'],
        "sensorType": data_obj['sensorType'],
        "sensorModel": data_obj['sensorModel'],
        "accessToken": data_obj['accessToken'],
        "protocol": data_obj['protocol'],
        "interval": data_obj['interval']
    }

    return json.dumps(msg)
