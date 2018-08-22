#Author Diego Salas
#Date 11/12/2017
import logging
import os
import datetime

def log(message):
    logging.basicConfig(filename= os.path.join(os.path.dirname(__file__), 'persist/log'),level=logging.DEBUG)
    logging.info(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") + " : " + message)
