> Obtiene los modelos y marcas de todos los autos, camionetas y 4x4 en chileautos.cl

```shell
python car_scrapper.py
```

## Output

Un archivo csv con las siguientes columnas

| Modelo | Marca     |
| ------ | --------- |
| Corsa  | Chevrolet |
| ...    | ...       |

## End points usados

make = marcas
type = tipo de auto

**Obtener los modelos**

```
http://chileautos.cl/autos/Search/Models&recordType={{type}}&make={{make}}
```

**Obtener las marcas**

```
http://chileautos.cl/autos/Search/Makes&recordType={{type}}
```

