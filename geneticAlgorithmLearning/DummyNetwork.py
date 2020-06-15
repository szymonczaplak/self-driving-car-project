import json
import random
import numpy as np
from keras.activations import sigmoid
from sklearn.neural_network._base import relu
from sklearn.preprocessing import normalize

class DummyNetwork:
    def __init__(self, params=None):
        self.nn_architecture = [
            {"input_dim": 5, "output_dim": 4, "activation": "relu"},
            {"input_dim": 4, "output_dim": 3, "activation": "sigmoid"},
        ]
        self.params_values = params

    def __str__(self):
        if self.params_values is not None:
            return str(self.params_values)
        else:
            return "Uninitialised Network"

    def init_layers(self):
        params_values = {}

        for idx, layer in enumerate(self.nn_architecture):
            layer_idx = idx + 1
            layer_input_size = layer["input_dim"]
            layer_output_size = layer["output_dim"]

            params_values['W' + str(layer_idx)] = np.random.randn(
                layer_output_size, layer_input_size) * 0.1
            params_values['b' + str(layer_idx)] = np.random.randn(
                layer_output_size, 1) * 0.1

        self.params_values = params_values

    def get_choice_for_vector(self, distance_vec):
        input_vec = np.array(distance_vec).reshape(-1,1)
        #input_vec = normalize(input_vec)
        out_vec = self.full_forward_propagation(input_vec)

        return np.argmax(out_vec)

    def single_layer_forward_propagation(self, A_prev, W_curr, b_curr, activation="relu"):
        Z_curr = np.dot(W_curr, A_prev) + b_curr

        if activation is "relu":
            activation_func = relu
        elif activation is "sigmoid":
            activation_func = sigmoid
        else:
            raise Exception('Non-supported activation function')

        return activation_func(Z_curr)

    def full_forward_propagation(self, X):
        A_curr = X

        for idx, layer in enumerate(self.nn_architecture):
            layer_idx = idx + 1
            A_prev = A_curr

            activ_function_curr = layer["activation"]
            W_curr = self.params_values["W" + str(layer_idx)]
            b_curr = self.params_values["b" + str(layer_idx)]
            A_curr = self.single_layer_forward_propagation(A_prev, W_curr, b_curr, activ_function_curr)

        return A_curr

    def toJSON(self):
        return json.dumps(self.params_values)

def sigmoid(Z):
    return 1 / (1 + np.exp(-Z))


def relu(Z):
    return np.maximum(0, Z)
