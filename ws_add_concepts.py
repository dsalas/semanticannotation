from cgi import urllib, escape
import json
import os
import io
import sys

sys.path.append('/var/www/pyapi/scripts')
import config
from pucp_automatic_annotation import createBaseOntology


# params:
# filepath
# concept list
#

def service(request_body):
    body = urllib.parse.parse_qs(request_body)
    filepath = body['filepath'][0]
    concepts = body['concepts']
    #result = createBaseOntology(filename,filepath)
    error = "none"
    extra = ""
    dictionary = {'concepts': concepts, 'error': error, 'extra': extra}
    return json.dumps(dictionary)
