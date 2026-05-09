import cv2
import numpy as np
import os
from tensorflow.keras.models import load_model

# Load AI model
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

# Load face detector
face_cascade = cv2.CascadeClassifier(
    'haarcascade_frontalface_default.xml'
)

# Open webcam
camera = cv2.VideoCapture(0)

last_emotion = ""
song_text = "Waiting for emotion..."

while True:

    ret, frame = camera.read()

    if not ret:
        break

    # Mirror effect
    frame = cv2.flip(frame, 1)

    # Resize window
    frame = cv2.resize(frame, (1280, 720))

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Top dark panel
    cv2.rectangle(frame, (0,0), (1280,80), (30,30,30), -1)

    # Bottom dark panel
    cv2.rectangle(frame, (0,580), (1280,720), (30,30,30), -1)

    # Project title
    cv2.putText(
        frame,
        "AI MUSIC RECOMMENDATION SYSTEM",
        (220,50),
        cv2.FONT_HERSHEY_SIMPLEX,
        1.2,
        (0,255,255),
        3
    )

    # Detect faces
    faces = face_cascade.detectMultiScale(
        gray,
        scaleFactor=1.3,
        minNeighbors=5
    )

    for (x, y, w, h) in faces:

        face = gray[y:y+h, x:x+w]

        face = cv2.resize(face, (48,48))

        face = face / 255.0

        face = np.reshape(face, (1,48,48,1))

        prediction = model.predict(face, verbose=0)

        emotion = emotion_labels[np.argmax(prediction)]

        # Emotion colors
        color = (255,255,255)

        if emotion == 'happy':
            color = (0,255,0)

        elif emotion == 'sad':
            color = (255,0,0)

        elif emotion == 'angry':
            color = (0,0,255)

        elif emotion == 'surprise':
            color = (0,255,255)

        # Face rectangle
        cv2.rectangle(
            frame,
            (x,y),
            (x+w,y+h),
            color,
            3
        )

        # Emotion background
        cv2.rectangle(
            frame,
            (x,y-40),
            (x+w,y),
            color,
            -1
        )

        # Emotion text
        cv2.putText(
            frame,
            emotion.upper(),
            (x+10,y-10),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.8,
            (0,0,0),
            2
        )

        # Song suggestion
        if emotion != last_emotion:

            last_emotion = emotion

            path = "songs/" + emotion

            if os.path.exists(path):

                files = os.listdir(path)

                if len(files) > 0:

                    song_text = ""

                    for file in files:
                        song_text += file + "   |   "

                else:
                    song_text = "No songs found"

            else:
                song_text = "Folder not found"

    # Song title
    cv2.putText(
        frame,
        "Recommended Songs",
        (30,630),
        cv2.FONT_HERSHEY_SIMPLEX,
        1,
        (0,255,255),
        3
    )

    # Song names
    cv2.putText(
        frame,
        song_text,
        (30,680),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.7,
        (255,255,255),
        2
    )

    # Exit instruction
    cv2.putText(
        frame,
        "Press ESC to Exit",
        (950,50),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.7,
        (255,255,255),
        2
    )

    # Show window
    cv2.imshow(
        "AI Music Recommendation System",
        frame
    )

    # ESC key
    if cv2.waitKey(1) == 27:
        break

camera.release()
cv2.destroyAllWindows()