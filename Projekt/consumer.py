from kafka import KafkaConsumer
import json
from dotenv import load_dotenv
import os
import tensorflow as tf
import pickle

from spotify import predict_new_track, get_token

load_dotenv()
client_id = os.getenv("CLIENT_ID") 
client_secret = os.getenv("CLIENT_SECRET")

token = get_token(client_id, client_secret)

with open("model.pkl", "rb") as f:
    model = pickle.load(f)

consumer = KafkaConsumer(
    'song-topic',
    bootstrap_servers=['localhost:9092'],
    value_deserializer=lambda x: json.loads(x.decode('utf-8'))
)

for message in consumer:
    track_info = message.value
    print("Received message:", track_info)
    
    if 'track_id' in track_info:
        prediction = predict_new_track(track_info['track_id'], token, model)
        print("Prediction:", prediction)
    else:
        print("Błąd: Brak track_id w otrzymanych danych")
