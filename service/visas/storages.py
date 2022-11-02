from service.db import db_session
from service.errors import NotFoundError
from service.models import Visa


class VisaStorage:
    name = 'visas'

    def add(self, country_id: int, name: str, desc: str) -> Visa:
        entity = Visa(country_id=country_id, name=name, desc=desc)

        db_session.add(entity)
        db_session.commit()

        return entity
