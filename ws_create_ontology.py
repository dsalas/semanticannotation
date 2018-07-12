from cgi import urllib, escape
import json
import os
import io
import sys

sys.path.append('/var/www/pyapi/scripts')
import config
from pucp_automatic_annotation import createBaseOntology


# params:
# data list
#

def service(request_body):
    filename = body['filename']
    filepath = config.OntologyDir
    status = 1
    result,filename,url = createBaseOntology(filename,filepath)
    if not result:
        status = 0
    error = "none"
    extra = ""
    dictionary = {'filepath': result, 'error': error, 'extra': extra, 'url': url,'filename':filename,'status':status}
    return json.dumps(dictionary)
