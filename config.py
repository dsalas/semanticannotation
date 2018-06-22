import configparser

config = configparser.ConfigParser()
config.read('config.ini')

RootDir = config['DEFAULT']['RootDir']#'/var/www/pyapi/scripts/'
OntologyDir = RootDir + config['DEFAULT']['OntologyDir']#'persist/ontology/'
OntologyNamespace = config['DEFAULT']['OntologyNamespace']#"http://test.org/"

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