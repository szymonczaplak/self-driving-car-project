@staticmethod
def calculate_x_intersection(A, B, a, angle):
    xA = A[0]
    yA = A[1]
    xB = B[0]
    yB = B[1]

    calculate_x_ = lambda a_: ((((yA - yB) / (xA - xB)) * xA) - yA) / ((yA - yB) / (xA - xB) - a_)  # dziala ok

    x = -np.inf
    y = -np.inf

    if (xA - xB != 0) and (yA - yB) / (xA - xB) - a != 0:
        x = calculate_x_(a)
        y = x * a
    elif xA == xB:
        x = xA / a
        y = x * a

    # if (angle == 0 or angle == 360 or angle == 180) and (xA - xB) != 0:
    #     x = xA if xA < xB else xB
    #     y = yA - (yA - yB) / (xA - xB) * xA

    return np.around(x, decimals=6), np.around(y, decimals=6)


def find_possible_intersections(self, points, scale):
    # compute sensor lines fo

    angle_straight = self.angle
    # angle_left = self.angle - self.sensor_angle
    # angle_right = self.angle + self.sensor_angle

    a = np.tan(np.deg2rad(angle_straight))
    # a_right = np.tan(np.deg2rad(-angle_right))  # may be the opposite
    # a_left = np.tan(np.deg2rad(-angle_left))

    possible_intersections_straight = []
    # possible_intersections_right = []
    # possible_intersections_left = []
    detector = self.position + Vector2(200, 0.0).rotate(-self.angle)

    # for every 2 points in row
    for i in range(len(points) - 1):
        # solving for stright sensor
        A = points[i]
        B = points[i + 1]
        xA = A[0]
        xB = B[0]

        x_straight, y_straight = line_intersection([A, B], [(0.0, 0.0), scale_to_small([detector.x, detector.y], scale,
                                                                                       self.position)])
        #   x_left, y_left = self.calculate_x_intersection(A, B, a_left, angle_left)
        #  x_right, y_right = self.calculate_x_intersection(A, B, a_right, angle_right)

        print("straight", self.angle, x_straight, y_straight, xA, xB, xA <= x_straight <= xB, xA >= x_straight >= xB)

        # equation to solve x

        # if(self.angle >= 180 and y_straight >= 0) or (self.angle <= 180 and y_straight <= 0):
        possible_intersections_straight.append((x_straight, y_straight))
        # if (xA <= x_left <= xB or xA >= x_left >= xB):
        #     possible_intersections_left.append((x_left, y_left))
        # if (xA <= x_right <= xB or xA >= x_right >= xB):
        #     possible_intersections_right.append((x_right, y_right))
    if not possible_intersections_straight:
        possible_intersections_straight = [(detector.x, detector.y)]
    return possible_intersections_straight



 def calculate_distances(self, map: Map, scale: int):
        # scale x and y so that car is always (0,0) point, so sensor lines are y = tan(alfa) * x
        new_out_points = [((x - self.position.x) / scale, (y - self.position.y) / scale) for x, y in map.out_path]
        new_in_points = [((x - self.position.x) / scale, (y - self.position.y) / scale) for x, y in map.in_path]

        car_point = np.array([0, 0])  # thanks to scaling

        #new_out_points = [rotate(car_point, point, self.angle) for point in new_out_points]
        #new_in_points = [rotate(car_point, point, self.angle) for point in new_in_points]

        print("New: \n")
        print(new_out_points[0], map.out_path[0])
        print("\n ")
        print(new_in_points[0], map.in_path[0])
        # compute possible intersections

        possible_intersections_straight_in \
            = self.find_possible_intersections(new_in_points, scale)

        possible_intersections_straight_out \
            = self.find_possible_intersections(new_out_points, scale)

        possible_intersections_straight = possible_intersections_straight_in + possible_intersections_straight_out
        #possible_intersections_left = possible_intersections_left_in + possible_intersections_left_out
        #possible_intersections_right = possible_intersections_right_in + possible_intersections_right_out

        print("Intersections", possible_intersections_straight)

        # sorting points by Euclidean distance



        closest_point_straight = Car.closest_point(possible_intersections_straight)
        # closest_point_left = Car.closest_point(possible_intersections_left)
        # closest_point_right = Car.closest_point(possible_intersections_right)

        straight_sensor_distance = euclidean(closest_point_straight, car_point)
        # left_sensor_distance = euclidean(closest_point_left, car_point)
        # right_sensor_distance = euclidean(closest_point_right, car_point)

        # possible_intersections_straight.sort(key=lambda point: euclidean(
        #                                              np.ndarray(car_position), np.ndarray(point)))
        # possible_intersections_right.sort(key=lambda point: euclidean(
        #                                           np.ndarray(car_position), np.ndarray(point)))
        # possible_intersections_left.sort(key=lambda point: euclidean(
        #                                          np.ndarray(car_position), np.ndarray(point)))

        # straight_sensor_distance = possible_intersections_straight[0] if possible_intersections_straight else -1
        # right_sensor_distance = possible_intersections_right[0] if possible_intersections_right else -1
        # left_sensor_distance = possible_intersections_left[0] if possible_intersections_left else -1

        # return straight_sensor_distance, left_sensor_distance, right_sensor_distance, \
        #        scale_to_large(closest_point_straight, scale, self.position), \
        #        scale_to_large(closest_point_left, scale, self.position), \
        #        scale_to_large(closest_point_right, scale, self.position)

        return  straight_sensor_distance, closest_point_straight