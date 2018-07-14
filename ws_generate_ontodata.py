import json
import sys
import os
sys.path.append(os.path.dirname(__file__))
from pucp_automatic_annotation import annotateDocumentsInList

# params:
# filepath
# concept list

def service(request_body):
    docList = request_body['source']
    ontoId = request_body['ontologyid']
    type = request_body["generateKnowledge"]
    extra = ""
    error = ""
    result = annotateDocumentsInList(docList,ontoId, type)
    dictionary = {'result': result, 'error': error, 'extra': extra}
    return json.dumps(dictionary)
