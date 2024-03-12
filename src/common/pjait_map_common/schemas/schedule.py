from pydantic import BaseModel


class Schedule(BaseModel):
    subject_id: int
    room_id: int
    weekday: int
    start: str  # start and end in "hh:mm" format,
    end: str  # so for now they are str


class NewSchedule(BaseModel):
    student_id: int
    schedule: Schedule


class ScheduleData(Schedule):
    schedule_id: int
