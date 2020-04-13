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
        self.sensor_angle = 80
        self.sensor_angle_2 = 15
        self.turning_radius = 2

    def update(self):
        self.position += self.velocity.rotate(-self.angle)
        # angular_velocity = self.velocity.x / self.turning_radius
        # self.angle += degrees(angular_velocity) * dt

    def find_possible_intersections(self, points, detector):
        possible_intersections_straight = []
        all_points = []
        # for every 2 points in row
        for i in range(len(points) - 1):
            # solving for stright sensor
            A = points[i]
            B = points[i + 1]
            xA = np.around(A[0], 2)
            xB = np.around(B[0], 2)
            yA = np.around(A[1], 2)
            yB = np.around(B[1], 2)


            my_x = np.around(self.position.x, 2)
            my_y = np.around(self.position.y, 2)

            detector_x = np.around(detector.x, 2)
            detector_y = np.around(detector.y, 2)


            x_straight, y_straight = line_intersection(line(A, B), line((my_x, my_y),
                                                                        [detector_x, detector_y]))

            if x_straight == "lala":
                continue

            x_straight = np.around(x_straight, 2)
            y_straight = np.around(y_straight, 2)

            all_points.append((x_straight, y_straight))

            if (xA < x_straight < xB or xA > x_straight > xB or (xA == x_straight == xB and (yA <= y_straight <= yB or yA > y_straight > yB)))\
                    and (my_x < x_straight < detector_x or my_x > x_straight > detector_x or (my_x == x_straight == detector_x and (my_y < y_straight < detector_y or my_y >= y_straight >= detector_y))):

                possible_intersections_straight.append((x_straight, y_straight))
        if not possible_intersections_straight:
            pass #(f"WARN all_points = {all_points}")
        return possible_intersections_straight

    def calculate_distances(self, map: Map):

        detector_straight = self.position + Vector2(1500000, 0.0).rotate(-self.angle)
        detector_left = self.position + Vector2(1500000, 0.0).rotate(-(self.angle + self.sensor_angle))
        detector_right = self.position + Vector2(1500000, 0.0).rotate(-(self.angle - self.sensor_angle))
        detector_left_2 = self.position + Vector2(1500000, 0.0).rotate(-(self.angle + self.sensor_angle_2))
        detector_right_2 = self.position + Vector2(1500000, 0.0).rotate(-(self.angle - self.sensor_angle_2))

        distance_point_tuples = []

        for detector in [detector_straight, detector_left, detector_right, detector_left_2, detector_right_2]:

            possible_intersections_out \
                = self.find_possible_intersections(map.out_path, detector)

            possible_intersections_in \
                = self.find_possible_intersections(map.in_path, detector)

            possible_intersections_straight = possible_intersections_out  + possible_intersections_in
            # closest_point_straight = possible_intersections_straight[0]
            closest_point_straight = Car.closest_point(possible_intersections_straight, self.position.x, self.position.y)

            distance_point_tuples.append((euclidean([self.position.x, self.position.y], closest_point_straight), closest_point_straight))
        # print("Closest point: ", closest_point_straight)
        return distance_point_tuples

    @staticmethod
    def closest_point(in_array, x=0, y=0):
        try:
            arr = np.array(in_array)
            dist = (arr[:, 0] - x) ** 2 + (arr[:, 1] - y) ** 2
            return arr[dist.argmin()]
        except:
            # print(f"WARNING, in_array = {in_array} x={x}, y={y}") # TODO: fix it
            return (x + 700, y + 700)


def rotate(origin, point, angle):
    """
    Rotate a point counterclockwise by a given angle aaround a given origin.

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
