import os

import numpy as np
import pygame
import tensorflow as tf
import keras.backend as K
from RFAgent import RFAgent
from Car import Car
from Map import Map


class RFGame:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption("Car tutorial")
        width = 1200
        height = 1200
        self.screen = pygame.display.set_mode((width, height))
        self.clock = pygame.time.Clock()
        self.ticks = 60
        self.exit = False
        self.scale = 40
        self.car = Car(2 * self.scale, 5 * self.scale, angle=270)
        self.map = Map(self.scale)


    def get_feedback(self, choice_vector):

        # Uzyj softmaxa / tanh zamiast argmaxa

        # if K.equal(choice, 1):
        #     self.car.angle = (self.car.angle - 2) % 360
        # elif K.equal(choice, 0):
        #     self.car.angle = (self.car.angle + 2) % 360

        self.car.angle = (self.car.angle + 2) % 360
        score = 0

        distance_point_tuples = self.car.calculate_distances(self.map)
        for distance, point in distance_point_tuples:
            print(f"Distance: {distance}")
            score += distance
            if distance < 10:
                score = 1
                break
        return tf.convert_to_tensor(np.array(score))

    def run(self, agent):
        current_dir = os.path.dirname(os.path.abspath(__file__))
        image_path = os.path.join(current_dir, "car.png")
        car_image = pygame.image.load(image_path)
        car = self.car
        map = self.map

        while not self.exit:
            # print(car.position, car.angle)

            # Event queue
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.exit = True
            # Logic
            car.update()
            # print("Car angle: ", car.angle)

            # Drawing
            self.screen.fill((0, 0, 0))
            map.draw(self.screen, [0, 255, 0])

            # draw inside

            distance_vec = []

            distance_point_tuples = car.calculate_distances(map)
            for distance, point in distance_point_tuples:
                print(f"Distance: {distance}")
                distance_vec.append(distance)
                if distance < 10:
                    # COLISION!
                    self.car = Car(2 * self.scale, 5 * self.scale)
                pygame.draw.circle(self.screen, [255, 0, 0], [int(el) for el in point], 5)

            rotated = pygame.transform.rotate(car_image, car.angle)
            rect = rotated.get_rect()
            self.screen.blit(rotated, car.position - (rect.width / 2, rect.height / 2))
            pygame.display.flip()

            # User input
            agent.train_and_act(distance_vec)

            self.clock.tick(self.ticks)
        pygame.quit()


if __name__ == '__main__':
    game = RFGame()
    agent = RFAgent(game)
    game.run(agent)
