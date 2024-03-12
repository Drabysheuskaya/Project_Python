from fastapi import APIRouter, Depends, Response
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session

import pjait_map_backend.crud as crud
from pjait_map_backend.dependencies import DatabaseManager
from pjait_map_common.schemas import Subject


router = APIRouter(prefix="/subject", dependencies=[Depends(DatabaseManager.get_db)])


@router.get("/")
async def get_subjects(db: Session = Depends(DatabaseManager.get_db)) -> list[Subject]:
    return [Subject(id=s.id, name=s.name) for s in crud.get_subjects(db)]


@router.get("/{subject_id}")
async def get_subject(
    subject_id: int, db: Session = Depends(DatabaseManager.get_db)
) -> Response:
    subject = crud.get_subject(subject_id, db)

    if subject is None:
        return Response(status_code=404)

    schema = Subject(id=subject.id, name=subject.name)

    return JSONResponse(content=jsonable_encoder(schema))
