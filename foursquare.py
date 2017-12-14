# coding=utf-8
import json, requests

def get_venues_by_category_and_ll(categoria, latitud, longitud):
    url = 'https://api.foursquare.com/v2/venues/search'
    switcher = {
        "cine": "4bf58dd8d48988d17f941735",
        "comida": "4d4b7105d754a06374d81259",
        "bar": "4d4b7105d754a06376d81259",
    }
    params = dict(
        client_id='NJOVTHQYG2VBQ2FDLSK1LSQGPAGQHXC01RJIFHMFUDSE5CLY',
        client_secret='WUEZT5RIOLCZRB4NOOPL4HQOUATAGDYGWJTBLWYA3BCBB14W',
        v='20171211',
        #intent="global",
        ll = str(latitud)+","+str(longitud),
        limit = 50,
        radius = 1000,
        #query = venue_name,
        categoryId = switcher.get(categoria,"nothing")
    )
    resp = requests.get(url=url, params=params)
    data = json.loads(resp.text)
    venues = []
    for venue in data['response']['venues']:
        d_venue = {}
        d_venue['id']=venue['id']
        d_venue['name']=venue['name']
        venues.append(d_venue)
    return venues

def get_venues_by_name(venue_name):
    url = 'https://api.foursquare.com/v2/venues/search'
    params = dict(
        client_id='NJOVTHQYG2VBQ2FDLSK1LSQGPAGQHXC01RJIFHMFUDSE5CLY',
        client_secret='WUEZT5RIOLCZRB4NOOPL4HQOUATAGDYGWJTBLWYA3BCBB14W',
        v='20171211',
        near = "Lima,Peru",
        limit = 50,
        query = venue_name,
        categoryId = "4d4b7105d754a06374d81259"
    )
    resp = requests.get(url=url, params=params)
    data = json.loads(resp.text)
    venues = []
    for venue in data['response']['venues']:
        venues.append(venue['id'])
    return venues

def get_venue_features(venue_id):
    url_desc = 'https://api.foursquare.com/v2/venues/'+venue_id
    url_hours = 'https://api.foursquare.com/v2/venues/'+venue_id+'/hours'
    url_menu = 'https://api.foursquare.com/v2/venues/'+venue_id+'/menu'
    params = dict(
        client_id='NJOVTHQYG2VBQ2FDLSK1LSQGPAGQHXC01RJIFHMFUDSE5CLY',
        client_secret='WUEZT5RIOLCZRB4NOOPL4HQOUATAGDYGWJTBLWYA3BCBB14W',
        v='20171211'
    )
    resp_desc = requests.get(url=url_desc, params=params)
    resp_hours = requests.get(url=url_hours, params=params)
    resp_menu = requests.get(url=url_menu, params=params)
    data_desc = json.loads(resp_desc.text)
    data_hours = json.loads(resp_hours.text)
    venues = {}
    v = data_desc['response']['venue']
    v_hours = data_hours['response']['popular']['timeframes']
    venues["id"]=venue_id
    venues["Nombre"] = v.get('name')
    venues["Dirección"]= str(v.get('location').get('address'))+", "+str(v.get('location').get('city'))+", "+v.get('location').get('country')
    venues["Rating"]=str(v.get('rating'))
    venues["Página Web"]=v.get('url')
    for attr in v.get('attributes').get('groups'):
        str_attrb =  ""
        for item in attr.get('items'):
            str_attrb = str_attrb + " " + item.get('displayValue')
        venues[attr.get('name')] = str_attrb
    venues["Teléfono"]=v.get('contact').get('phone')
    horarios = {}
    for day in v_hours:
        str_horario = ''
        flg = 1
        for horario in day['open']:
            if flg == 1:
                str_horario = horario['start'] + "-" + horario['end']
                flg = 0
            else:
                str_horario = str_horario + ", "+ horario['start'] + "-" + horario['end']
        switcher = {
            "1": "Lunes",
            "2": "Martes",
            "3": "Miércoles",
            "4": "Jueves",
            "5": "Viernes",
            "6": "Sábado",
            "7": "Domingo"
        }

        horarios[switcher.get(str(day['days'][0]),"nothing")]= str_horario
    venues["Horarios"] = horarios
    return venues

def get_venue_tips(venue_id):
    url = 'https://api.foursquare.com/v2/venues/'+venue_id+'/tips'
    params = dict(
      client_id='NJOVTHQYG2VBQ2FDLSK1LSQGPAGQHXC01RJIFHMFUDSE5CLY',
      client_secret='WUEZT5RIOLCZRB4NOOPL4HQOUATAGDYGWJTBLWYA3BCBB14W',
      v='20171211',
    )
    resp = requests.get(url=url, params=params)
    data = json.loads(resp.text)
    tips=[]
    for tip in data['response']['tips']['items']:
        tips.append(tip['text'])
    return tips
