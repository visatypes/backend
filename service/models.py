from sqlalchemy import Column, ForeignKey, Integer, String, UniqueConstraint
from sqlalchemy.orm import relationship

from service.db import Base, engine

MAX_DESC_LEN = 4000


class CountryDB(Base):
    __tablename__ = 'countries'

    uid = Column(Integer, primary_key=True)
    name = Column(String(length=20), nullable=False)
    desc = Column(String(length=MAX_DESC_LEN))

    visas = relationship('Visa')

    __table_args__ = (
        UniqueConstraint('name', name='сountry_name_uniq'),
    )


class Visa(Base):
    __tablename__ = 'visas'

    uid = Column(Integer, primary_key=True)
    country_id = Column(Integer, ForeignKey('countries.uid'), nullable=False)
    name = Column(String(length=100), nullable=False)
    desc = Column(String(length=MAX_DESC_LEN))

    __table_args__ = (
        UniqueConstraint('country_id', 'name', name='visas_country_id_name_uniq'),
    )


if __name__ == '__main__':
    Base.metadata.create_all(bind=engine)
