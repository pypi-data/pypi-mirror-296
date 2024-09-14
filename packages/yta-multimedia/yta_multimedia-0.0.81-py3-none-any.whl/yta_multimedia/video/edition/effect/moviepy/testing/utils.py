"""
These methods are useful to reuse the code and obtain coordinates
and different parameters we need to apply moviepy position effects.
"""

def move_from_to_center(t, initial_x, initial_y, clip, destination_clip, transition_time):
    """
    Moves the 'clip' from the provided ('initial_x', 'initial_y') to the 
    center of the 'destination_clip' in which it will be overlayed.
    """
    final_x = get_center_x(clip, destination_clip)
    final_y = get_center_y(clip, destination_clip)

    return move_from_to(t, initial_x, final_x, initial_y, final_y, transition_time)

def move_from_center_to(t, final_x, final_y, clip, destination_clip, transition_time):
    """
    Moves the 'clip' form the center of the 'destination_clip' in which it
    will be overlayed to the provided ('initial_x', 'initial_y').
    """
    initial_x = get_center_x(clip, destination_clip)
    initial_y = get_center_y(clip, destination_clip)

    return move_from_to(t, initial_x, final_x, initial_y, final_y, transition_time)

def move_from_to(t, initial_x, final_x, initial_y, final_y, transition_time):
    """
    Moves the 'clip' from the provided ('initial_x', 'initial_y') to the 
    provided ('final_x', 'final_y') position.
    """
    x_distance = __get_x_distance(initial_x, final_x)
    y_distance = __get_y_distance(initial_y, final_y)
    movement_factor = __get_movement_factor(t, transition_time)
    x = __calculate_coord(initial_x, movement_factor, x_distance)
    y = __calculate_coord(initial_y, movement_factor, y_distance)

    return x, y

def __calculate_coord(initial_value, movement_factor, distance_to_center):
    return initial_value + movement_factor * distance_to_center

def __get_movement_factor(t, time):
    """
    This method will obtain the movement factor we need to apply in
    effects. This factor represent the amount of movement we need to
    do in one instant (frame) according to the whole movement time 
    we are going to make.
    """
    movement_factor = 1
    if t < time:
        # At this moment the clip isn't still at center
        movement_factor = (t / time)

    return movement_factor

def get_center_x(clip, destination_clip):
    """
    Returns the 'x' coord in which the 'clip' will be centered
    according to the 'destination_clip' in which it will be
    overlayed.
    """
    return destination_clip.w / 2 - clip.w / 2

def get_center_y(clip, destination_clip):
    """
    Returns the 'y' coord in which the 'clip' will be centered
    according to the 'destination_clip' in which it will be
    overlayed.
    """
    return destination_clip.h / 2 - clip.h / 2

# I know these functions below could be incredible absurd but
# I want the code to be understandable for a child of 5 years
# The less you need to guess, the fastest you can build things
def __get_x_distance_to_center(initial_x, clip, destination_clip):
    return __get_x_distance(get_center_x(clip, destination_clip), initial_x)

def __get_y_distance_to_center(initial_y, clip, destination_clip):
    return __get_y_distance(get_center_y(clip, destination_clip), initial_y)

def __get_x_distance(initial_x, final_x):
    return final_x - initial_x

def __get_y_distance(initial_y, final_y):
    return final_y - initial_y