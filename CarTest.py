import pytest
import numpy as np
from Car import Car
from Map import Map


class TestCar:

    @staticmethod
    def testCalculateDistance():
        scale = 40
        car = Car(2 * scale, 5 * scale)
        map = Map(scale)

        for i in range(361):
            try:
                car.angle = i
                stright, left, right = car.calculate_distances(map, scale)

                print("output")
                print(stright, left, right)
            except IndexError:
                print("ERROR: ", i)
        print("end")
        pass

    @staticmethod
    def testCalculateIntersection():
        xA = 5
        yA = 0
        xB = 10
        yB = 0
        angle = 0

        calculate_x_ = lambda a_: ((((yA - yB) / (xA - xB)) * xA) - yA) / ((yA - yB) / (xA - xB) - a_)
        print(calculate_x_(np.tan(np.deg2rad(angle))))
        print(((xA - xB) != 0) and (yA - yB) / (xA - xB) - np.tan(np.deg2rad(angle)) != 0)

        print("Car output: ", Car.calculate_x_intersection([xA, yA], [xB, yB], np.tan(np.deg2rad(angle)), angle ))

if __name__ == '__main__':

    TestCar.testCalculateIntersection()