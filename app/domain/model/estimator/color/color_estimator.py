import numpy as np
import pandas as pd
import tensorflow as tf
from keras.callbacks import EarlyStopping, ModelCheckpoint

from domain.model.estimator import Estimator


class ColorEstimator(Estimator):
    class TextLayer:
        name = 'text_layer'

        def __init__(self, n_features: int):
            self.sequential = tf.keras.Sequential([
                tf.keras.layers.Flatten(input_shape=(n_features,), name=f"{self.name}_1"),
                tf.keras.layers.Dense(units=64, activation='relu', name=f"{self.name}_2"),
                tf.keras.layers.Dense(32, activation="relu", name=f"{self.name}_3")
            ], name=self.name)

    class ImageLayer:
        name = 'image_layer'

        def __init__(self, image_height: int, image_width: int, channel: int):
            self.sequential = tf.keras.models.Sequential([
                tf.keras.layers.Conv2D(32, (3, 3), strides=(1, 1), padding='valid', activation='relu',
                                       input_shape=(image_height, image_width, channel), name=f"{self.name}_conv2d_1"),
                tf.keras.layers.MaxPooling2D(pool_size=(2, 2), strides=None, padding='valid', name=f"{self.name}_max_pooling2d_1"),
                tf.keras.layers.Conv2D(64, (3, 3), activation='relu', name=f"{self.name}_conv2d_2"),
                tf.keras.layers.MaxPooling2D((2, 2), name=f"{self.name}_max_pooling2d_2"),
                tf.keras.layers.Flatten(),
                tf.keras.layers.Dense(32, activation='relu', name=f'{self.name}_dense_1'),
            ], name=self.name)

    def __init__(self, text_layer: TextLayer, image_layer: ImageLayer, n_class: int):
        combined = tf.keras.layers.concatenate([image_layer.sequential.output, text_layer.sequential.output])
        z = tf.keras.layers.Dense(32, activation="relu")(combined)
        z = tf.keras.layers.Dense(n_class, activation="softmax")(z)
        self.__model = tf.keras.Model(inputs=[image_layer.sequential.input, text_layer.sequential.input], outputs=z)

    def name(self) -> str:
        return 'color-estimator'

    def version(self) -> float:
        return 0.1

    def fit(self, X, Y):
        X_train, X_test = X
        Y_train, Y_test = Y

        self.__model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])

        history = self.__model.fit(
            X_train, Y_train, batch_size=32, epochs=20,
            validation_data=(X_test, Y_test),
            callbacks=[
                ModelCheckpoint(filepath='./weights/' + self.name() + '-' + str(self.version()) + '-{epoch:02d}.h5'),
                EarlyStopping(monitor='val_loss', patience=5),
            ]
        )

        history_df = pd.DataFrame(history.history, index=history.epoch)
        epoch = np.argmax(history_df['val_accuracy']) + 1
        self.__model.load_weights(f"./weights/{self.name()}-{str(self.version())}-{epoch:02d}.h5")

    def predict(self, X) -> np.ndarray:
        return self.__model.predict(X)
