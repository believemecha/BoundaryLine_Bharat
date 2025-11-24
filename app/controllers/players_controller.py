from fastapi import APIRouter, Depends
from fastapi import Query


from sqlalchemy.orm import Session
from app.database import get_db

from app.presenters.players.list_players_presenter import list_players_presenter
from app.response_formatter import render_success, render_error


router = APIRouter(prefix="/players", tags=["Batsman Stats"])

#List Players with optional filters
@router.get("/")
def list_players(
    db: Session = Depends(get_db),
    country: str | None = Query(None),
    search: str | None = Query(None),
    page: int = Query(1, ge=1),
    page_size: int = Query(10, ge=1, le=100),
):
    data = list_players_presenter(db, country=country, search=search, page=page, page_size=page_size)
    return render_success(data=data)


