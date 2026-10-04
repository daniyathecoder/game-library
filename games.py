from datetime import datetime
from fastapi import APIRouter,HTTPException
from database import get_database

router = APIRouter(prefix = "/api/games",tags = ["Games"])
@router.get("")
def get_games(category: str |None = None,
              q: str |None = None):
    connection = get_database()
    query = """SELECT * FROM games 
    WHERE published = 1"""
    parameters =[]
    if category :
        query += "AND category = ?"
        parameters.append(category)
    if q:
        query += "AND name LIKE ?"
        parameters.append(f"%{q}%")
    query += " ORDER BY featured DESC, date_added DESC"
    games = connection.execute(query,parameters).fetchall()
    connection.close()
    return[dict(game) for game in games]
@router.get("/{game_id}")
def get_game(game_id : int):
    connection = get_database()
    game = connection.execute("""SELECT *
    FROM games
    WHERE id = ? AND published = 1""",(game_id,)).fetchone()
    connection.close()
    if not game:
        raise HTTPException (status_code = 404,detail = "Game not Found")
    return dict(game)

@router.post("/{game_id}/play")
def record_play(game_id: int ):
    connection  = get_database()
    game = connection.execute("""Select id
    FROM games
    WHERE id = ? And published = 1 """,(game_id,)).fetchone()
    if not game:
        connection.close()

        raise HTTPException(status_code = 404 ,detail = "Game not found.")
    connection.execute("""UPDATE games
    SET play_count = play_count +1,updated_at = ?
    WHERE id = ? """,(datetime.utcnow().isoformat(),game_id))
    connection.commit()
    updated = connection.execute("""Select play_count
    FROM games
    WHERE id = ? """,(game_id,)).fetchone()
    connection.close()
    return{"game_id" : game_id,
           "play_count" : updated["play_count"]}