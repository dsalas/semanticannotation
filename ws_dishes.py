#!/usr/bin/python3
from cgi import parse_qs, escape
import json
import os 
import io
import sys
#params:
#data list
#

def service(request_body):
	data = 3 / 2
	dictionary = {'data': data}	
	return json.dumps(dictionary)
