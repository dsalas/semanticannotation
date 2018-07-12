from cgi import urllib, escape
import json
import os
import io
import sys

sys.path.append('/var/www/pyapi/scripts')
import config
from pucp_automatic_annotation import createBaseOntology
import coruja_database

# params:
# data list
#

def service(request_body):
    body = urllib.parse.parse_qs(request_body)
    filename = body['filename'][0]
    filepath = config.OntologyDir
    status = 1
    result,filename,uri = createBaseOntology(filename,filepath)
    if not result:
        status = 0
    error = "none"
    extra = ""
    dictionary = {'filepath': result, 'error': error, 'extra': extra, 'url': uri,'filename':filename,'status':status}
    return json.dumps(dictionary)
