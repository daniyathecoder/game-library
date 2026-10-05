from datetime import datetime
from fastapi import(APIRouter,Depends,File,Form,HTTPException,UploadFile,Request)
from database import get_database
from auth import require_admin

router = APIRouter(prefix = "/api/admin",tags= ["Admin"])
@router.post("/login")
def admin_login(request: Request,
                username:str = Form(...),password:str=Form(...)):
    print("LOGIN REceived")
    print("Username:",username)
    print("Password received:",bool(password))
    return{"messgae": "LOgin request reached backend"}
UPLOAD_DIRECTORY = "uploads/thumbnails"

def create_slug(name:str):
    return(name.lower()
           .strip()
           .replace(" ","-")
           .replace("/","-"))
@router.get("/games")
def admin_get_games(admin_id: int = Depends(require_admin)):
    connection = get_database()
    games = connection.execute(
        """
SELECT *
FROM games
ORDER BY date_added DESC"""    ).fetchall()
    connection.close()
    return[dict(game)for game in games]

@router.post("/games")
async def add_game(
    name:str = Form(...),
    description: str = Form(...),
    category: str = Form(...),
    playable_url: str = Form(...),
    github_url : str = Form(""),
    creator : str = Form(...),
    published: bool = Form(False),
    featured: bool = Form(False),
    thumbnail: UploadFile|None = File(None),
    admin_id: int = Depends(require_admin)

):
    import os
    import uuid
    os.makedirs(UPLOAD_DIRECTORY,exist_ok = True)
    now = datetime.utcnow().isoformat()
    date_added = now[:10]
    slug =create_slug(name)
    connection = get_database()
    existing = connection.execute("SELECT id FROM games WHERE slug = ?",(slug,)).fetchone()
    if existing:
        connection.close()
        raise HTTPException(status_code= 400,detail = "A game with this name already exists.")
    thumbnail_url = ""
    if thumbnail:
        extension = os.path.splitext(thumbnail.fileneme)[1].lower()
        allowed_extensions = [".png",".jpg",".jpeg",".webp"]
        if extension not in allowed_extensions:
            connection.close()
            raise HTTPException(status_code=400,detail="Invalid thumbnail format.")
        filename=(str(uuid.uuid4())+extension)
        file_path = os.path.join(UPLOAD_DIRECTORY,filename)
        contents = await thumbnail.read()
        with open(file_path,"wb")as file:
           file.write(contents)
           thumbnail_url = ("/uploads/thumbnails/"+filename)
           connection.execute("""INSRT INTO games(
           name,slug,description,thumbnail_url,category,playable_url,github_url,creator,date_added,published,featured,play_count,sreated_at,updated_at)
           Values(?,?,?,?,?,?,?,?,?,?,?,0,?,?)""",
           (name,slug,description,thumbnail_url,category,playable_url,github_url,creator,date_added,int(published),int(featured),now,now))
           connection.commit()
           game_id = connection.execute("SELECT last_insert_rowid()").fetchone()[0]
           connection.close()
           return{"message":"Game added successfully","game_id":game_id}
@router.put("/games/{game_id}")
async def edit_game(
    game_id: int,
    name:str = Form(...),
    description: str = Form(...),
    category: str = Form(...),
    playable_url: str = Form(...),
    github_url: str = Form(""),
    creator : str = Form(...),
    featured: bool = Form(False),
    thumbnail: UploadFile|None=File(None),
    admin_id : int = Depends(require_admin)
):
    import os
    import uuid
    connection = get_database()
    game = connection.execute("SELECT * FROM games WHERE id = ?",(game_id,)).fetchone()
    if not game:
        connection.close()
        raise HTTPException(status_code=404,detail="Game not Found")
    thumbnail_url = game["thumbnail_url"]
    if thumbnail:
        os.makedirs(UPLOAD_DIRECTORY,exist_ok = True)
        extension = os.path.splitext(thumbnail.filename)[1].lower()
        allowed_extensions = [ ".png",".jpg",".jpeg",".webp"]
        if extension not in allowed_extensions:
         connection.close()
         raise HTTPException(status_code=400,detail="Invalid thumnail format.")
        filename = (str(uuid.uuid4())+extension)
        file_path = os.path.join(UPLOAD_DIRECTORY,filename)
        contents = await thumbnail.read()
        with open(file_path,"wb") as file:
            file.write(contents)
        thumbnail_url = ("/uploads/thumbnails/" + filename)
        now = datetime.utcnow().isoformat()
        connection.execute("""UPDATE games
        SET
        name = ?,
        slug = ?,
        description = ?,thumbnail_url = ?,category = ?, playable_url = ?,github_url = ?,creator = ?,featured = ?,
        updated_at = ?
        WHERE id = ? """,(
            name,create_slug(name),description,thumbnail_url,category,playable_url,github_url,creator,int(featured),now,game_id))
        
        connection.commit()
        connection.close()
        return{"message":"Game updated successfully"}

@router.patch("/games/{game_id}?publish")
def change_publish_staatus(game_id : int,published: bool,admin_id : int = Depends(require_admin)):
    connection = get_database()
    game = connection.execute("SELECT id FROM games WHERE id = ?",(game_id,)).fetchone()
    if not game:
        connection.close()
        raise HTTPException(status_code=404,detail="Game not found.")
    connection.execute("""UPDATE games SET published = ?,updated_st ?
    WHERE id = ?
    """,(int(published),datetime.utcnow().isoformat(),game_id))
    connection.commit()
    connection.close()
    return{"message":"PUBLISH status updated","published" : published}
@router.delete("/games/{game_id}")
def delete_game(game_id:int,admin_id :int=Depends(require_admin)):
    connection = get_database()
    game = connection.execute("SELECT id FROM games WHERE id = ?",(game_id,)).fetchone()
    if not game:
       connection.close()
       raise HTTPException(status_code=404,detail="Game not Found.")
    connection.execute("DELETE FROM games WHERE id = ?",(game_id,))
    connection.commit()
    connection.close()
    return{"message": "Game deleted successfully"}

@router.put("/content/{content_key}")
def update_content(content_key : str,content_value: str=Form(...),
                   admin_id: int = Depends(require_admin)):
    connection = get_database()
    connection.execute("""
    INSRT INTO site_content(content_key,content_value)Values(?,?) ON CONFLICT(content_key) DO UPDATE SET 
    content_value = excluded.content_value""",(content_key,content_value))

    connection.commit()
    connection.close()
    return{"message": "Website content updated"}