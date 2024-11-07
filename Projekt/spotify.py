from dotenv import load_dotenv
import os
import base64
from requests import post
import requests
import numpy as np
from sklearn.preprocessing import StandardScaler


load_dotenv()
client_id = os.getenv("CLIENT_ID") 
client_secret = os.getenv("CLIENT_SECRET")

def get_token(client_id, client_secret):
    auth_string = client_id + ":" + client_secret
    auth_bytes = auth_string.encode("utf-8")
    auth_base64 = str(base64.b64encode(auth_bytes), "utf-8")
    token_url = "https://accounts.spotify.com/api/token"

    headers = {
        "Authorization": "Basic " + auth_base64,
        "Content-Type": "application/x-www-form-urlencoded"
    }

    data = {
        "grant_type": "client_credentials"
    }

    r = requests.post(token_url, headers=headers, data=data)
    token = r.json()["access_token"]
    return token

def get_auth_header(token):
    return {"Authorization": "Bearer " + token}

def search_for_artist(token, artist_name):
    search_url = "https://api.spotify.com/v1/search"
    headers = get_auth_header(token)
    query = f"artist:{artist_name}"
    query_url = f"{search_url}?q={query}&type=artist"
    r = requests.get(query_url, headers=headers)
    return r.json()["artists"]["items"][0]["id"]

def get_artist_id(token, artist_name):
    search_url = "https://api.spotify.com/v1/search"
    headers = get_auth_header(token)
    query = f"artist:{artist_name}"
    query_url = f"{search_url}?q={query}&type=artist"
    r = requests.get(query_url, headers=headers)
    return r.json()["artists"]["items"][0]["id"]

def get_genres(token, artist_id):
    artist_url = f"https://api.spotify.com/v1/artists/{artist_id}"
    headers = get_auth_header(token)
    r = requests.get(artist_url, headers=headers)
    return r.json()["genres"]

def get_recommendations(token, artist_id):
    recommendations_url = "https://api.spotify.com/v1/recommendations"
    headers = get_auth_header(token)
    query = f"seed_artists={artist_id}"
    query_url = f"{recommendations_url}?{query}"
    r = requests.get(query_url, headers=headers)
    return r.json()

def get_tracks(token, artist_id):
    tracks_url = "https://api.spotify.com/v1/artists/{artist_id}/top-tracks"
    headers = get_auth_header(token)
    query = f"country=US"
    query_url = f"{tracks_url}?{query}"
    r = requests.get(query_url, headers=headers)
    return r.json()

def get_albums(token, artist_id):
    albums_url = "https://api.spotify.com/v1/artists/{artist_id}/albums"
    headers = get_auth_header(token)
    query = f"country=US"
    query_url = f"{albums_url}?{query}"
    r = requests.get(query_url, headers=headers)
    return r.json()

def get_audio_features(token, track_id):
    audio_features_url = "https://api.spotify.com/v1/audio-features/{track_id}"
    headers = get_auth_header(token)
    query_url = audio_features_url.format(track_id=track_id)
    r = requests.get(query_url, headers=headers)
    return r.json()

def get_track_id(token, track_name, artist_name):
    search_url = "https://api.spotify.com/v1/search"
    headers = get_auth_header(token)
    query = f"{track_name} {artist_name}"
    query_url = f"{search_url}?q={query}&type=track"
    r = requests.get(query_url, headers=headers)
    return r.json()["tracks"]["items"][0]["id"]


token = get_token(client_id, client_secret)
search_for_artist(token, "Linkin Park")
get_artist_id(token, "Linkin Park")
get_genres(token, get_artist_id(token, "Linkin Park")) 
get_recommendations(token, get_artist_id(token, "Linkin Park"))
get_tracks(token, get_artist_id(token, "Linkin Park"))

get_albums(token, get_artist_id(token, "Linkin Park"))
get_track_id(token, "Numb", "Linkin Park")
get_audio_features(token, get_track_id(token, "Numb", "Linkin Park"))
get_audio_features(token, get_track_id(token, "Jak zapomnieć", "Jeden Osiem L"))
import requests

def print_track_info(track_id, token):
    headers = {"Authorization": f"Bearer {token}"}

    track_url = f"https://api.spotify.com/v1/tracks/{track_id}"
    audio_features_url = f"https://api.spotify.com/v1/audio-features/{track_id}"

    track_response = requests.get(track_url, headers=headers)
    audio_features_response = requests.get(audio_features_url, headers=headers)

    if track_response.status_code != 200 or audio_features_response.status_code != 200:
        print("Błąd w zapytaniu do API Spotify")
        return None

    track_info = track_response.json()
    audio_features_info = audio_features_response.json()

    info = {
        "duration_ms": track_info["duration_ms"],
        "explicit": track_info["explicit"],
        "danceability": audio_features_info["danceability"],
        "energy": audio_features_info["energy"],
        "key": audio_features_info["key"],
        "loudness": audio_features_info["loudness"],
        "mode": audio_features_info["mode"],
        "speechiness": audio_features_info["speechiness"],
        "acousticness": audio_features_info["acousticness"],
        "instrumentalness": audio_features_info["instrumentalness"],
        "liveness": audio_features_info["liveness"],
        "valence": audio_features_info["valence"],
        "tempo": audio_features_info["tempo"],
        "time_signature": audio_features_info["time_signature"]
    }

    return info
print_track_info(get_track_id(token, "Numb", "Linkin Park"), token)
import requests
import pandas as pd

def get_track_info(track_id, token):
    headers = {"Authorization": f"Bearer {token}"}

    track_url = f"https://api.spotify.com/v1/tracks/{track_id}"
    audio_features_url = f"https://api.spotify.com/v1/audio-features/{track_id}"

    track_response = requests.get(track_url, headers=headers)
    audio_features_response = requests.get(audio_features_url, headers=headers)

    if track_response.status_code != 200 or audio_features_response.status_code != 200:
        print("Błąd w zapytaniu do API Spotify")
        return None

    track_info = track_response.json()
    audio_features_info = audio_features_response.json()

    #explicit = bool(track_info["explicit"])

    info = pd.DataFrame({
        "duration_ms": [track_info["duration_ms"]],
        "explicit": [track_info["explicit"]],
        "danceability": [audio_features_info["danceability"]],
        "energy": [audio_features_info["energy"]],
        "key": [audio_features_info["key"]],
        "loudness": [audio_features_info["loudness"]],
        "mode": [audio_features_info["mode"]],
        "speechiness": [audio_features_info["speechiness"]],
        "acousticness": [audio_features_info["acousticness"]],
        "instrumentalness": [audio_features_info["instrumentalness"]],
        "liveness": [audio_features_info["liveness"]],
        "valence": [audio_features_info["valence"]],
        "tempo": [audio_features_info["tempo"]],
        "time_signature": [audio_features_info["time_signature"]]
    })

    return info
track = get_track_info(get_track_id(token, "Numb", "Linkin Park"), token)
track
track.values.shape
import tensorflow as tf

tensor = tf.convert_to_tensor(track.values, dtype=tf.float32)
tensor
import pickle

with open("model.pkl", "rb") as f:
    model = pickle.load(f)

prediction = model.predict(tensor)
np.argmax(prediction)
import tensorflow as tf
from sklearn.preprocessing import StandardScaler
import numpy as np

def predict_new_track(track_id, token, model):
    track = get_track_info(track_id, token)
    if track is not None:
        scaler = StandardScaler()
        track = scaler.fit_transform(track.values)
        tensor = tf.convert_to_tensor(track, dtype=tf.float32)
        prediction = model.predict(tensor)
        return prediction_to_text(np.argmax(prediction))
    else:
        return "Błąd: Nie udało się pobrać informacji o utworze"

def prediction_to_text(prediction):
    if prediction == 0:
        return "Potencjalna popularność utworu bardzo niska"
    elif prediction == 1:
        return "Potencjalna popularność utworu dosyc niska"
    elif prediction == 2:
        return "Potencjalna popularność utworu przecietna"
    elif prediction == 3:
        return "Potencjalna popularność utworu wysoka"
    else:
        return "Utwór przejawia potencjał ogromnego hitu!"
