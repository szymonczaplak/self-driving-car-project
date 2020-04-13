from NetworkIndividual import NetworkUnit
from GAstructure import GeneticAlgorithm
import unittest


class GAStructureTest(unittest.TestCase):
    def test_breed(self):
        NU = NetworkUnit()
        NU2 = NetworkUnit(params={'lstm_layers_number': 4})
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
        population = [NetworkUnit()]
        to_mutate = [0]

        ga = GeneticAlgorithm()

        ga.mutate_selected(to_mutate, population)

        print(population[0])

    def test_save_population(self):
        population = [NetworkUnit()]

        ga = GeneticAlgorithm()
        ga.save_population(population)

        from_file = ga.load_population()
        for idx, v in enumerate(from_file):
            assert str(v) == str(population[idx])




