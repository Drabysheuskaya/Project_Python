from sqlalchemy.orm import Mapped, relationship, mapped_column

from .registry import mapper_registry

from sqlalchemy.orm import registry

reg = registry()


@mapper_registry.mapped_as_dataclass
class Student:
    __tablename__ = "Student"

    number: Mapped[int] = mapped_column("Number", primary_key=True)
    password: Mapped[str] = mapped_column("Password")
    name: Mapped[str] = mapped_column("Name")
    surname: Mapped[str] = mapped_column("Surname")

    schedules: Mapped[list["Schedule"]] = relationship(
        back_populates="student", default_factory=lambda: []
    )
