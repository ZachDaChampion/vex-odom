import math
from units import *
from point import Point
from robot import Robot

class Odom:

    # state variables
    current_point = Point()
    translation_dir = Angle()
    linear_vel = LinearVel()
    angular_vel = AngularVel()
    last_step_time = Time()


    # physical characteristics
    constants = Robot()

    # initialize
    def __init__(self, start=Point()):
        self.current_point = start


    # step linearly (no angle change, so not arc based)
    def step_linear(self, dist_primary, dist_horizontal):
        return Point(
            Distance(dist_primary.get() * math.cos(self.current_point.angle.get('rad')) + dist_horizontal.get() * math.cos(self.current_point.angle.get('rad') + math.pi/2.0)), # delta x
            Distance(dist_primary.get() * math.sin(self.current_point.angle.get('rad')) + dist_horizontal.get() * math.sin(self.current_point.angle.get('rad') + math.pi/2.0)), # delta y
            Angle(0)                                                                                                                                                            # theta
        )


    # step arc-based
    def step_arc(self, dist_primary, dist_horizontal, theta):

        # horizontal tracking wheel distance, adjusted to remove distance from turning
        dist_horizontal_adjusted = Distance(dist_horizontal.get() - (theta.get('rad') / (2.0 * self.constants.horizontal_wheel_dist.get())))

        # radii of the arcs travelled
        radius_primary = Distance(abs(dist_primary.get() / theta.get('rad')))
        radius_horizontal = Distance(abs(dist_horizontal_adjusted.get() / theta.get('rad')))

        # calculate reference deltas
        delta_x_primary = Distance(math.cos(abs(theta.get('rad')) - (math.pi / 2.0)) * radius_primary.get())
        delta_y_primary = Distance(math.sin(abs(theta.get('rad')) - (math.pi / 2.0)) * radius_primary.get() + radius_primary.get())
        delta_x_horizontal = Distance(-math.cos(abs(theta.get('rad'))) * radius_horizontal.get() + radius_horizontal.get())
        delta_y_horizontal = Distance(-math.sin(abs(theta.get('rad'))) * radius_horizontal.get())

        # mirror over applicable axes
        delta_x_primary.set(delta_x_primary.get() * (-1 if dist_primary.get() < 0 else 1))
        delta_y_primary.set(delta_y_primary.get() * (-1 if dist_primary.get() * theta.get('rad') > 0 else 1))
        delta_x_horizontal.set(delta_x_horizontal.get() * (-1 if dist_horizontal_adjusted.get() * theta.get('rad') > 0 else 1))
        delta_y_horizontal.set(delta_y_horizontal.get() * (-1 if dist_horizontal_adjusted.get() < 0 else 1))

        # combine primary and horizontal measurements
        delta_x = Distance(delta_x_primary.get() + delta_x_horizontal.get())
        delta_y = Distance(delta_y_primary.get() + delta_y_horizontal.get())

        # transform delta to be field-centric rather than bot-centric
        delta = Point(
            Distance(delta_x.get() * math.cos(self.current_point.angle.get('rad')) - delta_y.get() * math.sin(self.current_point.angle.get('rad'))), # delta x
            Distance(delta_x.get() * math.sin(self.current_point.angle.get('rad')) + delta_y.get() * math.cos(self.current_point.angle.get('rad'))), # delta y
            theta                                                                                                                                    # theta
        )

        # return
        return delta

    
    # step
    def step(self, ticks_left, ticks_right, ticks_horizontal, time):

        # calculate primary and horizontal distances travelled
        dist_primary_left = Distance(ticks_left / self.constants.ticks_per_rev * 2.0 * math.pi * self.constants.wheel_radius.get())
        dist_primary_right = Distance(ticks_right / self.constants.ticks_per_rev * 2.0 * math.pi * self.constants.wheel_radius.get())
        dist_primary = Distance((dist_primary_left.get() + dist_primary_right.get()) / 2.0)
        dist_horizontal = Distance(ticks_horizontal / self.constants.ticks_per_rev * 2.0 * math.pi *self.constants.wheel_radius.get())
        
        # calculate angle change
        dist_difference = dist_primary_right.get() - dist_primary_left.get()
        theta = Angle(dist_difference / (self.constants.primary_wheel_dist.get() * 2.0), 'rad')

        # if there is no angle change, calculate linearly (not arc based)
        delta = Point()
        if theta.get() == Angle(0).get():
            print('linear')
            delta = self.step_linear(dist_primary, dist_horizontal)

        # if there is an angle change, calculate arc-based
        else:
            print('arc')
            delta = self.step_arc(dist_primary, dist_horizontal, theta)

        # calculate delta time
        delta_time = Time(time.get() - self.last_step_time.get())

        # calculate translation direction
        if delta.x.get() == Distance(0).get() and delta.y.get() == Distance(0).get(): self.translation_dir = Angle()
        else: self.translation_dir = Angle(math.atan2(delta.y.get(), delta.x.get()), 'rad')

        # calculate linear velocity
        raw_linear_vel = LinearVel(delta.get_dist(self.current_point).get() / delta_time.get())
        self.linear_vel = LinearVel(self.linear_vel.get() * .5 + raw_linear_vel.get() * .5)

        # calculate angular velocity
        raw_angular_vel = AngularVel(theta.get() / delta_time.get())
        self.angular_vel = AngularVel(self.angular_vel.get() * .5 + raw_angular_vel.get() * .5)

        # update state variables
        self.current_point.x = Distance(self.current_point.x.get() + delta.x.get())
        self.current_point.y = Distance(self.current_point.y.get() + delta.y.get())
        self.current_point.angle = Angle(self.current_point.angle.get() + delta.angle.get())
        self.last_step_time = time

        return self.current_point
    

odom = Odom()
steps = [
    (10, 10, 10, 10)
]
for step in steps:
    result = odom.step(step[0] * 360.0 / (6.5 * math.pi), step[1] * 360.0 / (6.5 * math.pi), step[2] * 360.0 / (6.5 * math.pi), Time(step[3]))
    print(result.x.get('in'), result.y.get('in'), result.angle.get('deg'))
