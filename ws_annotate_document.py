from cgi import urllib, escape
import json
import os
import io
import sys

sys.path.append(os.path.dirname(__file__))
import config
from pucp_automatic_annotation import annotateDocumentsInPath
import coruja_database
# params:
# type: 0 folder, 1 path, 2 database id
# filepath 
# docid

def service(request_body):
    body = urllib.parse.parse_qs(request_body)
    type = body['type'][0]
    ontoId = body['ontoId'][0]
    ontopath = coruja_database.getOntology(ontoId)
    status = 0	   
    error = "Incorrect type."
    extra = "Current type: " + type
    if (type == '0'):
        error = ""
        filepath = body['source'][0]
        status = annotateDocumentsInPath(filepath,ontopath)
    if (type == '1'):
        error = ""
        filepath = body['source'][0]
        status = annotateDocumentInPath(filepath, ontopath)
    if (type == '2'):
        #TODO: Get document path from BD using docid
        error = ""
        docid = body['source'][0]
        status = 1
    dictionary = {'status': status, 'error': error, 'extra': extra}
    return json.dumps(dictionary)
