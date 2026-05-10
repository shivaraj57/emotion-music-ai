from flask import Flask, render_template, jsonify
import os
import random
import cv2
import numpy as np
from keras.models import load_model

app = Flask(__name__)

# Load model
model = load_model("emotion_model.h5")

# Emotion labels
emotion_labels = [
    "Angry",
    "Disgust",
    "Fear",
    "Happy",
    "Sad",
    "Surprise",
    "Neutral"
]

# Face detector
face_cascade = cv2.CascadeClassifier(
    cv2.data.haarcascades +
    'haarcascade_frontalface_default.xml'
)

# Webcam
camera = cv2.VideoCapture(0)

emotion_data = {

    "Happy": {
        "songs":[
            {
                "name":"Shape of You",
                "youtube":"https://youtube.com",
                "spotify":"https://spotify.com"
            }
        ]
    },

    "Sad": {
        "songs":[
            {
                "name":"Fix You",
                "youtube":"https://youtube.com",
                "spotify":"https://spotify.com"
            }
        ]
    },

    "Angry": {
        "songs":[
            {
                "name":"Numb",
                "youtube":"https://youtube.com",
                "spotify":"https://spotify.com"
            }
        ]
    },

    "Neutral": {
        "songs":[
            {
                "name":"Perfect",
                "youtube":"https://youtube.com",
                "spotify":"https://spotify.com"
            }
        ]
    },

    "Surprise": {
        "songs":[
            {
                "name":"Faded",
                "youtube":"https://youtube.com",
                "spotify":"https://spotify.com"
            }
        ]
    }
}

@app.route('/')
def home():

    return render_template("index.html")

@app.route('/detect', methods=['POST'])
def detect():

    success, frame = camera.read()

    if not success:

        return jsonify({
            "emotion":"Camera Error"
        })

    gray = cv2.cvtColor(
        frame,
        cv2.COLOR_BGR2GRAY
    )

    faces = face_cascade.detectMultiScale(
        gray,
        1.3,
        5
    )

    emotion = "Neutral"

    for (x,y,w,h) in faces:

        face = gray[y:y+h, x:x+w]

        face = cv2.resize(face, (48,48))

        face = face / 255.0

        face = np.reshape(
            face,
            (1,48,48,1)
        )

        prediction = model.predict(
            face,
            verbose=0
        )

        emotion = emotion_labels[
            np.argmax(prediction)
        ]

        break

    if emotion not in emotion_data:

        emotion = "Neutral"

    song = random.choice(
        emotion_data[emotion]["songs"]
    )

    return jsonify({

        "emotion":emotion,
        "song":song["name"],
        "youtube":song["youtube"],
        "spotify":song["spotify"]

    })

if __name__ == '__main__':

    app.run(
        host="0.0.0.0",
        port=int(os.environ.get("PORT",5000))
    )