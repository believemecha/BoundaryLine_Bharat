# app/presenters/batsman_stats/get_batsman_stats.py

from sqlalchemy.orm import Session
from app.models import FormatwiseBatsmanStatsTable

def get_batsman_stats_presenter(format_id: int | None, player_id: int, db: Session):
    query = db.query(FormatwiseBatsmanStatsTable).filter(
        FormatwiseBatsmanStatsTable.batsman_id == player_id
    )

    # Optional filter by format (T20, ODI, Test)
    if format_id is not None:
        query = query.filter(FormatwiseBatsmanStatsTable.format_id == format_id)

    stats = query.all()

    return {
        "player_id": player_id,
        "format_id": format_id,
        "stats": stats
    }
