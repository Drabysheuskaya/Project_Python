from pydantic import BaseModel


class Position(BaseModel):
    x: int
    y: int


class ClassLocation(BaseModel):
    room: str
    file: str
    pos: Position  # x and y coordinates on the image


class Room(BaseModel):
    id: int
    name: str
