from cgi import parse_qs, escape
import json
import os
import io
import sys

sys.path.append('/var/www/pyapi/scripts')
from pucp_automatic_annotation import anotate


# params:
# data list
#

def service(request_body):
    dictionary = parse_qs(request_body)
    filename = ""
    # dictionary = {'Created': filename, 'Error': error, 'Extra': extra}
    return json.dumps(dictionary)
