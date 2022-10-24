from itertools import count
from flask import Flask, request
from typing import Any
from pydantic import BaseModel, ValidationError

app = Flask(__name__)

Json = dict[int, Any]

class Country(BaseModel):
    uid: int
    name: str
    desc: str

class LocalStorage:
    def __init__(self):
        self.countries: dict[int, Country] = {}
        self.last_uid = 0

    def add(self, country: Country) -> Country:
        self.last_uid += 1
        country.uid = self.last_uid
        self.countries[self.last_uid] = country
        return country

    def get_all(self) -> list[Country]:
        return list(self.countries.values())

    def get_by_id(self, uid: int) -> Country:
        return self.countries[uid]

    def update(self, uid: int, country: Country) -> Country:
        self.countries[uid] = country
        return country

    def delete(self, uid: int) -> None:
        self.countries.pop(uid)


storage = LocalStorage()

@app.post('/api/countries/')
def add_country():
    payload = request.json
    payload["uid"] = -1
    try:
        country = Country(**payload)
    except ValidationError as error:
        return {"error": str(error)}, 400
    country = storage.add(country)
    return country.dict(), 201

@app.get('/api/countries/')
def get_all():
    countries = storage.get_all()
    return [country.dict() for country in countries], 200
    

@app.get('/api/countries/<int:uid>')
def get_by_id(uid):
    country = storage.get_by_id(uid)
    return country.dict(), 200
    #return storage.get_by_id(uid), 200

@app.put('/api/countries/<int:uid>')
def update_by_id(uid):
    payload = request.json
    try:
        country = Country(**payload)
    except ValidationError as error:
        return {"error": str(error)}, 400
    country = storage.update(uid, country)
    return country.dict(), 200

@app.delete('/api/countries/<int:uid>')
def delete_country(uid):
    storage.delete(uid)
    return {}, 204


