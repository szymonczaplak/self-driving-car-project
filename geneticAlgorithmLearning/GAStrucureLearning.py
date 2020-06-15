from random import randint, random, seed
from random import choice as random_choice
from statistics import mean

import numpy as np
from DummyNetwork import DummyNetwork
from evaluator_new import Evaluator
import json
from numpy.random import seed

seed(42)


class GeneticAlgorithm:
    def __init__(self, history_file='history.txt'):
        self.history_file = history_file
        self.mutate = 0.2

    def start(self, target, population_count, ga_epochs, load_population=False, ):
        if load_population:
            curent_population = self.load_population(population_count)
        else:
            curent_population = self.spawn_population(population_count)
        for epoch_counter in range(ga_epochs):
            curent_population = self.evolve(curent_population, target, epoch_counter=epoch_counter, mutate=self.mutate)

    def evolve(self, pop, target, retain=0.2, random_select=0.05, mutate=0.2, epoch_counter=0):
        # train each idividual in population if needed

        # grade each individual from population and sort them

        unit_vs_grade = [(self.idividual_grade(x, target), x) for x in pop]
        grades = [x[0] for x in unit_vs_grade]
        if len(set(grades)) < 3:
            self.mutate = 0.5

        self.add_to_history(pop, grades, target, epoch_counter)
        sorted_unit_vs_grade = sorted(unit_vs_grade, key=lambda y: y[0])
        graded = [x[1] for x in sorted_unit_vs_grade]
        print(f"Best: {[sorted_unit_vs_grade[idx][0] for idx in range(10)]}")
        # choose parents
        retain_length = int(len(graded) * retain)
        parents = graded[:retain_length]

        # add non-best idividuals for diversity
        for individual in graded[retain_length:]:
            if random_select > random():
                parents.append(individual)

        # mutations
        to_mutate = []
        for individual_idx in range(1, len(parents)):
            if mutate > random():
                # change random element of the idividual
                to_mutate.append(individual_idx)

        self.mutate_selected(to_mutate, parents)

        print("All mutations finished!")

        # breed parents
        parents_length = len(parents)
        desired_length = len(pop) - parents_length
        children = []
        while len(children) < desired_length:
            male = randint(0, parents_length - 1)
            female = randint(male, parents_length - 1)
            if male != female:
                male = parents[male]
                female = parents[female]
                child = self.breed_parents(male, female)
                children.append(child)

        parents.extend(children)
        return parents

    @staticmethod
    def mutate_selected(to_mutate, parents):
        print("Mutation!")
        for idx in to_mutate:
            parents[idx].init_layers()

    def spawn_population(self, count):
        # Create a number of inviduals
        # return: a list of individuals
        pop = [DummyNetwork() for _ in range(count)]
        for ind in pop:
            ind.init_layers()
        print(pop)
        return pop

    def load_population_params(self):
        with open('last_population.txt', 'r') as last_population_file:
            population_params = json.load(last_population_file)

        population_params = [json.loads(param) for param in population_params]
        return population_params

    def load_population(self, population_count):
        parameters = [
            {'W1': [np.array([-0.08075051, -0.00991325, -0.13223971, -0.07179357, 0.03552764]),
                    np.array([0.04964046, 0.07877713, -0.03497126, 0.00275545, -0.05813531]),
                    np.array([-0.04141991, 0.08749575, 0.10646686, -0.0386272, -0.00092605]),
                    np.array([0.05735792, -0.05083285, -0.01187205, -0.00992187, -0.04029669])],
             'b1': [np.array([-0.02778843]), np.array([0.05890303]), np.array([0.0116377]), np.array([-0.01171745])],
             'W2': [np.array([-0.00152704, 0.09348534, 0.03575567, 0.02454027]),
                    np.array([-0.04502816, -0.01994074, 0.03037399, 0.0899285]),
                    np.array([0.02514854, 0.05683151, 0.03631307, 0.00758105])],
             'b2': [np.array([-0.03327081]), np.array([0.15642536]), np.array([-0.04355327])]}
,
            {'W1': [np.array([-0.08075051, -0.00991325, -0.13223971, -0.07179357, 0.03552764]),
                    np.array([0.04964046, 0.07877713, -0.03497126, 0.00275545, -0.05813531]),
                    np.array([-0.04141991, 0.08749575, 0.10646686, -0.0386272, -0.00092605]),
                    np.array([0.05735792, -0.05083285, -0.01187205, -0.00992187, -0.04029669])],
             'b1': [np.array([-0.02778843]), np.array([0.05890303]), np.array([0.0116377]), np.array([-0.01171745])],
             'W2': [np.array([-0.00152704, 0.09348534, 0.03575567, 0.02454027]),
                    np.array([-0.04502816, -0.01994074, 0.03037399, 0.0899285]),
                    np.array([0.02514854, 0.05683151, 0.03631307, 0.00758105])],
             'b2': [np.array([-0.03327081]), np.array([0.15642536]), np.array([-0.04355327])]}
,
            {'W1': [np.array([-0.08075051, -0.00991325, -0.13223971, -0.07179357, 0.03552764]),
                    np.array([0.04964046, 0.07877713, -0.03497126, 0.00275545, -0.05813531]),
                    np.array([-0.04141991, 0.08749575, 0.10646686, -0.0386272, -0.00092605]),
                    np.array([0.05735792, -0.05083285, -0.01187205, -0.00992187, -0.04029669])],
             'b1': [np.array([-0.02778843]), np.array([0.05890303]), np.array([0.0116377]), np.array([-0.01171745])],
             'W2': [np.array([-0.00152704, 0.09348534, 0.03575567, 0.02454027]),
                    np.array([-0.04502816, -0.01994074, 0.03037399, 0.0899285]),
                    np.array([0.02514854, 0.05683151, 0.03631307, 0.00758105])],
             'b2': [np.array([-0.03327081]), np.array([0.15642536]), np.array([-0.04355327])]}
        ]
        # population_params = self.load_population_params()
        population = [DummyNetwork(params=dict(param)) for param in parameters]
        if len(population) < population_count:
            for i in range(population_count - len(population)):
                d = DummyNetwork()
                d.init_layers()
                population.append(d)
        return population

    def save_population(self, population):
        # pop_to_string = [NU.toJSON() for NU in population]
        #
        # with open('last_population.txt', 'w+') as last_population_file:
        #     last_population_file.write(json.dumps(pop_to_string))
        pass

    def add_to_history(self, population, grades, target, epoch):
        print(f"Adding epoch {epoch} to history!\n")
        self.save_population(population)
        result_string = f'\nEPOCH {epoch}\n'
        for idx, individual in enumerate(population):
            result_string += "Model: \n" + str(individual) + "\n"
            result_string += f"Grade: {grades[idx]}\n"

        with open(self.history_file, 'a+') as history_file:
            history_file.write(result_string)

    @staticmethod
    def idividual_grade(individual, target):
        # Determine the fitness of an individual. Lower is better.
        evaluator = Evaluator(individual)
        left = evaluator.evaluate_agent('left')
        evaluator = Evaluator(individual)
        right = evaluator.evaluate_agent('right')
        return target - left - right

    @staticmethod
    def breed_parents(male, female):
        m_params = male.params_values
        f_params = female.params_values
        l_rate = 0.01
        new_params = {}

        for key in m_params:
            new_params[key] = []
            for i in range(len(m_params[key])):
                row = []
                for k in range(len(m_params[key][i])):
                    row.append((m_params[key][i][k] + f_params[key][i][k]) / 2)
                new_params[key].append(np.array(row))

        child = DummyNetwork(new_params)

        return child

seed(42)
ga = GeneticAlgorithm()
ga.start(20000, 20, 100, load_population=True)
print("Finished!")
