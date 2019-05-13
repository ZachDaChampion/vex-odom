# parent Unit class
class Unit:

    # dict of conversion factors
    conversions = {}

    # stored value
    value = 0

    # default unit
    default_unit = ''

    # initialize
    def __init__(self, value=0, unit=''):
        self.set(value, self.default_unit if unit == '' else unit)

    # set the stored value
    def set(self, value=0, unit=''):
        self.value = (value.get() if issubclass(type(value), Unit) else value) * self.conversions[self.default_unit if unit == '' else unit]

    # get the stored value
    def get(self, unit=''):
        return self.value / self.conversions[self.default_unit if unit == '' else unit]


# angle class, extends Unit
class Angle(Unit):

    # angular conversion factors
    conversions = {
        'rad': 1.0,
        'deg': 0.0174533
    }
    value = 0

    # default unit
    default_unit = 'rad'


# linear distance class, extends Unit
class Distance(Unit):

    # linear conversion factors
    conversions = {
        'in': 1.0,
        'ft': 12.0
    }
    value = 0

    # default unit
    default_unit = 'in'


# linear velocity class, extends Unit
class LinearVel(Unit):

    # velocity conversion factors
    conversions = {
        'in/sec': 1.0,
        'ft/sec': 12.0,
        'in/ms': 1000.0,
        'ft/ms': 12000.0
    }
    value = 0

    # default unit
    default_unit = 'in/sec'


# angular velocity class, extends Unit
class AngularVel(Unit):

    # velocity conversion factors
    conversions = {
        'rpm': 1.0,
        'rad/sec': 9.5493,
        'rad/ms': 9549.3,
        'deg/sec': 0.166667,
        'deg/ms': 166.667
    }
    value = 0

    # default unit
    default_unit = 'rad/sec'


# time class, extends Unit
class Time(Unit):

    # velocity conversion factors
    conversions = {
        'sec': 1,
        'ms': 1000
    }
    value = 0

    # default unit
    default_unit = 'sec'