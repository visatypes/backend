from flask import Flask, request
from pydantic import ValidationError

from service.countries.schemas import Country
from service.countries.storages import LocalStorage
from service.errors import AppError

app = Flask(__name__)

storage = LocalStorage()


def handle_app_error(error: AppError):
    return {'error': str(error)}, error.code


def handle_valid_error(error: ValidationError):
    return {'error': str(error)}, 400


app.register_error_handler(AppError, handle_app_error)
app.register_error_handler(ValidationError, handle_valid_error)


@app.post('/api/countries/')
def add_country():
    payload = request.json
    if not payload:
        raise AppError('empty payload')

    payload['uid'] = -1
    country = Country(**payload)
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


@app.put('/api/countries/<int:uid>')
def update_by_id(uid):
    payload = request.json
    if not payload:
        raise AppError('empty payload')

    country = Country(**payload)
    country = storage.update(uid, country)
    return country.dict(), 200


@app.delete('/api/countries/<int:uid>')
def delete_country(uid):
    storage.delete(uid)
    return {}, 204
