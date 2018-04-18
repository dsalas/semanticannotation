from cgi import urllib, escape
import json
import os
import io
import sys

sys.path.append('/var/www/pyapi/scripts')
import config
from pucp_automatic_annotation import anotate


# params:
# data list
#

def service(request_body):
    body = urllib.parse.parse_qs(request_body)
    filename = body['filename'][0]
    filepath = config.OntologyDir
    error = "none"
    extra = ""
    dictionary = {'filepath': filepath + filename, 'Error': error, 'Extra': extra}
    return json.dumps(dictionary)
