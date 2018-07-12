from cgi import urllib
import json
import sys
sys.path.append('/var/www/pyapi/scripts')
import config
from pucp_automatic_annotation import addConceptsToOntology


# params:
# filepath
# concept list
#

def service(request_body):
    namespace = request_body['namespace']
    root = request_body['root']
    status = 1
    extra = ""
    error = ""
    if (namespace != ""):
        config.editOntologyNamespace(namespace)
    if (root != ""):
        config.editOntologyRootDir(root)
    dictionary = {'status': status, 'error': error, 'extra': extra}
    return json.dumps(dictionary)
