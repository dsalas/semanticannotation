from cgi import urllib, escape
import json
import os
import io
import sys

sys.path.append('/var/www/pyapi/scripts')
import config
from pucp_automatic_annotation import addConceptsToOntology


# params:
# filepath
# concept list
#

def service(request_body):
    body = urllib.parse.parse_qs(request_body)
    filepath = body['filepath'][0]
    concepts = body['concepts']
    result = addConceptsToOntology(filepath,concepts)
    status = 0
    error = "No se pudo crear los conceptos en la ruta " + filepath
    if result:
       status = 1
       error = "none"
    extra = ""
    dictionary = {'status': status, 'error': error, 'extra': extra}
    return json.dumps(dictionary)
