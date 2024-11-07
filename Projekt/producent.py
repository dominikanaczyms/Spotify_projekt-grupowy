from kafka import KafkaProducer
import json
import time
from dotenv import load_dotenv
import os
import pandas as pd

load_dotenv()

from spotify import get_track_info, get_track_id, get_token

def json_serializer(data):
    return json.dumps(data).encode("utf-8")

producer = KafkaProducer(
    bootstrap_servers=['localhost:9092'],
    value_serializer=json_serializer
)

client_id = os.getenv("CLIENT_ID") 
client_secret = os.getenv("CLIENT_SECRET")

token = get_token(client_id, client_secret)

# Lista piosenek do przekazania
songs = [
    {"track_name": "Numb", "artist_name": "Linkin Park"},
    {"track_name": "In the End", "artist_name": "Linkin Park"},
    {"track_name": "You're Still The One", "artist_name": "Bailey Jehl"},
    {"track_name": "Jak zapomnieć", "artist_name": "Jeden Osiem L"},
    {"track_name": "Without You", "artist_name": "Parachute"},
    {"track_name": "I'm Yours", "artist_name": "Jason Mraz"},
    {"track_name": "Fine On The Outside", "artist_name": "Priscilla Ahn"},
    {"track_name": "I'll Be Home For Christmas", "artist_name": "Dave Barnes"},
    {"track_name": "Stairway to Heaven", "artist_name": "Led Zeppelin"},
    {"track_name": "Bohemian Rhapsody", "artist_name": "Queen"},
    {"track_name": "Hotel California", "artist_name": "Eagles"},
    {"track_name": "Smells Like Teen Spirit", "artist_name": "Nirvana"},
    {"track_name": "Imagine", "artist_name": "John Lennon"},
    {"track_name": "A Thousand Years", "artist_name": "Christina Perri"},
    {"track_name": "Hey Jude", "artist_name": "The Beatles"},
    {"track_name": "Wonderwall", "artist_name": "Oasis"},
    {"track_name": "Dust to Dust", "artist_name": "The Warning"},
    {"track_name": "Back in Black", "artist_name": "AC/DC"},
    {"track_name": "Beat it", "artist_name": "Michael Jackson"},
    {"track_name": "Livin' on a Prayer", "artist_name": "Bon Jovi"},
]

if __name__ == "__main__":
    while True:
        for song in songs:
            track_id = get_track_id(token, song["track_name"], song["artist_name"])
            track_info = get_track_info(track_id, token)
            print(f"Producing {song['track_name']} by {song['artist_name']} \n {track_info}")

            if track_info is not None:
                # Konwersja DataFrame do listy słowników i dodanie track_id
                track_info_dict = track_info.to_dict(orient='records')
                
                for record in track_info_dict:
                    record['track_id'] = track_id
                    producer.send("song-topic", record)
                    print(f"Sent message: {record}")
            else:
                print(f"Nie udało się pobrać informacji o {song['track_name']} by {song['artist_name']}")

            time.sleep(30)  # Wyślij dane co 30 sekund
