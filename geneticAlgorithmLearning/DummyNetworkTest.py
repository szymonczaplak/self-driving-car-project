from geneticAlgorithmLearning.DummyNetwork import DummyNetwork
import unittest


class DummyUnitParamsTest(unittest.TestCase):

    def test_randomize(self):
        d = DummyNetwork()
        d.init_layers()
        print(d)

    def test_get_choice(self):
        d = DummyNetwork()
        d.init_layers()
        choice = d.get_choice_for_vector([12,12,12,12,12])
        print(choice)