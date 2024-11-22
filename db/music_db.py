import sqlite3
import os
from flask import g , Flask 
from mutagen.flac import FLAC
from datetime import datetime, timedelta, timezone
from downloader import download_and_process_audio



#specifiy app


app = Flask("sangeet")



# db path

DB_path = os.path.join(os.getcwd() , "Databases","music_history.db")
MUSIC_DIR = os.getenv("MUSIC_DIR")

def downshare(video):
    video_id = video
    url = f"https://www.youtube.com/watch?v={video_id}"

    try:
        output_path = download_and_process_audio(url, ['musixmatch', 'lrclib', 'netease', 'megalobiz', 'genius'])
        filename = os.path.basename(output_path)
        return filename
    except Exception as e:
        return 0
    

def get_db():
    if 'db' not in g:
        g.db = sqlite3.connect(DB_path)
        g.db.row_factory = sqlite3.Row
    return g.db

def init_search_history_db():
    with app.app_context():
        db = get_db()
        c = db.cursor()
        c.execute('''CREATE TABLE IF NOT EXISTS listening_history
                     (id INTEGER PRIMARY KEY AUTOINCREMENT,
                      user_id INTEGER,
                      filename TEXT,
                      timestamp DATETIME,
                      position FLOAT,
                      FOREIGN KEY (user_id) REFERENCES users (id))''')
        c.execute('''CREATE TABLE IF NOT EXISTS song_stats
                     (user_id INTEGER,
                      filename TEXT,
                      title TEXT,
                      artist TEXT,
                      total_listens INTEGER DEFAULT 0,
                      total_time FLOAT DEFAULT 0,
                      last_listened DATETIME,
                      last_position FLOAT DEFAULT 0,
                      PRIMARY KEY (user_id, filename),
                      FOREIGN KEY (user_id) REFERENCES users (id))''')
        db.commit()


def update_history(filename , position , user_id):
  

    db = get_db()
    c = db.cursor()

    try:
        audio = FLAC(os.path.join(MUSIC_DIR, filename))
        title = audio.get('title', [filename])[0]
        artist = audio.get('artist', ['Unknown Artist'])[0]
    except Exception as e:
        print(f"Error reading metadata: {str(e)}")
        title = filename
        artist = 'Unknown Artist'

    c.execute('INSERT INTO listening_history (user_id, filename, timestamp, position) VALUES (?, ?, ?, ?)',
              (user_id, filename, datetime.now(timezone.utc), position))

    c.execute('''INSERT OR REPLACE INTO song_stats
                 (user_id, filename, title, artist, total_listens, total_time, last_listened, last_position)
                 VALUES (?, ?, ?, ?,
                         COALESCE((SELECT total_listens FROM song_stats WHERE user_id = ? AND filename = ?), 0) + 1,
                         COALESCE((SELECT total_time FROM song_stats WHERE user_id = ? AND filename = ?), 0) + ?,
                         ?, ?)''',
              (user_id, filename, title, artist, user_id, filename, user_id, filename, position, datetime.now(timezone.utc), position))

    db.commit()

    return "success"

def listening_history():
    user_id = g.user['id']  # Get the user ID from g.user
    db = get_db()
    c = db.cursor()

    c.execute('''SELECT h.filename, h.timestamp, h.position, s.title, s.artist
                 FROM listening_history h
                 LEFT JOIN song_stats s ON h.filename = s.filename AND h.user_id = s.user_id
                 WHERE h.user_id = ?
                 ORDER BY h.timestamp DESC
                 LIMIT 50''', (user_id,))
    history = [dict(row) for row in c.fetchall()]

    return history


def save_search(query):
    user_id = g.user['id']
    db = get_db()
    c = db.cursor()
    c.execute('INSERT INTO search_history (user_id, query, timestamp) VALUES (?, ?, ?)',
              (user_id, query, datetime.now(timezone.utc)))
    db.commit()
    return "success"



def lastplay(user_id):
    db = get_db()
    try:
        c = db.cursor()
        c.execute('''
            SELECT h.filename, h.timestamp, h.position, s.title, s.artist
            FROM listening_history h
            LEFT JOIN song_stats s ON h.filename = s.filename AND h.user_id = s.user_id
            WHERE h.user_id = ?
            ORDER BY h.timestamp DESC
            LIMIT 1
        ''', (user_id,))
        last_played = c.fetchone()
        
        if last_played and os.path.exists(os.path.join(MUSIC_DIR, last_played['filename'])):
            return os.path.join(MUSIC_DIR, last_played['filename'])
        else:
            return os.path.join(MUSIC_DIR, downshare("23R-OmEqspU"))
    except Exception as e:
        print(f"Error in lastplay(): {e}")
        return os.path.join(MUSIC_DIR, downshare("23R-OmEqspU"))
    finally:
        c.close()


def all_songs(search_term):
    songs = []
    for filename in os.listdir(MUSIC_DIR):
        if filename.endswith('.flac'):
            filepath = os.path.join(MUSIC_DIR, filename)
            audio = FLAC(filepath)
            title = audio.get('title', [filename])[0]
            artist = audio.get('artist', ['Unknown Artist'])[0]
            if search_term in title.lower() or search_term in artist.lower() or not search_term:
                file_size = os.path.getsize(filepath)

                file_name = os.path.basename(filename)
                name_without_extension = os.path.splitext(file_name)[0]
                thumbnail_url = f"https://img.youtube.com/vi/{name_without_extension}/0.jpg"

                songs.append({
                    'filename': filename,
                    'title': title,
                    'artist': artist,
                    'album': audio.get('album', ['Unknown Album'])[0],
                    'year': audio.get('date', ['Unknown Date'])[0],
                    'genre': audio.get('genre', ['Unknown Genre'])[0],
                    'size': file_size,
                    'thumbnail': thumbnail_url
                })

    db = get_db()
    c = db.cursor()
    for song in songs:
        filename = song['filename']
        c.execute('SELECT total_listens, total_time, last_listened, last_position FROM song_stats WHERE filename = ?', (filename,))
        stats = c.fetchone()
        if stats:
            song['total_listens'] = stats['total_listens']
            song['total_time'] = stats['total_time']
            song['last_listened'] = stats['last_listened']
            song['last_position'] = stats['last_position']
        else:
            song['total_listens'] = 0
            song['total_time'] = 0
            song['last_listened'] = None
            song['last_position'] = 0

    return songs









def cleanup():
    try:
        # Delete all files in the MUSIC_DIR
        for filename in os.listdir(MUSIC_DIR):
            file_path = os.path.join(MUSIC_DIR, filename)
            if os.path.isfile(file_path):
                os.remove(file_path)

        # Clear the database
        db = get_db()
        c = db.cursor()
        c.execute('DELETE FROM listening_history')
        c.execute('DELETE FROM song_stats')
        c.execute('DELETE FROM search_history')
        db.commit()

        return {"message": "Library cleaned up successfully"}
    except Exception as e:
        return {"error": str(e)}




init_search_history_db()




