from flask import Flask, render_template, jsonify
import os
import random
from tensorflow.keras.models import load_model

app = Flask(__name__)

# Load NEW compatible model
model = load_model("emotion_model.keras")

emotion_data = {

    "Happy": {
        "songs":[
            {
                "name":"Shape of You - Ed Sheeran",
                "youtube":"https://www.youtube.com/watch?v=JGwWNGJdvx8",
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

    # TEMP prediction
    emotion = random.choice(
        list(emotion_data.keys())
    )

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