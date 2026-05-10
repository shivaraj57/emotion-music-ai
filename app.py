from flask import Flask, render_template, jsonify
import os
import random
import cv2
import numpy as np
from tensorflow.keras.models import load_model

app = Flask(__name__)

# Load trained model
model = load_model(
    "emotion_model.h5",
    compile=False
)

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

# Songs for each emotion
emotion_data = {

    "Happy": {
        "songs":[
            {
                "name":"Shape of You - Ed Sheeran",
                "youtube":"https://www.youtube.com/watch?v=JGwWNGJdvx8",
                "spotify":"https://open.spotify.com/"
            },

            {
                "name":"Believer - Imagine Dragons",
                "youtube":"https://www.youtube.com/watch?v=7wtfhZwyrcc",
                "spotify":"https://open.spotify.com/"
            }
        ]
    },

    "Sad": {
        "songs":[
            {
                "name":"Fix You - Coldplay",
                "youtube":"https://www.youtube.com/watch?v=k4V3Mo61fJM",
                "spotify":"https://open.spotify.com/"
            }
        ]
    },

    "Angry": {
        "songs":[
            {
                "name":"Numb - Linkin Park",
                "youtube":"https://www.youtube.com/watch?v=kXYiU_JCYtU",
                "spotify":"https://open.spotify.com/"
            }
        ]
    },

    "Neutral": {
        "songs":[
            {
                "name":"Perfect - Ed Sheeran",
                "youtube":"https://www.youtube.com/watch?v=2Vv-BfVoq4g",
                "spotify":"https://open.spotify.com/"
            }
        ]
    },

    "Surprise": {
        "songs":[
            {
                "name":"Blinding Lights - Weeknd",
                "youtube":"https://www.youtube.com/watch?v=4NRXx6U8ABQ",
                "spotify":"https://open.spotify.com/"
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

        face = cv2.resize(
            face,
            (48,48)
        )

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