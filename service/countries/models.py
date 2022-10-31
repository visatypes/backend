from sqlalchemy import Column, Integer, String

from service.countries.db import Base, engine


class Country(Base):
    __tablename__ = 'countries'

    uid = Column(Integer, primary_key=True)
    name = Column(String)
    desc = Column(String)


if __name__ == '__main__':
    Base.metadata.create_all(bind=engine)
