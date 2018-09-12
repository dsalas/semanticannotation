#Author Diego Salas
#Date 11/12/2017
import logging
import os
import datetime

debug = True

def log(message):
    if debug:
        logging.basicConfig(filename= os.path.join(os.path.dirname(__file__), 'persist/log'),level=logging.DEBUG)
        logging.info(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") + " : " + message)
