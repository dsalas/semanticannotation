import json
import sys
sys.path.append('/var/www/pyapi/scripts')
import config
from pucp_automatic_annotation import annotateDocumentsInList


# params:
# filepath
# concept list
#

def service(request_body):
    docList = request_body['source']
    ontoId = request_body['ontologyid']
    result = 1
    extra = ""
    error = ""
    annotateDocumentsInList(docList,ontoId)
    dictionary = {'result': result, 'error': error, 'extra': extra}
    return json.dumps(dictionary)
