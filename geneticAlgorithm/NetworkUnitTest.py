from NetworkIndividual import NetworkUnit
import unittest


class NetworkUnitParamsTest(unittest.TestCase):
    def test_randomiser(self):
        NU = NetworkUnit()
        print(NU)

    def test_build_model(self):
        NU = NetworkUnit()
        print(NU.model.summary())

    def test_randomiser_set_params(self):
        NU = NetworkUnit(params={'dense_neurons': [42]})
        #assert NU.params['epochs'] == 42
        print(NU)

    def test_model_training(self):
        NU = NetworkUnit(params={'epochs': 1})
        NU.train()

    def test_model_predictions(self):
        NU = NetworkUnit(params={'epochs': 1})
        NU.train()
        choice = NU.get_choice_for_vector([300, 300, 123, 124, 424])
        print(choice)
