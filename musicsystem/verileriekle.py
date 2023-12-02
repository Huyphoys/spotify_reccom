
import os
import django



os.environ.setdefault("DJANGO_SETTINGS_MODULE", "musicsystem.settings")
django.setup()


import spotipy as sp
from spotipy.oauth2 import SpotifyClientCredentials
import pandas as pd 
import numpy as np
from musics.models import Track

CLIENT_ID ='c0f7bc444ee0441b96234f958161ca9b'
CLIENT_SECRET ='05a93b93e8ae420c85c451d88a7dbc64'

#"https://open.spotify.com/playlist/37i9dQZF1DXdnOj1VEuhgb"
#"https://open.spotify.com/playlist/37i9dQZF1DX9ASuQophyb3",
playlist =[
        "https://open.spotify.com/playlist/37i9dQZF1DWWY64wDtewQt?si=147da5a21c5940e1",
"https://open.spotify.com/playlist/37i9dQZF1DWXRqgorJj26U?si=94adbb8e865e4d78",
"https://open.spotify.com/playlist/1h0CEZCm6IbFTbxThn6Xcs?si=07769dd26a374589",
"https://open.spotify.com/playlist/2Z0x89wG9yWfsH0D9YYOhc?si=a62f94414fb84228",
"https://open.spotify.com/playlist/37i9dQZF1DWTwnEm1IYyoj?si=e74a715b08de431f",
"https://open.spotify.com/playlist/37i9dQZF1DXcRXFNfZr7Tp?si=94f825916f004e32",
"https://open.spotify.com/playlist/37i9dQZF1DX1C8KR4UJlnr?si=7d3777b6eb0c4aa8", 
"https://open.spotify.com/playlist/37i9dQZF1DX2S9rTKTX6JP?si=0f144a2976de4c02",
"https://open.spotify.com/playlist/37i9dQZF1DWTkxQvqMy4WW?si=2e617c5469db4639",
"https://open.spotify.com/playlist/37i9dQZF1DWSYVW0BVc4a3?si=36b9c2b340304c8a",
"https://open.spotify.com/playlist/37i9dQZF1DXaAWn8mryoAL?si=52982a2087e34967",
"https://open.spotify.com/playlist/37i9dQZF1DXd9rSDyQguIk?si=e200813c5be24ca3",
"https://open.spotify.com/playlist/37i9dQZF1DXbSbnqxMTGx9?si=e881fb3cadce4da7",
"https://open.spotify.com/playlist/37i9dQZF1DWZBCPUIUs2iR?si=71608e0586ca4338",
"https://open.spotify.com/playlist/37i9dQZF1DWWOaP4H0w5b0?si=3f671fd283544b3a",

]


client_credentials_manager = SpotifyClientCredentials(client_id=CLIENT_ID, client_secret=CLIENT_SECRET)
spotify = sp.Spotify(client_credentials_manager = client_credentials_manager, requests_timeout=5, retries=3, status_retries=3, backoff_factor=0.3, status_forcelist=[429, 500, 502, 503, 504])


def get_playlist_tracks(playlist_id):
    results = spotify.user_playlist_tracks("spotify", playlist_id)
    tracks = results['items']
    while results['next']:
        results = spotify.next(results)
        tracks.extend(results['items'])
    return tracks

def filter_important_audio_features(audio_features):
    feature_cols = ['danceability', 'energy', 'loudness', 'speechiness', 'acousticness', 'instrumentalness',
                    'liveness', 'valence', 'tempo', 'duration_ms', 'key', 'mode', 'time_signature']
    if audio_features is None or len(audio_features) == 0:
        return None
    return {k: audio_features[k] for k in feature_cols}

def format_genres(genres):
    return ','.join(genres)

def get_track_genres(track_id):
    artist_id = spotify.track(track_id)['artists'][0]['id']
    genres = spotify.artist(artist_id)['genres']
    return genres

#[0,1] arası değerlere ölçekleme
def normalize(df, columns):
    
    df_normalized = df.copy()
    
    for column in columns:
        df_normalized[column] = (df_normalized[column] - df_normalized[column].min()) / (df_normalized[column].max() - df_normalized[column].min())
    return df_normalized







if __name__ == '__main__':
    data = []

    # urlden playlist idyi almak
    playlist_ids = [url.split('/')[-1].split('?')[0] for url in playlist]
    print(f"Total playlists: {len(playlist_ids)}")

    totaltrack=0
    for i, playlist_id in enumerate(playlist_ids):
        playlist_name = spotify.playlist(playlist_id)['name']
        tracks = get_playlist_tracks(playlist_id)
        num_tracks = len(tracks)
        totaltrack+=num_tracks
        print(f"{num_tracks} tracks")

        # api çağrısını azaltmak
        artist_ids = [track['track']['artists'][0]['id'] for track in tracks] 
        artist_id_chunks = [artist_ids[i:i+50] for i in range(0, len(artist_ids), 50)] # 50 şer adet
        artists = []
        for artist_id_chunk in artist_id_chunks:
            artists.extend(spotify.artists(artist_id_chunk)['artists'])
        
        print(f"{len(artists)} artist details retrieved")

        
        track_ids = [track['track']['id'] for track in tracks]
        track_id_chunks = [track_ids[i:i+50] for i in range(0, len(track_ids), 50)] # 50'şer adet 
        audio_features = []
        for track_id_chunk in track_id_chunks:
            audio_features.extend(spotify.audio_features(track_id_chunk))

        print(f"{len(audio_features)} track audio features retrieved")

        #Track bilgilerini dataya aktarma
        for j, track in enumerate(tracks):
            track_id = track['track']['id']
            track_name = track['track']['name']
            track_artist_name = track['track']['artists'][0]['name']
            track_genres = format_genres(artists[j]['genres'])
            track_audio_features = filter_important_audio_features(audio_features[j]) 
            
        
           
            
            data.append({'id': track_id, 'name': track_name,
                         'artist': track_artist_name,
                          'playlist': playlist_name,
                         'genres': track_genres, **track_audio_features})
            
   
    #genres değeri olmayanları eleme
    data = [item for item in data if item['genres']]
    
    
    #filtreleme
    unique_ids = set()
    filtered_data = []

    for track in data:
        track_id = track['id']
        if not (track_id  in unique_ids or Track.objects.filter(id = track_id).exists()):
            unique_ids.add(track_id)
            filtered_data.append(track)
    

    data = filtered_data

    print(len(data))
    
    if len(data)>0:
        df = pd.DataFrame(data)
        num_cols = df.select_dtypes(include=np.number).columns
        df = normalize(df,num_cols)

        df['genres'] = df['genres'].str.replace(' ', '_')





        required_fields = [
        'id',
        'name',
        'artist',
        'playlist',
        'genres',
        'danceability',
        'energy',
        'loudness',
        'speechiness',
        'acousticness',
        'instrumentalness',
        'liveness',
        'valence',
        'tempo',
        'duration_ms',
        'key',
        'time_signature',
        'mode',
        ]    

        #veritabanına kayıt
        successful_saves=0
        unsuccesful_saves=0
        for _, row in df.iterrows():
            if all(pd.notna(row[field]) for field in required_fields):
                # Track nesnesini oluştur ve kaydet
                
                track = Track(
                    id=row['id'],
                    name=row['name'],
                    artist=row['artist'],
                    playlist=row['playlist'],
                    genres=row['genres'],
                    danceability=row['danceability'],
                    energy=row['energy'],
                    loudness=row['loudness'],
                    speechiness=row['speechiness'],
                    acousticness=row['acousticness'],
                    instrumentalness=row['instrumentalness'],
                    liveness=row['liveness'],
                    valence=row['valence'],
                    tempo=row['tempo'],
                    duration_ms=row['duration_ms'],
                    time_signature=row['time_signature'],
                    key=row['key'],
                    mode=row['mode'],
                    
                )
                
                track.save()
                    
        print(successful_saves)
        print(totaltrack)


                