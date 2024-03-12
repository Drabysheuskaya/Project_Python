import os

from fastapi import Depends, FastAPI
from fastapi.staticfiles import StaticFiles

from pjait_map_backend.dependencies import DatabaseManager
from pjait_map_backend.routers import (
    schedule_router,
    room_router,
    subject_router,
    student_router,
)


app = FastAPI(dependencies=[Depends(DatabaseManager.get_db)])

app.mount("/img", StaticFiles(directory="static/img"), name="img")

app.include_router(schedule_router)
app.include_router(room_router)
app.include_router(subject_router)
app.include_router(student_router)


@app.on_event("startup")
async def startup() -> None:
    default_url = "sqlite:///test.db"
    db_url = os.getenv("DB_URL", default_url)

    DatabaseManager.connect(db_url)


@app.on_event("shutdown")
async def shutdown() -> None:
    DatabaseManager.disconnect()
