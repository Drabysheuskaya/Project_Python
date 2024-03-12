from fastapi import APIRouter, Depends, Response
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session

import pjait_map_backend.crud as crud
from pjait_map_backend.dependencies import DatabaseManager
from pjait_map_common.schemas import ClassLocation, Position, Room


router = APIRouter(prefix="/room", dependencies=[Depends(DatabaseManager.get_db)])


@router.get("/")
async def get_rooms(db: Session = Depends(DatabaseManager.get_db)) -> list[Room]:
    return [Room(id=r.id, name=r.name) for r in crud.get_rooms(db)]


@router.get("/{room_id}")
async def get_room_details(
    room_id: int, db: Session = Depends(DatabaseManager.get_db)
) -> Response:
    room = crud.get_room(room_id, db)

    if room is None:
        return Response(status_code=404)

    location = ClassLocation(
        room=room.name,
        file=room.location.file.name,
        pos=Position(x=room.location.x, y=room.location.y),
    )

    return JSONResponse(content=jsonable_encoder(location))
