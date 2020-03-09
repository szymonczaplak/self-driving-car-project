from time import sleep

import Map
import numpy as np
from pygame.math import Vector2
from scipy.spatial.distance import euclidean
import scipy.spatial.distance as ds


class Car:
    def __init__(self, x, y, angle=270.0, length=10):
        self.position = Vector2(x, y)
        self.speed = 60
        self.velocity = Vector2(self.speed, 0.0)
        self.angle = angle
        self.length = length
        self.sensor_angle = 90
        self.turning_radius = 5

    def update(self, dt):
        self.position += self.velocity.rotate(-self.angle) * dt
        # angular_velocity = self.velocity.x / self.turning_radius
        # self.angle += degrees(angular_velocity) * dt

    def calculate_x_intersection(self, A, B, a, angle):
        xA = A[0]
        yA = A[1]
        xB = B[0]
        yB = B[1]

        calculate_x_ = lambda a_: ((((yA - yB) / (xA - xB)) * xA) - yA) / ((yA - yB) / (xA - xB) - a_)

        x = -np.inf
        y = -np.inf

        if (xA - xB != 0) and (yA - yB) / (xA - xB) - a != 0:
            x = calculate_x_(a)
            y = x * a
        elif xA == xB:
            x = xA / a
            y = x * a

        if (angle == 270 or angle == 270) and (xA - xB) != 0:
            x = 0
            y = yA - (yA - yB) / (xA - xB) * xA

        return np.around(x, decimals=6), np.around(y, decimals=6)

    def find_possible_intersections(self, points):
        # compute sensor lines fo

        angle_straight = self.angle
        angle_left = self.angle - self.sensor_angle
        angle_right = self.angle + self.sensor_angle

        a = np.tan(np.deg2rad(angle_straight))
        a_right = np.tan(np.deg2rad(angle_right))  # may be the opposite
        a_left = np.tan(np.deg2rad(angle_left))

        possible_intersections_straight = []
        possible_intersections_right = []
        possible_intersections_left = []

        # for every 2 points in row
        for i in range(len(points) - 1):
            # solving for stright sensor
            A = points[i]
            B = points[i + 1]
            xA = A[0]
            xB = B[0]

            x_straight, y_straight = self.calculate_x_intersection(A, B, a, angle_straight)
            x_left, y_left = self.calculate_x_intersection(A, B, a_left, angle_left)
            x_right, y_right = self.calculate_x_intersection(A, B, a_right, angle_right)

            print("straight", x_straight, y_straight)

            # equation to solve x

            if (xA <= x_straight <= xB or xA >= x_straight >= xB):
                possible_intersections_straight.append((x_straight, y_straight))
            if (xA <= x_left <= xB or xA >= x_left >= xB):
                possible_intersections_left.append((x_left, y_left))
            if (xA <= x_right <= xB or xA >= x_right >= xB):
                possible_intersections_right.append((x_right, y_right))

        return possible_intersections_straight, possible_intersections_left, possible_intersections_right

    def calculate_distances(self, map: Map, scale: int):
        # scale x and y so that car is always (0,0) point, so sensor lines are y = tan(alfa) * x
        new_out_points = [((x - self.position.x) / scale, (y - self.position.y) / scale) for x, y in map.out_path]
        new_in_points = [((x - self.position.x) / scale, (y - self.position.y) / scale) for x, y in map.in_path]

        # compute possible intersections

        possible_intersections_straight_in, possible_intersections_left_in, possible_intersections_right_in \
            = self.find_possible_intersections(new_in_points)

        possible_intersections_straight_out, possible_intersections_left_out, possible_intersections_right_out \
            = self.find_possible_intersections(new_out_points)

        possible_intersections_straight = possible_intersections_straight_in + possible_intersections_straight_out
        possible_intersections_left = possible_intersections_left_in + possible_intersections_left_out
        possible_intersections_right = possible_intersections_right_in + possible_intersections_right_out

        print("Intersections", possible_intersections_straight_in, possible_intersections_right, possible_intersections_left)

        # sorting points by Euclidean distance

        def closest_point(in_array, x=0, y=0):
            arr = np.array(in_array)
            dist = (arr[:, 0] - x) ** 2 + (arr[:, 1] - y) ** 2
            return arr[dist.argmin()]

        car_point = np.array([0,0]) # thanks to scaling

        straight_sensor_distance = euclidean(closest_point(possible_intersections_straight), car_point)
        left_sensor_distance = euclidean(closest_point(possible_intersections_right), car_point)
        right_sensor_distance = euclidean(closest_point(possible_intersections_left), car_point)

        # possible_intersections_straight.sort(key=lambda point: euclidean(
        #                                              np.ndarray(car_position), np.ndarray(point)))
        # possible_intersections_right.sort(key=lambda point: euclidean(
        #                                           np.ndarray(car_position), np.ndarray(point)))
        # possible_intersections_left.sort(key=lambda point: euclidean(
        #                                          np.ndarray(car_position), np.ndarray(point)))

        # straight_sensor_distance = possible_intersections_straight[0] if possible_intersections_straight else -1
        # right_sensor_distance = possible_intersections_right[0] if possible_intersections_right else -1
        # left_sensor_distance = possible_intersections_left[0] if possible_intersections_left else -1

        return straight_sensor_distance, left_sensor_distance, right_sensor_distance

    def check_colision(self, map: Map):
        x = self.position.x
        y = self.position.y
        pass
