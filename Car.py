from time import sleep
import math
import Map
import numpy as np
from pygame.math import Vector2
from scipy.spatial.distance import euclidean
import scipy.spatial.distance as ds

from geometry import line_intersection, line


class Car:
    def __init__(self, x, y, angle=270.0, length=10):
        self.position = Vector2(x, y)
        self.speed = 2
        self.velocity = Vector2(self.speed, 0.0)
        self.angle = angle
        self.length = length
        self.sensor_angle = 60
        self.turning_radius = 5

    def update(self):
        self.position += self.velocity.rotate(-self.angle)
        # angular_velocity = self.velocity.x / self.turning_radius
        # self.angle += degrees(angular_velocity) * dt

    def find_possible_intersections(self, points):
        possible_intersections_straight = []
        detector = self.position + Vector2(150, 0.0).rotate(-self.angle)

        # for every 2 points in row
        for i in range(len(points) - 1):
            # solving for stright sensor
            A = points[i]
            B = points[i + 1]
            xA = A[0]
            xB = B[0]

            x_straight, y_straight = line_intersection(line(A, B), line((self.position.x, self.position.y),
                                                                        [detector.x, detector.y]))
            if x_straight == "lala":
                continue
            if xA <= x_straight <= xB or xA >= x_straight >= xB:
                if (self.angle >= 180 and y_straight >= self.position.y) or (
                        self.angle <= 180 and y_straight <= self.position.y):
                    possible_intersections_straight.append((x_straight, y_straight))
        # if not possible_intersections_straight:
        #     possible_intersections_straight = [(detector.x, detector.y)]
        return possible_intersections_straight

    def calculate_distances(self, map: Map):
        detector = self.position + Vector2(200, 0.0).rotate(-self.angle)

        possible_intersections_straight_out \
            = self.find_possible_intersections(map.out_path)

        possible_intersections_straight_in \
           = self.find_possible_intersections(map.in_path)

        possible_intersections_straight = possible_intersections_straight_out   + possible_intersections_straight_in
        # closest_point_straight = possible_intersections_straight[0]
        closest_point_straight = Car.closest_point(possible_intersections_straight, self.position.x, self.position.y)

        # print("Closest point: ", closest_point_straight)
        return euclidean([self.position.x, self.position.y], closest_point_straight), closest_point_straight

    @staticmethod
    def closest_point(in_array, x=0, y=0):
        arr = np.array(in_array)
        dist = (arr[:, 0] - x) ** 2 + (arr[:, 1] - y) ** 2
        return arr[dist.argmin()]

    def check_colision(self, map: Map):
        x = self.position.x
        y = self.position.y
        pass


def rotate(origin, point, angle):
    """
    Rotate a point counterclockwise by a given angle around a given origin.

    The angle should be given in radians.
    """
    ox, oy = origin
    px, py = point

    qx = ox + math.cos(angle) * (px - ox) - math.sin(angle) * (py - oy)
    qy = oy + math.sin(angle) * (px - ox) + math.cos(angle) * (py - oy)
    return qx, qy


def scale_to_large(array, scale, position):
    return [array[0] * scale + position.x, array[1] * scale + position.y]


def scale_to_small(array, scale, position):
    return [(array[0] - position.x) / scale, (array[1] - position.x) / scale]
