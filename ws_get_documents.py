#Author Diego Salas
#Date 11/12/2017
import json
import os
import sys
sys.path.append(os.path.dirname(__file__))
from pucp_automatic_annotation import getDocuments

# params:
# query

def service(request_body):
    query = request_body['query']
    status = 1
    results = getDocuments(query)
    error = ""
    dictionary = {'status': status, 'error': error, 'extra': results}
    return json.dumps(dictionary)
