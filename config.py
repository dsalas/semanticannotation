#Author Diego Salas
#Date 11/12/2017
import configparser
import os

config = configparser.ConfigParser()
config_file = os.path.join(os.path.dirname(__file__), 'config.ini')
config.read(config_file)

RootDir = config['coruja']['RootDir']#'/var/www/pyapi/scripts/'
OntologyDir = RootDir + config['coruja']['OntologyDir']#'persist/ontology/'
OntologyNamespace = config['coruja']['OntologyNamespace']#"http://test.org/"
LogDir = RootDir + config['coruja']['LogDir']#persist/log/

def editOntologyNamespace(namespace):
    config.read(config_file)
    config.set('coruja', 'OntologyNamespace', namespace)
    with open(config_file, 'w') as configfile:
        config.write(configfile)

def editOntologyRootDir(root):
    config.read(config_file)
    config.set('coruja', 'RootDir', root)
    with open(config_file, 'w') as configfile:
        config.write(configfile)

