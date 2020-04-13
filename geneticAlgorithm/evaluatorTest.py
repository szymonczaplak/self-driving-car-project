from NetworkIndividual import NetworkUnit
from evaluator import Evaluator
import unittest


class EvaluatorTest(unittest.TestCase):
    def test_model_evaluation(self):

        model = NetworkUnit(params={'epochs': 1})
        model.train()
        evaluator = Evaluator(model)

        print(evaluator.evaluate_agent())
