from pydantic import BaseModel


class Country(BaseModel):
    uid: int
    name: str
    desc: str
