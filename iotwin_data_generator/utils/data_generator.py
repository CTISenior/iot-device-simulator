#!/usr/bin/python3

import numpy as np

import utils.setting as Setting


value_types = Setting.get_value_types()

class DataGenerator:
    def __init__(self, key, value, value_type='RN'):
        self.key = key
        self.value = value
        self.value_type = value_type

    def get_key(self):
        return self.key

    def generate_data(self):
        new_value = lambda x : self.value + x
        self.value = new_value(self.get_value())
        return self.convert(self.value)

    def get_value(self):
        '''
            RandomNumber
            RandomFloatNumber
        '''
        if self.value_type != 'CN':
            return self.generate(value_types[self.value_type]['value_list'])
        return 0 # ConstantNumber

    def generate(self, value_list, prob=[0.025, 0.95, 0.025]):
        return np.random.choice(value_list, 1, prob)[0]
        #numpy.random.choice(numpy.arange(1, 7), p=[0.1, 0.05, 0.05, 0.2, 0.4, 0.2])

    def convert(self, value):
        return float(value_types[self.value_type]['format'] . format(value))

    # def get_prob():

    # def set_prob():
