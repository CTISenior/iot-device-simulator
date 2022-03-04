#!/usr/bin/python

from mimetypes import init
import random
import sys
import time
import json
import numpy as np
 
class Simulator:
    def __init__(self, value1, measurement="0"):
        self.value = value1
        self.measurement = measurement
    def simulate(self):
        self.value = self.value + self.generateRandomValue()
        #print(self.type + " " + str(value) + " "+ self.measurement)
        return self.value
    def generateRandomValue(self):
        values = np.random.choice([-1, 0, 1], 1, p=[0.075, 0.85, 0.075]) #total p => 1
        return int(values[0]) 
        #return random.randint(-1, 1)
        #random.getrandbits(1)
        #random.choice([True, False])
        #random.choice(range(10, 101))
        #numpy.random.choice(numpy.arange(1, 7), p=[0.1, 0.05, 0.05, 0.2, 0.4, 0.2])

    def convert(self, measurement):
        if(measurement == "temp"):
            x=0
        elif(measurement == "hum"):
            x=1
        else:
            x=2
        print('convert test')

if __name__ == '__main__':
    print('Simulator')