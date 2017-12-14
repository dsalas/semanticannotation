from cgi import parse_qs, escape
import json
import chatbot_utils as cu
import foursquare as fq
import os
import io
#Params:
#question (String)
#
def getPlaces(dictionary, fname):
        if "question" in dictionary:
                question = dictionary['question'][0]
        else:
                return "{\"error\":\"Missing parameter question.\"}"
        categories = ["comida","cine","bar","tienda"]
        #category = cu.getCategory(question, categories)
        category = "comida"
        latitude = -12.069150
        longitude = -77.078453
        if "latitude" in dictionary:
                latitude = dictionary['latitude'][0]
        if "longitude" in dictionary:
                longitude = dictionary['longitude'][0]
        response = fq.get_venues_by_category_and_ll(category, latitude, longitude)
        saveJson(response, fname)
	return json.dumps(response)

def getRecomendation(dictionary, fname):
        if "question" in dictionary:
                question = dictionary['question'][0]
        else:
                return "{\"error\":\"Missing parameter question.\"}"
	places = loadJson(fname)
	os.remove(fname)
	lowQuestion = question.lower()
	for place in places:
		if place["name"].lower() in lowQuestion:
			return json.dumps(fq.get_venue_features(place["id"]))
	return "{\"error\":\"Place not found.\"}"

def saveJson(dictionary, fname):
    with io.open(fname, 'w', encoding='utf-8') as f:
        f.write(json.dumps(dictionary, ensure_ascii=False))	

def loadJson(fname):
    with open(fname) as json_data:
        d = json.load(json_data)
        return d #print(d)

def service(request_body):
	dictionary = parse_qs(request_body)
	fname = "/var/www/pyapi/scripts/persist/places.json"
	if os.path.isfile(fname):
		#There is a file with places
		return getRecomendation(dictionary, fname)
	else:
		#New start
		return getPlaces(dictionary, fname)
