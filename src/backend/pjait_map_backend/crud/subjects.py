from sqlalchemy import select
from sqlalchemy.orm import Session

from pjait_map_backend.models import Subject


def get_subject(id: int, db: Session) -> Subject | None:
    return db.get(Subject, id)


def get_subjects(db: Session) -> list[Subject]:
    return list(db.scalars(select(Subject)))
