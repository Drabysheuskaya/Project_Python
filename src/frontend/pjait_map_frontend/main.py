from typing import Annotated, Any

import requests
import datetime
from fastapi import FastAPI, Form, Request, Response, Depends
from fastapi.responses import RedirectResponse
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import parse_raw_as

from pjait_map_common.schemas import *
from uuid import UUID
from session import create_session, delete_session, SessionData, cookie, verifier

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="templates")


@app.get("/login", response_class=HTMLResponse)
def login(request: Request) -> HTMLResponse:
    return templates.TemplateResponse("login.html", {"request": request})


@app.post("/login", response_class=HTMLResponse)
async def login(
    username: Annotated[str, Form()], password: Annotated[str, Form()], request: Request
) -> Response:
    request_user = User(number=int(username[1:]), password=password)
    response = requests.post("http://localhost:8001/student/", json=request_user.dict())

    if response.status_code == 200:
        user_data = parse_raw_as(UserData, response.text)
        data = SessionData(student_id=user_data.number, name=user_data.name, surname=user_data.surname)
        response = RedirectResponse("/")

        await create_session(response, data)

        return response
    elif response.status_code == 404:
        error_message = "No such user"
        return templates.TemplateResponse(
            "login.html", {"request": request, "error_message": error_message}
        )
    elif response.status_code == 401:
        error_message = "Wrong password"
        return templates.TemplateResponse(
            "login.html", {"request": request, "error_message": error_message}
        )
    else:
        error_message = "Unable to login, try again later"
        return templates.TemplateResponse(
            "login.html", {"request": request, "error_message": error_message}
        )


@app.get("/signup", response_class=HTMLResponse)
def signup(request: Request) -> HTMLResponse:
    return templates.TemplateResponse("signup.html", {"request": request})


@app.post("/signup", response_class=HTMLResponse)
async def signup(
    username: Annotated[str, Form()],
    password: Annotated[str, Form()],
    name: Annotated[str, Form()],
    surname: Annotated[str, Form()],
    request: Request,
) -> Response:
    request_user = User(number=int(username[1:]), password=password)
    request_create = CreateUser(
        number=int(username[1:]), password=password, name=name, surname=surname
    )
    response = requests.post("http://localhost:8001/student/", json=request_user.dict())
    if response.status_code == 403:
        error_message = "User already exists"
        return templates.TemplateResponse(
            "signup.html", {"request": request, "error_message": error_message}
        )

    response_create = requests.post(
        "http://localhost:8001/student/new", json=request_create.dict()
    )
    message = "User created"
    return templates.TemplateResponse(
        "signup.html", {"request": request, "message": message}
    )


@app.post("/", dependencies=[Depends(cookie)])
@app.get("/", dependencies=[Depends(cookie)])
async def index(request: Request, session_data: SessionData | None = Depends(verifier)):
    if session_data is None:
        return RedirectResponse("/login")
    response = requests.get(
        f"http://localhost:8001/schedule/student/{session_data.student_id}"
    )
    response_schedules = parse_raw_as(list[Schedule], response.text)
    weekday = datetime.datetime.today().weekday()

    today = [s for s in response_schedules if s.weekday == weekday]
    locations = []
    subjects = []

    for schedule in today:
        resp = requests.get(f"http://localhost:8001/room/{schedule.room_id}")
        locations.append(parse_raw_as(ClassLocation, resp.text))

        resp = requests.get(f"http://localhost:8001/subject/{schedule.subject_id}")
        subjects.append(parse_raw_as(Subject, resp.text))

    subjects_today = zip(today, locations, subjects)

    return templates.TemplateResponse(
        "main.html",
        {"request": request, "subjects_today": subjects_today, "user": session_data, "backend": "http://127.0.0.1:8001"},
    )


@app.get("/logout", dependencies=[Depends(cookie)])
async def logout(session_id: UUID = Depends(cookie)):
    response = RedirectResponse("/login")
    await delete_session(response, session_id)
    return response


def find_by_id(l: list[Any], id: int) -> Any | None:
    for e in l:
        if e.id == id:
            return e
    return None

@app.post("/timetable", dependencies=[Depends(cookie)])
@app.get("/timetable", dependencies=[Depends(cookie)])
def get_timetable(
    request: Request, session_data: SessionData | None = Depends(verifier)
):
    if session_data is None:
        return RedirectResponse("/login")

    response = requests.get(
        f"http://localhost:8001/schedule/student/{session_data.student_id}"
    )
    response_s = requests.get(f"http://localhost:8001/subject/")
    response_r = requests.get(f"http://localhost:8001/room/")

    response_schedules = parse_raw_as(list[ScheduleData], response.text)
    response_subjects = parse_raw_as(list[Subject], response_s.text)
    response_rooms = parse_raw_as(list[Room], response_r.text)

    days = []
    for day in range(5):
        l = []
        for s in response_schedules:
            if s.weekday == day:
                room = find_by_id(response_rooms, s.room_id)
                subject = find_by_id(response_subjects, s.subject_id)
                l.append((s, room, subject))
        days.append(l)

    days_of_the_week = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]
    indices = [0, 1, 2, 3, 4]

    return templates.TemplateResponse(
        "timetable.html",
        {
            "request": request,
            "days": zip(days, days_of_the_week),
            "week": zip(indices,days_of_the_week),
            "subjects": response_subjects,
            "rooms": response_rooms,
        },
    )


@app.post("/timetable/{x}", dependencies=[Depends(cookie)])
def new_timetable(
    subject_id: Annotated[str, Form()],
    room_id: Annotated[str, Form()],
    weekday: Annotated[str, Form()],
    start: Annotated[str, Form()],
    end: Annotated[str, Form()],
    request: Request,
    session_data: SessionData | None = Depends(verifier),
):
    schedule = Schedule(
        subject_id=int(subject_id),
        room_id=int(room_id),
        weekday=int(weekday),
        start=start,
        end=end,
    )
    request_data = NewSchedule(student_id=session_data.student_id, schedule=schedule)

    response = requests.post("http://localhost:8001/schedule/", json=request_data.dict())
    
    return RedirectResponse("/timetable")


@app.delete("/timetable/{schedule_id}",  dependencies=[Depends(cookie)])
def delete_timetable(schedule_id: int, session_data: SessionData = Depends(verifier)):
    response = requests.delete(
        f"http://localhost:8001/schedule/{session_data.student_id}/{schedule_id}"
    )

    return Response(status_code=200)
