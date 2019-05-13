import math

# known values
prev_x = 0
prev_y = 0
prev_angle = 0 * (math.pi / 180.0)
current_angle = 90 * (math.pi / 180.0)
dist = 5
relationship_horizontal = 1.0/(15.2/2)
dist_wheel_horizontal = (current_angle - prev_angle) / (2*relationship_horizontal) + 5

# initialize for later
absolute_delta_x = 0
absolute_delta_y = 0

# if no change in angle, calculate linearly
if prev_angle == current_angle:
    absolute_delta_x = dist * math.cos(current_angle) + dist_wheel_horizontal * math.cos(current_angle + math.pi/2)
    absolute_delta_y = dist * math.sin(current_angle) + dist_wheel_horizontal * math.sin(current_angle + math.pi/2)
    
# otherwise calculate using arc-based method
else:

    # calculated values
    delta_angle = current_angle - prev_angle
    reference_angle = abs(delta_angle)
    dist_horizontal = dist_wheel_horizontal - (delta_angle/(2*relationship_horizontal))
    radius = abs(dist / delta_angle)
    radius_horizontal = abs(dist_horizontal/delta_angle)
    
    # caclulate reference delta position
    delta_x = math.cos(reference_angle - (math.pi*.5)) * radius
    delta_y = radius + math.sin(reference_angle - (math.pi*.5)) * radius
    
    delta_x_horizontal = radius_horizontal - math.cos(reference_angle) * radius_horizontal
    delta_y_horizontal = math.sin(reference_angle) * radius_horizontal
    
    # mirror over applicable axes
    delta_x *= -1 if dist < 0 else 1
    delta_y *= -1 if dist * delta_angle < 0 else 1
    delta_x_horizontal *= -1 if dist_horizontal * delta_angle > 0 else 1
    delta_y_horizontal *= -1 if dist_horizontal < 0 else 1
    
    # combine horizontal into standard
    delta_x += delta_x_horizontal
    delta_y += delta_y_horizontal
    
    # rotate to be relative to field instead of bot
    absolute_delta_x = (delta_x * math.cos(prev_angle)) - (delta_y * math.sin(prev_angle))
    absolute_delta_y = (delta_x * math.sin(prev_angle)) + (delta_y * math.cos(prev_angle))

# translate relative to previous position
current_x = prev_x + absolute_delta_x
current_y = prev_y + absolute_delta_y

# print new position
print('(' + str(current_x) + ', ' + str(current_y) + ')')