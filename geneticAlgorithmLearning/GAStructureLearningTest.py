from DummyNetwork import DummyNetwork
from GAStrucureLearning import GeneticAlgorithm
import unittest


class GAStructureLearningTest(unittest.TestCase):
    def test_breed(self):
        NU = DummyNetwork()
        NU2 = DummyNetwork()
        NU.init_layers()
        NU2.init_layers()
        ga = GeneticAlgorithm()
        NU3 = ga.breed_parents(NU, NU2)

        print(f"Parent1: {NU}")
        print(f"Parent2: {NU2}")

        print(f"Child: {NU3}")
        # NU3.epochs = 1
        # NU3.params['epochs'] = 1
        # NU3.train()
        # print(NU3)


    def test_mutate(self):
        d = DummyNetwork()
        d.init_layers()
        population = [d]
        to_mutate = [0]

        ga = GeneticAlgorithm()

        ga.mutate_selected(to_mutate, population)

        print(population[0])

    def test_save_population(self):
        d = DummyNetwork()
        d.init_layers()
        population = [d]

        ga = GeneticAlgorithm()
        ga.save_population(population)

        from_file = ga.load_population(1)
        for idx, v in enumerate(from_file):
            assert str(v) == str(population[idx])




