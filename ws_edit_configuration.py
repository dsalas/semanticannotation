import json
import sys
import os
sys.path.append(os.path.dirname(__file__))
import config

# params:
# namespace: namespace for ontologies
# root: api rootdir

def service(request_body):
    namespace = request_body.get('namespace',"")
    root = request_body.get('root',"")
    status = 1
    extra = ""
    error = ""
    if (namespace != ""):
        config.editOntologyNamespace(namespace)
    if (root != ""):
        config.editOntologyRootDir(root)
    dictionary = {'status': status, 'error': error, 'extra': extra}
    return json.dumps(dictionary)