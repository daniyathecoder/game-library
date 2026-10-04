from fastapi import APIRouter
from database import get_database

router = APIRouter(prefix = "/api/content",
                   tags= ["Website Content"])
@router.get("")
def get_content():
    connection = get_database()
    rows = connection.execute("""SELECT content_key,content_value
    From site_content """).fetchall()
    connection.close()
    return{row["content_key"]:row["content_value"]for row in rows}