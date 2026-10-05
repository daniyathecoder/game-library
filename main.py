from pathlib import Path
from fastapi import FastAPI,Form,HTTPException,Request
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from starlette.middleware.sessions import SessionMiddleware

from database import init_database,get_database
from auth import verify_password

from routes.games import router as games_router
from routes.admin import router as admin_router
from routes.content import router as content_router

BASE_DIR = Path(__file__).resolve().parent
FRONTEND_DIR = BASE_DIR.parent / "frontend"
UPLOADS_DIR = BASE_DIR / "uploads"

app = FastAPI(title = "Game Library API",version="1.0")
app.add_middleware(SessionMiddleware,secret_key = "CHANGE-THIS-LATER")
UPLOADS_DIR.mkdir(parents=True,exist_ok = True)
app.mount("/uploads",StaticFiles(directory=UPLOADS_DIR),name = "uploads")
app.mount("/assets",StaticFiles(directory=FRONTEND_DIR),name="assets")
init_database()
app.include_router(games_router)
app.include_router(admin_router)
app.include_router(content_router)

@app.get("/")
def home():
    return FileResponse(FRONTEND_DIR / "index.html")
@app.get("/game")
def game_page():
    return FileResponse(FRONTEND_DIR/"game.html")
@app.get("/admin")
def admin_page():
    return FileResponse(FRONTEND_DIR / "admin.html")
@app.post("/api/auth/login")
def login(request : Request,
          username: str = Form(...),password: str = Form(...)):
    connection = get_database()
    admin = connection.execute("""SELECT * FROM admins WHERE username = ? """, 
                               (username,)).fetchone()
    connection.close()
    if not admin:
        raise HTTPException(status_code = 401,detail="Invalid username or password")
    if not verify_password(password,admin["password_hash"]):
        raise HTTPException(status_code=401,detail = "Invalid password or username")
    request.session["admin_id"]= admin["id"]
    request.session["username"] = admin["username"]
    return{"message": "Login successful",
           "username": admin["username"]}

@app.post("/api/auth/logout")
def logout(request: Request):
    request.session.clear()
    return {"message": "Logged Out"}

@app.get("/api/auth/status")
def auth_status(request: Request):
    admin_id = request.session.get("admin_id")
    return {"logged_in": bool(admin_id),"username": request.session.get("username")}