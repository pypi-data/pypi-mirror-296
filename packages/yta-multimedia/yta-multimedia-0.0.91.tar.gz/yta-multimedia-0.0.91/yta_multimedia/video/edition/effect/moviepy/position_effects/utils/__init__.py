"""
Maybe move to a 'coordinates.py' or 'position.py'
"""
from yta_multimedia.video.edition.effect.moviepy.position_effects.objects.coordinate_center import CoordinateCenter
from yta_multimedia.video.edition.effect.moviepy.position_effects.objects.coordinate_corner import CoordinateCorner
from yta_multimedia.video.edition.effect.moviepy.position_effects.enums import ScreenPosition
from yta_general_utils.file_processor import file_is_video_file
from moviepy.editor import VideoFileClip, CompositeVideoClip, ImageClip, ColorClip
from typing import Union


def position_video_in(video: Union[str, VideoFileClip, CompositeVideoClip, ImageClip, ColorClip], background_video: Union[str, VideoFileClip, CompositeVideoClip, ImageClip, ColorClip], position: Union[ScreenPosition, CoordinateCenter, CoordinateCorner]):
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
        
    position = get_moviepy_position(video, background_video, position)

    return video.set_position(position)


"""
    Coords related functions below
"""
def get_moviepy_position(video, background_video, position: Union[ScreenPosition, CoordinateCenter, CoordinateCorner]):
    """
    In the process of overlaying and moving the provided 'video' over
    the also provided 'background_video', this method calculates the
    (x, y) tuple position that would be, hypothetically, adapted from
    a 1920x1080 black color background static image. The provided 
    'position' will be transformed into the (x, y) tuple according
    to our own definitions in which the video (that starts in upper left
    corner) needs to be placed to fit the desired 'position'.
    """
    # TODO: Add 'video' and 'background_video' checkings
    if not video:
        raise Exception('No "video" provided.')
    
    if not background_video:
        raise Exception('No "background_video" provided.')
    
    if not position:
        raise Exception('No "position" provided.')
    
    if not isinstance(position, ScreenPosition) and not isinstance(position, CoordinateCenter) and not isinstance(position, CoordinateCorner):
        raise Exception('Provided "position" is not ScreenPosition, CoordinateCenter or CoordinateCorner.')
    
    position_tuple = None

    if isinstance(position, ScreenPosition):
        position_tuple = position.get_moviepy_position(video, background_video)
    elif isinstance(position, CoordinateCenter):
        position_tuple = position.recalculate_for_video(video, background_video)
    elif isinstance(position, CoordinateCorner):
        position_tuple = position.recalculate_for_video(background_video)

    return position_tuple


"""
        Internal functions below
"""
def get_center_x(video, background_video):
    """
    Returns the 'x' coord in which the 'video' will be centered
    according to the 'background_video' in which it will be
    overlayed.
    """
    # TODO: Ensure 'video' and 'background_video' are valid videos
    return background_video.w / 2 - video.w / 2

def get_center_y(video, background_video):
    """
    Returns the 'y' coord in which the 'clip' will be centered
    according to the 'background_video' in which it will be
    overlayed.
    """
    # TODO: Ensure 'video' and 'background_video' are valid videos
    return background_video.h / 2 - video.h / 2


"""
        This below is a remaning that I want to check only
        and then, when everything is clear, remove it.
"""
# """
# I copied all these files from the "software" project in which
# I initially created them, just to preserve and adapt the ones
# we weant to keep in the code.
# """
# from yta_multimedia.video.edition.effect.moviepy.testing.position_effect import PositionEffect
# from moviepy.editor import CompositeVideoClip, ColorClip

# def clip_with_effect(clip, effect: PositionEffect, **kwargs):
#     """
#     This method will create a black background clip and will put
#     as an overlay the provided 'clip' with the also provided
#     'effect' applied on it.

#     This method will use the kwargs['time'] as the effect time if provided,
#     or will use the 'destination_clip' duration if no time provided. This
#     method will also crop the 'time' if provided to, as maximum, the
#     'destination_clip' duration.

#     Pay atenttion to the parameters of the PositionEffect you are trying
#     to use.

#     This method will return a CompositeVideoClip that includes the 
#     'destination_clip' and the effect applied over it.
#     """
#     background_clip = ColorClip(clip.size, [0, 0, 0], duration = clip.duration)

#     return __add_clip_with_effect(clip, effect = effect, destination_clip = background_clip, **kwargs)

# def add_clip_with_effect(clip, effect: PositionEffect, destination_clip, **kwargs):
#     """
#     Adds the provided 'clip' with the also provided 'effect' over the
#     'destination_clip'. The provided 'clip' is the clip that will be used 
#     in the effect. For example, an ImageClip that contains an emoji that 
#     is going to be slided in and out.

#     This method will use the kwargs['time'] as the effect time if provided,
#     or will use the 'destination_clip' duration if no time provided. This
#     method will also crop the 'time' if provided to, as maximum, the
#     'destination_clip' duration.

#     Pay atenttion to the parameters of the PositionEffect you are trying
#     to use.

#     This method will return a CompositeVideoClip that includes the 
#     'destination_clip' and the effect applied over it.
#     """
#     return __add_clip_with_effect(clip, effect = effect, destination_clip = destination_clip, **kwargs)

# def __add_clip_with_effect(clip, effect: PositionEffect, destination_clip, **kwargs):
#     """
#     This method is to avoid duplicating the code. Only for internal use.
#     """
#     if not 'time' in kwargs:
#         kwargs['time'] = destination_clip.duration

#     if kwargs.get('time') > destination_clip.duration:
#         kwargs['time'] = destination_clip.duration

#     if kwargs.get('time') < clip.duration:
#         return CompositeVideoClip([
#             destination_clip,
#             *effect(clip.subclip(0, kwargs['time']), **kwargs),
#             clip.subclip(kwargs['time'], clip.duration).set_start(kwargs['time'])
#         ])

#     return CompositeVideoClip([
#         destination_clip,
#         *effect(clip, **kwargs)
#     ])