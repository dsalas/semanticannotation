import logging
import os

def log(message):
    logging.basicConfig(filename= os.path.join(os.path.dirname(__file__), 'persist/log'),level=logging.DEBUG)
    logging.info(message)