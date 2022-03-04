#!/usr/bin/python

import sys
import logging

logging.basicConfig(filename="/log/test.log", level=logging.DEBUG)


class Logger:

    def __init__(self):
        print("init logger")
    
    def success(self):
        print("SUCCESS | ")

    def info(self):
        print("INFO | ")

    def error(self):
        print("ERROR | ")

    def warning(self):
        print("WARNING | ")

    def create_log_fle(self):
        print("date as filename")
    
    def write_txt(self, content, fileName="./data/logs.txt"):
        with open('test1','wb') as f:
            f.write(content)
        