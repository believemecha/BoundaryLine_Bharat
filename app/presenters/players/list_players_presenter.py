from sqlalchemy.orm import Session
from app.models import PlayerTable

def list_players_presenter(db: Session, country: str | None, search: str | None, page: int, page_size: int):
    query = db.query(PlayerTable)

    # Filter by country if provided
    if country is not None:
        query = query.filter(PlayerTable.country.ilike(f"%{country}%"))

    # Search by name (case-insensitive)
    if search is not None:
        query = query.filter(PlayerTable.name.ilike(f"%{search}%"))

    total_count = query.count()

    # Pagination
    offset = (page - 1) * page_size
    players = query.offset(offset).limit(page_size).all()

    return {
        "page": page,
        "page_size": page_size,
        "total_records": total_count,
        "total_pages": (total_count + page_size - 1) // page_size,
        "players": players
    }
