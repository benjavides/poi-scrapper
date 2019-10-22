> Scrapper que permite obtener puntos de interés en las comunas de Santiago.

# Setup

Crear un proyecto en Google Cloud

Activar la API de Google Places

Generar una API_KEY

Reemplazar esa API_KEY en la línea 90 de `poi.py`

```
python poi.py
```

# Output

La salida son los archivos `points_of_interest.json` y `points_of_interest.csv` codificado en UTF-8.

Formato del json:

```json
{
    "La Reina": {
        "Estadio Banco Central": {
            "id": "ChIJ3acDXlTOYpYRyN9BDmhbdGk",
            "direccion": "Príncipe de Gales 6030, La Reina, Región Metropolitana",
            "comuna": "La Reina",
            "tipo": [
                "stadium",
                "point_of_interest",
                "establishment"
            ],
            "lat": -33.4373338,
            "lng": -70.5707422,
            "ciudad": "Santiago",
            "icono": "https://maps.gstatic.com/mapfiles/place_api/icons/generic_business-71.png"
        },
        "Parque Padre Hurtado": {...},
	},
	"Pudahuel":{...
	},
}
```

Formato de csv:

| Nombre | Comuna | Direccion | Tipos | Lng  | Lat  | Ciudad | Icono | Id   |
| ------ | ------ | --------- | ----- | ---- | ---- | ------ | ----- | ---- |
|        |        |           |       |      |      |        |       |      |

# Funcionamiento

Usa la función `textsearch` de la [API de google places](https://developers.google.com/places/) para buscar la query "places in [comuna]". Se piden solo lugares que correspondan a las siguientes categorías: 

- tourist_attraction
- hospital
- city_hall
- university
- library
- shopping_mall
- museum
- stadium

[Aqui la lista completa](https://developers.google.com/places/supported_types#table1) de las que se podrían solicitar.

De cada lugar se obtienen los campos:

- Nombre
- Comuna
- Direccion
- Tipos
- Lng
- Lat
- Ciudad
- Icono
- Id (Corresponde al ID único de un lugar en la API de Google Places)

En el resultado **pueden haber lugares repetidos** y cuando se buscan lugares para cierta comuna, puede encontrar lugares de otra. Por eso el valor de la columna comuna se saca de la dirección de cada lugar y no de la comuna utilizada en la query. 

# TO DO

Lo anterior podría mejorarse pasando los parámetros `location` y `radius` en la query. Donde `location` es una tupla de coordenadas y `radius` el radio de búsqueda. Creo que esto podría hacer que aparezcan más resultados porque la API tiene información más exacta con respecto a dónde se busca.

Para hacer esto hay que implementar la función `get_comuna_location(comuna)` y luego pasar su resultado y un `radius` a `search_places_by_query()` .