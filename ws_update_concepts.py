import json
import sys
import os
sys.path.append(os.path.dirname(__file__))
from pucp_automatic_annotation import updateConcepts

# params:
# query

def service(request_body):
    docId = request_body['documentid']
    ontoId = request_body['ontologyid']
    concepts = request_body['concepts']
    status = updateConcepts(docId,ontoId,concepts)
    error = ""
    dictionary = {'status': status, 'error': error, 'status': status}
    return json.dumps(dictionary)
