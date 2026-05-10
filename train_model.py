from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense
from tensorflow.keras.layers import Conv2D
from tensorflow.keras.layers import Flatten
from tensorflow.keras.layers import MaxPooling2D
from tensorflow.keras.preprocessing.image import ImageDataGenerator

# Dataset folder
train_dir = "train"

# Image preprocessing
train_datagen = ImageDataGenerator(
    rescale=1./255
)

# Load dataset
train_generator = train_datagen.flow_from_directory(

    train_dir,

    target_size=(48,48),

    color_mode="grayscale",

    batch_size=32,

    class_mode="categorical"

)

# CNN Model
model = Sequential()

model.add(

    Conv2D(

        32,

        (3,3),

        activation='relu',

        input_shape=(48,48,1)

    )

)

model.add(

    MaxPooling2D((2,2))

)

model.add(

    Conv2D(

        64,

        (3,3),

        activation='relu'

    )

)

model.add(

    MaxPooling2D((2,2))

)

model.add(Flatten())

model.add(

    Dense(

        128,

        activation='relu'

    )

)

model.add(

    Dense(

        7,

        activation='softmax'

    )

)

# Compile model
model.compile(

    optimizer='adam',

    loss='categorical_crossentropy',

    metrics=['accuracy']

)

# Train model
model.fit(

    train_generator,

    epochs=10

)

# Save new compatible model
model.save("emotion_model.keras")

print("MODEL TRAINED SUCCESSFULLY")