#!/usr/bin/python3

import os, glob
import sys
import json
#import yaml
import threading
import logging

devices_json_file = 'data/devices.json'
device_log_directory = './logs/deviceLogs'

def get_client_name():
    return 'client_'

def get_thread_name():
    return 'thread-client_'

def get_device_log_file(sn):
    return f'{device_log_directory}/{sn}.log'

def create_directory(fileName):
    try:
        os.makedirs(fileName)
    except FileExistsError:
        err = 'file exists'

def init():
    create_directory(device_log_directory)
    create_directory('./certificates')

def read_json():
    with open(devices_json_file, 'r') as file:
        file_data = json.load(file)
    return file_data
    
def check_device_exist(sn):
    devices = read_json()['devices']
    i=0
    
    for dev in devices:
        if sn == dev['serialNumber']:
            return dev, i; #obj, #position
        i=i+1
    return False

def update_json(new_data):
    status = check_device_exist(new_data['serialNumber'])
    if status == False:
        with open(devices_json_file,'r+') as file:
            file_data = json.load(file)
            file_data["devices"].append(new_data)
            file.seek(0)
            json.dump(file_data, file, indent = 4)

def delete_json(sn):
    data = read_json()
    
    deviceData, position = check_device_exist(sn)
    data['devices'].pop(position)

    with open(devices_json_file, 'w') as json_file_modified:
        json.dump(data, json_file_modified, indent = 4)

def get_device_data(sn):
    deviceData, position = check_device_exist(sn)
    return deviceData

def get_device_instance(device_instance_list, sn):
    if bool(device_instance_list):
        for inst in device_instance_list:
            if inst.clientID == "client_"+sn:
                return inst
    return False

def check_thread_status(thread1):
    if thread1.is_alive():
        return "Running"
    else:
        return "Stopped!"
    
    #return t1.is_alive()

def get_running_device_count():
    return threading.active_count()-1 #exclude main thread

def read_log_file(logfile):
    if os.path.isfile(logfile):
        with open(logfile) as f:
            f = f.readlines()
        return f
    return None

def remove_device_log_files():
    for file in os.scandir(device_log_directory):
        os.remove(file.path)

    '''
    files = glob.glob(f'{device_log_directory}}/*')
    for f in files:
        os.remove(f)
    '''

def validate_field(inp):
    if inp != '' or len(inp) >= 3:
        return True
    return False

def check_duplicated_keys(key_list):
    return any(key_list.count(element) > 1 for element in key_list)


def create_logger(name ,log_file):
    logger = logging.getLogger( name )
    logger.setLevel(logging.DEBUG)
    fh = logging.FileHandler( log_file )
    fh.setFormatter(logging.Formatter('%(asctime)s | %(levelname)s | %(name)s | %(message)s', "%m/%d/%Y %H:%M:%S"))
    logger.addHandler(fh)
    return logger

def create_message(dataObj):
    msg = {
        "serialNumber": dataObj['serialNumber'],
        "sensorType": dataObj['sensorType'],
        "sensorModel": dataObj['sensorModel'],
        "accessToken": dataObj['accessToken'],
        "protocol": dataObj['protocol'],
        "interval": dataObj['interval'],
    }

    return json.dumps(msg)

