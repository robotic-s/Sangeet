import yt_dlp
import os
import subprocess
import json
from mutagen.flac import FLAC, Picture
import requests
from io import BytesIO
from PIL import Image
import shutil
import syncedlyrics
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from fuzzywuzzy import fuzz
import time
import argparse
from pytube import YouTube
from ytmusicapi import YTMusic
from dotenv import load_dotenv
load_dotenv()
ytmusic = YTMusic()

# Define directory structure
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
DOWNLOAD_DIR = os.getenv("MUSIC_DIR")
CREDENTIALS_DIR = os.path.join(BASE_DIR, "credentials")
CREDENTIALS_FILE = os.path.join(CREDENTIALS_DIR, "creds.json")

def create_session_dir(video_id):
    session_id = f"{int(time.time())}_{video_id}"
    session_dir = os.path.join(BASE_DIR, "sessions", session_id)
    os.makedirs(session_dir, exist_ok=True)
    return session_dir

def load_spotify_credentials():
    try:
        with open(CREDENTIALS_FILE, 'r') as f:
            creds = json.load(f)
        return creds.get('SPOTIPY_CLIENT_ID'), creds.get('SPOTIPY_CLIENT_SECRET')
    except FileNotFoundError:
        print(f"Credentials file not found: {CREDENTIALS_FILE}")
        return None, None
    except json.JSONDecodeError:
        print(f"Error decoding JSON from credentials file: {CREDENTIALS_FILE}")
        return None, None

# Load Spotify API credentials
SPOTIPY_CLIENT_ID, SPOTIPY_CLIENT_SECRET = load_spotify_credentials()

# if SPOTIPY_CLIENT_ID and SPOTIPY_CLIENT_SECRET:
#     sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(client_id=SPOTIPY_CLIENT_ID, client_secret=SPOTIPY_CLIENT_SECRET))
# else:
#     print("Spotify credentials not found or invalid. Spotify-assisted lyrics search will be disabled.")
#     sp = None

def ensure_dirs_exist():
    os.makedirs(DOWNLOAD_DIR, exist_ok=True)
    os.makedirs(CREDENTIALS_DIR, exist_ok=True)

def get_audio_info(file_path):
    cmd = ['ffprobe', '-v', 'quiet', '-print_format', 'json', '-show_format', '-show_streams', file_path]
    result = subprocess.run(cmd, capture_output=True, text=True)
    data = json.loads(result.stdout)
    
    audio_stream = next((stream for stream in data['streams'] if stream['codec_type'] == 'audio'), None)
    
    if audio_stream:
        # Use FFmpeg to get the exact bitrate
        bitrate_cmd = ['ffprobe', '-v', 'error', '-select_streams', 'a:0', '-show_entries', 'stream=bit_rate', '-of', 'default=noprint_wrappers=1:nokey=1', file_path]
        bitrate_result = subprocess.run(bitrate_cmd, capture_output=True, text=True)
        bitrate = bitrate_result.stdout.strip()
        
        return {
            'bitrate': f"{int(bitrate) // 1000} kbps" if bitrate.isdigit() else 'Unknown',
            'sample_rate': audio_stream.get('sample_rate', 'Unknown'),
            'channels': audio_stream.get('channels', 'Unknown')
        }
    return {'bitrate': 'Unknown', 'sample_rate': 'Unknown', 'channels': 'Unknown'}

def download_thumbnail(url):
    response = requests.get(url)
    if response.status_code == 200:
        return BytesIO(response.content)
    print("Failed to download thumbnail")
    return None

def embed_thumbnail(audio, thumbnail_data):
    img = Image.open(thumbnail_data)
    img = img.convert('RGB')

    imgdata = BytesIO()
    img.save(imgdata, "JPEG", quality=95)
    imgdata.seek(0)

    picture = Picture()
    picture.type = 3
    picture.mime = "image/jpeg"
    picture.desc = "Cover"
    picture.data = imgdata.getvalue()

    audio.add_picture(picture)

def sanitize_filename(filename):
    return "".join([c for c in filename if c.isalpha() or c.isdigit() or c in ' -_.']).rstrip()

def safe_get(dict_obj, key, default=""):
    value = dict_obj.get(key, default)
    return str(value) if value is not None else default

def get_spotify_song_details(title, artist):
    # if not sp:
    #     return None, None
    sp = None
    query = f"track:{title} artist:{artist}"
    results = sp.search(q=query, type='track', limit=1)
    
    if results['tracks']['items']:
        track = results['tracks']['items'][0]
        return track['name'], track['artists'][0]['name']
    return None, None

def get_lyrics(video_id):
    ytmusic = YTMusic()
    try:
        watch_playlist = ytmusic.get_watch_playlist(videoId=video_id)
        lyrics_browse_id = watch_playlist.get('lyrics')
        if lyrics_browse_id:
            lyrics_data = ytmusic.get_lyrics(lyrics_browse_id)
            if lyrics_data and 'lyrics' in lyrics_data:
                return lyrics_data['lyrics']
        return False
    except Exception as e:
        return False

def get_upload_date(url, info):
    # First, try to get the upload date from yt-dlp info
    upload_date = safe_get(info, 'upload_date', None)
    
    if upload_date and len(upload_date) >= 4:
        return upload_date[:4]
    
    # If yt-dlp fails, try pytube
    try:
        yt = YouTube(url)
        publish_date = yt.publish_date
        if publish_date:
            return str(publish_date.year)
    except Exception as e:
        print(f"Failed to get upload date using pytube: {str(e)}")
    
    # If both methods fail, return "Unknown"
    return "Unknown"

def download_and_process_audio(url, lyrics_providers):
    ensure_dirs_exist()
    

    with yt_dlp.YoutubeDL({'quiet': True}) as ydl:
        info = ydl.extract_info(url, download=False)
        video_id = info['id']
    if os.path.exists(os.path.join(DOWNLOAD_DIR, f"{video_id}.flac")):
       return os.path.join(DOWNLOAD_DIR, f"{video_id}.flac")
    url =  f"https://music.youtube.com/watch?v={video_id}"

    session_dir = create_session_dir(video_id)
    temp_dir = os.path.join(session_dir, "temp")
    working_dir = os.path.join(session_dir, "working")
    os.makedirs(temp_dir, exist_ok=True)
    os.makedirs(working_dir, exist_ok=True)
    # with open("logs.txt", 'a') as log_file:
    #     ydl_opts = [
    #         'yt-dlp',
    #         '-x',
    #         '--output', os.path.join(temp_dir, '%(id)s.%(ext)s'),
    #         '--audio-format', 'flac',
    #         '-f', 'bestaudio',
    #         '--no-post-overwrites',
    #         '--embed-thumbnail',
    #         '--cookies', 'cookies.txt',
    #         '--add-metadata',
    #         '--embed-metadata',
    #         url
    #     ]


    #     # Run yt-dlp asynchronously and redirect output to the log file
    #     process = subprocess.Popen(ydl_opts, stdout=log_file, stderr=log_file)

    #     # Wait for the process to complete
    #     process.wait()
    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': os.path.join(temp_dir, '%(id)s.%(ext)s'),
        'config_location' : 'yt_dlp.conf',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'flac',
            'preferredquality': '0',
        }],
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])

    title = safe_get(info, 'title')
    artist = safe_get(info, 'uploader')
    album = "Sangeet Audio!"
    release_date = get_upload_date(url, info)
    genre = 'Sangeet Joy!'

    temp_file = os.path.join(temp_dir, f"{video_id}.flac")
    working_file = os.path.join(working_dir, f"{video_id}.flac")
    output_path = os.path.join(DOWNLOAD_DIR, f"{video_id}.flac")

    if os.path.exists(output_path):
        print(f"File already exists: {output_path}")
        shutil.rmtree(session_dir)
        return output_path

    shutil.move(temp_file, working_file)

    audio_info = get_audio_info(working_file)
    thumbnail_url = info.get('thumbnail')
    thumbnail_data = download_thumbnail(thumbnail_url) if thumbnail_url else None

    # Get lyrics
    lyrics = get_lyrics(video_id)

    audio = FLAC(working_file)
    audio['title'] = title
    audio['artist'] = artist
    audio['album'] = album
    audio['date'] = release_date
    audio['genre'] = genre
    audio['comment'] = f"Downloaded from Sangeet!: {url}"
    audio['bitrate'] = audio_info['bitrate']
    audio['sample_rate'] = str(audio_info['sample_rate'])
    audio['channels'] = str(audio_info['channels'])
    audio['tracknumber'] = '1'  # Default track number

    print("\nEmbedded Metadata:")
    print(f"Title: {title}")
    print(f"Artist: {artist}")
    print(f"Album: {album}")
    print(f"Date: {release_date}")
    print(f"Genre: {genre}")
    print(f"Bitrate: {audio_info['bitrate']}")
    print(f"Sample Rate: {audio_info['sample_rate']}")
    print(f"Channels: {audio_info['channels']}")

    if lyrics:
        audio['lyrics'] = lyrics
        print("Lyrics: Embedded")
    else:
        print("Lyrics: Not available")

    if thumbnail_data:
        embed_thumbnail(audio, thumbnail_data)
        print("Thumbnail: Embedded")
    else:
        print("Thumbnail: Not available")

    audio.save()

    # Move the processed file to the download directory
    shutil.move(working_file, output_path)

    # Clean up session directory
    shutil.rmtree(session_dir)

    print(f"\nAudio downloaded and processed: {output_path}")
    return output_path

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Download YouTube audio with enhanced metadata and lyrics.")
    parser.add_argument("url", help="YouTube URL to download")
    parser.add_argument("-p", "--providers", nargs="+", choices=['musixmatch', 'lrclib', 'netease', 'megalobiz', 'genius'],
                        default=['musixmatch', 'lrclib', 'netease', 'megalobiz', 'genius'],
                        help="Specify lyrics providers to use")
    args = parser.parse_args()

    result = download_and_process_audio(args.url, args.providers)
    print(f"File saved at: {result}")
