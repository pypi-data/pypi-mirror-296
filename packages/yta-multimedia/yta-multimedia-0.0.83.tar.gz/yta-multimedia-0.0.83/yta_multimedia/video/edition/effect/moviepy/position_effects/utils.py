from yta_multimedia.video.edition.effect.moviepy.position_effects.enums import ScreenPosition


def move_video_from_pos_to_pos(video, background_video, initial_position: ScreenPosition, final_position: ScreenPosition, start_time: float, duration: float):
    """
    Returns the 'video' positioned (with '.set_position(...)') to go from 
    the provided 'initial_position' to the 'final_position'. It will set the
    'video' start (with '.set_start()') with the provided 'start_time' and
    will also calculate the animation to fit the provided 'duration', that
    will be also set as the video duration (with '.set_duration()').

    This method will return the video positioned as a single element, so 
    make to wrap it properly in an array if it is part of a complex
    animation.
    """
    # TODO: Implement checks
    initial_coords = get_moviepy_position(video, background_video, initial_position)
    final_coords = get_moviepy_position(video, background_video, final_position)

    return video.set_position(lambda t: __move_from_to(t, initial_coords[0], initial_coords[1], final_coords[0], final_coords[1], duration)).set_start(start_time).set_duration(duration)

def move_video_from_coord_to_coord(video, background_video, initial_x: int, initial_y: int, final_x: int, final_y: int, start_time: float, duration: float):
    """
    Returns the 'video' positioned (with '.set_position(...)') to go from 
    the provided initial position ('initial_x', 'initial_y') to the 
    final position ('final_x', 'final_y'). It will set the 'video' start 
    (with '.set_start()') with the provided 'start_time' and will also 
    calculate the animation to fit the provided 'duration', that will be 
    also set as the video duration (with '.set_duration()').

    This method will return the video positioned as a single element, so 
    make to wrap it properly in an array if it is part of a complex
    animation.

    Imagine a scene of a 1920x1080 black background and that the 'x' and 'y'
    you give as parameters are the center of the 'video'. We will calculate 
    to place the provided 'video' there in the real situation, over the 
    'background_video' that could be not 1920x1080.
    """
    # TODO: Implement checks
    initial_coords = get_moviepy_position_by_coords(video, background_video, initial_x, initial_y)
    final_coords = get_moviepy_position_by_coords(video, background_video, final_x, final_y)

    return video.set_position(lambda t: __move_from_to(t, initial_coords[0], initial_coords[1], final_coords[0], final_coords[1], duration)).set_start(start_time).set_duration(duration)


"""
    Coords related functions below
"""
def get_moviepy_position_by_coords(video, background_video, x: int, y: int):
    """
    This method will return the coords (x, y) in which we need to place the
    'video' to have its center in the desired ('x', 'y') position over the 
    also provided 'background_video' by making some calculations as below.

    Imagine a scene of a 1920x1080 black background and that the 'x' and 'y'
    you give as parameters are the center of the 'video'. We will calculate 
    to place the provided 'video' there in the real situation, over the 
    'background_video' that could be not 1920x1080.

    This method seems to calculate and return the same as the other method
    'get_moviepy_position' but giving the user the freedom to provided the
    'x' and 'y' he needs, not a fixed position.

    TODO: Maybe we could mix this method with 'get_moviepy_position' and
    handle the parameter type to do one thing or another.
    """
    # Considering a 1920x1080 scene, recalculate actual coords
    x = (int) (background_video.w * x / 1920)
    y = (int) (background_video.h * y / 1080)

    # This is the place in which we need to center the 'video'
    x -= (video.w / 2)
    y -= (video.h / 2)

    x = int(x)
    y = int(y)

    return (x, y)

def get_moviepy_position(video, background_video, position: ScreenPosition):
    """
    This method will calculate the (x, y) tuple position for the provided
    'video' over the also provided 'background_video' that would be,
    hypothetically, a 1920x1080 black color background static image. The
    provided 'position' will be transformed into the (x, y) tuple according
    to our own definitions.
    """
    position_tuple = None

    if position == ScreenPosition.CENTER:
        position_tuple = (__get_center_x(video, background_video), __get_center_y(video, background_video))

    #           Edges below
    # TOP
    elif position == ScreenPosition.OUT_TOP:
        position_tuple = ((background_video.w / 2) - (video.w / 2), -video.h)
    elif position == ScreenPosition.IN_EDGE_TOP:
        position_tuple = ((background_video.w / 2) - (video.w / 2), -(video.h / 2))
    elif position == ScreenPosition.TOP:
        position_tuple = ((background_video.w / 2) - (video.w / 2), 0)
    # TOP RIGHT
    elif position == ScreenPosition.OUT_TOP_RIGHT:
        position_tuple = (background_video.w, -video.h)
    elif position == ScreenPosition.IN_EDGE_TOP_RIGHT:
        position_tuple = (background_video.w - (video.w / 2), -(video.h / 2))
    elif position == ScreenPosition.TOP_RIGHT:
        position_tuple = (background_video.w - video.w, 0)
    # RIGHT
    elif position == ScreenPosition.OUT_RIGHT:
        position_tuple = (background_video.w, (background_video.h / 2) - (video.h / 2))
    elif position == ScreenPosition.IN_EDGE_RIGHT:
        position_tuple = (background_video.w - (video.w / 2), (background_video.h / 2) - (video.h / 2))
    elif position == ScreenPosition.RIGHT:
        position_tuple = (background_video.w - video.w, (background_video.h / 2) - (video.h / 2))
    # BOTTOM RIGHT
    elif position == ScreenPosition.OUT_BOTTOM_RIGHT:
        position_tuple = (background_video.w, background_video.h)
    elif position == ScreenPosition.IN_EDGE_BOTTOM_RIGHT:
        position_tuple = (background_video.w - (video.w / 2), background_video.h - (video.h / 2))
    elif position == ScreenPosition.BOTTOM_RIGHT:
        position_tuple = (background_video.w - video.w, background_video.h - video.h)
    # BOTTOM
    elif position == ScreenPosition.OUT_BOTTOM:
        position_tuple = ((background_video.w / 2) - (video.w / 2), background_video.h)
    elif position == ScreenPosition.IN_EDGE_BOTTOM:
        position_tuple = ((background_video.w / 2) - (video.w / 2), background_video.h - (video.h / 2))
    elif position == ScreenPosition.BOTTOM:
        position_tuple = ((background_video.w / 2) - (video.w / 2), background_video.h - video.h)
    # BOTTOM LEFT
    elif position == ScreenPosition.OUT_BOTTOM_LEFT:
        position_tuple = (-video.w, background_video.h)
    elif position == ScreenPosition.IN_EDGE_BOTTOM_LEFT:
        position_tuple = (-(video.w / 2), background_video.h - (video.h / 2))
    elif position == ScreenPosition.BOTTOM_LEFT:
        position_tuple = (0, background_video.h - video.h)
    # LEFT
    elif position == ScreenPosition.OUT_LEFT:
        position_tuple = (-video.w, (background_video.h / 2) - (video.h / 2))
    elif position == ScreenPosition.IN_EDGE_LEFT:
        position_tuple = (-(video.w / 2), (background_video.h / 2) - (video.h / 2))
    elif position == ScreenPosition.LEFT:
        position_tuple = (0, (background_video.h / 2) - (video.h / 2))
    # TOP LEFT
    elif position == ScreenPosition.OUT_TOP_LEFT:
        position_tuple = (-video.w, -video.h)
    elif position == ScreenPosition.IN_EDGE_TOP_LEFT:
        position_tuple = (-(video.w / 2), -(video.h / 2))
    elif position == ScreenPosition.TOP_LEFT:
        position_tuple = (0, 0)

    return position_tuple


"""
Internal utils below
"""

def __move_from_to(t, initial_x, final_x, initial_y, final_y, transition_time):
    """
    Returns the (x, y) position for each 't' to make a movement (by
    using the '.set_position()') from the initial position to the
    final position in the 'transition_time'.
    """
    x_distance = final_x - initial_x
    y_distance = final_y - initial_y
    movement_factor = __get_movement_factor(t, transition_time)
    x = __calculate_coord(initial_x, movement_factor, x_distance)
    y = __calculate_coord(initial_y, movement_factor, y_distance)

    return x, y

def __calculate_coord(initial_value, movement_factor, distance):
    """
    Returns the next coordinate based on the 'initial_value' of that
    coordinate, the 'movement_factor' and the 'distance'.
    """
    return initial_value + movement_factor * distance

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

def __get_center_x(video, background_video):
    """
    Returns the 'x' coord in which the 'video' will be centered
    according to the 'background_video' in which it will be
    overlayed.
    """
    # TODO: Ensure 'video' and 'background_video' are valid videos
    return background_video.w / 2 - video.w / 2

def __get_center_y(video, background_video):
    """
    Returns the 'y' coord in which the 'clip' will be centered
    according to the 'background_video' in which it will be
    overlayed.
    """
    # TODO: Ensure 'video' and 'background_video' are valid videos
    return background_video.h / 2 - video.h / 2