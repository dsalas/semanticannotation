from cgi import urllib
import json
import sys
import config
sys.path.append('/var/www/pyapi/scripts')
from pucp_automatic_annotation import addConceptsToOntology


# params:
# filepath
# concept list
#

def service(request_body):
    body = urllib.parse.parse_qs(request_body)
    namespace = body['namespace'][0]
    root = body['root'][0]
    status = 1
    extra = ""
    error = ""
    if (namespace != ""):
        config.editOntologyNamespace(namespace)
    if (root != ""):
        config.editOntologyRootDir(root)
    dictionary = {'status': status, 'error': error, 'extra': extra}
    return json.dumps(dictionary)
