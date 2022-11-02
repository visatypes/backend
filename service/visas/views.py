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
