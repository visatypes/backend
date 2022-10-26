from service.countries.schems import Country
from service.errors import AppError, NotFoundError

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
        if uid not in self.countries:
            raise NotFoundError('countries', uid)
        return self.countries[uid]

    def update(self, uid: int, country: Country) -> Country:
        if uid not in self.countries:
            raise NotFoundError('countries', uid)
        self.countries[uid] = country
        return country

    def delete(self, uid: int) -> None:
        if uid not in self.countries:
            raise NotFoundError('countries', uid)
        self.countries.pop(uid)