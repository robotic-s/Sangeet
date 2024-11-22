import db.music_db
import db.tokens_db
import db.users_db
from start import startup
from mutagen.flac import FLAC
import requests 
from flask import Flask , g , jsonify , request , flash , redirect , url_for , session , make_response , render_template , send_file , Response , stream_with_context , abort
from pytube import YouTube
import downloader
from db import tokens_db
import db 
import base64
from mail import mail as email
import re
import ipaddress
from functools import lru_cache
import pytz
import secrets
import random
from PIL import Image
import hashlib
import concurrent.futures
import yt_dlp
from yt import yt
import logging
from yt import radio
from io import BytesIO
from spotify.mathersd import get_spotify_youtube_matches
from db import users_db
import socket
import json
import urllib
from aes import aes
from dotenv import load_dotenv
from datetime import timedelta
import string
from functools import wraps
import encryption.encryption as enc
from db import music_db

from generator import tokens
import encryption.enc1 as ss
import sqlite3
from datetime import datetime
import os
from ytmusicapi import YTMusic
from werkzeug.security import generate_password_hash, check_password_hash
from flask import Flask, request
from werkzeug.middleware.proxy_fix import ProxyFix

app = Flask(__name__)

# Enable ProxyFix to correctly handle headers from reverse proxies
app.wsgi_app = ProxyFix(app.wsgi_app, x_for=1, x_proto=1, x_host=1, x_port=1)



app = Flask("sangeet")
app.secret_key = aes.generate_aes_key()



# app config


app.config['UPLOAD_FOLDER'] = 'static/profile_pics'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max-limit
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(days=5)
app.jinja_env.cache = {}

#dir..
load_dotenv()
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
ytmusic = YTMusic()
MUSIC_DIR = os.getenv("MUSIC_DIR")
HOST = os.getenv("HOST")
DEFAULT_ARTWORK_PATH = os.path.join(os.getcwd(), 'static', 'default_artwork.jpg')

#making setup checks

startup.setup()





# making db setups

#initialize db for history , users and tokens


db.music_db.init_search_history_db()


db.users_db.init_db_auth()


db.tokens_db.init_token_db()

#imp functions..

def urls():
    url = f"{request.scheme}://{request.host}{request.path}"
    return url
@app.before_request
def restrict_host():
    if not request.scheme + "://" +  request.host == f"http://127.0.0.1:{os.getenv('port')}":
        if os.getenv("allowed_sceheme") == "http":
            expected_host = os.getenv("host")
            expected_scheme = os.getenv("allowed_scheme")
            if request.scheme + "://" +  request.host != expected_host:
                abort(403 , description = "server url is not valid please go to official server by sangeet or admin")
        elif os.getenv("allowed_sceheme") == "https":
            expected_host = os.getenv("host_https")
            if  request.host != expected_host:
                abort(403 , description = "server url is not valid please go to official server by sangeet or admin")





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
    

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        token = request.cookies.get('auth_token')
        if token:
            user = tokens.verify_auth_token(token)
            if user:
                g.user = user
                return f(*args, **kwargs)
        flash('Please log in to access this page.', 'error')
        return redirect(url_for('login'))
    return decorated_function
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


class TimezoneHandler:
    DEFAULT_TIMEZONE = 'Asia/Kolkata'
    TIMEZONE_CACHE_TTL = 3600  # Cache timezone info for 1 hour
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        
    @lru_cache(maxsize=1000)
    def get_timezone_from_ip(self, ip_address):
        """
        Get timezone from IP address using ipapi.co
        Uses caching to prevent excessive API calls
        """
        try:
            response = requests.get(
                'https://ipapi.co/json/',
                timeout=5,  # 5 seconds timeout
                headers={'User-Agent': 'Sangeet-Music-App'}
            )
            response.raise_for_status()
            data = response.json()
            
            if 'timezone' in data:
                return data['timezone']
            
        except requests.RequestException as e:
            self.logger.warning(f"Failed to get timezone from IP API: {e}")
        except Exception as e:
            self.logger.error(f"Unexpected error getting timezone: {e}")
            
        return None

    def validate_timezone(self, timezone_str):
        """Validate if a timezone string is valid"""
        try:
            pytz.timezone(timezone_str)
            return True
        except pytz.exceptions.UnknownTimeZoneError:
            return False

    def get_user_timezone(self):
        """
        Get user's timezone with multiple fallback mechanisms
        Returns a pytz timezone object
        """
        try:
            # First check if timezone is stored in session
            if 'user_timezone' in session:
                timezone_str = session['user_timezone']
                if self.validate_timezone(timezone_str):
                    return pytz.timezone(timezone_str)

            # Try to get timezone from IP
            timezone_str = self.get_timezone_from_ip(None)  # IP is automatically detected
            if timezone_str and self.validate_timezone(timezone_str):
                session['user_timezone'] = timezone_str
                return pytz.timezone(timezone_str)

            # Try to get system timezone
            system_timezone = datetime.now().astimezone().tzinfo
            if system_timezone:
                timezone_str = str(system_timezone)
                if self.validate_timezone(timezone_str):
                    session['user_timezone'] = timezone_str
                    return pytz.timezone(timezone_str)

        except Exception as e:
            self.logger.error(f"Error in timezone detection: {e}")

        # Fallback to default timezone
        return pytz.timezone(self.DEFAULT_TIMEZONE)

    def format_timestamp(self, timestamp, timezone=None):
        """
        Format timestamp into user-friendly string based on how recent it is
        """
        if timezone is None:
            timezone = self.get_user_timezone()

        if isinstance(timestamp, str):
            timestamp = datetime.fromisoformat(timestamp)

        local_time = timestamp.astimezone(timezone)
        now = datetime.now(timezone)
        
        # Format time
        time_str = local_time.strftime("%I:%M %p").lstrip('0')
        
        # Calculate time difference in days
        time_diff = (now.date() - local_time.date()).days
        
        if time_diff == 0:
            return f"Today at {time_str}"
        elif time_diff == 1:
            return f"Yesterday at {time_str}"
        elif time_diff < 7:
            return f"{local_time.strftime('%A')} at {time_str}"  # Day name
        elif local_time.year == now.year:
            return f"{local_time.strftime('%b %d')} at {time_str}"
        else:
            return f"{local_time.strftime('%b %d, %Y')} at {time_str}"

    def get_time_slot_name(self, hour):
        """
        Get user-friendly name for a time slot based on hour
        """
        if 0 <= hour < 6:
            return "Late Night (12AM - 6AM)"
        elif 6 <= hour < 12:
            return "Morning (6AM - 12PM)"
        elif 12 <= hour < 17:
            return "Afternoon (12PM - 5PM)"
        elif 17 <= hour < 20:
            return "Evening (5PM - 8PM)"
        else:
            return "Night (8PM - 12AM)"

# Initialize the timezone handler
timezone_handler = TimezoneHandler()

# Updated get_user_timezone function for backward compatibility
def get_user_timezone():
    return timezone_handler.get_user_timezone()



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
@app.before_request
def check_auth_token():
    if 'user_id' not in session and 'auth_token' in request.cookies:
        token = request.cookies.get('auth_token')
        user = tokens.verify_auth_token(token)
        if user:
            db = users_db.get_db_auth()
            # Here, we're using the 'id' from the user object directly
            user_from_db = db.execute('SELECT * FROM users WHERE id = ?', (user['id'],)).fetchone()
    
            if user_from_db and user_from_db['status'] == 'active':
                session['user_id'] = user['id']
                session.permanent = True




def ensure_upload_dir():
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)


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
def downshare(video):
    video_id = video
    url = f"https://www.youtube.com/watch?v={video_id}"

    try:
        output_path = downloader.download_and_process_audio(url, ['musixmatch', 'lrclib', 'netease', 'megalobiz', 'genius'])
        filename = os.path.basename(output_path)
        return filename
    except Exception as e:
        return 0
@app.before_request
def load_logged_in_user():
    g.user = None
    token = request.cookies.get('auth_token')
    if token:
        try:
            user = tokens.verify_auth_token(token)
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
def get_upload_year(url):

        # Create a YouTube object
        video = YouTube(url)

        # Get the publish date of the video
        publish_date = video.publish_date

        # Extract the year from the publish date
        upload_year = publish_date.strftime("%Y")

        return upload_year
def get_video_info(video_id):
    try:
        video_data = ytmusic.get_song(video_id)
        
        # Extract title and author
        title = video_data.get('videoDetails', {}).get('title', 'Unknown Title')
        author = video_data.get('videoDetails', {}).get('author', 'Unknown Author')
        
        return title, author
    except Exception as e:
        print(f"Error getting video info: {e}")
        return None, None

def s(stringsd , option):
    if option == 1:
       vals = ss.enc(stringsd)
    elif  option == 2:
        vals = ss.dec(stringsd)
    return vals
sharesession = s("share" , 1)
#main routes






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
                session[sharesession] = s(music_db.lastplay(g.user['id']), 1) 
                return render_template("index.html", hostid=os.getenv("host"), user=g.user)
        else:
            session["yes"] = "yes"
            session[sharesession] = s(music_db.lastplay(g.user['id']), 1)    
            return render_template("index.html", user=g.user)
    else:
        # User is not authenticated
        return redirect(url_for("login"))
    


@app.route('/authentication/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # Check if it's an AJAX request
        is_ajax = request.headers.get('X-Requested-With') == 'XMLHttpRequest'
        
        email = request.form.get('email')
        password = request.form.get('password')

        if not email or not password:
            if is_ajax:
                return jsonify({
                    'success': False,
                    'message': 'Email and password are required.'
                })
            flash('Email and password are required.', 'error')
            return render_template('login.html')
        
        db = users_db.get_db_auth()
        user = db.execute('SELECT * FROM users WHERE email = ?', (email,)).fetchone()

        if user and check_password_hash(user['password'], password):
            if user['status'] == 'banned':
                if is_ajax:
                    return jsonify({
                        'success': False,
                        'message': 'Your account has been banned. Please contact support.'
                    })
                flash('Your account has been banned. Please contact support.', 'error')
                return render_template('login.html')
                
            if user['status'] == 'suspended':
                if is_ajax:
                    return jsonify({
                        'success': False,
                        'message': 'Your account is suspended. Please visit /suspend to reactivate.',
                        'redirect': url_for('suspend')
                    })
                flash('Your account is suspended. Please visit /suspend to reactivate.', 'info')
                return redirect(url_for('suspend'))
            
            # Generate and store new token
            token = tokens.create_auth_token(user['id'])
            
            if is_ajax:
                response = jsonify({
                    'success': True,
                    'message': 'Logged in successfully.',
                    'redirect': url_for('index')
                })
            else:
                response = make_response(redirect(url_for('index')))
            
            # Set cookie for both AJAX and non-AJAX responses
            is_secure = request.is_secure
            response.set_cookie(
                'auth_token',
                token,
                max_age=5*24*3600,
                httponly=True,
                secure=is_secure,
                samesite='Lax'
            )
            
            return response
        else:
            if is_ajax:
                return jsonify({
                    'success': False,
                    'message': 'Invalid email or password.'
                })
            flash('Invalid email or password.', 'error')
    
    # GET request - just render the template
    return render_template('login.html')

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
    



@app.route('/update_history', methods=['POST'])
@login_required
def update_history():
    data = request.json
    resp = music_db.update_history(data['filename'] , data['position'] , g.user['id'])
    if resp == "success":
      return jsonify({"status": "success"})
    else:
        return jsonify({"status": "Failed"})
    



@app.route('/listening_history')
@login_required
def listening_history():

    return jsonify( music_db.listening_history())


@app.route('/save_search', methods=['POST'])
@login_required
def save_search():
    query = request.json['query']
    resp = music_db.save_search(query)
    if resp == "success":
      return jsonify({"status": "success"})
    else:
        return jsonify({"status": "failed.."})
    

@app.route('/search_suggestions', methods=['GET'])
@login_required
def search_suggestions():
    query = request.args.get('query', '').lower()
    suggestions = ytmusic.get_search_suggestions(query)
    return jsonify(suggestions)



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
    return jsonify(  music_db.all_songs(search_term))


@app.route('/v3/search/<knskd>')
def v33(knskd):
    return render_template("embeds.html", hj=knskd)


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
        rate.write(f"{rating} for {music_db.lastplay()}")

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
    db = music_db.get_db()
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
        db = music_db.get_db()
        c = db.cursor()
        c.execute('DELETE FROM listening_history WHERE filename = ?', (filename,))
        c.execute('DELETE FROM song_stats WHERE filename = ?', (filename,))
        db.commit()

        return jsonify({"status": "success", "message": f"Song {filename} deleted successfully"})
    except Exception as e:
        print(e)
        return jsonify({"status": "error", "message": str(e)}), 500





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
        if yt.is_youtube_url(search_term):
            if 'music.youtube.com' in search_term:
                # Handle YouTube Music URL
                results = yt.process_ytmusic_url(search_term)
            else:
                # Handle regular YouTube URL
                results = yt.process_with_ytdlp(search_term)
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
                ytmusic_future = executor.submit(yt.fetch_ytmusic_results, search_term)
                ytdlp_future = executor.submit(yt.fetch_ytdlp_results, search_term) if include_out_universe else None

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
        output_path = downloader.download_and_process_audio(url, ['musixmatch', 'lrclib', 'netease', 'megalobiz', 'genius'])
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
        output_path = downloader.download_and_process_audio(url, ['musixmatch', 'lrclib', 'netease', 'megalobiz', 'genius'])
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




@app.route('/cleanup', methods=['POST'])
def cleanup():
    try:
        # Delete all files in the MUSIC_DIR
        for filename in os.listdir(MUSIC_DIR):
            file_path = os.path.join(MUSIC_DIR, filename)
            if os.path.isfile(file_path):
                os.remove(file_path)

        # Clear the database
        db = music_db.get_db()
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

        db = users_db.get_db_auth()
        
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
@app.route('/send_verification_otp', methods=['POST'])
def send_verification_otp():
    email = request.json.get('email')
    if not email:
        return jsonify({'success': False, 'message': 'Email is required.'}), 400

    db = users_db.get_db_auth()
    
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

    db = users_db.get_db_auth()
    user = db.execute('SELECT * FROM users WHERE email = ? AND otp = ?', (email, otp)).fetchone()
    
    if user:
        db.execute('UPDATE users SET otp = NULL, email_verified = 1 WHERE email = ?', (email,))
        db.commit()
        return jsonify({'success': True, 'message': 'Email verified successfully.'}), 200
    else:
        return jsonify({'success': False, 'message': 'Invalid OTP.'}), 400
@app.route('/authentication/dashboard', methods=['GET', 'POST'])
@login_required
def dashboard():
    """Dashboard route handling user profile and listening history"""
    try:
        # Initialize database connections
        db = users_db.get_db_auth()
        m_d = music_db.get_db()
        
        # Get user information
        user = db.execute('SELECT * FROM users WHERE id = ?', 
                         (session['user_id'],)).fetchone()
        
        # Handle POST request for profile update
        if request.method == 'POST':
            name = request.form.get('name')
            if name:
                db.execute('UPDATE users SET name = ? WHERE id = ?', 
                          (name, session['user_id']))
                db.commit()
                flash('Profile updated successfully', 'success')
            return redirect(url_for('dashboard'))
        
        # Get user's timezone
        user_timezone = timezone_handler.get_user_timezone()
        
        # Fetch listening history
        listening_history = m_d.execute('''
            SELECT h.filename, h.timestamp, h.position, s.title, s.artist
            FROM listening_history h
            LEFT JOIN song_stats s ON h.filename = s.filename 
            AND h.user_id = s.user_id
            WHERE h.user_id = ?
            ORDER BY h.timestamp DESC
        ''', (session['user_id'],)).fetchall()

        # Process listening history
        song_counts = {}
        time_slots = {}
        
        for song in listening_history:
            # Get local time
            utc_time = datetime.fromisoformat(song['timestamp'])
            local_time = utc_time.astimezone(user_timezone)
            
            # Process song counts
            title = song['title'] or 'Unknown Title'
            artist = song['artist'] or 'Unknown Artist'
            filename = song['filename']
            
            # Update song counts
            if title not in song_counts:
                song_counts[title] = {
                    'title': title,
                    'artist': artist,
                    'count': 0,
                    'thumbnail': f"https://img.youtube.com/vi/{filename.replace('.flac', '')}/0.jpg"
                }
            song_counts[title]['count'] += 1
            
            # Process time slots
            hour = local_time.hour
            time_slot = timezone_handler.get_time_slot_name(hour)
            time_slots[time_slot] = time_slots.get(time_slot, 0) + 1

        # Prepare most listened songs
        most_listened_songs = sorted(
            song_counts.values(), 
            key=lambda x: x['count'], 
            reverse=True
        )[:10]
        
        # Prepare listening times statistics
        listening_times = [
            {'time_slot': slot, 'listen_count': count} 
            for slot, count in time_slots.items()
        ]
        listening_times.sort(key=lambda x: x['listen_count'], reverse=True)
        
        # Prepare recently listened songs
        recently_listened_songs = []
        for song in listening_history[:10]:
            title = song['title'] or 'Unknown Title'
            artist = song['artist'] or 'Unknown Artist'
            filename = song['filename']
            
            recently_listened_songs.append({
                'filename': filename,
                'timestamp': timezone_handler.format_timestamp(
                    song['timestamp'], 
                    user_timezone
                ),
                'title': title,
                'artist': artist,
                'thumbnail': f"https://img.youtube.com/vi/{filename.replace('.flac', '')}/0.jpg"
            })

        # Render dashboard template
        return render_template(
            'dashboard.html',
            user=user,
            most_listened_songs=most_listened_songs,
            listening_times=listening_times,
            recently_listened_songs=recently_listened_songs,
            current_timezone=user_timezone.zone
        )
        
    except Exception as e:
        # Log any errors
        logging.error(f"Error in dashboard route: {e}", exc_info=True)
        flash('An error occurred while loading the dashboard', 'error')
        return redirect(url_for('index'))

@app.route('/authentication/reactivate_account', methods=['GET', 'POST'])
@login_required
def reactivate_account():
    db = users_db.get_db_auth()
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
        db = users_db.get_db_auth()
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
    db = users_db.get_db_auth()
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



@app.route('/authentication/forgot_password', methods=['GET', 'POST'])
def forgot_password():
    if request.method == 'POST':
        email = request.form.get('email')
        if not email:
            flash('Email is required.', 'error')
            return render_template('forgot_password.html')

        db = users_db.get_db_auth()
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

        db = users_db.get_db_auth()
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
    db = users_db.get_db_auth()
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

@app.route('/authentication/logout')
def logout():
    token = request.cookies.get('auth_token')
    if token:
        db = tokens_db.get_token_db()
        db.execute('DELETE FROM auth_tokens WHERE token = ?', (token,))
        db.commit()

    response = make_response(redirect(url_for('home')))
    response.delete_cookie('auth_token')
    flash('You have been logged out.', 'success')
    return response


@app.route('/authentication/delete_account', methods=['POST'])
@login_required
def delete_account():
    user_id = g.user['id']
    
    # Connect to all databases
    auth_db = users_db.get_db_auth()
    music_db = music_db.get_db()
    token_db = tokens_db.get_token_db()
    
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



@app.route('/dsearch')
def dsearch_page():
    return render_template('download.html')

@app.route('/dsearch_youtube', methods=['POST'])
def dsearch_youtube():
    search_term = request.json['search_term']
    # Use your existing search_youtube function here
    # Return the results as JSON
    results = yt.getresults(search_term)
    return jsonify(results)

@app.route('/ddownload/<video_id>')
def ddownload_song(video_id):
    try:
        url = f"https://www.youtube.com/watch?v={video_id}"
        yt = YouTube(url)
        status = downloader.download_and_process_audio(url , "hi")
        
        # Send the file to the user
        return send_file(status, as_attachment=True, download_name=f"{yt.title}.flac")
    except Exception as e:
        print(f"Error downloading {video_id}: {str(e)}")
        return jsonify({'status': 'failed', 'error': str(e)}), 500



@app.route('/radio')
def radiorender():
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
    url = yt.get_audio_url(video_id)
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
    
    db = radio.get_db_radio()
    song = db.execute('SELECT * FROM play_history WHERE video_id = ?', (video_id,)).fetchone()
    if song:
        db.execute('UPDATE play_history SET timestamp = CURRENT_TIMESTAMP WHERE video_id = ?', (video_id,))
    else:
        try:
            song_info = radio.get_song_info(video_id)
            db.execute('INSERT OR REPLACE INTO play_history (video_id, title, artist, thumbnail) VALUES (?, ?, ?, ?)',
                       (video_id, song_info['title'], song_info['artist'], song_info['thumbnail']))
        except Exception as e:
            app.logger.error(f"Error adding song to history: {str(e)}")
            return jsonify({'error': 'Failed to add song to history'}), 500
    db.commit()
    return jsonify({'success': True})

@app.route('/radio/recent_songs')
def radiorecent_songs():
    db = radio.get_db_radio()
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
        info = radio.get_song_info(video_id)
        return jsonify(info)
    except Exception as e:
        app.logger.error(f"Error getting song info: {str(e)}")
        return jsonify({'error': 'Failed to get song info'}), 500

@app.route('/radio/previous_song')
def radioprevious_song():
    db = radio.get_db_radio()
    previous_songs = db.execute('SELECT * FROM play_history ORDER BY timestamp DESC LIMIT 2').fetchall()
    if len(previous_songs) > 1:
        return jsonify(dict(previous_songs[1]))
    else:
        return jsonify({'error': 'No previous song found'}), 404

app.run(port = os.getenv("port") , host = "0.0.0.0")

