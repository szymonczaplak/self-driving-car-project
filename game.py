import os
from time import sleep

import pygame
from Car import Car
from Map import Map

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
        car = Car(2 * scale, 5 * scale)
        map = Map(scale)

        while not self.exit:
            #print(car.position, car.angle)

            # Event queue
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.exit = True

            # User input
            pressed = pygame.key.get_pressed()

            if pressed[pygame.K_RIGHT]:
                car.angle = (car.angle - 2) % 360
            elif pressed[pygame.K_LEFT]:
                car.angle = (car.angle + 2) % 360

            # Logic
            car.update()
            #print("Car angle: ", car.angle)


            # Drawing
            self.screen.fill((0, 0, 0))
            map.draw(self.screen, [0, 255, 0])

            # draw inside

            s, A = car.calculate_distances(map)
            print("Distance: ", s)
            pygame.draw.circle(self.screen, [255,0,0], [int(el) for el in A], 5)
            # pygame.draw.circle(self.screen, [255,0,0], [int(el) for el in B], 5)
            # pygame.draw.circle(self.screen, [255,0,0], [int(el) for el in C], 5)


            rotated = pygame.transform.rotate(car_image, car.angle)
            rect = rotated.get_rect()
            self.screen.blit(rotated, car.position - (rect.width / 2, rect.height / 2))
            pygame.display.flip()

            self.clock.tick(self.ticks)
        pygame.quit()


if __name__ == '__main__':
    game = Game()
    game.run()
