import foursquare as fq

for venue in fq.get_venues_by_category_and_ll("comida",-12.069150, -77.078453):
    print(venue)
#print(fq.get_venue_features("4b99a9f9f964a5209c8a35e3"))
#hola