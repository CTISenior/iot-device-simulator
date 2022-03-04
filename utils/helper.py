#!/usr/bin/python

import sys
import json
import threading


filename='data/devices.json'


def init_json():
    print("init json")
    file_data = {
        "devices": [

        ]
    }
    
def write_json(new_data):
    print("write json")

def read_json():
    with open(filename, 'r') as file:
        file_data = json.load(file)
    return file_data
    
def checkDeviceExist(sn):
    i=0
    
    devices = read_json()['devices']
    for dev in devices:
        if(sn == dev['serialNumber']):
            return dev, i; #obj, #position
        i=i+1

    return False


def update_json(new_data):
    status = checkDeviceExist(new_data['serialNumber'])
    if(status == False):
        with open(filename,'r+') as file:
            file_data = json.load(file)
            file_data["devices"].append(new_data)
            file.seek(0)
            json.dump(file_data, file, indent = 4)


def delete_json(sn): #to delete device item, the device thread must be stopped!
    deviceData, position = checkDeviceExist(sn)
    data = read_json()
    data['devices'].pop(position)

    with open(filename, 'w') as json_file_modified:
        json.dump(data, json_file_modified, indent = 4)

def get_device_data(sn):
    deviceData, position = checkDeviceExist(sn)
    return deviceData

def get_device_instance(device_instance_list, sn):
    if bool(device_instance_list):
        for inst in device_instance_list:
            if(inst.clientID == "client_"+sn):
                return inst
    return False

def check_thread_status(thread1):
    if thread1.is_alive():
        return "Running"
    else:
        return "Stopped!"
    
    #return t1.is_alive()

def getRunningDeviceCount():
    return threading.active_count()-1 #exclude main thread



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
