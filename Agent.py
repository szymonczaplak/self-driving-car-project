from pickle import load

import keras
import numpy as np
from keras import optimizers
from keras.layers import Dense, Dropout
from sklearn.preprocessing import PolynomialFeatures


class Agent:

    def __init__(self):
        self.model = self.load_model_testing_lstm()
        self.scaler = self.load_scaler_lstm()
        self.history_length = 5

    def load_scaler(self):
        return load(open('scaler.pkl', 'rb'))

    def load_scaler_lstm(self):
        return load(open('scaler_lstm.pkl', 'rb'))

    def load_model(self):
        model = self.build_model()
        model.load_weights('trained_model_test_1st_whole_circle.h5')
        return model

    def load_model_testing(self):
        model = self.build_model_testing()
        model.load_weights('trained_model_test.h5')
        return model

    def load_model_testing_lstm(self):
        print("Loading lstm")
        model = self.build_model_testing_lstm()
        model.load_weights('trained_model_test_lstm.h5')
        return model


    def build_model_testing(self):
        network = keras.Sequential()
        network.add(Dense(25, activation='relu', input_shape=(5,)))
        network.add(Dense(25, activation='relu'))
        network.add(Dense(25, activation='relu'))
        network.add(Dense(15, activation='relu'))
        network.add(Dense(3, activation='softmax'))
        optimizer = optimizers.Adam(learning_rate=0.001, beta_1=0.9, beta_2=0.999, amsgrad=False)
        network.compile(optimizer='adam',
                        loss='categorical_crossentropy',
                        metrics=['accuracy'])
        return network

    def build_model_testing_lstm(self):
        model = keras.Sequential()

        model.add(keras.layers.LSTM(
            units=64, return_sequences=True,
            input_shape=(1, 462)
        ))
        model.add(keras.layers.LSTM(
            units=64, return_sequences=True))

        model.add(Dense(30, activation='relu'))
        model.add(Dense(30, activation='relu'))
        #model.add(Dense(30, activation='relu'))
        model.add(Dense(3, activation='softmax'))

        model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])

        return model

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
        print(vec)
        poly = PolynomialFeatures(6)
        vec = poly.fit_transform(vec)
        print(vec)
        scaled = self.scaler.transform(vec)

        predictions = self.model.predict(scaled.reshape(-1,1,462))


        return np.argmax(predictions) # 0 - lefft / 1- right / 2 - straight