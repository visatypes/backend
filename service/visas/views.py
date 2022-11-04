from flask import Blueprint, request
from service.errors import AppError
from service.visas.schemas import Visa
from service.visas.storages import VisaStorage

visa_view = Blueprint('visas', __name__)

storage = VisaStorage()


@visa_view.post('/')
def add_visa():
    payload = request.json
    if not payload:
        raise AppError('empty payload')

    payload['uid'] = -1
    visa = Visa(**payload)
    entity = storage.add(country_id=visa.country_id, name=visa.name, desc=visa.desc)
    visa = Visa.from_orm(entity)
    return visa.dict(), 201


@visa_view.get('/')
def get_all():
    entities = storage.get_all()
    visas = [Visa.from_orm(entity) for entity in entities]
    return [visa.dict() for visa in visas], 200


@visa_view.get('/<int:uid>')
def get_by_id(uid):
    entity = storage.get_by_id(uid)
    visa = Visa.from_orm(entity)
    return visa.dict(), 200


@visa_view.put('/<int:uid>')
def update(uid):
    payload = request.json

    if not payload:
        raise AppError('empty payload')

    payload['uid'] = uid
    visa = Visa(**payload)
    entity = storage.update(
        uid,
        name=visa.name,
        desc=visa.desc,
    )
    visa = Visa.from_orm(entity)
    return visa.dict(), 200


@visa_view.delete('/<int:uid>')
def delete(uid):
    storage.delete(uid)
    return {}, 204
