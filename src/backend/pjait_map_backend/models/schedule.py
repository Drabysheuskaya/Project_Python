from sqlalchemy.orm import Mapped, relationship, mapped_column
from sqlalchemy.sql.schema import ForeignKey

from .registry import mapper_registry


@mapper_registry.mapped_as_dataclass
class Schedule:
    __tablename__ = "Schedule"

    start: Mapped[int] = mapped_column("Start")
    end: Mapped[int] = mapped_column("End")

    student_id: Mapped[int] = mapped_column("Student", ForeignKey("Student.Number"))
    student: Mapped["Student"] = relationship(back_populates="schedules")

    subject_id: Mapped[int] = mapped_column("Subject", ForeignKey("Subject.SubjectId"))
    subject: Mapped["Subject"] = relationship(back_populates="schedules")

    room_id: Mapped[int] = mapped_column("Room", ForeignKey("Room.RoomId"))
    room: Mapped["Room"] = relationship(back_populates="schedules")

    id: Mapped[int | None] = mapped_column(
        "ScheduleId", primary_key=True, autoincrement=True, default_factory=lambda: None
    )
