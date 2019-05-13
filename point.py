import math
from units import Units

# generic Point class
class Point:

    # position and angle
    x = 0
    y = 0
    angle = 0

    # initialize
    def __init__(self, x=0, y=0, angle=0):
        self.x = x
        self.y = y
        self.angle = angle

    # get euclidian distance to other point
    def get_dist(self, p):
        return (self.x - p.x ** 2.0 + (self.y - p.y) ** 2.0) ** .5

    # normalize vector
    def normalize(self, mag=1.0):
        angle = math.atan2(self.y.get(), self.x.get()) * Units.RAD
        self.x = mag * math.cos(angle)
        self.y = mag * math.sin(angle)

    