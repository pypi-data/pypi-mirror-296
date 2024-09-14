from yta_multimedia.video.edition.effect.moviepy.testing.utils import move_from_center_to, move_from_to, move_from_to_center, get_center_x, get_center_y
from yta_multimedia.video.edition.effect.moviepy.testing.others import shake_at_center
from yta_multimedia.video.edition.effect.moviepy.position_effects.enums import ScreenEdge

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
        shake_at_center(clip, destination_clip, SHORT_TIME)[0].set_start(SHORT_TIME).set_duration(LONG_TIME),
        #clip.set_position(lambda t: shake_at_center(t, destination_clip, SHORT_TIME)).set_start(SHORT_TIME).set_duration(LONG_TIME),
        clip.set_position(lambda t: slide_from_center_to_right(t, clip, destination_clip, SHORT_TIME)).set_start(SHORT_TIME + LONG_TIME).set_duration(SHORT_TIME)
    ]



def slide_in_and_slide_out(video, background_video, time: float, in_screen_edge: ScreenEdge = ScreenEdge.LEFT, out_screen_edge: ScreenEdge = ScreenEdge.RIGHT):
    # TODO: Implement 'video' checkings
    # TODO: Implement 'background_video' checkings
    # TODO: Check 'time' is valid
    # TODO: Check 'in_screen_edge' is valid
    # TODO: Check 'out_screen_edge' is valid

    MOVEMENT_TIME = (time / 6)
    STAY_TIME = (time / 6) * 4

    stay_video = video.set_position(get_center_x(video, background_video), get_center_y(video, background_video)).set_start(MOVEMENT_TIME).set_duration(STAY_TIME)

    in_video = None
    if in_screen_edge == ScreenEdge.TOP:
        in_video = video.set_position(lambda t: slide_from_top_to_center(t, video, background_video, MOVEMENT_TIME)).set_start(0).set_duration(MOVEMENT_TIME)
    elif in_screen_edge == ScreenEdge.TOP_RIGHT:
        in_video = video.set_position(lambda t: slide_from_top_right_to_center(t, video, background_video, MOVEMENT_TIME)).set_start(0).set_duration(MOVEMENT_TIME)
    elif in_screen_edge == ScreenEdge.RIGHT:
        in_video = video.set_position(lambda t: slide_from_right_to_center(t, video, background_video, MOVEMENT_TIME)).set_start(0).set_duration(MOVEMENT_TIME)
    elif in_screen_edge == ScreenEdge.BOTTOM_RIGHT:
        in_video = video.set_position(lambda t: slide_from_bottom_right_to_center(t, video, background_video, MOVEMENT_TIME)).set_start(0).set_duration(MOVEMENT_TIME)
    elif in_screen_edge == ScreenEdge.BOTTOM:
        in_video = video.set_position(lambda t: slide_from_bottom_to_center(t, video, background_video, MOVEMENT_TIME)).set_start(0).set_duration(MOVEMENT_TIME)
    elif in_screen_edge == ScreenEdge.BOTTOM_LEFT:
        in_video = video.set_position(lambda t: slide_from_bottom_left_to_center(t, video, background_video, MOVEMENT_TIME)).set_start(0).set_duration(MOVEMENT_TIME)
    elif in_screen_edge == ScreenEdge.LEFT:
        in_video = video.set_position(lambda t: slide_from_left_to_center(t, video, background_video, MOVEMENT_TIME)).set_start(0).set_duration(MOVEMENT_TIME)
    elif in_screen_edge == ScreenEdge.TOP_LEFT:
        in_video = video.set_position(lambda t: slide_from_top_left_to_center(t, video, background_video, MOVEMENT_TIME)).set_start(0).set_duration(MOVEMENT_TIME)

    out_video = None
    if out_screen_edge == ScreenEdge.TOP:
        out_video = video.set_position(lambda t: slide_from_center_to_top(t, video, background_video, MOVEMENT_TIME)).set_start(MOVEMENT_TIME + STAY_TIME).set_duration(MOVEMENT_TIME)
    elif out_screen_edge == ScreenEdge.TOP_RIGHT:
        out_video = video.set_position(lambda t: slide_from_center_to_top_right(t, video, background_video, MOVEMENT_TIME)).set_start(MOVEMENT_TIME + STAY_TIME).set_duration(MOVEMENT_TIME)
    elif out_screen_edge == ScreenEdge.RIGHT:
        out_video = video.set_position(lambda t: slide_from_center_to_right(t, video, background_video, MOVEMENT_TIME)).set_start(MOVEMENT_TIME + STAY_TIME).set_duration(MOVEMENT_TIME)
    elif out_screen_edge == ScreenEdge.BOTTOM_RIGHT:
        out_video = video.set_position(lambda t: slide_from_center_to_bottom_right(t, video, background_video, MOVEMENT_TIME)).set_start(MOVEMENT_TIME + STAY_TIME).set_duration(MOVEMENT_TIME)
    elif out_screen_edge == ScreenEdge.BOTTOM:
        out_video = video.set_position(lambda t: slide_from_center_to_bottom(t, video, background_video, MOVEMENT_TIME)).set_start(MOVEMENT_TIME + STAY_TIME).set_duration(MOVEMENT_TIME)
    elif out_screen_edge == ScreenEdge.BOTTOM_LEFT:
        out_video = video.set_position(lambda t: slide_from_center_to_bottom_left(t, video, background_video, MOVEMENT_TIME)).set_start(MOVEMENT_TIME + STAY_TIME).set_duration(MOVEMENT_TIME)
    elif out_screen_edge == ScreenEdge.LEFT:
        out_video = video.set_position(lambda t: slide_from_center_to_left(t, video, background_video, MOVEMENT_TIME)).set_start(MOVEMENT_TIME + STAY_TIME).set_duration(MOVEMENT_TIME)
    elif out_screen_edge == ScreenEdge.TOP_LEFT:
        out_video = video.set_position(lambda t: slide_from_center_to_top_left(t, video, background_video, MOVEMENT_TIME)).set_start(MOVEMENT_TIME + STAY_TIME).set_duration(MOVEMENT_TIME)

    return [
        in_video,
        stay_video,
        out_video
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

    This method returns x, y.
    """
    distance_to_exit = initial_x + clip.w
    transition_moment_movement = 1
    if t < transition_time:
        # Only at this moment the object is still shown in the video
        transition_moment_movement = (t / transition_time)

    return initial_x - transition_moment_movement * distance_to_exit, initial_y

def slide_out_through_right(t, initial_x, initial_y, clip, destination_clip, transition_time):
    """
    Moves the clip from the initial position (initial_x, initial_y) to out 
    of the screen by the right. This will move the clip  out in just
    'transition_time' seconds.

    It is interesting to use this position effect with a '.subclip' to avoid
    having this clip out of the screen but loaded in memory.

    This method returns x, y.
    """
    distance_to_exit = destination_clip.w - initial_x
    transition_moment_movement = 1
    if t < transition_time:
        # Only at this moment the object is still shown in the video
        transition_moment_movement = (t / transition_time)

    return initial_x + transition_moment_movement * distance_to_exit, initial_y

def slide_out_through_top(t, initial_x, initial_y, clip, destination_clip, transition_time):
    """
    Moves the clip from the initial position (initial_x, initial_y) to out 
    of the screen by the top. This will move the clip  out in just
    'transition_time' seconds.

    It is interesting to use this position effect with a '.subclip' to avoid
    having this clip out of the screen but loaded in memory.

    This method returns x, y.
    """
    distance_to_exit = initial_y + clip.h
    transition_moment_movement = 1
    if t < transition_time:
        # Only at this moment the object is still shown in the video
        transition_moment_movement = (t / transition_time)

    return initial_x - transition_moment_movement * distance_to_exit, initial_y

def slide_out_through_bottom(t, initial_x, initial_y, clip, destination_clip, transition_time):
    """
    Moves the clip from the initial position (initial_x, initial_y) to out 
    of the screen by the bottom. This will move the clip  out in just
    'transition_time' seconds.

    It is interesting to use this position effect with a '.subclip' to avoid
    having this clip out of the screen but loaded in memory.

    This method returns x, y.
    """
    distance_to_exit = destination_clip.h - initial_y
    transition_moment_movement = 1
    if t < transition_time:
        # Only at this moment the object is still shown in the video
        transition_moment_movement = (t / transition_time)

    return initial_x + transition_moment_movement * distance_to_exit, initial_y