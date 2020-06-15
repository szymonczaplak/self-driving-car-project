import pygame

from Car import Car
from Map import Map
from Map2 import Map2

class Evaluator:
    def __init__(self, agent):
        pygame.init()
        pygame.display.set_caption("Self driving car project")
        width = 1200
        height = 1200
        self.screen = pygame.display.set_mode((width, height))
        self.clock = pygame.time.Clock()
        self.ticks = 60
        self.exit = False
        self.agent = agent

    def evaluate_agent_map1(self, direction='left'):
        scale = 40
        print(direction)
        car_image = pygame.image.load('car.png')
        if direction is 'left':
            car = Car(3 * scale, 5 * scale, angle=270)
        else:
            car = Car(3 * scale, 5 * scale, angle=70)

        map = Map2(scale)
        agent = self.agent

        frames_counter = 0
        turns_counter = 0

        while not self.exit:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.exit = True

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
                turns_counter += 1
                car.angle = (car.angle - 2) % 360
            elif choice == 0:
                turns_counter += 1
                car.angle = (car.angle + 2) % 360

            frames_counter += 1
            # if frames_counter == 4000:
            #     break


            self.screen.fill((0, 0, 0))
            map.draw(self.screen, [0, 255, 0])
            # pygame.draw.circle(self.screen, [255,0,0], [int(el) for el in car.position], 2)
            # pygame.display.flip()

            rotated = pygame.transform.rotate(car_image, car.angle)
            rect = rotated.get_rect()
            self.screen.blit(rotated, car.position - (rect.width / 2, rect.height / 2))
            pygame.display.flip()

            self.clock.tick(self.ticks)


        return frames_counter + turns_counter

    def evaluate_agent(self, direction):
        # returns number of frames 'survived' of map1 lef and right
        right_score = self.evaluate_agent_map1(direction=direction)
        return right_score
