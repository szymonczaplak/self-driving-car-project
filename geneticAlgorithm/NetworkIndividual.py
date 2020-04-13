import json
from random import randint, random

from keras.callbacks import EarlyStopping, ModelCheckpoint, ReduceLROnPlateau
from sklearn.preprocessing import PolynomialFeatures
from sklearn.preprocessing import StandardScaler
from pickle import dump
import numpy as np
import uuid

import keras
import pandas as pd


class NetworkUnit:
    def __init__(self, train_filename='testing.csv', params=None):
        self.id = uuid.uuid4()
        self.train_filename = train_filename
        self.epochs = 25
        self.lstm_layers_number_range = (1, 3)  # must be > 0
        self.lstm_neurons_range = (16, 128)
        self.dense_layers_number_range = (1, 4)
        self.dense_neurons_range = (10, 400)
        self.polynomial_number_range = (1, 3)
        self.params = {'id': str(self.id), 'epochs': self.epochs}
        if params is None:
            self.randomise()
        else:
            self.randomise()
            self.params.update(params)
            if 'lstm_layers_number' in params:
                if 'lstm_neurons' not in params or len(self.params['lstm_neurons']) != self.params[
                    'lstm_layers_number']:
                    self.params['lstm_neurons'] = [randint(self.lstm_neurons_range[0], self.lstm_neurons_range[1] + 1)
                                                   for _ in range(self.params['lstm_layers_number'])]

            if 'dense_layers_number' in params:
                if 'dense_neurons' not in params or len(self.params['dense_neurons']) != self.params[
                    'dense_layers_number']:
                    self.params['dense_neurons'] = [
                        randint(self.dense_neurons_range[0], self.dense_neurons_range[1] + 1)
                        for _ in range(self.params['dense_layers_number'])]

            if 'dense_neurons' in params:
                self.params['dense_layers_number'] = len(self.params['dense_neurons'])
            if 'lstm_neurons' in params:
                self.params['lstm_layers_number'] = len(self.params['lstm_neurons'])

        self.model = None
        self.scaler = None
        self.n_features = None
        self.trained = False

    def __str__(self):
        return str(self.params)

    def randomise(self):
        self.params['lstm_layers_number'] = randint(self.lstm_layers_number_range[0],
                                                    self.lstm_layers_number_range[1] + 1)
        self.params['lstm_neurons'] = [randint(self.lstm_neurons_range[0], self.lstm_neurons_range[1] + 1)
                                       for _ in range(self.params['lstm_layers_number'])]
        self.params['dense_layers_number'] = randint(self.dense_layers_number_range[0],
                                                     self.dense_layers_number_range[1] + 1)
        self.params['dense_neurons'] = [randint(self.dense_neurons_range[0], self.dense_neurons_range[1] + 1)
                                        for _ in range(self.params['dense_layers_number'])]
        self.params['polynomial_exponent'] = randint(self.polynomial_number_range[0],
                                                     self.polynomial_number_range[1] + 1)

    def build_model(self, n_of_input_features):
        network = keras.Sequential()

        # because lstm layers number > 0 // input shape
        network.add(keras.layers.LSTM(
            units=self.params['lstm_neurons'][0], return_sequences=True,
            input_shape=(1, n_of_input_features)
        ))

        # adding additional lstm layers
        for idx in range(1, self.params['lstm_layers_number']):
            try:
                network.add(keras.layers.LSTM(
                    units=self.params['lstm_neurons'][idx], return_sequences=True,
                ))
            except:
                print("EXCEPTION LSTM layers - something is wrong with breeding")
                self.params['lstm_layers_number'] = idx
                break

        # adding dense layers
        for idx in range(self.params['dense_layers_number']):
            try:
                network.add(keras.layers.Dense(self.params['dense_neurons'][idx], activation='relu'))
            except:
                print("EXCEPTION dense layers - something is wrong with breeding")
                self.params['dense_layers_number'] = idx
                break

        # output layer
        network.add(keras.layers.Dense(3, activation='softmax'))

        network.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])

        return network

    def save_scaler(self):
        scaler_out_file = f'scalers/{self.id}_scaler.pkl'
        dump(self.scaler, open(scaler_out_file, 'wb+'))

    def preprocess_train_data(self):
        headers = ['sensor_1', 'sensor_2', 'sensor_3', 'sensor_4', 'sensor_5', 'decision']
        data_original = pd.read_csv(self.train_filename, names=headers)
        df = pd.get_dummies(data_original, columns=['decision'])
        x = df.iloc[:, :-3]
        y = df.iloc[:, -3:]
        poly = PolynomialFeatures(self.params['polynomial_exponent'])
        features = poly.fit_transform(x)
        self.n_features = len(features[0])
        x = pd.DataFrame(features)
        self.scaler = StandardScaler()
        x = self.scaler.fit_transform(x)
        x = x.reshape(-1, 1, self.n_features)
        y = np.array(y).reshape(-1, 1, 3)
        self.save_scaler()

        return x, y

    def train(self):
        self.trained = True
        x, y = self.preprocess_train_data()

        self.model = self.build_model(self.n_features)

        earlyStopping = EarlyStopping(monitor='val_loss', patience=10, verbose=0, mode='min')
        mcp_save = ModelCheckpoint(f'models/{self.id}_model_weights.hdf5', save_best_only=True, monitor='val_loss',
                                   mode='min')
        reduce_lr_loss = ReduceLROnPlateau(monitor='val_loss', factor=0.1, patience=7, verbose=1, epsilon=1e-4,
                                           mode='min')
        self.model.fit(x, y, verbose=0, epochs=self.params['epochs'],
                       callbacks=[earlyStopping, mcp_save, reduce_lr_loss], validation_split=0.25, )

        self.model.load_weights(f'models/{self.id}_model_weights.hdf5')

    def get_choice_for_vector(self, vec):
        vec = np.array(vec).reshape(1, -1)
        poly = PolynomialFeatures(self.params['polynomial_exponent'])
        vec = poly.fit_transform(vec)
        scaled = self.scaler.transform(vec)

        predictions = self.model.predict(scaled.reshape(-1, 1, self.n_features))

        return np.argmax(predictions)  # 0 - lefft / 1- right / 2 - straight

    def toJSON(self):
        return json.dumps(self.params)
