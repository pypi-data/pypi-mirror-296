import numpy as np
import math


def in_circles(t, x, y, radius: int = 200, cicle_time: float = 2):
    """
    Returns the (x, y) position tuple for the moviepy '.set_position()' effect,
    for each 't' provided, that will make the element move in circles with the
    provided 'radius'. The 'radius' parameter is the distance between the origin
    and the path the clip will follow. The 'cicle_time' is the time (in seconds)
    needed for a complete circle to be completed by the movement.
    """
    return x + radius * np.cos((t / cicle_time) * 2 * math.pi), y + radius * np.sin((t / cicle_time) * 2 * math.pi)