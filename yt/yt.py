from ytmusicapi import YTMusic
import os

from dotenv import load_dotenv


import yt_dlp
import re
import concurrent
from functools import lru_cache
ytmusic = YTMusic()

load_dotenv()
MUSIC_DIR = os.getenv("MUSIC_DIR")
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
def is_youtube_url(url):
    youtube_regex = (
        r'(https?://)?(www\.)?'
        '(youtube|youtu|youtube-nocookie)\.(com|be)/'
        '(watch\?v=|embed/|v/|.+\?v=)?([^&=%\?]{11})'
    )
    youtube_regex_match = re.match(youtube_regex, url)
    return youtube_regex_match is not None

def getresults(term):
    search_term = term
    include_out_universe = True

    if is_youtube_url(search_term):
        # Handle YouTube URL
        ydl_opts = {
            'format': 'bestaudio/best',
            'quiet': True,
            'no_warnings': True,
    
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




