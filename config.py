import configparser
import os

config = configparser.ConfigParser()
config_file = os.path.join(os.path.dirname(__file__), 'config.ini')
config.read(config_file)

RootDir = config['DEFAULT']['RootDir']#'/var/www/pyapi/scripts/'
OntologyDir = RootDir + config['DEFAULT']['OntologyDir']#'persist/ontology/'
OntologyNamespace = config['DEFAULT']['OntologyNamespace']#"http://test.org/"
LogDir = RootDir + config['DEFAULT']['LogDir']#persist/log/

def editOntologyNamespace(namespace):
    config.read(config_file)
    config.set('DEFAULT', 'OntologyNamespace', namespace)
    with open(config_file, 'w') as configfile:
        config.write(configfile)

def editOntologyRootDir(root):
    config.read(config_file)
    config.set('DEFAULT', 'RootDir', root)
    with open(config_file, 'w') as configfile:
        config.write(configfile)
