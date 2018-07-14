#Author Diego Salas
#Date 11/12/2017
import json
import os
import sys
sys.path.append(os.path.dirname(__file__))
import config
from pucp_automatic_annotation import createBaseOntology

# params:
# filename: ontology name

def service(request_body):
    filename = request_body['filename']
    filepath = config.OntologyDir
    status = 1
    result,filename,uri = createBaseOntology(filename,filepath)
    if not result:
        status = 0
    error = "none"
    extra = ""
    dictionary = {'filepath': result, 'error': error, 'extra': extra, 'url': uri,'filename':filename,'status':status}
    return json.dumps(dictionary)
