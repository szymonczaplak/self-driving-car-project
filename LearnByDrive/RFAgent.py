from pickle import load

import keras
import numpy as np
from keras import optimizers
from keras.layers import Dense, Dropout


class RFAgent:

    def __init__(self, game):
        print("Hello")
        self.game = game
        self.model = self.build_model()
        self.scaler = self.load_scaler()

    def load_scaler(self):
        return load(open('scaler.pkl', 'rb'))

    def build_model(self):
        network = keras.Sequential()
        network.add(Dense(2000, activation='relu', input_shape=(5,)))
        network.add(Dense(3, activation='softmax'))
        optimizer = optimizers.Adam(learning_rate=0.0001, beta_1=0.9, beta_2=0.999, amsgrad=False)
        network.compile(optimizer=optimizer,
                        loss=self.custom_loss_function(self.game))
        return network

    def train_and_act(self, vec):
        vec = np.array(vec).reshape(1, -1)
        scaled = self.scaler.transform(vec)

        predictions = self.model.fit(scaled)

        return np.argmax(predictions)  # 0 - lefft / 1- right / 2 - straight

    def custom_loss_function(self, game):
        def loss(y_true, y_pred):
            return game.get_feedback(y_pred)
        # Return a function
        return loss

