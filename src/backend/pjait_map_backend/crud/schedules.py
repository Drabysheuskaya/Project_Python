from sqlalchemy import delete
from sqlalchemy.orm import Session

from pjait_map_backend.dependencies import to_seconds
from pjait_map_backend.models import Schedule, Subject, Student, Room
from pjait_map_common.schemas import NewSchedule, ScheduleData


def get_schedule(id: int, db: Session) -> Schedule | None:
    return db.get(Schedule, id)


def add_schedule(data: NewSchedule, db: Session) -> Schedule:
    start = to_seconds(data.schedule.weekday, data.schedule.start)
    end = to_seconds(data.schedule.weekday, data.schedule.end)

    schedule = Schedule(
        start=start,
        end=end,
        student_id=data.student_id,
        student=db.get(Student, data.student_id),
        subject_id=data.schedule.subject_id,
        subject=db.get(Subject, data.schedule.subject_id),
        room_id=data.schedule.room_id,
        room=db.get(Room, data.schedule.room_id),
    )

    db.add(schedule)
    db.commit()
    db.refresh(schedule)

    return schedule


def update_schedule(data: ScheduleData, db: Session) -> Schedule | None:
    start = to_seconds(data.weekday, data.start)
    end = to_seconds(data.weekday, data.end)

    schedule = db.get(Schedule, data.schedule_id)

    if schedule is None:
        return None

    schedule.start = start
    schedule.end = end
    schedule.subject_id = data.subject_id
    schedule.subject = db.get(Subject, data.subject_id)
    schedule.room_id = data.room_id
    schedule.room = db.get(Room, data.room_id)

    db.commit()

    return schedule


def delete_schedule(schedule_id: int, db: Session) -> None:
    stmt = delete(Schedule).where(Schedule.id == schedule_id)
    db.execute(stmt)
    db.commit()
