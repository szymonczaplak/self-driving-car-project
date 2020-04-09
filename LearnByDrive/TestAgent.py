from pickle import load

import keras
import numpy as np
from keras import optimizers, Input, Model
from keras.layers import Dense, Dropout, Flatten
from rl import SequentialMemory
from rl.agents import DQNAgent
from rl.policy import LinearAnnealedPolicy, EpsGreedyQPolicy


class RFAgent:

    def __init__(self, game):
        print("Hello")
        self.game = game
        self.model = self.build_model()
        self.scaler = self.load_scaler()

    def load_scaler(self):
        return load(open('scaler.pkl', 'rb'))

    def build_model(state_size, num_actions):
        input = Input(shape=(1, state_size))
        x = Flatten()(input)
        x = Dense(16, activation='relu')(x)
        x = Dense(16, activation='relu')(x)
        x = Dense(16, activation='relu')(x)
        output = Dense(num_actions, activation='linear')(x)
        model = Model(inputs=input, outputs=output)
        print(model.summary())
        memory = SequentialMemory(limit=50000, window_length=1)
        policy = LinearAnnealedPolicy(EpsGreedyQPolicy(), attr='eps', value_max=1., value_min=.1, value_test=.05,
                                      nb_steps=10000)
        dqn = DQNAgent(model=model, nb_actions=num_actions, memory=memory, nb_steps_warmup=10,
                       target_model_update=1e-2, policy=policy)
        return model

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

