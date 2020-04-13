import os

import numpy as np
import pygame

from Agent import Agent
from Car import Car
from Map import Map
from Map2 import Map2


class Game:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption("Car tutorial")
        width = 1200
        height = 1200
        self.screen = pygame.display.set_mode((width, height))
        self.clock = pygame.time.Clock()
        self.ticks = 60
        self.exit = False

    def run(self):
        current_dir = os.path.dirname(os.path.abspath(__file__))
        image_path = os.path.join(current_dir, "car.png")
        car_image = pygame.image.load(image_path)
        scale = 40
        car = Car(5 * scale, 3 * scale, angle=70)
        map = Map(scale)
        agent = Agent()

        vec_history = []
        history_length = agent.history_length
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

            distance_point_tuples = car.calculate_distances(map)
            for distance, point in distance_point_tuples:
                print(f"Distance: {distance}")
                vec_history.append(distance)
                if distance < 10:
                    # COLISION!
                    car = Car(3 * scale, 5 * scale, angle = 270)
                pygame.draw.circle(self.screen, [255, 0, 0], [int(el) for el in point], 5)

            rotated = pygame.transform.rotate(car_image, car.angle)
            rect = rotated.get_rect()
            self.screen.blit(rotated, car.position - (rect.width / 2, rect.height / 2))
            pygame.display.flip()

            if len(vec_history) > history_length:
                vec_history = vec_history[5:]

            # User input
            if len(vec_history) == history_length:
                choice = agent.get_choice(np.array(vec_history).reshape(1, -1))
            else:
                choice = 2

            if choice == 1:
                car.angle = (car.angle - 2) % 360
            elif choice == 0:
                car.angle = (car.angle + 2) % 360

            self.clock.tick(self.ticks)
        pygame.quit()


if __name__ == '__main__':
    game = Game()
    game.run()
