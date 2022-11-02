from pydantic import BaseModel


class Visa(BaseModel):
    uid: int
    country_id: int
    name: str
    desc: str

    class Config:
        orm_mode=True
