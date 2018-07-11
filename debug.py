from api_log import log
import os
import textract
import string
import getpass
path = "/var/www/pyapi/scripts/persist/debug/test_docs/pc_test"
files = [f for f in os.listdir(path) if os.path.isfile(path + "/" + f)]
files = filter(lambda f: f.endswith(('.pdf', '.PDF')), files)
for file in files:
    filepath = path + "/" + file
    #print(filepath)

filename = "/var/www/pyapi/scripts/persist/debug/test_docs/pc_test/Practicas pasadas\INF220 2011-2 P2 --- .pdf"
text = textract.process(filename)
decoded = text.decode("utf-8")
print(decoded)
#log(getpass.getuser())
