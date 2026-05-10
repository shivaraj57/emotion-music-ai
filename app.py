from flask import Flask, render_template, request, jsonify
import os
import random

app = Flask(__name__)

emotions = [
    "Happy",
    "Sad",
    "Angry",
    "Neutral",
    "Surprise"
]

@app.route('/')
def home():

    return render_template("index.html")

@app.route('/detect', methods=['POST'])
def detect():

    emotion = random.choice(emotions)

    return jsonify({
        "emotion": emotion
    })

if __name__ == '__main__':

    app.run(
        host="0.0.0.0",
        port=int(os.environ.get("PORT", 5000))
    )