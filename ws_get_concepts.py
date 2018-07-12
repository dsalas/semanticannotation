import json
import sys

sys.path.append('/var/www/pyapi/scripts')
import config
from pucp_automatic_annotation import getConcepts

# params:
# query

def service(request_body):
    docId = request_body['documentid']
    ontoId = request_body['ontologyid']
    status = 1
    results = getConcepts(docId,ontoId)
    error = ""
    dictionary = {'status': status, 'error': error, 'result': results}
    return json.dumps(dictionary)
