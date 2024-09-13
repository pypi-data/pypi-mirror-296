from yta_multimedia.video.edition.effect.moviepy.moviepy_effect import MoviepyEffect
from yta_multimedia.video.edition.effect.video_effect import VideoEffect
from yta_general_utils.type_checker import variable_is_type
from yta_general_utils.file_processor import file_is_video_file
from moviepy.editor import VideoFileClip, CompositeVideoClip, ImageClip
from typing import Union, Any


# The effects that we are using here are the ones prepared for the
# segment, with information about the time and that stuff
# TODO: Actually, effects will inherit from these classes, but will
# be not these classes, so I don't know if this below works
def apply_effect_to_video(video: Union[str, VideoFileClip, CompositeVideoClip, ImageClip], effect: Union[MoviepyEffect, VideoEffect]):
    # Ok, this is a general method, not our main flow method.
    # We just need to apply the effect in the video, so lets
    # check that the effect is valid, apply on the video if
    # possible, and return the video
    if not video:
        raise Exception('No "video" provided.')
    
    if not effect:
        raise Exception('No "effect" provided.')
    
    # We check if the parent of the effect is one of the 
    # expected ones
    effect_parent_classes = effect.__bases__
    if not MoviepyEffect in effect_parent_classes and not VideoEffect in effect_parent_classes:
        raise Exception('Provided "effect" is not valid.')
    
    if variable_is_type(video, str):
        if not file_is_video_file(video):
            return None
        
        video = VideoFileClip(video)

    return effect(video).apply()