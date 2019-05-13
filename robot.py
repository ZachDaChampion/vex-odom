from units import *

class Robot:

    # radius of tracking wheels
    wheel_radius = Distance(3.25, 'in')

    # encoder ticks per wheel revolution
    ticks_per_rev = 360.0

    # distance from center of rotation to primary tracking wheels
    primary_wheel_dist = Distance(8.0, 'in')

    # distance from center of rotation to horizontal tracking wheel
    horizontal_wheel_dist = Distance(6.0, 'in')