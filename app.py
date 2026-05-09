from flask import Flask, render_template, Response
import cv2
import numpy as np
import os
from keras.models import load_model

app = Flask(__name__)

# Load trained model
model = load_model('emotion_model.h5')

# Emotion labels
emotion_labels = [
    'angry',
    'disgust',
    'fear',
    'happy',
    'sad',
    'surprise',
    'neutral'
]

# Current emotion
current_emotion = "neutral"

# Face detector
face_cascade = cv2.CascadeClassifier(
    'haarcascade_frontalface_default.xml'
)

# Webcam
camera = cv2.VideoCapture(0)

# Spotify links
spotify_links = {

    "happy":
    "https://open.spotify.com/",

    "sad":
    "https://open.spotify.com/",

    "angry":
    "https://open.spotify.com/",

    "surprise":
    "https://open.spotify.com/",

    "neutral":
    "https://open.spotify.com/"
}

# YouTube links
youtube_links = {

    "happy":
    "https://youtube.com/",

    "sad":
    "https://youtube.com/",

    "angry":
    "https://youtube.com/",

    "surprise":
    "https://youtube.com/",

    "neutral":
    "https://youtube.com/"
}

def generate_frames():

    global current_emotion

    while True:

        success, frame = camera.read()

        if not success:
            break

        gray = cv2.cvtColor(
            frame,
            cv2.COLOR_BGR2GRAY
        )

        faces = face_cascade.detectMultiScale(
            gray,
            scaleFactor=1.3,
            minNeighbors=5
        )

        for (x, y, w, h) in faces:

            face = gray[y:y+h, x:x+w]

            face = cv2.resize(face, (48, 48))

            face = face / 255.0

            face = np.reshape(
                face,
                (1, 48, 48, 1)
            )

            prediction = model.predict(
                face,
                verbose=0
            )

            emotion = emotion_labels[
                np.argmax(prediction)
            ]

            current_emotion = emotion

            # Draw rectangle
            cv2.rectangle(
                frame,
                (x, y),
                (x+w, y+h),
                (0, 255, 255),
                3
            )

            # Show emotion text
            cv2.putText(
                frame,
                emotion,
                (x, y-10),
                cv2.FONT_HERSHEY_SIMPLEX,
                1,
                (0, 255, 255),
                2
            )

        ret, buffer = cv2.imencode(
            '.jpg',
            frame
        )

        frame = buffer.tobytes()

        yield (
            b'--frame\r\n'
            b'Content-Type: image/jpeg\r\n\r\n' +
            frame +
            b'\r\n'
        )

@app.route('/')
def home():

    songs = []

    folder_path = "static/songs/" + current_emotion

    if os.path.exists(folder_path):

        songs = os.listdir(folder_path)

    return render_template(
        'index.html',
        emotion=current_emotion,
        songs=songs,
        spotify=spotify_links.get(current_emotion, "#"),
        youtube=youtube_links.get(current_emotion, "#")
    )

@app.route('/video')
def video():

    return Response(
        generate_frames(),
        mimetype='multipart/x-mixed-replace; boundary=frame'
    )

if __name__ == '__main__':

    app.run(
        host="0.0.0.0",
        port=int(os.environ.get("PORT", 5000))
    )