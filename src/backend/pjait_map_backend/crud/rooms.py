from sqlalchemy import select
from sqlalchemy.orm import Session

from pjait_map_backend.models import Room


def get_rooms(db: Session) -> list[Room]:
    return list(db.scalars(select(Room)))


def get_room(id: int, db: Session) -> Room | None:
    return db.get(Room, id)
