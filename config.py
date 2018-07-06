import configparser
import os

config = configparser.ConfigParser()
config_file = os.path.join(os.path.dirname(__file__), 'config.ini')
config.read(config_file)

RootDir = config['DEFAULT']['RootDir']#'/var/www/pyapi/scripts/'
OntologyDir = RootDir + config['DEFAULT']['OntologyDir']#'persist/ontology/'
OntologyNamespace = config['DEFAULT']['OntologyNamespace']#"http://test.org/"
LogDir = config['DEFAULT']['LogDir']#persist/log/

def editOntologyNamespace(namespace):
    config.read('config.ini')
    config.set('DEFAULT', 'OntologyNamespace', namespace)
    with open('config.ini', 'w') as configfile:
        config.write(configfile)

def editOntologyRootDir(root):
    config.read('config.ini')
    config.set('DEFAULT', 'RootDir', root)
    with open('config.ini', 'w') as configfile:
        config.write(configfile)
