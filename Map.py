import pygame


class Map:
    def __init__(self, scale):
        self.out_path = [
            (3, 0),
            (1, 2),
            (0, 4),
            (0, 13),
            (2, 15),
            (4, 16),
            (12, 16),
            (16, 20),
            (25, 20),
            (25, 9),
            (20, 4),
            (19, 4),
            (15, 0),
            (3, 0)
        ]

        self.in_path = [
            (6, 3),
            (4, 5),
            (4, 12),
            (5, 13),
            (13, 13),
            (15, 14),
            (18, 17),
            (21, 17),
            (22, 16),
            (22, 12),
            (17, 7),
            (17, 6),
            (14, 3),
            (6, 3)
        ]
        self.scale(scale)
        self.translate(20, 20)

    def scale(self, scale):
        self.out_path = [(x * scale, y * scale) for x, y in self.out_path]
        self.in_path = [(x * scale, y * scale) for x, y in self.in_path]

    def translate(self, a, b):
        self.out_path = [(x + a, y + b) for x, y in self.out_path]
        self.in_path = [(x + a, y + b) for x, y in self.in_path]

    def draw(self, screen, color):
        pygame.draw.lines(screen, color, False, self.out_path)
        pygame.draw.lines(screen, color, False, self.in_path)



