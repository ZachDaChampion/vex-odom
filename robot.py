from units import Units

class Robot:

    # radius of tracking wheels
    wheel_radius = 3.25 * Units.INCHES

    # encoder ticks per wheel revolution
    ticks_per_rev = 360.0

    # distance from center of rotation to primary tracking wheels
    primary_wheel_dist = 8.0 * Units.INCHES

    # distance from center of rotation to horizontal tracking wheel
    horizontal_wheel_dist = 6.0 * Units.INCHES