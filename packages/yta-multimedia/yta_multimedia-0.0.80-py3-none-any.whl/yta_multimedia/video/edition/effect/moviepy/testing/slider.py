from yta_multimedia.video.edition.effect.moviepy.testing.utils import move_from_center_to, move_from_to, move_from_to_center, get_center_x, get_center_y
from yta_multimedia.video.edition.effect.moviepy.testing.others import shake_at_center

"""

            METHODS FOR EXTERNAL BELOW
        These methods will be used in
        PositionEffect enum.

"""
def slide_in_shake_and_slide_out(clip, destination_clip, time):
    SHORT_TIME = (time / 6)
    LONG_TIME = (time / 6) * 4

    return [
        clip.set_position(lambda t: slide_from_left_to_center(t, clip, destination_clip, SHORT_TIME)).set_start(0).set_duration(SHORT_TIME),
        clip.set_position(lambda t: shake_at_center(t, destination_clip, SHORT_TIME)).set_start(SHORT_TIME).set_duration(LONG_TIME),
        clip.set_position(lambda t: slide_from_center_to_right(t, clip, destination_clip, SHORT_TIME)).set_start(SHORT_TIME + LONG_TIME).set_duration(SHORT_TIME)
    ]


"""

            METHODS TO BUILD EFFECTS BELOW
        These methods will be used by other ones
        here in the top section, but won't be
        expose.

"""

def slide_from_right_to_center(t, clip, destination_clip, transition_time):
    """
    Makes the clip appear from the right side and be placed in the
    center of the 'destination_clip in just 'transition_time' seconds.
    Then, it stays there the rest of the clip duration.
    """
    initial_x = destination_clip.w
    initial_y = get_center_y(clip, destination_clip)
    
    return move_from_to_center(t, initial_x, initial_y, clip, destination_clip, transition_time)

def slide_from_center_to_right(t, clip, destination_clip, transition_time):
    """
    Makes the clip dissapear on the right from the center of the
    'destination_clip' in just 'transition_time' seconds. Then,
    it stays outside of the screen the rest of the clip duration.
    """
    final_x = destination_clip.w
    final_y = get_center_y(clip, destination_clip)

    return move_from_center_to(t, final_x, final_y, clip, destination_clip, transition_time)

def slide_from_left_to_center(t, clip, destination_clip, transition_time):
    """
    Makes the clip appear from the left side and be placed in the
    center of the 'destination_clip in just 'transition_time' seconds.
    Then, it stays there the rest of the clip duration.
    """
    initial_x = -clip.w
    initial_y = get_center_y(clip, destination_clip)
    
    return move_from_to_center(t, initial_x, initial_y, clip, destination_clip, transition_time)

def slide_from_center_to_left(t, clip, destination_clip, transition_time):
    """
    Makes the clip dissapear on the left from the center of the
    'destination_clip' in just 'transition_time' seconds. Then,
    it stays outside of the screen the rest of the clip duration.
    """
    final_x = -destination_clip.w
    final_y = get_center_y(clip, destination_clip)

    return move_from_center_to(t, final_x, final_y, clip, destination_clip, transition_time)

def slide_from_top_to_center(t, clip, destination_clip, transition_time):
    """
    Makes the clip appear from the top side and be placed in the
    center of the 'destination_clip in just 'transition_time' seconds.
    Then, it stays there the rest of the clip duration.
    """
    initial_x = get_center_x(clip, destination_clip)
    initial_y = -clip.h

    return move_from_to_center(t, initial_x, initial_y, clip, destination_clip, transition_time)

def slide_from_center_to_top(t, clip, destination_clip, transition_time):
    """
    Makes the clip dissapear on the top from the center of the
    'destination_clip' in just 'transition_time' seconds. Then,
    it stays outside of the screen the rest of the clip duration.
    """
    final_x = get_center_x(clip, destination_clip)
    final_y = -clip.h

    return move_from_center_to(t, final_x, final_y, clip, destination_clip, transition_time)

def slide_from_bottom_to_center(t, clip, destination_clip, transition_time):
    """
    Makes the clip appear from the bottom side and be placed in the
    center of the 'destination_clip in just 'transition_time' seconds.
    Then, it stays there the rest of the clip duration.
    """
    initial_x = get_center_x(clip, destination_clip)
    initial_y = destination_clip.h
    
    return move_from_to_center(t, initial_x, initial_y, clip, destination_clip, transition_time)

def slide_from_center_to_bottom(t, clip, destination_clip, transition_time):
    """
    Makes the clip dissapear on the bottom from the center of the
    'destination_clip' in just 'transition_time' seconds. Then,
    it stays outside of the screen the rest of the clip duration.
    """
    final_x = get_center_x(clip, destination_clip)
    final_y = destination_clip.h

    return move_from_center_to(t, final_x, final_y, clip, destination_clip, transition_time)

def slide_from_bottom_left_to_center(t, clip, destination_clip, transition_time):
    """
    Makes the clip appear from the bottom left side and be placed in the
    center of the 'destination_clip in just 'transition_time' seconds.
    Then, it stays there the rest of the clip duration.
    """
    initial_x = -clip.w
    initial_y = destination_clip.h

    return move_from_to_center(t, initial_x, initial_y, clip, destination_clip, transition_time)

def slide_from_center_to_bottom_left(t, clip, destination_clip, transition_time):
    """
    Makes the clip dissapear on the bottom left from the center 
    of the 'destination_clip' in just 'transition_time' seconds. 
    Then, it stays outside of the screen the rest of the clip duration.
    """
    final_x = -clip.w
    final_y = destination_clip.h

    return move_from_center_to(t, final_x, final_y, clip, destination_clip, transition_time)

def slide_from_bottom_right_to_center(t, clip, destination_clip, transition_time):
    """
    Makes the clip appear from the bottom right side and be placed in the
    center of the 'destination_clip in just 'transition_time' seconds.
    Then, it stays there the rest of the clip duration.
    """
    initial_x = destination_clip.w
    initial_y = destination_clip.h

    return move_from_to_center(t, initial_x, initial_y, clip, destination_clip, transition_time)

def slide_from_center_to_bottom_right(t, clip, destination_clip, transition_time):
    """
    Makes the clip dissapear on the bottom right from the center
    of the 'destination_clip' in just 'transition_time' seconds.
    Then, it stays outside of the screen the rest of the clip 
    duration.
    """
    final_x = destination_clip.w
    final_y = destination_clip.h

    return move_from_center_to(t, final_x, final_y, clip, destination_clip, transition_time)

def slide_from_top_right_to_center(t, clip, destination_clip, transition_time):
    """
    Makes the clip appear from the top right side and be placed in the
    center of the 'destination_clip in just 'transition_time' seconds.
    Then, it stays there the rest of the clip duration.
    """
    initial_x = destination_clip.w
    initial_y = -clip.h

    return move_from_to_center(t, initial_x, initial_y, clip, destination_clip, transition_time)

def slide_from_center_to_top_right(t, clip, destination_clip, transition_time):
    """
    Makes the clip dissapear on the top right from the center
    of the 'destination_clip' in just 'transition_time' seconds.
    Then, it stays outside of the screen the rest of the clip 
    duration.
    """
    final_x = destination_clip.w
    final_y = -clip.h

    return move_from_center_to(t, final_x, final_y, clip, destination_clip, transition_time)

def slide_from_top_left_to_center(t, clip, destination_clip, transition_time):
    """
    Makes the clip appear from the top left side and be placed in the
    center of the 'destination_clip in just 'transition_time' seconds.
    Then, it stays there the rest of the clip duration.
    """
    initial_x = -clip.w
    initial_y = -clip.h

    return move_from_to_center(t, initial_x, initial_y, clip, destination_clip, transition_time)

def slide_from_center_to_top_left(t, clip, destination_clip, transition_time):
    """
    Makes the clip dissapear on the top left from the center
    of the 'destination_clip' in just 'transition_time' seconds.
    Then, it stays outside of the screen the rest of the clip 
    duration.
    """
    final_x = -clip.w
    final_y = -clip.h

    return move_from_center_to(t, final_x, final_y, clip, destination_clip, transition_time)

def slide_from_top_right_to_center(t, clip, destination_clip, transition_time):
    """
    Makes the clip appear from the top right side and be placed in the
    center of the 'destination_clip in just 'transition_time' seconds.
    Then, it stays there the rest of the clip duration.
    """
    initial_x = destination_clip.w
    initial_y = -clip.h

    return move_from_to_center(t, initial_x, initial_y, clip, destination_clip, transition_time)

def slide_from_center_to_top_right(t, clip, destination_clip, transition_time):
    """
    Makes the clip dissapear on the top right from the center
    of the 'destination_clip' in just 'transition_time' seconds.
    Then, it stays outside of the screen the rest of the clip 
    duration.
    """
    final_x = destination_clip.w
    final_y = -clip.h

    return move_from_center_to(t, final_x, final_y, clip, destination_clip, transition_time)



def slide_out_through_left(t, initial_x, initial_y, clip, destination_clip, transition_time):
    """
    Moves the clip from the initial position (initial_x, initial_y) to out 
    of the screen by the left. This will move the clip  out in just
    'transition_time' seconds.

    It is interesting to use this position effect with a '.subclip' to avoid
    having this clip out of the screen but loaded in memory.
    """
    distance_to_exit = initial_x + clip.w
    transition_moment_movement = 1
    if t < transition_time:
        # Only at this moment the object is still shown in the video
        transition_moment_movement = (t / transition_time)

    return  initial_x - transition_moment_movement * distance_to_exit, initial_y

def slide_out_through_right(t, initial_x, initial_y, clip, destination_clip, transition_time):
    """
    Moves the clip from the initial position (initial_x, initial_y) to out 
    of the screen by the right. This will move the clip  out in just
    'transition_time' seconds.

    It is interesting to use this position effect with a '.subclip' to avoid
    having this clip out of the screen but loaded in memory.
    """
    distance_to_exit = destination_clip.w - initial_x
    transition_moment_movement = 1
    if t < transition_time:
        # Only at this moment the object is still shown in the video
        transition_moment_movement = (t / transition_time)

    return  initial_x + transition_moment_movement * distance_to_exit, initial_y

def slide_out_through_top(t, initial_x, initial_y, clip, destination_clip, transition_time):
    """
    Moves the clip from the initial position (initial_x, initial_y) to out 
    of the screen by the top. This will move the clip  out in just
    'transition_time' seconds.

    It is interesting to use this position effect with a '.subclip' to avoid
    having this clip out of the screen but loaded in memory.
    """
    distance_to_exit = initial_y + clip.h
    transition_moment_movement = 1
    if t < transition_time:
        # Only at this moment the object is still shown in the video
        transition_moment_movement = (t / transition_time)

    return  initial_x - transition_moment_movement * distance_to_exit, initial_y

def slide_out_through_bottom(t, initial_x, initial_y, clip, destination_clip, transition_time):
    """
    Moves the clip from the initial position (initial_x, initial_y) to out 
    of the screen by the bottom. This will move the clip  out in just
    'transition_time' seconds.

    It is interesting to use this position effect with a '.subclip' to avoid
    having this clip out of the screen but loaded in memory.
    """
    distance_to_exit = destination_clip.h - initial_y
    transition_moment_movement = 1
    if t < transition_time:
        # Only at this moment the object is still shown in the video
        transition_moment_movement = (t / transition_time)

    return  initial_x + transition_moment_movement * distance_to_exit, initial_y