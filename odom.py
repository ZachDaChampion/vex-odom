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
        return (
            Distance(dist_primary.get() * math.cos(self.current_point.angle.get('rad')) + dist_horizontal.get() * math.cos(self.current_point.angle.get('rad') + math.pi/2.0)), # delta x
            Distance(dist_primary.get() * math.sin(self.current_point.angle.get('rad')) + dist_horizontal.get() * math.sin(self.current_point.angle.get('rad') + math.pi/2.0)) # delta y
        )

    
    # step
    def step(self, ticks_left, ticks_right, ticks_horizontal, time):

        # calculate primary distance travelled
        dist_primary = Distance()
        dist_horizontal = Distance()
        
        # calculate angle change
        theta = Angle(0)

        # if there is no angle change, calculate linearly (not arc based)
        delta = (Distance(), Distance())
        if theta == Angle(0):
            delta = self.step_linear(dist_primary, dist_horizontal)
    