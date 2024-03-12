from sqlalchemy.orm import Session

from pjait_map_backend.models import Student
from pjait_map_common.schemas import CreateUser


def get_student(number: int, db: Session) -> Student | None:
    return db.get(Student, number)


def add_student(schema: CreateUser, db: Session) -> Student:
    student = Student(
        number=schema.number,
        password=schema.password,
        name=schema.name,
        surname=schema.surname,
    )

    db.add(student)
    db.commit()
    db.refresh(student)

    return student
