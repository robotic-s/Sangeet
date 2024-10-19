import os
import sqlite3
from flask import Flask, render_template, send_file, jsonify, request, g, redirect, render_template_string, session
from mutagen.flac import FLAC
from io import BytesIO
import yt_dlp
from datetime import datetime, timedelta
from datetime import datetime, timedelta
from file2 import download_and_process_audio
from pytube import YouTube
import encryption.enc1 as ss
import socket
import shutil
import subprocess
from spotify.mathersd import get_spotify_youtube_matches
import ipaddress
from datetime import datetime, timedelta, timezone
import secrets
import urllib
import base64
import hashlib
import random
import string
import json
import encryption.encryption as enc
from mail import mail as email
from itertools import chain
# auth ones

from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify, send_file, make_response
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
from functools import wraps
import sqlite3
import os
import secrets
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from dotenv import load_dotenv
import re
from PIL import Image
from io import BytesIO
import base64
from itsdangerous import TimedSerializer
from datetime import timedelta

#till here





import base64
import hashlib
import random
import string




from dotenv import load_dotenv


from ytmusicapi import YTMusic
from flask import Flask, render_template, request, jsonify, Response, stream_with_context
from ytmusicapi import YTMusic
import yt_dlp
import requests
from concurrent.futures import ThreadPoolExecutor
import sqlite3
from functools import lru_cache
ytmusic = YTMusic()


load_dotenv()

app = Flask(__name__)
app.secret_key = "mlknlknslnlnldlmde"
#sangeet auth
app.config['UPLOAD_FOLDER'] = 'static/profile_pics'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max-limit
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(days=5)
#till here!!!
app.jinja_env.cache = {}
# Initialize YTMusic
ytmusic = YTMusic()
from functools import wraps
from flask import session, redirect, url_for, flash
# Add these imports if not already present
from flask import make_response, request
from functools import wraps

# Get token database connection

# Generate a new token
def generate_token():
    return secrets.token_urlsafe(32)

# Modified login_required decorator
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        token = request.cookies.get('auth_token')
        if token:
            user = verify_auth_token(token)
            if user:
                g.user = user
                return f(*args, **kwargs)
        flash('Please log in to access this page.', 'error')
        return redirect(url_for('login'))
    return decorated_function

# Configuration
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
MUSIC_DIR = os.path.join(BASE_DIR, "downloads")
DB_PATH = os.path.join(BASE_DIR, 'music_history.db')
DEFAULT_ARTWORK_PATH = os.path.join(BASE_DIR, 'static', 'default_artwork.jpg')
def get_db():
    if 'db' not in g:
        g.db = sqlite3.connect(DB_PATH)
        g.db.row_factory = sqlite3.Row
    return g.db
# Ensure necessary directories exist
os.makedirs(MUSIC_DIR, exist_ok=True)
HOST = os.getenv("host")

def s(stringsd , option):
    if option == 1:
       vals = ss.enc(stringsd)
    elif  option == 2:
        vals = ss.dec(stringsd)
    return vals
sharesession = s("share" , 1)




@app.route('/sangeet/playback/history/"<path:song>"')
def history_playback_sangeet(song):
    if os.path.exists(os.path.join(MUSIC_DIR , song + ".flac")):
        path = os.path.join(MUSIC_DIR , song + ".flac")
        session[sharesession] = s(path , 1)
        return jsonify({
            'status': 'started dom',
            'message': f'Started playback ',
            'file_path': path
        }), 200
    else:
        runtime = downshare(song)
        his = runtime
        runtime = os.path.join(MUSIC_DIR , runtime)
        print(runtime)
        if not runtime == 0:
            session[sharesession] = s(runtime , 1)
            return jsonify({
            'status': 'started dom',
            'message': f'Started playback ',
            'file_path': his
        }), 200
        else:
            return jsonify({
            'status': 'failed to start dom',
            'message': f'playback resp error from ssd19 ',
            'file_path': his
        }), 500
def downshare(video):
    video_id = video
    url = f"https://www.youtube.com/watch?v={video_id}"

    try:
        output_path = download_and_process_audio(url, ['musixmatch', 'lrclib', 'netease', 'megalobiz', 'genius'])
        filename = os.path.basename(output_path)
        return filename
    except Exception as e:
        return 0
def get_ip():
    try:
        # Create a socket and connect to an external server
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except Exception as e:
        print(f"An error occurred: {e}")
        return None
    

import sqlite3
from flask import g, request, make_response, redirect, url_for, flash
from datetime import datetime, timedelta
import secrets

# ... (keep your existing imports)

def get_db_auth():
    if 'auth_db' not in g:
        g.auth_db = sqlite3.connect('users.db')
        g.auth_db.row_factory = sqlite3.Row
    return g.auth_db

def get_token_db():
    if 'token_db' not in g:
        g.token_db = sqlite3.connect('tokens.db')
        g.token_db.row_factory = sqlite3.Row
    return g.token_db

def init_db_auth():
    with app.app_context():
        db = get_db_auth()
        db.execute('''CREATE TABLE IF NOT EXISTS users 
                      (id INTEGER PRIMARY KEY, 
                       name TEXT, 
                       email TEXT UNIQUE, 
                       password TEXT, 
                       profile_pic TEXT, 
                       status TEXT DEFAULT 'pending',
                       otp TEXT,
                       email_verified INTEGER DEFAULT 0)''')
        db.commit()

def init_token_db():
    with app.app_context():
        db = get_token_db()
        db.execute('''CREATE TABLE IF NOT EXISTS auth_tokens
                      (id INTEGER PRIMARY KEY,
                       user_id INTEGER,
                       token TEXT UNIQUE,
                       expires_at DATETIME,
                       FOREIGN KEY (user_id) REFERENCES users (id))''')
        db.commit()

def create_auth_token(user_id):
    token = secrets.token_urlsafe(32)
    expires_at = datetime.now(timezone.utc) + timedelta(days=5)
    db = get_token_db()
    db.execute('INSERT INTO auth_tokens (user_id, token, expires_at) VALUES (?, ?, ?)',
               (user_id, token, expires_at))
    db.commit()
    return token

# Call these initialization functions when your app starts
init_db_auth()
init_token_db()

@app.route('/')
def index():
    if g.user:
        # User is authenticated
        if "reserve" in session:
            if session["reserve"] == "reserve":
                session["yes"] = "yes"
                session.pop("reserve", None)
                return render_template("index.html", hostid=os.getenv("host"), user=g.user)
            else:
                session["yes"] = "yes"
                session[sharesession] = s(lastplay(g.user['id']), 1) 
                return render_template("index.html", hostid=os.getenv("host"), user=g.user)
        else:
            session["yes"] = "yes"
            session[sharesession] = s(lastplay(g.user['id']), 1)    
            return render_template("index.html", user=g.user)
    else:
        # User is not authenticated
        return redirect(url_for("login"))

# ... (rest of your code)
@app.route('/sangeet/share/music/"<path:song>"')
def sharesd(song):
    if os.path.exists(os.path.join(MUSIC_DIR , song + ".flac")):
        path = os.path.join(MUSIC_DIR , song + ".flac")
        print("path" +path)
        session[sharesession] = s(path , 1)
        session["reserve"] = "reserve"
        return redirect("/")
    else:
        runtime = downshare(song)
        runtime = os.path.join(MUSIC_DIR , runtime)
        print("runtime" +runtime)
        if not runtime == 0:
            session[sharesession] = s(runtime , 1)
            session["reserve"] = "reserve"
            return redirect("/")
        else:
            return "something went wrong dear sorry!"

@app.route('/checkcustom')
def check_custom():
    if sharesession in session:
        if session[sharesession]  != None:


            return "check"
        else:
            return "no check"


    else:
        return "non check"
from flask import g

@app.route('/update_history', methods=['POST'])
@login_required
def update_history():
    data = request.json
    filename = data['filename']
    position = data['position']
    user_id = g.user['id']  # Get the user ID from g.user

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

    return jsonify({"status": "success"})

@app.route('/listening_history')
@login_required
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

    return jsonify(history)

# Update the database schema to include user_id in the search_history table
def init_search_history_db():
    with app.app_context():
        db = get_db()
        c = db.cursor()
        c.execute('''CREATE TABLE IF NOT EXISTS search_history
                     (id INTEGER PRIMARY KEY AUTOINCREMENT,
                      user_id INTEGER,
                      query TEXT,
                      timestamp DATETIME,
                      FOREIGN KEY (user_id) REFERENCES users (id))''')
        db.commit()

# Update the save_search route to include user_id
@app.route('/save_search', methods=['POST'])
@login_required
def save_search():
    query = request.json['query']
    user_id = g.user['id']
    db = get_db()
    c = db.cursor()
    c.execute('INSERT INTO search_history (user_id, query, timestamp) VALUES (?, ?, ?)',
              (user_id, query, datetime.now(timezone.utc)))
    db.commit()
    return jsonify({"status": "success"})

# Update the search_suggestions route to be user-specific
@app.route('/search_suggestions', methods=['GET'])
@login_required
def search_suggestions():
    query = request.args.get('query', '').lower()
    suggestions = ytmusic.get_search_suggestions(query)
    return jsonify(suggestions)
init_search_history_db()



@app.route('/share')
def share():
    # This route will return the metadata for a specific song
    # For demonstration purposes, we'll just return the first song in the MUSIC_DIR
        full_path = s(session[sharesession] , 2)
        session.pop(sharesession , None)
        filepath = full_path
        filename = os.path.basename(full_path)
        audio = FLAC(filepath)
        file_size = os.path.getsize(filepath)
        name_without_extension = os.path.splitext(filename)[0]
        thumbnail_url = f"https://img.youtube.com/vi/{name_without_extension}/0.jpg"

        metadata = {
            'filename': filename,
            'title': audio.get('title', [filename])[0],
            'artist': audio.get('artist', ['Unknown Artist'])[0],
            'album': audio.get('album', ['Unknown Album'])[0],
            'date': audio.get('date', ['Unknown Date'])[0],
            'genre': audio.get('genre', ['Unknown Genre'])[0],
            'bitrate': f"{audio.info.bitrate / 1000:.0f} kbps",
            'sample_rate': f"{audio.info.sample_rate / 1000:.1f} kHz",
            'channels': audio.info.channels,
            'file_size': file_size,
            'duration': audio.info.length,
            'thumbnail': thumbnail_url,
            'download': f'/download/"{filename}"'
        }
        print(metadata)
        return jsonify(metadata)



@app.before_request
def check_auth_token():
    if 'user_id' not in session and 'auth_token' in request.cookies:
        token = request.cookies.get('auth_token')
        user = verify_auth_token(token)
        if user:
            db = get_db_auth()
            # Here, we're using the 'id' from the user object directly
            user_from_db = db.execute('SELECT * FROM users WHERE id = ?', (user['id'],)).fetchone()
    
            if user_from_db and user_from_db['status'] == 'active':
                session['user_id'] = user['id']
                session.permanent = True

def verify_auth_token(token):
    token_db = get_token_db()
    auth_db = get_db_auth()
    token_info = token_db.execute('SELECT user_id, expires_at FROM auth_tokens WHERE token = ?', (token,)).fetchone()
    
    if token_info and datetime.fromisoformat(token_info['expires_at']) > datetime.now(timezone.utc):
        user = auth_db.execute('SELECT * FROM users WHERE id = ?', (token_info['user_id'],)).fetchone()
        return user
    return None

@app.before_request
def load_logged_in_user():
    g.user = None
    token = request.cookies.get('auth_token')
    if token:
        try:
            user = verify_auth_token(token)
            if user:
                g.user = user
            else:
                # Token is invalid or expired, remove it
                response = make_response()
                response.delete_cookie('auth_token')
        except sqlite3.OperationalError as e:
            # Handle database errors gracefully
            print(f"Database error: {e}")
            # You might want to log this error or handle it in some way

# Make sure to initialize your databases
def init_dbs():
    init_db_auth()
    init_token_db()

# Call this function when your app starts
with app.app_context():
    init_dbs()
def init_db():
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
init_db()
def get_upload_year(url):

        # Create a YouTube object
        video = YouTube(url)

        # Get the publish date of the video
        publish_date = video.publish_date

        # Extract the year from the publish date
        upload_year = publish_date.strftime("%Y")

        return upload_year

@app.route('/download/"<filename>"')
def downlsd(filename):
    audio = FLAC(os.path.join(MUSIC_DIR , filename))
    return send_file(os.path.join(MUSIC_DIR , filename) , as_attachment = True , download_name = audio.get('title', [filename])[0] + ".flac")
@app.route('/year/<filename>')
def get_year(filename):
    try:
        year = get_upload_year(f"https://www.youtube.com/watch?v={filename.replace('.flac' , '')}")
        return year
    except Exception as e:
        print(f'Error fetching year for {filename}: {e}')
        return 'Unknown'
# Routes



@app.route('/css/<type>')
def assetssss(type):
    if type == "embeded":
        client_ip = get_client_ip()
        sanitized_ip = sanitize_ip(client_ip)
        filename = f'{sanitized_ip}embed.bin'
        with open(os.path.join("temp", filename), "r") as embedsd:
            embed = embedsd.read()
        if embed == "True":
           with open(os.path.join("temp", filename), "w") as embedsd:
               embedsd.write("False")
           return send_file(os.path.join(os.getcwd(), "doms", "embed.css"))
        else:
            return "not allowed!!"
    else:
        return "bad request!!!"


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


@app.route('/receive/"<path:salt>"/"<path:encrypted_message>"')
def receive(encrypted_message , salt):
    try:
        decoded_message = urllib.parse.unquote(encrypted_message)
        decrypted_message = enc.decrypt(decoded_message, salt)
        user_data = json.loads(decrypted_message)
        session["username"] = s(user_data["username"] , 1)
        session["address"] = s(user_data["address"] , 1)
        session["id"] = s(str(user_data["id"]) ,1)
        session["email"] = s(user_data["email"] , 1)
        session["mobile"] = s(str(user_data["mobile"]) , 1)
        return "okay!!!!!"
    except json.JSONDecodeError:
        return f"Received and decrypted message (not JSON): {decrypted_message}"
    except Exception as e:
        return f"Error processing message: {str(e)}"


@app.route("/pic")
def default_pic():
    return send_file(os.path.join(os.getcwd() , "assets" ,  "default.png"))
@app.route('/css/20/<bn>')
def csssd(bn):
    if "yes" in session:
        if session["yes"] == "yes":
            session.pop("yes" , None)
            if bn == "main":
               return send_file(os.path.join(os.getcwd() ,"css" ,  "index.css") , mimetype = "text/css")
            elif bn == "swap":
               return send_file(os.path.join(os.getcwd() ,"doms" ,  "swap.css") , mimetype = "text/css")
            elif bn == "material":
               return send_file(os.path.join(os.getcwd() ,"doms" ,  "material.css") , mimetype = "text/css")
            elif bn == "chart":
               return send_file(os.path.join(os.getcwd() ,"doms" ,  "chart.js") , mimetype = "text/js")
            elif bn == "embeder":
               return send_file(os.path.join(os.getcwd() ,"doms" ,  "embeder.css") , mimetype = "text/css")
            else:
                return "mdsdnnfljnfljnlj"
        else:
            return "ndknknf"
    else:
        return "noNjknd"
       

@app.route('/all_songs')
def all_songs():
    search_term = request.args.get('search', '').lower()
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

    return jsonify(songs)

@app.route('/v3/search/<knskd>')
def v33(knskd):
    return render_template("embeds.html", hj=knskd)
def get_video_info(video_id):
    try:
        yt = YouTube(f'https://www.youtube.com/watch?v={video_id}')
        return yt.title, yt.author
    except Exception as e:
        print(f"Error getting video info: {e}")
        return None, None
@app.route('/v3/<filename>')
def v3(filename):
    filepath = os.path.join(MUSIC_DIR, filename + ".flac" )
    if not os.path.exists(filepath):
        runtime = downshare(filename)
        if runtime != 0:
            filepath = os.path.join(MUSIC_DIR, filename + ".flac" )
        else:
           filepath = None
    if not filename == None:
        title, artist = get_video_info(filename)
    
        # Generate hash and encoded filename
        hashed_filename, encoded_filename = encrypt_and_hash(filename)
    
        return jsonify({
            "audio_url": f'/v3/audio/"{hashed_filename}"/"{encoded_filename}"',
            "title": title or "Unknown Title",
            "artist": artist or "Unknown Artist",
            "thumbnail": f"https://img.youtube.com/vi/{filename}/0.jpg"
        })
    else:
        return 500

@app.route('/v3/embed/details/sangeet/all/<video_id>')
def guideemvbedsdd(video_id ):
    video_url = f'https://www.youtube.com/watch?v={video_id}'  # Replace with the actual video URL
    
    try:
        # Fetch video details using yt-dlp
        with yt_dlp.YoutubeDL() as ydl:
            info = ydl.extract_info(video_url, download=False)
            
            song_data = {
                'thumbnail_url': info['thumbnail'],
                'title': info['title'],
                'artist_name': info['uploader'],
            }
            session["yes"] = "yes"
            return render_template("renderembedall.html", **song_data, video_id=video_id , hostid = os.getenv("host"))
    except Exception as e:
        return f"Error: {str(e)}"
def get_client_ip():
    # Try to get the IP from X-Forwarded-For header first
    ip = request.headers.get('X-Forwarded-For')
    if ip:
        # X-Forwarded-For can contain multiple IPs; we want the client's original IP
        ip = ip.split(',')[0].strip()
    else:
        # If X-Forwarded-For is not set, fall back to remote address
        ip = request.remote_addr
    
    # Validate and return the IP
    try:
        return str(ipaddress.ip_address(ip))
    except ValueError:
        # If the IP is invalid, return None
        return None
def encrypt_and_hash(input_string):
    # Ensure input_string is actually a string
    input_string = str(input_string)
    
    # Simple encryption (XOR with a random key)
    key = ''.join(random.choices(string.ascii_letters + string.digits, k=16))
    encrypted = ''.join(chr(ord(a) ^ ord(b)) for a, b in zip(input_string, key * len(input_string)))
    
    # Combine encrypted string with key
    combined = encrypted + "||" + key
    
    # Encode to base64
    encoded = base64.b64encode(combined.encode()).decode()
    
    # Generate a hash
    hash_value = hashlib.sha256(encoded.encode()).hexdigest()[:16]
    
    return hash_value, encoded

def decrypt_from_encoded(encoded_string):
    # Decode from base64
    decoded = base64.b64decode(encoded_string).decode()
    
    # Split the encrypted string and key
    encrypted, key = decoded.split("||")
    
    # Decrypt
    decrypted = ''.join(chr(ord(a) ^ ord(b)) for a, b in zip(encrypted, key * len(encrypted)))
    
    return decrypted

def sanitize_ip(ip):
    return ip.replace(':', '_').replace('.', '_')
@app.route('/v3/songs/sangeet/latest/embed/<video_id>')
def embed(video_id):
    client_ip = get_client_ip()
    sanitized_ip = sanitize_ip(client_ip)
    filename = f'{sanitized_ip}embed.bin'
    with open(os.path.join("temp", filename), "w") as embedsd:
        embedsd.write("True")
    return render_template("embeds.html", hj=video_id)
@app.route('/v3/songs/sangeet/latest/embed2/<video_id>')
def embedkdkdkkd(video_id ):
    return render_template("embeds2.html", hj=video_id)
import base64

@app.route('/v3/audio/"<path:audio_hash>"/"<path:encoded>"')
def serve_audio(audio_hash , encoded):
    audio_hash = decrypt_from_encoded(encoded)
    # Map the audio_hash to the actual filename (you might want to use a database for this in a real application)
    # For this example, we'll just use it directly
    filepath = os.path.join(MUSIC_DIR, f"{audio_hash}.flac")
    return send_file(filepath)


@app.route('/stream/<filename>')
def stream_audio(filename):
    filepath = os.path.join(MUSIC_DIR, filename)
    if not os.path.exists(filepath):
        runtime = downshare(filename)
        runtime = os.path.join(MUSIC_DIR , runtime)
        print(runtime)
        if not runtime == 0:
            return send_file(runtime, mimetype='audio/flac'  ,  max_age=31536000)
        else:
           return jsonify({"error": "File not found"}), 404
    return send_file(filepath, mimetype='audio/flac'  ,  max_age=31536000)

@app.route('/artwork/<filename>')
def get_artwork(filename):
    filepath = os.path.join(MUSIC_DIR, filename)
    if not os.path.exists(filepath):
        return send_file(DEFAULT_ARTWORK_PATH, mimetype='image/jpeg')

    file_name = os.path.basename(filepath)
    name_without_extension = os.path.splitext(file_name)[0]
    artwork = f"https://img.youtube.com/vi/{name_without_extension}/0.jpg"
    return artwork

@app.route('/metadata/<filename>')
def get_metadata(filename):
    filepath = os.path.join(MUSIC_DIR, filename)
    if not os.path.exists(filepath):
        return jsonify({"error": "File not found"}), 404

    audio = FLAC(filepath)
    file_size = os.path.getsize(filepath)
    file_name = os.path.basename(filename)
    name_without_extension = os.path.splitext(file_name)[0]
    thumbnail_url = f"https://img.youtube.com/vi/{name_without_extension}/0.jpg"
    addr = get_ip()
    print(request.remote_addr)
    if request.remote_addr == "127.0.0.1":
        addr = "http://127.0.0.1:" + request.environ.get('SERVER_PORT')
    elif request.remote_addr == "localhost":
        addr = "http://localhost:" + request.environ.get('SERVER_PORT')
    else:
        if not addr == None:
            addr = addr + ":" + request.environ.get('SERVER_PORT')
        else:
            addr = "your host!"
    metadata = {
        'filename': filename,
        'title': audio.get('title', [filename])[0],
        'artist': audio.get('artist', ['Unknown Artist'])[0],
        'album': audio.get('album', ['Unknown Album'])[0],
        'date': audio.get('date', ['Unknown Date'])[0],
        'genre': audio.get('genre', ['Unknown Genre'])[0],
        'bitrate': f"{audio.info.bitrate / 1000:.0f} kbps",
        'sample_rate': f"{audio.info.sample_rate / 1000:.1f} kHz",
        'channels': audio.info.channels,
        'file_size': file_size,
        'duration': audio.info.length,
        'thumbnail': thumbnail_url,
        'download' : f'/download/"{filename}"',
        'share' : f'{HOST}/sangeet/share/music/"{name_without_extension}"'
    }
    return jsonify(metadata)


@app.route('/rate', methods=['POST'])
def rate_sangeet():
    data = request.json
    rating = data.get('rating')

    if rating is None or not isinstance(rating, int) or rating < 1 or rating > 5:
        return jsonify({'message': 'Invalid rating. Please provide a number between 1 and 5.'}), 400

    with open("rating.txt" , "a") as rate:
        rate.write(f"{rating} for {lastplay()}")

    return jsonify({'message': 'Your rating has been recorded. Thank you for your feedback!'}), 200
@app.route('/icons/<name>')
def ic(name):
    if name == "hdd":
        return send_file(os.path.join(os.getcwd() , "static" , "hdd.png") ,  mimetype="image/png")
@app.route('/music_stats')
def music_stats():
    total_files = 0
    total_size = 0
    for filename in os.listdir(MUSIC_DIR):
        if filename.endswith('.flac'):
            total_files += 1
            total_size += os.path.getsize(os.path.join(MUSIC_DIR, filename))

    return jsonify({
        'total_files': total_files,
        'total_size': total_size
    })

@app.route('/sangeet/embed/<video_id>')
def embedsharesangeettsong(video_id):
    return render_template("test.html" , vd = video_id)
@app.route('/song_stats/<filename>')
@login_required
def song_stats(filename):
    user_id = session['user_id']  # Get the user ID from the session
    db = get_db()
    c = db.cursor()

    c.execute('SELECT * FROM song_stats WHERE user_id = ? AND filename = ?', (user_id, filename))
    stats = c.fetchone()

    if not stats:
        try:
            audio = FLAC(os.path.join(MUSIC_DIR, filename))
            title = audio.get('title', [filename])[0]
            artist = audio.get('artist', ['Unknown Artist'])[0]
        except Exception as e:
            print(f"Error reading metadata: {str(e)}")
            title = filename
            artist = 'Unknown Artist'

        c.execute('''INSERT INTO song_stats
                     (user_id, filename, title, artist, total_listens, total_time, last_listened, last_position)
                     VALUES (?, ?, ?, ?, 0, 0, NULL, 0)''',
                  (user_id, filename, title, artist))
        db.commit()

        c.execute('SELECT * FROM song_stats WHERE user_id = ? AND filename = ?', (user_id, filename))
        stats = c.fetchone()

    c.execute('SELECT timestamp, position FROM listening_history WHERE user_id = ? AND filename = ? ORDER BY timestamp DESC LIMIT 10', (user_id, filename))
    history = [dict(row) for row in c.fetchall()]

    return jsonify({
        "filename": filename,
        "title": stats['title'],
        "artist": stats['artist'],
        "total_listens": stats['total_listens'],
        "total_time": stats['total_time'],
        "last_listened": stats['last_listened'],
        "last_position": stats['last_position'],
        "history": history
    })

import re
import os

@app.route('/delete_song', methods=['POST'])
def delete_song():
    data = request.json
    filename = data['filename']
    filepath = os.path.join(MUSIC_DIR, filename)

    try:
        # Delete the file from storage
        if os.path.exists(filepath):
            os.remove(filepath)

        # Delete from the database
        db = get_db()
        c = db.cursor()
        c.execute('DELETE FROM listening_history WHERE filename = ?', (filename,))
        c.execute('DELETE FROM song_stats WHERE filename = ?', (filename,))
        db.commit()

        return jsonify({"status": "success", "message": f"Song {filename} deleted successfully"})
    except Exception as e:
        print(e)
        return jsonify({"status": "error", "message": str(e)}), 500
def is_youtube_url(url):
    youtube_regex = (
        r'(https?://)?(www\.)?'
        '(youtube|youtu|youtube-nocookie)\.(com|be)/'
        '(watch\?v=|embed/|v/|.+\?v=)?([^&=%\?]{11})'
    )
    youtube_regex_match = re.match(youtube_regex, url)
    return youtube_regex_match is not None
# @app.route('/search_youtube', methods=['POST'])
# def search_youtube():
#     search_term = request.json['search_term']
#       # Check if it's a Spotify URL
#     spotify_pattern = r'https?://(?:open\.)?spotify\.com/(track|album|playlist)/([a-zA-Z0-9]+)'
#     spotify_match = re.match(spotify_pattern, search_term)
#     if is_youtube_url(search_term):
#         ydl_opts = {
#             'format': 'bestaudio/best',
#             'quiet': True,
#             'no_warnings': True,
#             'extract_flat': 'in_playlist',
#             'skip_download': True,
#         }

#         with yt_dlp.YoutubeDL(ydl_opts) as ydl:
#             info = ydl.extract_info(search_term, download=False)

#         results = []
#         if 'entries' in info:
#             # It's a playlist
#             playlist_title = info.get('title', 'Unknown Playlist')
#             playlist_author = info.get('uploader', 'Unknown Uploader')
#             playlist_thumbnail = f"https://img.youtube.com/vi/{info['entries'][0]['id']}/0.jpg" if info['entries'] else ""

#             # Add playlist metadata as the first item
#             results.append({
#                 'id': info['id'],
#                 'title': playlist_title,
#                 'author': playlist_author,
#                 'thumbnail': playlist_thumbnail,
#                 'track_count': len(info['entries']),
#                 'type': 'playlist'
#             })

#             # Add individual tracks
#             for video in info['entries']:
#                 if video and 'title' in video:
#                     results.append({
#                         'id': video['id'],
#                         'title': video['title'],
#                         'author': video.get('uploader', 'Unknown'),
#                         'thumbnail': f"https://img.youtube.com/vi/{video['id']}/0.jpg",
#                         'duration': video.get('duration', 0),
#                         'file_exists': os.path.exists(os.path.join(MUSIC_DIR, f"{video['id']}.flac"))
#                     })
#         elif info and 'title' in info:
#             # It's a single video
#             results.append({
#                 'id': info['id'],
#                 'title': info['title'],
#                 'author': info.get('uploader', 'Unknown'),
#                 'thumbnail': f"https://img.youtube.com/vi/{info['id']}/0.jpg",
#                 'duration': info.get('duration', 0),
#                 'file_exists': os.path.exists(os.path.join(MUSIC_DIR, f"{info['id']}.flac"))
#             })
  

#         return jsonify(results)

#     elif spotify_match:
#          # Handle Spotify URL
#         spotify_type = spotify_match.group(1)
#         spotify_id = spotify_match.group(2)
#         spotify_url = f"https://open.spotify.com/{spotify_type}/{spotify_id}"
#         spotify_results = get_spotify_youtube_matches(spotify_url)

#         filtered_results = []
#         for match in spotify_results.get('matches', []):
#             spotify_track = match['spotify']
#             youtube_track = match['youtube']
#             if spotify_track and youtube_track and 'name' in spotify_track and 'artists' in spotify_track and spotify_track['artists']:
#                 video_id = youtube_track.get('videoId')
#                 if video_id:
#                     filename = f"{video_id}.flac"
#                     filtered_results.append({
#                         'id': video_id,
#                         'title': spotify_track['name'],
#                         'author': ', '.join(spotify_track['artists']),
#                         'thumbnail': f"https://img.youtube.com/vi/{video_id}/0.jpg",
#                         'duration': int(spotify_track.get('duration_ms', 0) / 1000),
#                         'file_exists': os.path.exists(os.path.join(MUSIC_DIR, filename)),
#                         'spotify_type': spotify_type
#                     })

#         # If it's an album or playlist, add metadata only if we have valid tracks
#         if spotify_type in ['album', 'playlist'] and filtered_results:
#             first_video_id = filtered_results[0]['id']
#             metadata = {
#                 'id': spotify_id,
#                 'title': spotify_results.get('album_name', '') if spotify_type == 'album' else spotify_results.get('playlist_name', ''),
#                 'author': spotify_results.get('artist_name', '') if spotify_type == 'album' else spotify_results.get('playlist_owner', ''),
#                 'thumbnail': f"https://img.youtube.com/vi/{first_video_id}/0.jpg",
#                 'track_count': len(filtered_results),
#                 'spotify_type': spotify_type
#             }
#             # Only add metadata if we have a title
#             if metadata['title']:
#                 filtered_results.insert(0, metadata)
       
#         return jsonify(filtered_results)
#     else:
#         search_results = ytmusic.search(search_term, filter="songs", limit=2)

#         filtered_results = []
#         for result in search_results:
#             if result['resultType'] == 'song':
#                 video_id = result['videoId']
#                 thumbnail_url =  f"https://img.youtube.com/vi/{video_id}/0.jpg"
#                 filename = f"{video_id}.flac"
#                 file_exists = os.path.exists(os.path.join(MUSIC_DIR, filename))
                
#                 filtered_results.append({
#                     'id': video_id,
#                     'title': result['title'],
#                     'author': result['artists'][0]['name'] if result['artists'] else 'Unknown Artist',
#                     'thumbnail': thumbnail_url,
#                     'duration': result['duration_seconds'],
#                     'file_exists': file_exists
#                 })

#         return jsonify(filtered_results)
    


from itertools import chain
import yt_dlp
from ytmusicapi import YTMusic
import os
import re

# Make sure these are initialized elsewhere in your code


import concurrent.futures



import re
import os
import yt_dlp
from flask import Flask, request, jsonify
from ytmusicapi import YTMusic

def is_youtube_url(url):
    youtube_regex = (
        r'(https?://)?(www\.)?'
        '(youtube|youtu|youtube-nocookie|music\.youtube)\.(com|be)/'
        '(watch\?v=|embed/|v/|playlist\?list=|album/|track/|.+\?v=)?([^&=%\?]{11,})'
    )
    return re.match(youtube_regex, url) is not None

def fetch_ytmusic_results(search_term):
    try:
        ytmusic_results = ytmusic.search(search_term, filter="songs", limit=100)
        filtered_results = []
        for result in ytmusic_results:
            if result['resultType'] == 'song' and 'videoId' in result:
                video_id = result['videoId']
                thumbnail_url = f"https://img.youtube.com/vi/{video_id}/0.jpg"
                filename = f"{video_id}.flac"
                file_exists = os.path.exists(os.path.join(MUSIC_DIR, filename))
                
                filtered_results.append({
                    'id': video_id,
                    'title': result.get('title', 'Unknown Title'),
                    'author': result['artists'][0]['name'] if result.get('artists') else 'Unknown Artist',
                    'thumbnail': thumbnail_url,
                    'duration': result.get('duration_seconds', 0),
                    'file_exists': file_exists,
                    'source': 'ytmusic'
                })
        return filtered_results
    except Exception as e:
        print(f"Error in fetch_ytmusic_results: {str(e)}")
        return []

def fetch_ytdlp_results(search_term):
    ydl_opts = {
        'format': 'bestaudio/best',
        'config_location' : 'yt_dlp.conf',
        'username' : 'oauth2',
        'quiet': True,
        'no_warnings': True,
        'extract_flat': 'in_playlist',
        'skip_download': True,
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            yt_dlp_results = ydl.extract_info(f"ytsearch100:{search_term}", download=False)['entries']

        filtered_results = []
        for result in yt_dlp_results:
            if result and 'id' in result:
                video_id = result['id']
                duration = result.get('duration')
                
                # Skip shorts (typically less than 60 seconds)
                if duration and duration < 60:
                    continue
                
                thumbnail_url = f"https://img.youtube.com/vi/{video_id}/0.jpg"
                filename = f"{video_id}.flac"
                file_exists = os.path.exists(os.path.join(MUSIC_DIR, filename))
                
                filtered_results.append({
                    'id': video_id,
                    'title': result.get('title', 'Unknown Title'),
                    'author': result.get('uploader', 'Unknown Uploader'),
                    'thumbnail': thumbnail_url,
                    'duration': duration,
                    'file_exists': file_exists,
                    'source': 'ytdlp'
                })
        return filtered_results
    except Exception as e:
        print(f"Error in fetch_ytdlp_results: {str(e)}")
        return []

def process_ytmusic_url(url):
    results = []
    playlist_id = None
    
    if 'playlist' in url:
        playlist_id = re.search(r'list=([^&]+)', url)
        if playlist_id:
            playlist_id = playlist_id.group(1)
    elif 'album' in url:
        playlist_id = url.split('album/')[-1]
    elif 'track' in url:
        video_id = url.split('track/')[-1]
        return process_single_track(video_id)

    if playlist_id:
        try:
            playlist_info = ytmusic.get_playlist(playlist_id)
            if playlist_info and 'title' in playlist_info and playlist_info.get('tracks'):
                results.append({
                    'id': playlist_id,
                    'title': playlist_info['title'],
                    'author': playlist_info['author']['name'] if 'author' in playlist_info and 'name' in playlist_info['author'] else 'Unknown',
                    'thumbnail': playlist_info['thumbnails'][-1]['url'] if 'thumbnails' in playlist_info and playlist_info['thumbnails'] else '',
                    'track_count': len(playlist_info['tracks']),
                    'type': 'playlist'
                })
                
                # Skip the first track (index 0) as it's often blank
                for track in playlist_info['tracks'][1:]:
                    if 'videoId' in track and 'title' in track:
                        video_id = track['videoId']
                        filename = f"{video_id}.flac"
                        results.append({
                            'id': video_id,
                            'title': track['title'],
                            'author': track['artists'][0]['name'] if 'artists' in track and track['artists'] else 'Unknown Artist',
                            'thumbnail': f"https://img.youtube.com/vi/{video_id}/0.jpg",
                            'duration': track.get('duration_seconds', 0),
                            'file_exists': os.path.exists(os.path.join(MUSIC_DIR, filename))
                        })
            else:
                print("Invalid or empty playlist data received")
                results = process_with_ytdlp(url)
        except Exception as e:
            print(f"Error processing YouTube Music URL with ytmusicapi: {str(e)}")
            print("Falling back to yt_dlp method...")
            results = process_with_ytdlp(url)
    else:
        results = process_with_ytdlp(url)

    # Filter out any results with empty or invalid data
    results = [result for result in results if result.get('title') and result.get('id')]
    
    return results

def process_single_track(video_id):
    try:
        track_info = ytmusic.get_song(video_id)
        filename = f"{video_id}.flac"
        return [{
            'id': video_id,
            'title': track_info['videoDetails'].get('title', 'Unknown Title'),
            'author': track_info['videoDetails'].get('author', 'Unknown Artist'),
            'thumbnail': f"https://img.youtube.com/vi/{video_id}/0.jpg",
            'duration': int(track_info['videoDetails'].get('lengthSeconds', 0)),
            'file_exists': os.path.exists(os.path.join(MUSIC_DIR, filename))
        }]
    except Exception as e:
        print(f"Error processing single track: {str(e)}")
        return process_with_ytdlp(f"https://music.youtube.com/watch?v={video_id}")

def process_with_ytdlp(url):
    ydl_opts = {
        'format': 'bestaudio/best',
        'quiet': True,
        'no_warnings': True,
        'config_location' : 'yt_dlp.conf',
        'username' : 'oauth2',
        'extract_flat': 'in_playlist',
        'skip_download': True,
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)

        results = []
        if 'entries' in info and info['entries']:
            # It's a playlist
            results.append({
                'id': info['id'],
                'title': info.get('title', 'Unknown Playlist'),
                'author': info.get('uploader', 'Unknown Uploader'),
                'thumbnail': info.get('thumbnail', ''),
                'track_count': len(info['entries']),
                'type': 'playlist'
            })

            for video in info['entries']:
                if video and 'id' in video and 'title' in video:
                    video_id = video['id']
                    filename = f"{video_id}.flac"
                    results.append({
                        'id': video_id,
                        'title': video.get('title', 'Unknown Title'),
                        'author': video.get('uploader', 'Unknown Uploader'),
                        'thumbnail': f"https://img.youtube.com/vi/{video_id}/0.jpg",
                        'duration': video.get('duration', 0),
                        'file_exists': os.path.exists(os.path.join(MUSIC_DIR, filename))
                    })
        elif info and 'id' in info and 'title' in info:
            # It's a single video
            video_id = info['id']
            filename = f"{video_id}.flac"
            results.append({
                'id': video_id,
                'title': info.get('title', 'Unknown Title'),
                'author': info.get('uploader', 'Unknown Uploader'),
                'thumbnail': f"https://img.youtube.com/vi/{video_id}/0.jpg",
                'duration': info.get('duration', 0),
                'file_exists': os.path.exists(os.path.join(MUSIC_DIR, filename))
            })

        # Filter out any results with empty or invalid data
        results = [result for result in results if result.get('title') and result.get('id')]

        return results
    except Exception as e:
        print(f"Error in process_with_ytdlp: {str(e)}")
        return []



@app.route('/search_youtube', methods=['POST'])
def search_youtube():
    search_term = request.json.get('search_term', '')
    include_out_universe = request.json.get('include_out_universe', False)

    if not search_term:
        return jsonify({'error': 'No search term provided'}), 400

    # Check if it's a Spotify URL
    spotify_pattern = r'https?://(?:open\.)?spotify\.com/(track|album|playlist)/([a-zA-Z0-9]+)'
    spotify_match = re.match(spotify_pattern, search_term)

    try:
        if is_youtube_url(search_term):
            if 'music.youtube.com' in search_term:
                # Handle YouTube Music URL
                results = process_ytmusic_url(search_term)
            else:
                # Handle regular YouTube URL
                results = process_with_ytdlp(search_term)
        elif spotify_match:
            # Handle Spotify URL
            spotify_type = spotify_match.group(1)
            spotify_id = spotify_match.group(2)
            spotify_url = f"https://open.spotify.com/{spotify_type}/{spotify_id}"
            spotify_results = get_spotify_youtube_matches(spotify_url)

            results = []
            for match in spotify_results.get('matches', []):
                spotify_track = match['spotify']
                youtube_track = match['youtube']
                if spotify_track and youtube_track and 'name' in spotify_track and 'artists' in spotify_track and spotify_track['artists']:
                    video_id = youtube_track.get('videoId')
                    if video_id:
                        filename = f"{video_id}.flac"
                        results.append({
                            'id': video_id,
                            'title': spotify_track['name'],
                            'author': ', '.join(spotify_track['artists']),
                            'thumbnail': f"https://img.youtube.com/vi/{video_id}/0.jpg",
                            'duration': int(spotify_track.get('duration_ms', 0) / 1000),
                            'file_exists': os.path.exists(os.path.join(MUSIC_DIR, filename)),
                            'spotify_type': spotify_type
                        })

            # If it's an album or playlist, add metadata only if we have valid tracks
            if spotify_type in ['album', 'playlist'] and results:
                first_video_id = results[0]['id']
                metadata = {
                    'id': spotify_id,
                    'title': spotify_results.get('album_name', '') if spotify_type == 'album' else spotify_results.get('playlist_name', ''),
                    'author': spotify_results.get('artist_name', '') if spotify_type == 'album' else spotify_results.get('playlist_owner', ''),
                    'thumbnail': f"https://img.youtube.com/vi/{first_video_id}/0.jpg",
                    'track_count': len(results),
                    'spotify_type': spotify_type
                }
                # Only add metadata if we have a title
                if metadata['title']:
                    results.insert(0, metadata)
        else:
            # Regular search
            search_term = "song " + search_term
            with concurrent.futures.ThreadPoolExecutor() as executor:
                ytmusic_future = executor.submit(fetch_ytmusic_results, search_term)
                ytdlp_future = executor.submit(fetch_ytdlp_results, search_term) if include_out_universe else None

                ytmusic_results = ytmusic_future.result()
                ytdlp_results = ytdlp_future.result() if include_out_universe else []

            # Remove duplicates
            seen_ids = set()
            unique_ytmusic_results = []
            unique_ytdlp_results = []

            for result in ytmusic_results:
                if result['id'] not in seen_ids:
                    unique_ytmusic_results.append(result)
                    seen_ids.add(result['id'])

            for result in ytdlp_results:
                if result['id'] not in seen_ids:
                    unique_ytdlp_results.append(result)
                    seen_ids.add(result['id'])

            # Sort results within each category
            unique_ytmusic_results.sort(key=lambda x: x['file_exists'], reverse=True)
            unique_ytdlp_results.sort(key=lambda x: x['file_exists'], reverse=True)

            # Combine results in the desired order
            results = []
            results.extend(unique_ytmusic_results[:6])  # First 6 YTMusic results
            results.extend(unique_ytdlp_results)        # All YT-DLP results
            results.extend(unique_ytmusic_results[6:])  # Remaining YTMusic results

        # Final filtering of results
        results = [result for result in results if result.get('title') and result.get('id')]
        return jsonify(results[:100])  # Return up to 100 results

    except Exception as e:
        print(f"Error in search_youtube: {str(e)}")
        return jsonify({'error': str(e)}), 500


# Note: The get_spotify_youtube_matches function is not provided in the code snippets.
# You'll need to implement this function to handle Spotify URL matching.
from flask import request, jsonify
import yt_dlp

@app.route('/play_youtube', methods=['POST'])
def play_youtube():
    url = request.json['url']

    try:
        # Use yt-dlp to extract video information
        ydl_opts = {
            'format': 'bestaudio/best',
            'quiet': True,
            'no_warnings': True,
            'extract_flat': 'in_playlist',
            'skip_download': True,
            'config_location' : 'yt_dlp.conf',
            'username' : 'oauth2',
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)

        if 'entries' in info:
            # It's a playlist, take the first video
            video = info['entries'][0]
        else:
            # It's a single video
            video = info

        # Process the video (download audio, convert to FLAC, etc.)
        output_path = download_and_process_audio(url, ['musixmatch', 'lrclib', 'netease', 'megalobiz', 'genius'])
        filename = os.path.basename(output_path)

        # Return the filename to be played
        session[sharesession] = s(output_path , 1)
        return jsonify({
            'status': 'success',
            'filename': filename,
            'title': video['title'],
            'artist': video['uploader']
        })

    except Exception as e:
        print(f"Error processing YouTube URL: {str(e)}")
        return jsonify({'status': 'error', 'message': str(e)}), 500
@app.route('/download_youtube', methods=['POST'])
def download_youtube():
    video_id = request.json['video_id']
    url = f"https://www.youtube.com/watch?v={video_id}"

    try:
        output_path = download_and_process_audio(url, ['musixmatch', 'lrclib', 'netease', 'megalobiz', 'genius'])
        filename = os.path.basename(output_path)
        return jsonify({'status': 'completed', 'filename': filename})
    except Exception as e:
        print(f"Error downloading {video_id}: {str(e)}")
        return jsonify({'status': 'failed', 'error': str(e)}), 500

@app.route('/download_status/<video_id>')
def download_status(video_id):
    filename = f"{video_id}.flac"
    if os.path.exists(os.path.join(MUSIC_DIR, filename)):
        return jsonify({'status': 'completed'})
    else:
        return jsonify({'status': 'not_found'})
@app.route('/artwork2/<filename>')
def get_artwork2(filename):
    filepath = os.path.join(MUSIC_DIR, filename)
    if not os.path.exists(filepath):
        return send_file(DEFAULT_ARTWORK_PATH, mimetype='image/jpeg')

    audio = FLAC(filepath)
    artwork = audio.pictures
    if artwork:
        img = artwork[0].data
        return send_file(BytesIO(img), mimetype='image/jpeg')
    else:
        return send_file(DEFAULT_ARTWORK_PATH, mimetype='image/jpeg')
import os


@app.route('/cleanup', methods=['POST'])
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

        return jsonify({"message": "Library cleaned up successfully"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
@app.errorhandler(404)
def not_found_error(error):
    return jsonify({"error": "Not found"}), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({"error": "Internal server error"}), 500

@app.route('/asset/<type>')
def assets(type):
    if type == "watermark":
        return send_file(os.path.join(os.getcwd() , "assets" , "asset1.png") ,  max_age=31536000)
    elif type == "light":
        return send_file(os.path.join(os.getcwd() , "assets" , "images" ,  "light.png") ,  max_age=31536000)
    elif type == "dark":
        return send_file(os.path.join(os.getcwd() , "assets" , "images" ,  "dark.png"),  max_age=31536000 )
    elif type == "resource":
        return send_file(os.path.join(os.getcwd() , "assets" , "images" ,  "resource.png") ,  max_age=31536000)
    # elif type == "backgroundlight":
    #     return send_file(os.path.join(os.getcwd() , "assets" , "images" ,  "backgroundlight.png") ,  max_age=31536000)
    # elif type == "backgrounddark":
    #     return send_file(os.path.join(os.getcwd() , "assets" , "images" ,  "backgrounddark.png") ,  max_age=31536000)
    elif type == "search":
        return send_file(os.path.join(os.getcwd() , "assets" , "images" ,  "search.png") ,  max_age=31536000)
    elif type == "fullplayer":
        return send_file(os.path.join(os.getcwd() , "assets" , "images" ,  "bigplayer.png"),  max_age=31536000)
    elif type == "lyrics":
        return send_file(os.path.join(os.getcwd() , "assets" , "images" ,  "lyrics.png") ,  max_age=31536000)
    elif type == "settings":
        return send_file(os.path.join(os.getcwd() , "assets" , "images" ,  "settings.png"),  max_age=31536000 )
  
    else:
        return "not found!!!"
from ytmusicapi import YTMusic

@app.route('/lyrics/<video_id>')
def get_lyrics(video_id):
    ytmusic = YTMusic()
    try:
        watch_playlist = ytmusic.get_watch_playlist(videoId=video_id)
        lyrics_browse_id = watch_playlist.get('lyrics')
        if lyrics_browse_id:
            lyrics_data = ytmusic.get_lyrics(lyrics_browse_id)
            if lyrics_data and 'lyrics' in lyrics_data:
                return jsonify({
                    'status': 'success',
                    'lyrics': lyrics_data['lyrics'],
                    'source': "Sangeet One..."
                })
        return jsonify({
            'status': 'not_found',
            'message': 'No lyrics available for this song.'
        })
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500



# from this section of code the authentication logic code will be started so there will be no sangeet code , function or anythingb  realted to playback or sangeet exacept auth




ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

def ensure_upload_dir():
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)







init_db_auth()

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def send_email(to_email, subject, body):
    email.send_mail_request(to_email , subject , body)
    return True



@app.route('/authentication')
def home():
    if 'user_id' in session:
        return redirect(url_for("index"))
    return render_template('home.html')

@app.route('/authentication/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')

        if not all([name, email, password, confirm_password]):
            flash('All fields are required.', 'error')
            return render_template('register.html')

        if password != confirm_password:
            flash('Passwords do not match.', 'error')
            return render_template('register.html')
        #enable it if you want the user to add the password strength else keep it untouched
        # if not re.match(r'^(?=.*[A-Za-z])(?=.*\d)(?=.*[@$!%*#?&])[A-Za-z\d@$!%*#?&]{8,}$', password):
        #     flash('Password must be at least 8 characters long and contain at least one letter, one number, and one special character.', 'error')
        #     return render_template('register.html')

        db = get_db_auth()
        
        user = db.execute('SELECT * FROM users WHERE email = ? AND email_verified = 1', (email,)).fetchone()
        
        if not user:
            flash('Email not verified. Please verify your email first.', 'error')
            return render_template('register.html')

        try:
            db.execute('''UPDATE users 
                          SET name = ?, password = ?, status = "active"
                          WHERE email = ?''',
                       (name, generate_password_hash(password), email))
            db.commit()
            
            user = db.execute('SELECT id FROM users WHERE email = ?', (email,)).fetchone()
            if user:
                session['user_id'] = user['id']
                session.permanent = True
                
                flash('Account created successfully. Welcome!', 'success')
                return redirect(url_for('index'))
            else:
                flash('An error occurred during registration. Please try again.', 'error')
                return render_template('register.html')
        except Exception as e:
            print(f"Error during registration: {str(e)}")
            flash('An error occurred during registration. Please try again.', 'error')
            return render_template('register.html')
    
    return render_template('register.html')

@app.route('/send_verification_otp', methods=['POST'])
def send_verification_otp():
    email = request.json.get('email')
    if not email:
        return jsonify({'success': False, 'message': 'Email is required.'}), 400

    db = get_db_auth()
    
    existing_user = db.execute('SELECT * FROM users WHERE email = ?', (email,)).fetchone()
    
    otp = secrets.token_hex(3)  # 6-character OTP
    
    try:
        if existing_user:
            db.execute('UPDATE users SET otp = ? WHERE email = ?', (otp, email))
        else:
            db.execute('INSERT INTO users (email, otp, status) VALUES (?, ?, "pending")', (email, otp))
        db.commit()
    except sqlite3.IntegrityError as e:
        print(f"Database error: {str(e)}")
        return jsonify({'success': False, 'message': 'An error occurred. Please try again.'}), 500
    
    if send_email(email, "Email Verification OTP", f"Your OTP for email verification is: {otp}"):
        return jsonify({'success': True, 'message': 'OTP sent successfully.'}), 200
    else:
        return jsonify({'success': False, 'message': 'Failed to send OTP.'}), 500

@app.route('/verify_email_otp', methods=['POST'])
def verify_email_otp():
    email = request.json.get('email')
    otp = request.json.get('otp')
    
    if not email or not otp:
        return jsonify({'success': False, 'message': 'Email and OTP are required.'}), 400

    db = get_db_auth()
    user = db.execute('SELECT * FROM users WHERE email = ? AND otp = ?', (email, otp)).fetchone()
    
    if user:
        db.execute('UPDATE users SET otp = NULL, email_verified = 1 WHERE email = ?', (email,))
        db.commit()
        return jsonify({'success': True, 'message': 'Email verified successfully.'}), 200
    else:
        return jsonify({'success': False, 'message': 'Invalid OTP.'}), 400


import secrets

@app.route('/authentication/dashboard', methods=['GET', 'POST'])
@login_required
def dashboard():
    db = get_db_auth()
    user = db.execute('SELECT * FROM users WHERE id = ?', (session['user_id'],)).fetchone()

    if request.method == 'POST':
        # Handle form submission
        name = request.form.get('name')
        if name:
            db.execute('UPDATE users SET name = ? WHERE id = ?', (name, session['user_id']))
            db.commit()
            flash('Profile updated successfully', 'success')
        return redirect(url_for('dashboard'))

    music_db = get_db()
    
    # Fetch listening history for the current user
    listening_history = music_db.execute('''
        SELECT h.filename, h.timestamp, h.position, s.title, s.artist 
        FROM listening_history h
        LEFT JOIN song_stats s ON h.filename = s.filename AND h.user_id = s.user_id
        WHERE h.user_id = ?
        ORDER BY h.timestamp DESC
    ''', (session['user_id'],)).fetchall()

    # Analyze the listening history to get most listened songs
    song_counts = {}
    for song in listening_history:
        title = song['title'] or 'Unknown Title'
        artist = song['artist'] or 'Unknown Artist'
        if title not in song_counts:
            song_counts[title] = {
                'title': title,
                'artist': artist,
                'count': 0,
                'thumbnail': f"https://img.youtube.com/vi/{song['filename'].replace('.flac', '')}/0.jpg"
            }
        song_counts[title]['count'] += 1
    
    most_listened_songs = sorted(song_counts.values(), key=lambda x: x['count'], reverse=True)[:10]

    # Analyze the listening history to get listening times
    time_slots = {}
    for song in listening_history:
        timestamp = datetime.fromisoformat(song['timestamp'])
        hour = timestamp.hour
        if hour < 6:
            time_slot = '12am - 6am'
        elif hour < 12:
            time_slot = '6am - 12pm'
        elif hour < 18:
            time_slot = '12pm - 6pm'
        else:
            time_slot = '6pm - 12am'
        
        if time_slot not in time_slots:
            time_slots[time_slot] = 0
        time_slots[time_slot] += 1
    
    listening_times = [{'time_slot': slot, 'listen_count': count} for slot, count in time_slots.items()]
    listening_times.sort(key=lambda x: x['listen_count'], reverse=True)

    # Get recently listened songs
    recently_listened_songs = []
    for song in listening_history[:10]:
        title = song['title'] or 'Unknown Title'
        artist = song['artist'] or 'Unknown Artist'
        recently_listened_songs.append({
            'filename': song['filename'],
            'timestamp': song['timestamp'],
            'title': title,
            'artist': artist,
            'thumbnail': f"https://img.youtube.com/vi/{song['filename'].replace('.flac', '')}/0.jpg"
        })

    return render_template('dashboard.html', 
                           user=user, 
                           most_listened_songs=most_listened_songs,
                           listening_times=listening_times,
                           recently_listened_songs=recently_listened_songs)

@app.route('/authentication/reactivate_account', methods=['GET', 'POST'])
@login_required
def reactivate_account():
    db = get_db_auth()
    user = db.execute('SELECT * FROM users WHERE id = ?', (session['user_id'],)).fetchone()

    if user['status'] != 'suspended':
        flash('Your account is not suspended.', 'info')
        return redirect(url_for('dashboard'))

    if request.method == 'POST':
        if 'send_otp' in request.form:
            otp = secrets.token_hex(3)  # 6-character OTP
            db.execute('UPDATE users SET otp = ? WHERE id = ?', (otp, user['id']))
            db.commit()
            
            if send_email(user['email'], "Account Reactivation OTP", f"Your OTP for account reactivation is: {otp}"):
                flash('An OTP has been sent to your email.', 'success')
            else:
                flash('Failed to send OTP. Please try again later.', 'error')
        
        elif 'verify_otp' in request.form:
            submitted_otp = request.form.get('otp')
            if submitted_otp == user['otp']:
                db.execute('UPDATE users SET status = "active", otp = NULL WHERE id = ?', (user['id'],))
                db.commit()
                flash('Your account has been reactivated successfully.', 'success')
                return redirect(url_for('dashboard'))
            else:
                flash('Invalid OTP. Please try again.', 'error')

    return render_template('reactivate_account.html', user=user)
import os
from flask import jsonify, request, current_app
from werkzeug.utils import secure_filename

@app.route('/update_profile_pic', methods=['POST'])
@login_required
def update_profile_pic():
    if 'profile_pic' not in request.files:
        return jsonify({'success': False, 'message': 'No file part'}), 400
    
    file = request.files['profile_pic']
    
    if file.filename == '':
        return jsonify({'success': False, 'message': 'No selected file'}), 400
    
    if file and allowed_file(file.filename):
        filename = secure_filename(f"user_{session['user_id']}_profile.png")
        file_path = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
        
        # Save the file
        file.save(file_path)
        
        # Update the user's profile in the database
        db = get_db_auth()
        db.execute('UPDATE users SET profile_pic = ? WHERE id = ?', (filename, session['user_id']))
        db.commit()
  
        
        return jsonify({
            'success': True,
            'message': 'Profile picture updated successfully',
            'image_url': url_for('static', filename=f'profile_pics/{filename}')
        })
    
    return jsonify({'success': False, 'message': 'Invalid file type'}), 400

@app.route('/remove_profile_pic', methods=['POST'])
@login_required
def remove_profile_pic():
    db = get_db_auth()
    user = db.execute('SELECT profile_pic FROM users WHERE id = ?', (session['user_id'],)).fetchone()
    
    if user and user['profile_pic']:
        # Remove the file from the server
        file_path = os.path.join(current_app.config['UPLOAD_FOLDER'], user['profile_pic'])
        if os.path.exists(file_path):
            os.remove(file_path)
        
        # Update the user's profile in the database
        db.execute('UPDATE users SET profile_pic = NULL WHERE id = ?', (session['user_id'],))
        db.commit()
        
  
        return jsonify({'success': True, 'message': 'Profile picture removed successfully'})
    

    return jsonify({'success': False, 'message': 'No profile picture to remove'}), 400

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in {'png', 'jpg', 'jpeg', 'gif'}


@app.route('/authentication/forgot_password', methods=['GET', 'POST'])
def forgot_password():
    if request.method == 'POST':
        email = request.form.get('email')
        if not email:
            flash('Email is required.', 'error')
            return render_template('forgot_password.html')

        db = get_db_auth()
        user = db.execute('SELECT * FROM users WHERE email = ?', (email,)).fetchone()
        
        if user:
            otp = secrets.token_hex(3)  # 6-character OTP
            db.execute('UPDATE users SET otp = ? WHERE id = ?', (otp, user['id']))
            db.commit()
            
            if send_email(email, "Password Reset OTP", f"Your OTP for password reset is: {otp}"):
                flash('An OTP has been sent to your email.', 'success')
                return redirect(url_for('reset_password', user_id=user['id']))
            else:
                flash('Failed to send OTP. Please try again later.', 'error')
        else:
            flash('Email not found.', 'error')
        
      
    
    return render_template('forgot_password.html')

@app.route('/authentication/reset_password/<int:user_id>', methods=['GET', 'POST'])
def reset_password(user_id):
    if request.method == 'POST':
        otp = request.form.get('otp')
        new_password = request.form.get('new_password')
        confirm_password = request.form.get('confirm_password')

        if not all([otp, new_password, confirm_password]):
            flash('All fields are required.', 'error')
            return render_template('reset_password.html', user_id=user_id)

        if new_password != confirm_password:
            flash('Passwords do not match.', 'error')
            return render_template('reset_password.html', user_id=user_id)

        if not re.match(r'^(?=.*[A-Za-z])(?=.*\d)(?=.*[@$!%*#?&])[A-Za-z\d@$!%*#?&]{8,}$', new_password):
            flash('Password must be at least 8 characters long and contain at least one letter, one number, and one special character.', 'error')
            return render_template('reset_password.html', user_id=user_id)

        db = get_db_auth()
        user = db.execute('SELECT * FROM users WHERE id = ?', (user_id,)).fetchone()

        if user and user['otp'] == otp:
            db.execute('UPDATE users SET password = ?, otp = NULL WHERE id = ?',
                       (generate_password_hash(new_password), user_id))
            db.commit()
            flash('Password has been reset successfully. Please log in.', 'success')
            return redirect(url_for('login'))
        else:
            flash('Invalid OTP. Please try again.', 'error')



    return render_template('reset_password.html', user_id=user_id)

@app.route('/authentication/assets/<type>')
def asset(type):
    if type == "background":
        return send_file(os.path.join(os.getcwd(), "assets", "images", "background1.png"))
    elif type == "logo":
        return send_file(os.path.join(os.getcwd(), "assets", "images", "logo.png"))
    else:
        return "Asset not found", 404

@app.route('/authentication/profile', methods=['GET', 'POST'])
@login_required
def profile():
    ensure_upload_dir()
    db = get_db_auth()
    user = db.execute('SELECT * FROM users WHERE id = ?', (session['user_id'],)).fetchone()

    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')

        if not name or not email:
            flash('Name and email are required.', 'error')
            return render_template('profile.html', user=user)

        if 'profile_pic' in request.form and request.form['profile_pic']:
            try:
                img_data = request.form['profile_pic']
                if ',' in img_data:
                    img_data = img_data.split(',')[1]  # Remove the "data:image/png;base64," part
                img = Image.open(BytesIO(base64.b64decode(img_data)))
                
                filename = f"user_{session['user_id']}_profile.png"
                file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                img.save(file_path)
                
                db.execute('UPDATE users SET profile_pic = ? WHERE id = ?', (filename, session['user_id']))
            except Exception as e:
                print(f"Error processing profile picture: {str(e)}")
                flash('Error processing profile picture. Please try again.', 'error')

        db.execute('UPDATE users SET name = ?, email = ? WHERE id = ?', (name, email, session['user_id']))
        db.commit()
        
        flash('Profile updated successfully.', 'success')
        return redirect(url_for('profile'))


    return render_template('profile.html', user=user)
import secrets
from datetime import datetime, timedelta

# @app.route('/authentication/login', methods=['GET', 'POST'])
# def login():
#     if request.method == 'POST':
#         email = request.form.get('email')
#         password = request.form.get('password')

#         if not email or not password:
#             flash('Email and password are required.', 'error')
#             return render_template('login.html')
        
#         db = get_db_auth()
#         user = db.execute('SELECT * FROM users WHERE email = ?', (email,)).fetchone()

#         if user and check_password_hash(user['password'], password):
#             if user['status'] == 'banned':
#                 flash('Your account has been banned. Please contact support.', 'error')
#                 return render_template('login.html')
#             if user['status'] == 'suspended':
#                 flash('Your account is suspended. Please visit /suspend to reactivate.', 'info')
#                 return redirect(url_for('suspend'))
            
#             # Generate and store new token
#             token = create_auth_token(user['id'])
            
#             response = make_response(redirect("/"))
#             response.set_cookie('auth_token', token, max_age=5*24*3600, httponly=True, secure=True, samesite='Lax')
            
#             flash('Logged in successfully.', 'success')
#             return response
#         else:
#             flash('Invalid email or password.', 'error')
    
#     return render_template('login.html')
@app.route('/authentication/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        if not email or not password:
            flash('Email and password are required.', 'error')
            return render_template('login.html')
        
        db = get_db_auth()
        user = db.execute('SELECT * FROM users WHERE email = ?', (email,)).fetchone()

        if user and check_password_hash(user['password'], password):
            if user['status'] == 'banned':
                flash('Your account has been banned. Please contact support.', 'error')
                return render_template('login.html')
            if user['status'] == 'suspended':
                flash('Your account is suspended. Please visit /suspend to reactivate.', 'info')
                return redirect(url_for('suspend'))
            
            # Generate and store new token
            token = create_auth_token(user['id'])
            
            response = make_response(redirect("/"))
            
            # WARNING: Setting secure=False allows the cookie to be transmitted over insecure connections.
            # This should only be used for local development or in controlled, secure environments.
            is_secure = request.is_secure
            response.set_cookie('auth_token', token, max_age=5*24*3600, httponly=True, secure=is_secure, samesite='Lax')
            
            flash('Logged in successfully.', 'success')
            return response
        else:
            flash('Invalid email or password.', 'error')
    
    return render_template('login.html')
# Modified logout route
@app.route('/authentication/logout')
def logout():
    token = request.cookies.get('auth_token')
    if token:
        db = get_token_db()
        db.execute('DELETE FROM auth_tokens WHERE token = ?', (token,))
        db.commit()

    response = make_response(redirect(url_for('home')))
    response.delete_cookie('auth_token')
    flash('You have been logged out.', 'success')
    return response

# Add this to your initialization code
init_token_db()

# Modify your be
# Update your delete_account function to remove tokens
@app.route('/authentication/delete_account', methods=['POST'])
@login_required
def delete_account():
    user_id = g.user['id']
    
    # Connect to all databases
    auth_db = get_db_auth()
    music_db = get_db()
    token_db = get_token_db()
    
    try:
        # Start transactions
        auth_db.execute('BEGIN')
        music_db.execute('BEGIN')
        token_db.execute('BEGIN')
        
        # Delete user's listening history and song stats
        music_db.execute('DELETE FROM listening_history WHERE user_id = ?', (user_id,))
        music_db.execute('DELETE FROM song_stats WHERE user_id = ?', (user_id,))
        music_db.execute('DELETE FROM search_history WHERE user_id = ?', (user_id,))
        
        # Delete user's auth tokens
        token_db.execute('DELETE FROM auth_tokens WHERE user_id = ?', (user_id,))
        
        # Delete the user account
        auth_db.execute('DELETE FROM users WHERE id = ?', (user_id,))
        
        # Commit the transactions
        auth_db.commit()
        music_db.commit()
        token_db.commit()
        
        # Clear the session and remove the auth token
        response = make_response(redirect(url_for('home')))
        response.delete_cookie('auth_token')
        
        flash('Your account and all associated data have been permanently deleted.', 'success')
        return response
        
    except Exception as e:
        # If any error occurs, rollback all transactions
        auth_db.rollback()
        music_db.rollback()
        token_db.rollback()
        print(f"Error during account deletion: {str(e)}")
        flash('An error occurred while deleting your account. Please try again later.', 'error')
        return redirect(url_for('dashboard'))
    finally:
        # Close the database connections
        auth_db.close()
        music_db.close()
        token_db.close()
@app.route('/terms')
def terms():
    return render_template('terms.html')

@app.route('/privacy')
def privacy():
    return render_template('privacy.html')

@app.route('/help')
def help():
    return render_template('help.html')





def getresults(term):
    search_term = term
    include_out_universe = True

    if is_youtube_url(search_term):
        # Handle YouTube URL
        ydl_opts = {
            'format': 'bestaudio/best',
            'quiet': True,
            'no_warnings': True,
            'config_location' : 'yt_dlp.conf',
            'username' : 'oauth2',
            'extract_flat': 'in_playlist',
            'skip_download': True,
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(search_term, download=False)

        results = []
        if 'entries' in info:
            # It's a playlist
            playlist_title = info.get('title', 'Unknown Playlist')
            playlist_author = info.get('uploader', 'Unknown Uploader')
            playlist_thumbnail = f"https://img.youtube.com/vi/{info['entries'][0]['id']}/0.jpg" if info['entries'] else ""

            results.append({
                'id': info['id'],
                'title': playlist_title,
                'author': playlist_author,
                'thumbnail': playlist_thumbnail,
                'track_count': len(info['entries']),
                'type': 'playlist'
            })

            for video in info['entries']:
                if video and 'title' in video:
                    results.append({
                        'id': video['id'],
                        'title': video['title'],
                        'author': video.get('uploader', 'Unknown'),
                        'thumbnail': f"https://img.youtube.com/vi/{video['id']}/0.jpg",
                        'duration': video.get('duration', 0),
                        'file_exists': os.path.exists(os.path.join(MUSIC_DIR, f"{video['id']}.flac"))
                    })
        elif info and 'title' in info:
            # It's a single video
            results.append({
                'id': info['id'],
                'title': info['title'],
                'author': info.get('uploader', 'Unknown'),
                'thumbnail': f"https://img.youtube.com/vi/{info['id']}/0.jpg",
                'duration': info.get('duration', 0),
                'file_exists': os.path.exists(os.path.join(MUSIC_DIR, f"{info['id']}.flac"))
            })

        return results

    else:
        # Regular search2
        search_term = "song  "   + search_term
        with concurrent.futures.ThreadPoolExecutor() as executor:
            ytmusic_future = executor.submit(fetch_ytmusic_results, search_term)
            ytdlp_future = executor.submit(fetch_ytdlp_results, search_term)

            ytmusic_results = ytmusic_future.result()
            ytdlp_results = ytdlp_future.result() if include_out_universe else []

        # Remove duplicates
        seen_ids = set()
        unique_ytmusic_results = []
        unique_ytdlp_results = []

        for result in ytmusic_results:
            if result['id'] not in seen_ids:
                unique_ytmusic_results.append(result)
                seen_ids.add(result['id'])

        for result in ytdlp_results:
            if result['id'] not in seen_ids:
                unique_ytdlp_results.append(result)
                seen_ids.add(result['id'])

        # Sort results within each category
        unique_ytmusic_results.sort(key=lambda x: x['file_exists'], reverse=True)
        unique_ytdlp_results.sort(key=lambda x: x['file_exists'], reverse=True)

        # Combine results in the desired order
        final_results = []
        final_results.extend(unique_ytmusic_results[:6])  # First 6 YTMusic results
        final_results.extend(unique_ytdlp_results)        # All YT-DLP results
        final_results.extend(unique_ytmusic_results[6:])  # Remaining YTMusic results

        return final_results[:100]  # Return up to 100 results

@app.route('/dsearch')
def dsearch_page():
    return render_template('download.html')

@app.route('/dsearch_youtube', methods=['POST'])
def dsearch_youtube():
    search_term = request.json['search_term']
    # Use your existing search_youtube function here
    # Return the results as JSON
    results = getresults(search_term)
    return jsonify(results)

@app.route('/ddownload/<video_id>')
def ddownload_song(video_id):
    try:
        url = f"https://www.youtube.com/watch?v={video_id}"
        yt = YouTube(url)
        status = download_and_process_audio(url , "hi")
        
        # Send the file to the user
        return send_file(status, as_attachment=True, download_name=f"{yt.title}.flac")
    except Exception as e:
        print(f"Error downloading {video_id}: {str(e)}")
        return jsonify({'status': 'failed', 'error': str(e)}), 500






#till here



#sangeet radio

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

init_db_radio()

@lru_cache(maxsize=100)
def get_audio_url(video_id):
    ydl_opts = {
        'format': 'bestaudio/best',
        'quiet': True,
        'no_warnings': True,
        'config_location' : 'yt_dlp.conf',
        'username' : 'oauth2',
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(f"https://www.youtube.com/watch?v={video_id}", download=False)
        return info['url']

def get_song_info(video_id):
    ydl_opts = {
        'quiet': True,
        'config_location' : 'yt_dlp.conf',
        'username' : 'oauth2',
        'no_warnings': True,
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(f"https://www.youtube.com/watch?v={video_id}", download=False)
        return {
            'title': info.get('title', 'Unknown Title'),
            'artist': info.get('artist', 'Unknown Artist'),
            'thumbnail': f"https://img.youtube.com/vi/{video_id}/0.jpg"
        }

@app.route('/radio')
def radio():
    return render_template('radio.html')
@app.route('/radio/search')
def radiosearch():
    query = request.args.get('q', '')
    page = int(request.args.get('page', 1))
    per_page = 80
    
    try:
        results = ytmusic.search(query, filter="songs")
        start = (page - 1) * per_page
        end = start + per_page
        paginated_results = results[start:end]
        
        songs = []
        for result in paginated_results:
            if result['resultType'] == 'song':
                songs.append({
                    'video_id': result['videoId'],
                    'title': result['title'],
                    'artist': result['artists'][0]['name'] if result['artists'] else 'Unknown Artist',
                    'thumbnail': f"https://img.youtube.com/vi/{result['videoId']}/0.jpg"
                })
        return jsonify(songs)
    except Exception as e:
        app.logger.error(f"Error searching songs: {str(e)}")
        return jsonify({'error': 'Failed to search songs'}), 500

@app.route('/radio/lyrics/<video_id>')
def radioget_lyrics(video_id):
    ytmusic = YTMusic()
    try:
        watch_playlist = ytmusic.get_watch_playlist(videoId=video_id)
        lyrics_browse_id = watch_playlist.get('lyrics')
        if lyrics_browse_id:
            lyrics_data = ytmusic.get_lyrics(lyrics_browse_id)
            if lyrics_data and 'lyrics' in lyrics_data:
                return jsonify({
                    'status': 'success',
                    'lyrics': lyrics_data['lyrics'],
                    'source': "Sangeet One..."
                })
        return jsonify({
            'status': 'not_found',
            'message': 'No lyrics available for this song.'
        })
    except Exception as e:
        app.logger.error(f"Error getting lyrics: {str(e)}")
        return jsonify({
            'status': 'error',
            'message': f"Failed to fetch lyrics: {str(e)}"
        }), 500


@app.route('/radio/stream/<video_id>')
def radiostream(video_id):
    url = get_audio_url(video_id)
    def generate():
        with requests.get(url, stream=True) as r:
            for chunk in r.iter_content(chunk_size=4096):
                yield chunk
    return Response(stream_with_context(generate()), content_type="audio/mp3")

@app.route('/radio/add_to_history', methods=['POST'])
def radioadd_to_history():
    video_id = request.form.get('video_id')
    if not video_id:
        return jsonify({'error': 'No video_id provided'}), 400
    
    db = get_db_radio()
    song = db.execute('SELECT * FROM play_history WHERE video_id = ?', (video_id,)).fetchone()
    if song:
        db.execute('UPDATE play_history SET timestamp = CURRENT_TIMESTAMP WHERE video_id = ?', (video_id,))
    else:
        try:
            song_info = get_song_info(video_id)
            db.execute('INSERT OR REPLACE INTO play_history (video_id, title, artist, thumbnail) VALUES (?, ?, ?, ?)',
                       (video_id, song_info['title'], song_info['artist'], song_info['thumbnail']))
        except Exception as e:
            app.logger.error(f"Error adding song to history: {str(e)}")
            return jsonify({'error': 'Failed to add song to history'}), 500
    db.commit()
    return jsonify({'success': True})

@app.route('/radio/recent_songs')
def radiorecent_songs():
    db = get_db_radio()
    songs = db.execute('SELECT * FROM play_history ORDER BY timestamp DESC LIMIT 20').fetchall()
    return jsonify([dict(song) for song in songs])

@app.route('/radio/suggest')
def radiosuggest():
    query = request.args.get('q', '')
    suggestions = ytmusic.get_search_suggestions(query)
    return jsonify(suggestions)

@app.route('/radio/next_song')
def radionext_song():
    current_song_id = request.args.get('current_song_id')
    if not current_song_id:
        return jsonify({'error': 'No current_song_id provided'}), 400

    try:
        watch_playlist = ytmusic.get_watch_playlist(videoId=current_song_id)
        if watch_playlist and 'tracks' in watch_playlist and watch_playlist['tracks']:
            next_song = watch_playlist['tracks'][0]  # Get the first recommended song
            return jsonify({
                'video_id': next_song['videoId'],
                'title': next_song['title'],
                'artist': next_song['artists'][0]['name'] if next_song['artists'] else 'Unknown Artist',
                'thumbnail': f"https://img.youtube.com/vi/{next_song['videoId']}/0.jpg"
            })
        return jsonify({'error': 'No next song found'}), 404
    except Exception as e:
        app.logger.error(f"Error getting next song: {str(e)}")
        return jsonify({'error': 'Failed to get next song'}), 500

@app.route('/radio/song_info/<video_id>')
def radiosong_info(video_id):
    try:
        info = get_song_info(video_id)
        return jsonify(info)
    except Exception as e:
        app.logger.error(f"Error getting song info: {str(e)}")
        return jsonify({'error': 'Failed to get song info'}), 500

@app.route('/radio/previous_song')
def radioprevious_song():
    db = get_db_radio()
    previous_songs = db.execute('SELECT * FROM play_history ORDER BY timestamp DESC LIMIT 2').fetchall()
    if len(previous_songs) > 1:
        return jsonify(dict(previous_songs[1]))
    else:
        return jsonify({'error': 'No previous song found'}), 404

if __name__ == '__main__':
    try:
        os.rmdir("temp")
    except:
        pass
    try:
        os.mkdir("temp")
    except:
        pass
    app.run(host="0.0.0.0", port=os.getenv("port"))
