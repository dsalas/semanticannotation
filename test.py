#Author Diego Salas
#Date 11/12/2017 
#path /test
from cgi import parse_qs, escape
import json

def service(request_body):
	dictionary = parse_qs(request_body)
	return json.dumps(dictionary)
	#param = dictionary['param']
	#return "{\"test\":\"this is a test json: " + param +  "\"}"
