from service.db import db_session
from service.errors import NotFoundError
from service.models import CountryDB, Visa
from service.visas.schemas import Visa as VisaSchema


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

    def get_for_country(self, uid: int) -> list[VisaSchema]:
        country = CountryDB.query.get(uid)

        if not country:
            raise NotFoundError('countries', uid)

        entities = country.visas

        all_visas = []

        for visa in entities:
            result = VisaSchema(uid=visa.uid,
                    country_id=visa.country_id,
                    name=visa.name,
                    desc=visa.desc,
            )
            all_visas.append(result)

        return all_visas
