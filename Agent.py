from pickle import load

import keras
import numpy as np
from keras import optimizers
from keras.layers import Dense, Dropout


class Agent:

    def __init__(self):
        self.model = self.load_model()
        self.scaler = self.load_scaler()

    def load_scaler(self):
        return load(open('scaler.pkl', 'rb'))

    def load_model(self):
        model = self.build_model()
        model.load_weights('trained_model_test_1st_whole_circle.h5')
        return model

    def load_model_testing(self):
        model = self.build_model_testing()
        model.load_weights('trained_model_test.h5')
        return model

    def build_model_testing(self):
        network = keras.Sequential()
        network.add(Dense(2000, activation='relu', input_shape=(5,)))
        network.add(Dropout(0.15))
        network.add(Dense(2000, activation='relu', input_shape=(5,)))
        network.add(Dropout(0.15))
        network.add(Dense(3, activation='softmax'))
        optimizer = optimizers.Adam(learning_rate=0.0001, beta_1=0.9, beta_2=0.999, amsgrad=False)
        network.compile(optimizer='adam',
                        loss='categorical_crossentropy',
                        metrics=['accuracy'])
        return network

    def build_model(self):
        network = keras.Sequential()
        network.add(Dense(4000, activation='relu', input_shape=(5,)))
        network.add(Dense(3, activation='softmax'))
        optimizer = optimizers.Adam(learning_rate=0.001, beta_1=0.9, beta_2=0.999, amsgrad=False)
        network.compile(optimizer=optimizer,
                        loss='categorical_crossentropy',
                        metrics=['accuracy'])
        return network

    def get_choice(self, vec):
        scaled = self.scaler.transform(vec)

        predictions = self.model.predict(scaled)

        return np.argmax(predictions) # 0 - lefft / 1- right / 2 - straight