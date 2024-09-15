"""
Maybe move to a 'coordinates.py' or 'position.py'
"""
from yta_multimedia.video.edition.effect.moviepy.position_effects.enums import ScreenPosition
from yta_general_utils.file_processor import file_is_video_file
from moviepy.editor import VideoFileClip, CompositeVideoClip, ImageClip, ColorClip
from random import randrange, choice as randomchoice
from typing import Union


def position_video_in(video: Union[str, VideoFileClip, CompositeVideoClip, ImageClip, ColorClip], background_video: Union[str, VideoFileClip, CompositeVideoClip, ImageClip, ColorClip], position: Union[ScreenPosition, tuple]):
    """
    Returns the 'video' positioned (with '.set_position(...)') to stay in 
    the provided 'position' without movement. It won't set any other
    property more than the duration (you will need to manually add
    '.set_duration()' or '.set_start()' if needed).

    This method will return the video positioned as a single element, so 
    make to wrap it properly in an array if it is part of a complex
    animation. 
    """
    if not video:
        raise Exception('No "video" provided.')
    
    if isinstance(video, str):
        if not file_is_video_file:
            raise Exception('Provided "video" is not a valid video file.')
        
        video = VideoFileClip(video)

    if not background_video:
        raise Exception('No "background_video" provided.')

    if isinstance(background_video, str):
        if not file_is_video_file:
            raise Exception('Provided "background_video" is not a valid video file.')
        
        background_video = VideoFileClip(background_video)

    if not isinstance(position, ScreenPosition):
        if not isinstance(position, tuple) and len(position) != 2:
            raise Exception('Provided "position" is not a valid ScreenPosition enum or (x, y) tuple.')
        
    # Convert ScreenPosition enums to  if necessary
    if isinstance(position, ScreenPosition):
        position = get_moviepy_position(video, background_video, position)
    else:
        position = get_moviepy_position_by_coords(video, background_video, position[0], position[1])

    return video.set_position(position)


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

    elif position == ScreenPosition.RANDOM_INSIDE:
        lower_limit = get_moviepy_position(video, background_video, ScreenPosition.TOP_LEFT)
        upper_limit = get_moviepy_position(video, background_video, ScreenPosition.BOTTOM_RIGHT)
        position_tuple = (randrange(lower_limit[0], upper_limit[0]), randrange(lower_limit[1], upper_limit[1]))
    elif position == ScreenPosition.RANDOM_OUTSIDE:
        # By now I'm choosing one of the 'OUT' available options
        out_options = [ScreenPosition.OUT_BOTTOM, ScreenPosition.OUT_BOTTOM_LEFT, ScreenPosition.OUT_LEFT, ScreenPosition.OUT_TOP_LEFT, ScreenPosition.OUT_TOP, ScreenPosition.OUT_TOP_RIGHT, ScreenPosition.OUT_RIGHT, ScreenPosition.OUT_BOTTOM_RIGHT]
        position_tuple = randomchoice(out_options)

    return position_tuple


"""
        Internal functions below
"""
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