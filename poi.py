# Fuente: https://python.gotrained.com/google-places-api-extracting-location-data-reviews/

import requests
import json
import time
import csv

def pretty_print_request(req):
    #Fuente: https://stackoverflow.com/questions/20658572/python-requests-print-entire-http-request-raw
    print('{}\n{}\r\n{}\r\n\r\n{}'.format(
        '-----------START-----------',
        req.method + ' ' + req.url,
        '\r\n'.join('{}: {}'.format(k, v) for k, v in req.headers.items()),
        req.body,
    ))

class GooglePlaces(object):
    def __init__(self, apiKey):
        super(GooglePlaces, self).__init__()
        self.apiKey = apiKey

    def get_comuna_location(self, comuna):
        pass

    def search_places_by_query(self, query, types):
        endpoint_url = "https://maps.googleapis.com/maps/api/place/textsearch/json"
        places = []
        params = {
            'key': self.apiKey,
            'query': query,
            'types': types,
            'region': 'cl',
            'language': 'es-419',
            # 'location': location,
            # 'radius': radius
        }
        #debugear el request
        # req = requests.Request('GET', endpoint_url, params=params)
        # prepared = req.prepare()
        # pretty_print_request(prepared)
        # s = requests.Session()
        # res = s.send(prepared)
        res = requests.get(endpoint_url, params = params)
        results =  json.loads(res.content)
        # print(f"API response: {results}")
        places.extend(results['results'])
        time.sleep(2)
        while "next_page_token" in results:
            params['pagetoken'] = results['next_page_token'],
            res = requests.get(endpoint_url, params = params)
            results = json.loads(res.content)
            # print(f"API response: {results}")
            places.extend(results['results'])
            time.sleep(2)
        return places

    def search_places_by_coordinate(self, location, radius, types=[]):
        endpoint_url = "https://maps.googleapis.com/maps/api/place/nearbysearch/json"
        places = []
        params = {
            'location': location,
            'radius': radius,
            'types': types,
            'key': self.apiKey
        }
        res = requests.get(endpoint_url, params = params)
        results =  json.loads(res.content)
        places.extend(results['results'])
        time.sleep(2)
        while "next_page_token" in results:
            params['pagetoken'] = results['next_page_token'],
            res = requests.get(endpoint_url, params = params)
            results = json.loads(res.content)
            places.extend(results['results'])
            time.sleep(2)
        return places

    def get_place_details(self, place_id, fields):
        endpoint_url = "https://maps.googleapis.com/maps/api/place/details/json"
        params = {
            'placeid': place_id,
            'fields': ",".join(fields),
            'key': self.apiKey
        }
        res = requests.get(endpoint_url, params = params)
        place_details =  json.loads(res.content)
        return place_details

if __name__ == "__main__":
    API_KEY = "key goes here"
    api = GooglePlaces(API_KEY)
    types = ["tourist_attraction", "city_hall", "university", "library", "shopping_mall", "museum", "stadium"] #https://developers.google.com/places/supported_types#table1
    fields = ["name", "formatted_address", "geometry", "type", "icon"]
    output_filename = "points_of_interest"
    # radius = 5000 #radio en el que se buscaran lugares dentro de la comuna (con centro en el location de comuna)

    #leemos comunas
    with open('comunas.json', 'r') as f:
        comunas = json.load(f)
    # comunas = ["Providencia"]

    points_of_interest = {}
    with open(output_filename+".csv", 'w', newline='', encoding='utf8') as csvfile:
        filewriter = csv.writer(csvfile, delimiter=',')
        filewriter.writerow(['Nombre', 'Comuna','Direccion', 'Tipos', 'Lng', 'Lat', 'Ciudad','Icono', 'Id'])
        for comuna in comunas:
            print(f"\ncomuna: {comuna}")
            query = f"places in '{comuna}'"
            # location = api.get_comuna_location(comuna)
            for tipo in types: #Solo se puede especificar un tipo a la vez
                print(f"--tipo: {tipo}")
                places = api.search_places_by_query(query, [tipo])

                points_of_interest[comuna] = {}
                for place in places:
                    # details = api.get_place_details(place['place_id'], fields) #no es necesario, usamos solo info básica que ya tenemos
                    try:
                        address = place['formatted_address']
                    except KeyError:
                        address = ""

                    try:
                        tipos = place['types']
                    except KeyError:
                        tipos = []

                    try:
                        icono = place['icon']
                    except KeyError:
                        icono = ""

                    try:
                        idd = place['place_id']
                    except KeyError:
                        idd = ""

                    try:
                        location = place['geometry']["location"]
                        lat = location["lat"]
                        lng = location["lng"]
                    except KeyError:
                        lat = ""
                        lng = ""

                    try:
                        name = place['name']
                        print(f"lugar: {name}")
                        try:
                            comuna = address.split(",")[-2].strip()
                        except IndexError:
                            pass
                        points_of_interest[comuna][name] = {}
                        points_of_interest[comuna][name]["id"] = idd
                        points_of_interest[comuna][name]["direccion"] = address
                        points_of_interest[comuna][name]["comuna"] = comuna
                        points_of_interest[comuna][name]["tipo"] = tipos
                        points_of_interest[comuna][name]["lat"] = lat
                        points_of_interest[comuna][name]["lng"] = lng
                        points_of_interest[comuna][name]["ciudad"] = "Santiago"
                        points_of_interest[comuna][name]["icono"] = icono
                        filewriter.writerow([name, comuna, address, tipos, lat, lng, "Santiago", icono, idd])
                    except KeyError:
                        name = ""

    # print(points_of_interest)
    with open(output_filename+".json", 'w', encoding='utf8') as f:
        json.dump(points_of_interest, f)
