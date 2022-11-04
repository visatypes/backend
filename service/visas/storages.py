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

    def get_all(self) -> list[Visa]:
        return Visa.query.all()

    def get_by_id(self, uid: int) -> Visa:
        entity = Visa.query.get(uid)

        if not entity:
            raise NotFoundError(self.name, uid)

        return entity

    def update(self, uid: int, name: str, desc: str) -> Visa:
        entity = Visa.query.get(uid)
        if not entity:
            raise NotFoundError(self.name, uid)

        entity.name = name
        entity.desc = desc

        db_session.commit()

        return entity

    def delete(self, uid: int) -> None:
        entity = Visa.query.get(uid)
        if not entity:
            raise NotFoundError(self.name, uid)

        db_session.delete(entity)
        db_session.commit()
