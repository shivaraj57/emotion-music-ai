from keras.models import load_model

model = load_model("emotion_model.h5", compile=False)

model.save("new_emotion_model.h5")