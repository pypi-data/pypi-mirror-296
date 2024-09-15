import numpy as np
import math


def circular_movement(t, x, y, radius: int = 200, cicle_time: float = 2):
    """
    Returns the (x, y) position tuple for the moviepy '.set_position()' effect,
    for each 't' provided, that will make the element move in circles with the
    provided 'radius'. The 'radius' parameter is the distance between the origin
    and the path the clip will follow. The 'cicle_time' is the time (in seconds)
    needed for a complete circle to be completed by the movement.
    """
    return x + radius * np.cos((t / cicle_time) * 2 * math.pi), y + radius * np.sin((t / cicle_time) * 2 * math.pi)

def sinusoidal_movement(t, start_pos, end_pos, duration):
    """
    Define a non-linear movement, in this case a sinusoidal function.
    :param t: Current time
    :param start_pos: Starting position (x, y)
    :param end_pos: Ending position (x, y)
    :param duration: Total duration of the animation
    :return: New position (x, y)
    """
    progress = t / duration
    amplitude = 100  # amplitude of the sine wave
    frequency = 2  # frequency of the sine wave
    x = start_pos[0] + (end_pos[0] - start_pos[0]) * progress
    y = start_pos[1] + (end_pos[1] - start_pos[1]) * progress + amplitude * np.sin(2 * np.pi * frequency * progress)
    return (x, y)

def parabolic_movement(t, start_pos, end_pos, duration):
    """
    Define a parabolic movement.
    :param t: Current time
    :param start_pos: Starting position (x, y)
    :param end_pos: Ending position (x, y)
    :param duration: Total duration of the animation
    :return: New position (x, y)
    """
    progress = t / duration
    # Define the parabolic path parameters
    x = start_pos[0] + (end_pos[0] - start_pos[0]) * progress
    y_start = start_pos[1]
    y_end = end_pos[1]
    # Parabolic curve: y = a * (x - h)^2 + k
    # where (h, k) is the vertex of the parabola
    a = -4  # Controls the curvature
    h = (start_pos[0] + end_pos[0]) / 2
    k = (y_start + y_end) / 2
    y = a * (x - h) ** 2 + k
    return (x, y)