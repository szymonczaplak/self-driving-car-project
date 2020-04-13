import pygame

from Car import Car
from Map import Map


class Evaluator:
    def __init__(self, agent):
        self.clock = pygame.time.Clock()
        self.ticks = 60
        self.exit = False
        self.agent = agent

    def evaluate_agent_map1(self, direction='left'):
        scale = 40
        if direction == 'left':
            car = Car(2 * scale, 5 * scale, angle=270)
        else:
            car = Car(2 * scale, 5 * scale, angle=70)

        map = Map(scale)
        agent = self.agent

        frames_counter = 0

        while not self.exit:
            # Logic
            car.update()

            distance_vec = []

            distance_point_tuples = car.calculate_distances(map)
            for distance, point in distance_point_tuples:
                distance_vec.append(distance)
                if distance < 10:
                    # COLISION!
                    self.exit = True

            choice = agent.get_choice_for_vector(distance_vec)

            if choice == 1:
                car.angle = (car.angle - 2) % 360
            elif choice == 0:
                car.angle = (car.angle + 2) % 360

            frames_counter += 1
            if frames_counter == 10000:
                break

        return frames_counter

    def evaluate_agent(self):
        # returns number of frames 'survived' of map1 lef and right
        left_score = self.evaluate_agent_map1(direction='left')
        right_score = self.evaluate_agent_map1(direction='right')
        return left_score + right_score
