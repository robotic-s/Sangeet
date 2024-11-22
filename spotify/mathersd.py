import os
import json
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from ytmusicapi import YTMusic
import re
from fuzzywuzzy import fuzz
from concurrent.futures import ThreadPoolExecutor, as_completed
from functools import partial
from dotenv import load_dotenv
load_dotenv()
# Set Spotify API credentials
SPOTIPY_CLIENT_ID = os.getenv("spotifyid")
SPOTIPY_CLIENT_SECRET = os.getenv("spotifysecret")

def set_spotify_credentials():
    os.environ['SPOTIPY_CLIENT_ID'] = SPOTIPY_CLIENT_ID
    os.environ['SPOTIPY_CLIENT_SECRET'] = SPOTIPY_CLIENT_SECRET

def get_spotify_item_type(url):
    pattern = r'https?://(?:open\.)?spotify\.com/(track|album|playlist)/([a-zA-Z0-9]+)'
    match = re.match(pattern, url)
    return match.groups() if match else (None, None)

def get_spotify_track_details(sp, track_id):
    try:
        track = sp.track(track_id)
        return {
            'name': track['name'],
            'artists': [artist['name'] for artist in track['artists']],
            'album': track['album']['name'],
            'duration_ms': track['duration_ms'],
            'url': track['external_urls']['spotify'],
            'image_url': track['album']['images'][0]['url'] if track['album']['images'] else None
        }
    except spotipy.exceptions.SpotifyException as e:
        print(f"Error fetching track {track_id}: {str(e)}")
        return None

def get_spotify_tracks(spotify_url):
    set_spotify_credentials()
    item_type, item_id = get_spotify_item_type(spotify_url)
    if not item_type:
        return "Error: Invalid Spotify URL"

    try:
        client_credentials_manager = SpotifyClientCredentials()
        sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)
    except Exception as e:
        return f"Error: Unable to authenticate with Spotify. {str(e)}"

    try:
        if item_type == 'track':
            track = get_spotify_track_details(sp, item_id)
            return [track] if track else []
        elif item_type == 'album':
            album = sp.album(item_id)
            with ThreadPoolExecutor(max_workers=10) as executor:
                tracks = list(executor.map(partial(get_spotify_track_details, sp), 
                                           [track['id'] for track in album['tracks']['items']]))
            return [track for track in tracks if track]
        elif item_type == 'playlist':
            tracks = []
            results = sp.playlist_items(item_id)
            while True:
                with ThreadPoolExecutor(max_workers=10) as executor:
                    batch = list(executor.map(partial(get_spotify_track_details, sp), 
                                              [item['track']['id'] for item in results['items'] if item['track']]))
                tracks.extend([track for track in batch if track])
                if not results['next']:
                    break
                results = sp.next(results)
            return tracks
    except spotipy.exceptions.SpotifyException as e:
        return f"Error: {str(e)}"

def search_youtube_music(query):
    try:
        ytmusic = YTMusic()
        search_results = ytmusic.search(query, filter="songs")
        return search_results
    except Exception as e:
        print(f"Error searching YouTube Music: {str(e)}")
        return []

def calculate_match_score(spotify_track, yt_track):
    title_score = fuzz.ratio(spotify_track['name'].lower(), yt_track['title'].lower())
    
    yt_artists = [artist['name'].lower() for artist in yt_track.get('artists', [])]
    if yt_artists and spotify_track['artists']:
        artist_scores = [max((fuzz.ratio(s_artist.lower(), yt_artist) for yt_artist in yt_artists), default=0)
                         for s_artist in spotify_track['artists']]
        artist_score = sum(artist_scores) / len(artist_scores)
    else:
        artist_score = 0

    duration_score = 0
    if 'duration_seconds' in yt_track and yt_track['duration_seconds']:
        duration_diff = abs(spotify_track['duration_ms'] - yt_track['duration_seconds'] * 1000)
        duration_score = max(0, 100 - (duration_diff / 1000))

    album_score = 0
    if 'album' in yt_track and yt_track['album'].get('name'):
        album_score = fuzz.ratio(spotify_track['album'].lower(), yt_track['album']['name'].lower())

    return (title_score * 0.4) + (artist_score * 0.3) + (duration_score * 0.2) + (album_score * 0.1)

def find_best_match(spotify_track, yt_tracks):
    best_match = None
    best_score = 0
    for yt_track in yt_tracks:
        try:
            score = calculate_match_score(spotify_track, yt_track)
            if score > best_score:
                best_score = score
                best_match = yt_track
        except Exception as e:
            print(f"Error calculating match score: {str(e)}")
    return best_match, best_score

def process_track(spotify_track):
    try:
        search_query = f"{spotify_track['name']} {' '.join(spotify_track['artists'])}"
        yt_tracks = search_youtube_music(search_query)
        
        if yt_tracks:
            best_match, score = find_best_match(spotify_track, yt_tracks)
            if best_match:
                artists = [{'name': artist['name'], 'id': artist.get('id')} for artist in best_match.get('artists', [])]
                return {
                    'spotify': spotify_track,
                    'youtube': {
                        'title': best_match['title'],
                        'artists': artists,
                        'url': f"https://music.youtube.com/watch?v={best_match['videoId']}",
                        'duration': best_match.get('duration_seconds'),
                        'album': best_match.get('album', {}).get('name'),
                        'videoId': best_match['videoId'],
                        'thumbnails': best_match.get('thumbnails', []),
                        'isExplicit': best_match.get('isExplicit', False),
                        'year': best_match.get('year'),
                        'category': best_match.get('category'),
                        'resultType': best_match.get('resultType'),
                        'duration_formatted': best_match.get('duration'),
                    },
                    'match_score': score
                }
        return {'spotify': spotify_track, 'youtube': None, 'match_score': 0}
    except Exception as e:
        print(f"Error processing track {spotify_track['name']}: {str(e)}")
        return {'spotify': spotify_track, 'youtube': None, 'match_score': 0}

def get_spotify_youtube_matches(spotify_url):
    spotify_tracks = get_spotify_tracks(spotify_url)

    if isinstance(spotify_tracks, str):  # Error message
        return {'error': spotify_tracks}

    results = []
    with ThreadPoolExecutor(max_workers=10) as executor:
        future_to_track = {executor.submit(process_track, track): track for track in spotify_tracks}
        for future in as_completed(future_to_track):
            try:
                result = future.result()
                results.append(result)
            except Exception as e:
                print(f"Error processing result: {str(e)}")

    return {
        'spotify_url': spotify_url,
        'track_count': len(results),
        'matches': results
    }

def main():
    spotify_url = input("Enter the Spotify URL (track, album, or playlist): ")
    results = get_spotify_youtube_matches(spotify_url)
    print(json.dumps(results, indent=2))


