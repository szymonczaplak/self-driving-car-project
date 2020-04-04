import keras
from keras.layers import Dense
import numpy as np
from pickle import load
import sklearn

class Agent:

    def __init__(self):
        self.model = self.load_model()
        self.scaler = self.load_scaler()

    def load_scaler(self):
        return load(open('scaler.pkl', 'rb'))

    def load_model(self):
        model = self.build_model()
        model.load_weights('trained_model_test.h5')
        return model

    def build_model(self):
        network = keras.Sequential()
        network.add(Dense(4000, activation='relu', input_shape=(5,)))
        network.add(Dense(3, activation='softmax'))
        network.compile(optimizer='rmsprop',
                        loss='categorical_crossentropy',
                        metrics=['accuracy'])
        return network

    def get_choice(self, vec):
        scaled = self.scaler.transform(vec)

        predictions = self.model.predict(scaled)

        return np.argmax(predictions) # 0 - lefft / 1- right / 2 - straight