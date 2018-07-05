from cgi import urllib, escape
import json
import os
import io
import sys

sys.path.append('/var/www/pyapi/scripts')
import config
from pucp_automatic_annotation import getDocuments

# params:
# query

def service(request_body):
    body = urllib.parse.parse_qs(request_body)
    query = body['query'][0]
    status = 1
    results = getDocuments(query)
    error = ""
    dictionary = {'status': status, 'error': error, 'extra': results}
    return json.dumps(dictionary)
