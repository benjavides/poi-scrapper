import requests
import json
import time
import csv

"""
Recibe un archivo csv en que las filas representan un lugar del que solo se sabe: Nombre, lat, lon
Entrega un archivo csv completado con: Nombre, Comuna, Direccion, Tipos, Lon, Lat, Ciudad, Icono, Id
"""

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
    
    def search_places_by_coordinates(self, lat, lng):
        endpoint_url = "https://maps.googleapis.com/maps/api/geocode/json?"
        latlng = f"{lat},{lng}"
        params = {
            'key': self.apiKey,
            'latlng': latlng,
            'region': 'cl',
            'language': 'es-419',
        }
        #debugear el request
        # req = requests.Request('GET', endpoint_url, params=params)
        # prepared = req.prepare()
        # pretty_print_request(prepared)
        # s = requests.Session()
        # res = s.send(prepared)
        res = requests.get(endpoint_url, params = params)
        results =  json.loads(res.content)
        
        places = []
        # print(f"API response: {results}")
        places.extend(results['results'])
        # time.sleep(2)
        # while "next_page_token" in results:
        #     params['pagetoken'] = results['next_page_token'],
        #     res = requests.get(endpoint_url, params = params)
        #     results = json.loads(res.content)
        #     # print(f"API response: {results}")
        #     places.extend(results['results'])
        #     time.sleep(2)
        return places

if __name__ == "__main__":
    API_KEY = "Reemplazar este string"
    input_csv_path = "Agregados_Manualmente.csv"
    output_csv_path = "Agregados_Manualmente_complete.csv"

    api = GooglePlaces(API_KEY)

    with open(output_csv_path, 'w', newline='', encoding='utf-8') as output_csvfile:
        filewriter = csv.writer(output_csvfile, delimiter=',')
        filewriter.writerow(['Nombre', 'Comuna','Direccion', 'Tipos', 'Lng', 'Lat', 'Ciudad','Icono', 'Id'])
        
        with open(input_csv_path, 'r', newline='', encoding='utf-8') as input_csvfile:
            csv_reader = csv.DictReader(input_csvfile)
            line_count = 0
            for row in csv_reader:
                lat = row["Y"]
                lng = row["X"]
                name = row["Name"]
                results = api.search_places_by_coordinates(lat, lng)
                done = False
                print(" ")
                # print(results)
        
                for address_result in results:
                    if not done:
                        print("")
                        # print(address_result)
                        address = address_result["formatted_address"]
                        comuna = address.split(",")[-3].strip().upper()
                        address = address.rsplit(",", 1)[0]
                        print(f"address: {address}")
                        print(f"comuna: {comuna}")
                        idd = address_result["place_id"]
                        print(f"id: {idd}")
                        filewriter.writerow([name, comuna, address, " ", lng, lat, "SANTIAGO", " ", idd])
                        done = True
                        line_count += 1



    
    
    
   