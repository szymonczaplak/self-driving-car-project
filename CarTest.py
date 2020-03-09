import pytest
from Car import Car
from Map import Map


class TestCar:

    @staticmethod
    def testCalculateDistance():
        scale = 40
        car = Car(2 * scale, 5 * scale)
        map = Map(scale)
        stright, left, right = car.calculate_distances(map, scale)

        print("output")
        print(stright, left, right)
        pass


if __name__ == '__main__':

    TestCar.testCalculateDistance()