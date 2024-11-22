from functools import lru_cache
import sqlite3
from flask import Flask
from concurrent.futures import ThreadPoolExecutor
import yt_dlp

app = Flask("sangeet")
executor = ThreadPoolExecutor(max_workers=20)

def get_db_radio():
    db = sqlite3.connect('sangeet_radio.db')
    db.row_factory = sqlite3.Row
    return db

def init_db_radio():
    with app.app_context():
        db = get_db_radio()
        db.execute('''CREATE TABLE IF NOT EXISTS play_history
                      (id INTEGER PRIMARY KEY AUTOINCREMENT,
                       video_id TEXT UNIQUE,
                       title TEXT,
                       artist TEXT,
                       thumbnail TEXT,
                       timestamp DATETIME DEFAULT CURRENT_TIMESTAMP)''')
        db.commit()

@lru_cache(maxsize=100)
def get_audio_url(video_id):
    ydl_opts = {
        'format': 'bestaudio/best',
        'quiet': True,
        'no_warnings': True,
 
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(f"https://www.youtube.com/watch?v={video_id}", download=False)
        return info['url']

def get_song_info(video_id):
    ydl_opts = {
        'quiet': True,

        'no_warnings': True,
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(f"https://www.youtube.com/watch?v={video_id}", download=False)
        return {
            'title': info.get('title', 'Unknown Title'),
            'artist': info.get('artist', 'Unknown Artist'),
            'thumbnail': f"https://img.youtube.com/vi/{video_id}/0.jpg"
        }

init_db_radio()