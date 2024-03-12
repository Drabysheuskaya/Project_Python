from pydantic import BaseModel


class User(BaseModel):
    number: int
    password: str


class CreateUser(User):
    name: str
    surname: str

class UserData(BaseModel):
    number: int
    name: str
    surname: str
