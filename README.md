# Shiptrader API

## Starships endpoints:

- Get list of all Starships:

`GET: /api/starships/`

- Get list of Starships filtered by class:

`GET: /api/starships/?starship_class=<str>`

- Get Starship by id:

`GET: /api/starships/<id>`

- Create Starship:

`POST: /api/starships/`

```
payload: {
            'cargo_capacity': <int>,
            'crew': <int>,
            'hyperdrive_rating': <float>,
            'length': <int>,
            'manufacturer': <str>,
            'passengers': <int>,
            'starship_class': <str>
        }
```

- Delete Starship:

`DELETE: /api/starships/<id>`

## Listings Endpoints


- Create listing:

`POST: /api/listings/`

```
payload: {
            'name': <int>,
            'ship_type': <id>,
            'price': <int>
         }
```

- Get list of all listings:

`GET: /api/listings/`

- Get list of all listings sorted by price:

ascending order:

`GET: /api/listings/?ordering=price`

descending order:

`GET: /api/listings/?ordering=-price`

- Get list of all listings sorted by time:

ascending order:

`GET: /api/listings/?ordering=created_at`

descending order:

`GET: /api/listings/?ordering=-created_at`

- Get listing by id:

`GET: /api/listing/<id>/`

- Update listing

`PATCH: /api/listing/<id>/`

to activate or deactivate listing:
 
 ```payload={'active': True/False}```


## Importing data from SWAPI

`python manage.py import_starships`
