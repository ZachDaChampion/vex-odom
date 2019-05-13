import math
from units import *

# generic Point class
class Point:

    # position and angle
    x = Distance()
    y = Distance()
    angle = Angle()

    # initialize
    def __init__(self, x=0, y=0, angle=0):
        self.x = x if x is Distance else Distance(x)
        self.y = y if y is Distance else Distance(y)
        self.angle = angle if angle is Angle else Angle(angle)

    # get euclidian distance to other point
    def get_dist(self, p):
        return Distance(((self.x.get() - p.x.get()) ** 2.0 + (self.y.get() - p.y.get()) ** 2.0) ** .5)

    # normalize vector
    def normalize(self, mag=1.0):
        angle = Angle(math.atan2(self.y.get(), self.x.get()), 'rad')
        self.x.set(mag * math.cos(angle.get('rad')))
        self.y.set(mag * math.sin(angle.get('rad')))

    