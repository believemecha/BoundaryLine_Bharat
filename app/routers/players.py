# app/routers/players.py
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from engine.models import PlayerTable
from app.dependencies import get_db

router = APIRouter(prefix="/players", tags=["Players"])

@router.get("/")
def get_players(db: Session = Depends(get_db)):
    return db.query(PlayerTable).all()
