from yta_general_utils.file_processor import file_is_video_file
from moviepy.editor import VideoFileClip, CompositeVideoClip, ImageClip, ColorClip, concatenate_videoclips
from typing import Union


def set_video_duration(video: Union[str, VideoFileClip, CompositeVideoClip, ImageClip, ColorClip], duration = float):
    """
    This method will return a copy of the provided 'video' with the desired
    'duration' by applying crops or loops. If the provided 'duration' is
    lower than the actual 'video' duration, it will be shortened. If it is
    greater, it will be looped until we reach the desired 'duration'.

    This method makes a 'video.copy()' internally to work and avoid problems.
    """
    if not video:
        raise Exception('No "video" provided.')

    if isinstance(video, str):
        if not file_is_video_file:
            raise Exception('Provided "video" is not a valid video file.')
        
        video = VideoFileClip(video)

    final_video = video.copy()

    if video.duration > duration:
        final_video = final_video.subclip(0, duration)
    elif video.duration < duration:
        times_to_loop = (int) (duration / video.duration) - 1
        remaining_time = duration % video.duration
        for i in range(times_to_loop):
            final_video = concatenate_videoclips([final_video, video])
        final_video = concatenate_videoclips([final_video, video.subclip(0, remaining_time)])

    return final_video