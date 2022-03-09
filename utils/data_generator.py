#!/usr/bin/python3

import sys
import json
import numpy as np
 
class DataGenerator:
    
    def __init__(self, value, value_type='RN'):
        self.value = value
        self.value_type = value_type

    def generateData(self):
        newValue = lambda generated_value: self.value + generated_value
        self.value = newValue(self.get_random_value())
        return self.value

    def get_random_value(self):
        values = np.random.choice([-1, 0, 1], 1, p=[0.075, 0.85, 0.075]) #total p => 1
        return int(values[0]) 
        #numpy.random.choice(numpy.arange(1, 7), p=[0.1, 0.05, 0.05, 0.2, 0.4, 0.2])

    def get_random_float_value(self):
        values = np.random.choice([-0.1, 0, 0.1], 1, p=[0.075, 0.85, 0.075])
        return int(values[0]) 

    def get_random_float_value2(self):
        values = np.random.choice([-0.5, 0, 0.5], 1, p=[0.075, 0.85, 0.075])
        return int(values[0]) 

    def get_constant(self):
        return self.value

    #def get_custom_value(self):

    '''
    def convert(self):
        if(self.value_type == 'RN'): #RandomNumber

        elif(self.value_type == 'RFN'): #RandomFloatNumber

        elif(self.value_type == 'RFN-2'): #RandomFloatNumber

        else(self.value_type == 'CN'): #ConstantNumber
    '''