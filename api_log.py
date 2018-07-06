import logging
import config

def log(message):
    logging.basicConfig(filename=config.LogDir,level=logging.DEBUG)
    logging.info(message)