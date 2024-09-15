from random import randint

import numpy as np
import math

"""

            METHODS FOR EXTERNAL BELOW
        These methods will be used in
        PositionEffect enum.

"""

def shake_at(clip, x, y, time):
    return [
        clip.set_position(lambda t: __shake(t, x, y)).set_start(0).set_duration(time)
    ]

def shake_increasing_at(clip, x, y, time):
    return [
        clip.set_position(lambda t: __shake_increasing(t, x, y, time)).set_start(0).set_duration(time)
    ]

def shake_decreasing_at(clip, x, y, time):
    return [
        clip.set_position(lambda t: __shake_decreasing(t, x, y, time)).set_start(0).set_duration(time)
    ]
    
def shake_at_center(clip, background_clip, time):
    x =  background_clip.w / 2 - clip.w / 2
    y = background_clip.h / 2 - clip.h / 2

    return shake_at(clip, x, y, time)

def shake_increasing_at_center(clip, background_clip, time):
    x =  background_clip.w / 2 - clip.w / 2
    y = background_clip.h / 2 - clip.h / 2

    return shake_increasing_at(clip, x, y, time)

def shake_decreasing_at_center(clip, background_clip, time):
    x =  background_clip.w / 2 - clip.w / 2
    y = background_clip.h / 2 - clip.h / 2

    return shake_decreasing_at(clip, x, y, time)


"""

            METHODS FOR INTERNAL USE
        These methods below will be used
        by the other ones above but won't
        be exposed.

        These ones are the real effects,
        the logic that is applied in each
        frame to get what we need.

"""

def __in_circles(t, x, y, radius = 200):
    """
    Places the clip in (x, y) position and moves it in circles doing
    a complete spin in 2 seconds.

    The 'radius' parameter is the distance between the origin and the
    path the clip will follow.
    """
    cicle_time = 2

    return x + radius * np.cos((t / cicle_time) * 2 * math.pi), y + radius * np.sin((t / cicle_time) * 2 * math.pi)

def __shake(t, x, y):
    """
    Places the clip in (x, y) position and shakes it the whole time with
    the same shaking factor.
    """
    pos = [x, y]
    speed = t * 4
    d = randint(0, 4)

    if 0 == d: #top
        return (pos[0], pos[1] + speed)
    elif 1 == d: #left
        return (pos[0] - speed, pos[1])
    elif 2 == d: #bot
        return (pos[0], pos[1] - speed)
    else: #right
        return (pos[0] + speed, pos[1])
    
def __shake_increasing(t, x, y, duration):
    """
    Places the clip in (x, y) position and shakes it in an increasing way.
    This means, the clip will start without any shake, but the shake will
    increase slowly.
    """
    MAX_SHAKE_SPEED = 20
    pos = [x, y]
    # Speed will increase progressively from 0 to MAX_SHAKE_SPEED
    # and this process will last the whole clip duration
    speed = (t / duration) * MAX_SHAKE_SPEED
    d = randint(0, 4)

    if 0 == d: #top
        return (pos[0], pos[1] + speed)
    elif 1 == d: #left
        return (pos[0] - speed, pos[1])
    elif 2 == d: #bot
        return (pos[0], pos[1] - speed)
    else: #right
        return (pos[0] + speed, pos[1])
    
def __shake_decreasing(t, x, y, duration):
    """
    Places the clip in (x, y) position and shakes it in an increasing way.
    This means, the clip will start shaking so hard, but the shake will
    decrease slowly.
    """
    MAX_SHAKE_SPEED = 20
    pos = [x, y]
    # Speed will increase progressively from 0 to MAX_SHAKE_SPEED
    # and this process will last the whole clip duration
    speed = MAX_SHAKE_SPEED - ((t / duration) * MAX_SHAKE_SPEED)
    d = randint(0, 4)

    if 0 == d: #top
        return (pos[0], pos[1] + speed)
    elif 1 == d: #left
        return (pos[0] - speed, pos[1])
    elif 2 == d: #bot
        return (pos[0], pos[1] - speed)
    else: #right
        return (pos[0] + speed, pos[1])
    