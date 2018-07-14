import json
import os
import sys

sys.path.append(os.path.dirname(__file__))
from pucp_automatic_annotation import annotateDocumentsInPath
import coruja_database
# params:
# source: filepath of doc repository
# ontoId: id of ontology used

def service(request_body):
    ontoId = request_body['ontoId']
    ontopath = coruja_database.getOntology(ontoId)
    extra = ""
    error = ""
    filepath = request_body['source']
    status = annotateDocumentsInPath(filepath,ontopath)
    dictionary = {'status': status, 'error': error, 'extra': extra}
    return json.dumps(dictionary)
