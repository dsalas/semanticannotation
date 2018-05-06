from cgi import parse_qs, escape
import json
import os 
import io
import sys
sys.path.append('/var/www/pyapi/scripts')
import pucp_automatic_annotation as paa

def service(request_body):
	dictionary = parse_qs(request_body)
	document = dictionary['document'][0]
	concepts = dictionary['concepts[]']
	paa.createOntology(document,concepts)	
	data = {'result': 'success'}
	return json.dumps(data)
