#!/usr/bin/python3

import sys
import json
import numpy as np
 
class DataGenerator:
    
    def __init__(self, key, value, value_type='RN'):
        self.key = key
        self.value = value
        self.value_type = value_type

    def get_key(self):
        return self.key

    def generate_data(self):
        newValue = lambda generated_value: self.value + generated_value
        self.value = newValue( self.get_value() )
        return self.value

    def get_value(self):
        if self.value_type == 'RN': #RandomNumber
            return self.generate_random_value()
        elif self.value_type == 'RFN': #RandomFloatNumber
            return self.generate_random_float_value()
        elif self.value_type == 'RFN-2': #RandomFloatNumber
            return self.generate_random_float_value2()
        else: #ConstantNumber
            return self.generate_constant()

    def generate_random_value(self):
        return int( 
            self.generate([-1, 0, 1]) 
            )
        
    def generate_random_float_value(self):
        return float("{0:.2f}".format( 
            self.generate([-0.1, 0, 0.1]) 
            ))

    def generate_random_float_value2(self):
        return float("{0:.2f}".format( 
            self.generate([-0.5, 0, 0.5]) 
            ))

    def generate_random_float_value3(self):
        return float("{0:.3f}".format( 
            self.generate([-0.05, 0, 0.05]) 
            ))

    def generate_random_float_value4(self):
        return float("{0:.3f}".format( 
            self.generate([-0.01, 0, 0.01]) 
            ))

    def generate_constant(self):
        return self.value

    def generate(self, valueList, p=[0.05, 0.9, 0.05]):
        return np.random.choice(valueList, 1, p)[0]
        #numpy.random.choice(numpy.arange(1, 7), p=[0.1, 0.05, 0.05, 0.2, 0.4, 0.2])

    #def get_custom_value(self):


    #def get_prob():

    #def set_prob():