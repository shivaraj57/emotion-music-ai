import os
import random
from pygame import mixer

# Start mixer
mixer.init()

# Ask emotion
emotion = input("Enter emotion: ")

# Emotion folder
folder_path = "songs/" + emotion.lower()

# Get all songs
songs = os.listdir(folder_path)

# Pick random song
song = random.choice(songs)

# Full path
song_path = os.path.join(folder_path, song)

# Play song
mixer.music.load(song_path)
mixer.music.play()

print("Playing:", song)

input("Press Enter to stop music")