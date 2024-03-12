from sqlalchemy.orm import Mapped, relationship, mapped_column

from .registry import mapper_registry


@mapper_registry.mapped_as_dataclass
class Subject:
    __tablename__ = "Subject"

    id: Mapped[int] = mapped_column("SubjectId", primary_key=True)
    name: Mapped[str] = mapped_column("Name")

    schedules: Mapped[list["Schedule"]] = relationship(
        back_populates="subject", default_factory=lambda: []
    )
