from fastapi import APIRouter, HTTPException, Path
from fastapi import Depends
from config import SessionLocal
from sqlalchemy.orm import Session
from schemas import BookSchema, Request, Response, RequestBook

import crud

router = APIRouter()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/create")
async def create_service(request, db: Session = Depends(get_db)):
    crud.create(db, book=request.parameter)
    return Response(status="Ok",
                    code="200",
                    message="").dict(exclude_none=True)
