from flask import Blueprint, request

from service.countries.schemas import Country
from service.countries.storages import DBStorage
from service.errors import AppError
from service.visas.storages import VisaStorage

country_view = Blueprint('countries', __name__)

storage = DBStorage()

visa_storage = VisaStorage()


@country_view.post('/')
def add_country():
    payload = request.json
    if not payload:
        raise AppError('empty payload')

    payload['uid'] = -1
    country = Country(**payload)
    country = storage.add(country)
    return country.dict(), 201


@country_view.get('/')
def get_all():
    countries = storage.get_all()
    return [country.dict() for country in countries], 200


@country_view.get('/<int:uid>')
def get_by_id(uid):
    country = storage.get_by_id(uid)
    return country.dict(), 200


@country_view.put('/<int:uid>')
def update_by_id(uid):
    payload = request.json
    if not payload:
        raise AppError('empty payload')

    country = Country(**payload)
    country = storage.update(uid, country)
    return country.dict(), 200


@country_view.delete('/<int:uid>')
def delete_country(uid):
    storage.delete(uid)
    return {}, 204


@country_view.get('/<int:uid>/visas/')
def get_all_visas(uid):
    visas = visa_storage.get_for_country(uid)
    return [visa.dict() for visa in visas], 200

