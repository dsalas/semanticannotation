from cgi import urllib, escape
import json
import os
import io
import sys

sys.path.append('/var/www/pyapi/scripts')
import config
from pucp_automatic_annotation import addConceptsToOntology

# params:
# type: 0 folder, 1 path, 2 database id
# filepath 
# docid

def service(request_body):
    body = urllib.parse.parse_qs(request_body)
    type = body['type'][0]
    status = 0	   
    error = "Incorrect type."
    extra = "Type: " + type
    if (type == '0'):
        filepath = body['filepath'][0]
        status = 1
        extra = "type 0"
    if (type == '1'):
        filepath = body['filepath'][0]
        status = 1
        extra = "type 1"
    if (type == '2'):
        status = 1
        extra = "type 2"
    dictionary = {'status': status, 'error': error, 'extra': extra}
    return json.dumps(dictionary)
