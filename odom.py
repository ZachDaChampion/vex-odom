import math
from units import Units
from point import Point
from robot import Robot

class Odom:

    # state variables
    current_point = Point()
    translation_dir = 0
    linear_vel = 0
    angular_vel = 0
    last_step_time = 0


    # physical characteristics
    constants = Robot()

    # initialize
    def __init__(self, start=Point()):
        self.current_point = start


    # step linearly (no angle change, so not arc based)
    def step_linear(self, dist_primary, dist_horizontal):
        return Point(
            dist_primary * math.cos(self.current_point.angle) + dist_horizontal * math.cos(self.current_point.angle + 90 * Units.DEG), # delta x
            dist_primary * math.sin(self.current_point.angle) + dist_horizontal * math.sin(self.current_point.angle + 90 * Units.DEG), # delta y
            0                                                                                                                          # theta
        )


    # step arc-based
    def step_arc(self, dist_primary, dist_horizontal, theta):

        # horizontal tracking wheel distance, adjusted to remove distance from turning
        dist_horizontal_adjusted = dist_horizontal - (theta / (2.0 * self.constants.horizontal_wheel_dist))

        # radii of the arcs travelled
        radius_primary = abs(dist_primary / theta)
        radius_horizontal = abs(dist_horizontal_adjusted / theta)

        # calculate reference deltas
        delta_x_primary = math.cos(abs(theta) - 90 * Units.DEG) * radius_primary
        delta_y_primary = math.sin(abs(theta) - 90 * Units.DEG) * radius_primary + radius_primary
        delta_x_horizontal = -math.cos(abs(theta)) * radius_horizontal + radius_horizontal
        delta_y_horizontal = -math.sin(abs(theta)) * radius_horizontal

        # mirror over applicable axes
        delta_x_primary *= -1 if dist_primary < 0 else 1
        delta_y_primary *= -1 if dist_primary * theta > 0 else 1
        delta_x_horizontal *= -1 if dist_horizontal_adjusted * theta > 0 else 1
        delta_y_horizontal *= -1 if dist_horizontal_adjusted < 0 else 1

        # combine primary and horizontal measurements
        delta_x = delta_x_primary + delta_x_horizontal
        delta_y = delta_y_primary + delta_y_horizontal

        # transform delta to be field-centric rather than bot-centric
        delta = Point(
            delta_x * math.cos(self.current_point.angle) - delta_y * math.sin(self.current_point.angle), # delta x
            delta_x * math.sin(self.current_point.angle) + delta_y * math.cos(self.current_point.angle), # delta y
            theta                                                                                        # theta
        )

        # return
        return delta

    
    # step
    def step(self, ticks_left, ticks_right, ticks_horizontal, time):

        # calculate primary and horizontal distances travelled
        dist_primary_left = ticks_left / self.constants.ticks_per_rev * 2.0 * math.pi * self.constants.wheel_radius
        dist_primary_right = ticks_right / self.constants.ticks_per_rev * 2.0 * math.pi * self.constants.wheel_radius
        dist_primary = (dist_primary_left + dist_primary_right) / 2.0
        dist_horizontal = ticks_horizontal / self.constants.ticks_per_rev * 2.0 * math.pi * self.constants.wheel_radius
        
        # calculate angle change
        dist_difference = dist_primary_right - dist_primary_left
        theta = dist_difference / (self.constants.primary_wheel_dist * 2.0)

        # if there is no angle change, calculate linearly (not arc based)
        delta = Point()
        if theta == 0:
            print('linear')
            delta = self.step_linear(dist_primary, dist_horizontal)

        # if there is an angle change, calculate arc-based
        else:
            print('arc')
            delta = self.step_arc(dist_primary, dist_horizontal, theta)

        # calculate delta time
        delta_time = time - self.last_step_time

        # calculate translation direction
        if delta.x != 0 or delta.y != 0:
            self.translation_dir = math.atan2(delta.y, delta.x)

        if delta_time > 0:
            
            # calculate linear velocity
            raw_linear_vel = delta.get_dist(self.current_point) / delta_time
            self.linear_vel = self.linear_vel * .5 + raw_linear_vel * .5

            # calculate angular velocity
            raw_angular_vel = theta / delta_time
            self.angular_vel = self.angular_vel * .5 + raw_angular_vel * .5

        # update state variables
        self.current_point.x = self.current_point.x + delta.x
        self.current_point.y = self.current_point.y + delta.y
        self.current_point.angle = self.current_point.angle + delta.angle
        self.last_step_time = time

        return self.current_point
    

# debug
odom = Odom()
steps = [
    (10 * Units.INCHES, 10 * Units.INCHES, 10 * Units.INCHES, 5 * Units.MS),
    (0 * Units.INCHES, 0 * Units.INCHES, -5 * Units.INCHES, 10 * Units.MS),
    (5 * Units.INCHES, 5 * Units.INCHES, 0 * Units.INCHES, 15 * Units.MS),
    (5 * Units.INCHES, -5 * Units.INCHES, 0 * Units.INCHES, 20 * Units.MS),
]
for step in steps:
    result = odom.step(
        step[0] * odom.constants.ticks_per_rev / (odom.constants.wheel_radius * 2.0 * math.pi),
        step[1] * odom.constants.ticks_per_rev / (odom.constants.wheel_radius * 2.0 * math.pi),
        step[2] * odom.constants.ticks_per_rev / (odom.constants.wheel_radius * 2.0 * math.pi),
        step[3]
    )
    print(result.x / Units.INCHES, result.y / Units.INCHES, result.angle / Units.DEG)
