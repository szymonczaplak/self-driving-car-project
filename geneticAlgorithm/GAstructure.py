from random import randint, random
from random import choice as random_choice
from NetworkIndividual import NetworkUnit
from evaluator import Evaluator
import json
from numpy.random import seed
seed(42)

class GeneticAlgorithm:
    def __init__(self, history_file='history.txt'):
        self.history_file = history_file

    def start(self,  target, population_count, ga_epochs, load_population=False,):
        if load_population:
            curent_population = self.load_population(population_count)
        else:
            curent_population = self.spawn_population(population_count)
        for epoch_counter in range(ga_epochs):
            curent_population = self.evolve(curent_population, target, epoch_counter=epoch_counter)

    def evolve(self, pop, target, retain=0.2, random_select=0.05, mutate=0.1, epoch_counter=0):
        # train each idividual in population if needed
        for ind in pop:
            if not ind.trained:
                ind.train()
        self.add_to_history(pop, target, epoch_counter)
        # grade each individual from population and sort them
        graded = [x[1] for x in sorted([(self.idividual_grade(x, target), x) for x in pop], key=lambda y: y[0])]

        # choose parents
        retain_length = int(len(graded) * retain)
        parents = graded[:retain_length]

        # add non-best idividuals for diversity
        for individual in graded[retain_length:]:
            if random_select > random():
                parents.append(individual)

        # mutations
        to_mutate = []
        for individual_idx in range(2, len(parents)):
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
            original_individual = parents[idx]
            original_params = original_individual.params
            param_to_mutate = random_choice(list(original_params.keys()))
            additional_param = None

            if param_to_mutate == 'lstm_neurons':
                additional_param = 'lstm_layers_number'
            elif param_to_mutate == 'lstm_layers_number':
                additional_param = 'lstm_neurons'
            elif param_to_mutate == 'dense_layers_number':
                additional_param = 'dense_neurons'
            elif param_to_mutate == 'dense_neurons':
                additional_param = 'dense_layers_number'

            new_params = original_params.copy()
            del new_params[param_to_mutate]
            if additional_param:
                del new_params[additional_param]
            parents[idx] = NetworkUnit(params=new_params)

        print("Mutation finished!")

    def spawn_population(self, count):
        # Create a number of inviduals
        # return: a list of individuals
        return [NetworkUnit() for _ in range(count)]

    def load_population_params(self):
        with open('last_population.txt', 'r') as last_population_file:
            population_params = json.load(last_population_file)

        population_params = [json.loads(param) for param in population_params]
        return population_params

    def load_population(self, population_count):
        population_params = self.load_population_params()
        population = [NetworkUnit(params=dict(param)) for param in population_params]
        if len(population) < population_count:
            for i in range(population_count - len(population)):
                population.append(NetworkUnit())
        return population

    def save_population(self, population):
        pop_to_string = [NU.toJSON() for NU in population]

        with open('last_population.txt', 'w+') as last_population_file:
            last_population_file.write(json.dumps(pop_to_string))

    def add_to_history(self, population, target, epoch):
        print(f"Adding epoch {epoch} to history!\n")
        self.save_population(population)
        result_string = f'\nEPOCH {epoch}\n'
        for individual in population:
            result_string += "Model: \n" + str(individual) + "\n"
            if individual.trained:
                result_string += f"Grade: {GeneticAlgorithm.idividual_grade(individual, target)}\n"

        with open(self.history_file, 'a+') as history_file:
            history_file.write(result_string)

    @staticmethod
    def idividual_grade(individual, target):
        # Determine the fitness of an individual. Lower is better.
        evaluator = Evaluator(individual)
        return target - evaluator.evaluate_agent()

    @staticmethod
    def breed_parents(male, female):
        print("Breeding!")
        m_params = male.params
        f_params = female.params

        new_params = {}

        param = random_choice(['lstm_layers_number', 'dense_layers_number', 'polynomial_exponent'])
        choice = randint(0, 3)
        if choice == 0:
            new_params[param] = m_params[param]
        elif choice == 1:
            new_params[param] = f_params[param]
        else:
            new_params[param] = int((f_params[param] + m_params[param]) / 2)

        list_param = random_choice(['lstm_neurons', 'dense_neurons'])
        working_param = m_params[list_param].copy()
        for idx in range(min(len(m_params[list_param]), len(f_params[list_param]))):
            choice = randint(0, 3)
            if choice == 0:
                working_param[idx] = m_params[list_param][idx]
            elif choice == 1:
                working_param[idx] = f_params[list_param][idx]
            else:
                working_param[idx] = int((f_params[list_param][idx] + m_params[list_param][idx]) / 2)
        new_params[list_param] = working_param

        child = NetworkUnit(params=new_params)
        print("Breed finished!")
        return child


ga = GeneticAlgorithm()
ga.start(20000, 20, 20, load_population=True)
