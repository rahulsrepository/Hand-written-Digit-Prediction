import numpy as np
import tensorflow as tf
from PIL import Image
import base64
import io

class DigitPredictor:
    def __init__(self):
        try:
            self.model = tf.keras.models.load_model('mnist_cnn_model.h5')
            print("Loaded pre-trained model.")
        except:
            print("Model not found. Training a new model.")
            self.train_model()

    def train_model(self):
        (x_train, y_train), (x_test, y_test) = tf.keras.datasets.mnist.load_data()
        x_train = x_train.reshape((x_train.shape[0], 28, 28, 1))
        x_test = x_test.reshape((x_test.shape[0], 28, 28, 1))
        x_train = x_train.astype('float32') / 255
        x_test = x_test.astype('float32') / 255
        y_train = tf.keras.utils.to_categorical(y_train, 10)
        y_test = tf.keras.utils.to_categorical(y_test, 10)

        model = tf.keras.models.Sequential([
            tf.keras.layers.Conv2D(32, (3, 3), activation='relu', input_shape=(28, 28, 1)),
            tf.keras.layers.MaxPooling2D((2, 2)),
            tf.keras.layers.Conv2D(64, (3, 3), activation='relu'),
            tf.keras.layers.MaxPooling2D((2, 2)),
            tf.keras.layers.Conv2D(64, (3, 3), activation='relu'),
            tf.keras.layers.Flatten(),
            tf.keras.layers.Dense(64, activation='relu'),
            tf.keras.layers.Dense(10, activation='softmax')
        ])

        model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])
        model.fit(x_train, y_train, epochs=5, batch_size=64, validation_split=0.2)
        model.save('mnist_cnn_model.h5')
        self.model = model
        print("Model trained and saved as 'mnist_cnn_model.h5'")

    def predict(self, image_data):
        # Remove the data URL prefix
        image_data = image_data.split(',')[1]
        
        # Decode base64 image
        image = Image.open(io.BytesIO(base64.b64decode(image_data)))
        
        # Preprocess the image
        image = image.convert('L')  # Convert to grayscale
        image = image.resize((28, 28))  # Resize to 28x28
        img_array = np.array(image)
        img_array = img_array.astype('float32') / 255
        img_array = img_array.reshape(1, 28, 28, 1)
        
        # Make prediction
        prediction = self.model.predict(img_array)
        return np.argmax(prediction)