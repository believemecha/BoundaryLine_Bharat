from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db

from app.presenters.batsman_stats.get_batsman_stats_presenter import get_batsman_stats_presenter
from app.response_formatter import render_success, render_error


router = APIRouter(prefix="/batsman_stats", tags=["Batsman Stats"])

#Gets batsman stats by player_id and optional format_id
@router.get("/{player_id}")
def get_batsman_stats(player_id: int, format_id: int | None = None, db: Session = Depends(get_db)):
    data = get_batsman_stats_presenter(format_id, player_id, db)
    return render_success(data=data)

@router.get("/{player_id}/detailed")
def get_detailed_batsman_stats(player_id: int, db: Session = Depends(get_db)):
    try:
        # Placeholder for detailed stats logic
        detailed_stats = {
            "player_id": player_id,
            "details": "Detailed stats would be here"
        }
        return render_success(data=detailed_stats)
    except Exception as e:
        return render_error(message="Failed to fetch detailed stats", details=str(e))
