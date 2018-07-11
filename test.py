#Author Diego Salas
#Date 11/12/2017 
#path /test
from cgi import parse_qs, escape
import json
import sys
sys.path.append('/var/www/pyapi/scripts')

def service(request_body):
    dictionary = parse_qs(request_body)
    dictionary["extra"] = sys.version
    return json.dumps(dictionary)
