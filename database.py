import sqlite3
from pathlib import Path
BASE_DIR = Path(__file__).resolve().parent
DATABASE_PATH = BASE_DIR / "game_platform.db"

def get_connection():
    connection = sqlite3.connect(DATABASE_PATH)
    connection.row_factory = sqlite3.Row
    return connection

def init_database():
    connection = get_connection()
    cursor = connection.cursor()

    #Game Table
    cursor.execute(""" CREATE TABLE IF NOT EXISTS
    games(id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    slug TEXT UNIQUE NOT NULL,
    thumbnail_url TEXT,
    category TEXT NOT NULL,
    playable_url TEXT NOT NULL,
    github_url TEXT,
    category TEXT NOT NULL,
    date_added TEXT NOT NULL,
    published INTEGER DEFAULT 0,
    featured INTEGER DEFAULT 0,
    updated at TEXT NOT NULL)""")

    #ADMIN USRS
    cursor.execute("""CREATE TABLE IF NOT EXISTS
    admin(id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE NOT NULL,
    password_hash TEXT NOT NULL)""")

    #WEBSITE'S EDITABLE CONTEMNT
    cursor.execute("""CREATE TABLE IF NOT EXIDTS
    site_content(content_key TEXT PRIMARY KEY,
    content_value TEXT NOT NULL)""")

    #default website content 
    default_content = {
    "hero_title":"Welcome to Game Universe",
    "hero_subtitle": "Play.Explore.Discover.",
    "announcement" :"NEew games are coming soon!",
    "about_text": "A collection of games built by two creative people: Daniya and Rameesha!!!"
    }
    for key,value in default_content.items():
        cursor.execute("""INSERT OR IGNORE INTO 
        site_content(content_key,content_value)
        VALUES(?,?)""",(key,value))
    connection.commit()
    connection.close()

def get_database():
    return get_connection()