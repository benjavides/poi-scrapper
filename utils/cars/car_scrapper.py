
import requests
import json
import csv
from tqdm import tqdm

def pretty_print_request(req):
    #Fuente: https://stackoverflow.com/questions/20658572/python-requests-print-entire-http-request-raw
    print('{}\n{}\r\n{}\r\n\r\n{}'.format(
        '-----------START-----------',
        req.method + ' ' + req.url,
        '\r\n'.join('{}: {}'.format(k, v) for k, v in req.headers.items()),
        req.body,
    ))

def remove_duplicates(seq):
    # Conserva el orden original
    seen = set()
    seen_add = seen.add
    return [x for x in seq if not (x in seen or seen_add(x))]

def get_models(tipo, brand):
    endpoint_url = "http://chileautos.cl/autos/Search/models"
    params = {
            'recordType': tipo,
            'make': brand,
    }
    req = requests.Request('GET', endpoint_url, params=params)
    prepared = req.prepare()
    # pretty_print_request(prepared)
    s = requests.Session()
    res = s.send(prepared)
    results =  json.loads(res.content)["Modelo"]
    models = [item["value"] for item in results if item["value"] != ""]
    return models

def get_brands(tipo):
    endpoint_url = "http://chileautos.cl/autos/Search/makes"
    params = {
            'recordType': tipo
    }
    req = requests.Request('GET', endpoint_url, params=params)
    prepared = req.prepare()
    # pretty_print_request(prepared)
    s = requests.Session()
    res = s.send(prepared)
    results =  json.loads(res.content)["Marca"]
    brands = [item["value"] for item in results if item["value"] != ""]
    brands = remove_duplicates(brands)
    return brands


if __name__ == "__main__":
    tipo = "autos, camionetas y 4x4"
    # marcas = get_brands(tipo)
    # with open("marcas.json", 'w', encoding='utf8') as f:
    #     json.dump(marcas, f)
    with open("marcas.json", 'r', encoding='utf8') as f:
        marcas = json.load(f)
    
    cars = {}
    with open("cars.csv", 'w', newline='', encoding='utf8') as csvfile:
        filewriter = csv.writer(csvfile, delimiter=',')
        filewriter.writerow(['Modelo', 'Marca'])
        
        pbar = tqdm(total=len(marcas))
        for marca in marcas:
            models = get_models(tipo, marca)
            cars[marca] = models
            for model in models:
                model_nice = model.strip()
                filewriter.writerow([model_nice, marca])
            pbar.update()
        pbar.close()
            

    with open("cars.json", 'w', encoding='utf8') as f:
        json.dump(cars, f)

    print(cars)