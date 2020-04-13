import pygame


class Map2:
    def __init__(self, scale):
        self.out_path = [
            (3, 1),
            (1, 3),
            (1, 9),
            (4, 12),
            (1, 17),
            (6, 20),
            (12, 20),
            (13, 16),
            (13, 8),
            (14, 8),
            (14, 20),
            (19, 20),
            (21, 18),
            (21, 1),
            (3, 1)
        ]

        self.in_path = [
            (4, 6),
            (9, 11),
            (6, 16),
            (9, 16),
            (10, 14),
            (10, 7),
            (13, 5),
            (17, 6),
            (17, 16),
            (18, 16),
            (18, 5),
            (13, 3),
            (9, 3),
            (4, 6)
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


