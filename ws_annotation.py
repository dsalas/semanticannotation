from cgi import parse_qs, escape
import json
import os 
import io
#params:
#data list
#

def service(request_body):
	filename = ""
	error = "none"
	extra = ""
	tempPdfPath = '/var/www/pyapi/scripts/persist'
	filepath = os.path.join(tempPdfPath,'new.pdf')
	#  if os.path.exists('persist'):
	#	extra = "Persist is a valid dir"
	extra = os.getcwd()
	try:
		file = open(filepath, 'wb+')	
		file.write(request_body)
		filename = file.name
	except IOError as e:
		error = e.strerror
	dictionary = {'Created': filename, 'Error': error, 'Extra': extra}
	return json.dumps(dictionary)