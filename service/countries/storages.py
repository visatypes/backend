from service.countries.schemas import Country as CountrySchema
from service.db import db_session
from service.errors import NotFoundError
from service.models import CountryDB


class DBStorage:
    name = 'countries'

    def add(self, country: CountrySchema) -> CountrySchema:
        entity = CountryDB(name=country.name, desc=country.desc)

        db_session.add(entity)
        db_session.commit()

        return CountrySchema(uid=entity.uid, name=entity.name, desc=entity.desc)

    def get_all(self) -> list[CountrySchema]:
        entities = CountryDB.query.all()

        return [
            CountrySchema(uid=entity.uid, name=entity.name, desc=entity.desc)
            for entity in entities
        ]

    def get_by_id(self, uid: int) -> CountrySchema:
        entity = CountryDB.query.get(uid)
        if not entity:
            raise NotFoundError(self.name, uid)
        return CountrySchema(uid=entity.uid, name=entity.name, desc=entity.desc)

    def update(self, uid: int, country: CountrySchema) -> CountrySchema:
        entity = CountryDB.query.get(uid)
        if not entity:
            raise NotFoundError(self.name, uid)
        entity.name = country.name
        entity.desc = country.desc

        db_session.commit()

        return CountrySchema(uid=entity.uid, name=entity.name, desc=entity.desc)

    def delete(self, uid: int) -> None:
        entity = CountryDB.query.get(uid)

        if not entity:
            raise NotFoundError(self.name, uid)

        db_session.delete(entity)
        db_session.commit()
