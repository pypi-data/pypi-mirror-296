from yta_multimedia.video.edition.effect.moviepy.position_effects.objects.base_position_moviepy_effect import BasePositionMoviepyEffect
from yta_multimedia.video.edition.effect.moviepy.position_effects.enums import ScreenPosition
from yta_multimedia.video.edition.effect.moviepy.position_effects.utils import move_video_from_a_to_b, position_video_in, get_random_moviepy_position_in_bounds
from yta_multimedia.video.edition.effect.moviepy.position_effects.utils.shake import __shake
from yta_general_utils.file_processor import file_is_video_file
from moviepy.editor import VideoFileClip, CompositeVideoClip, ImageClip, ColorClip
from typing import Union
from random import randrange


class ShakeAtPositionMoviepyEffect(BasePositionMoviepyEffect):
    """
    Effect of shaking the given 'video' when initialized in a specific
    position given (if given as parameter when applying) or randomly
    generated (inside the bounds according to the also provided
    'background_video' dimensions).
    """
    def apply(self, position: Union[ScreenPosition, tuple, None] = None):
        """
        Applies the effect to the 'video' provided when initializing this
        effect class, and puts the video over a static black background
        image of 1920x1080.
        """
        background_video = ColorClip((1920, 1080), [0, 0, 0], duration = self.video.duration)

        return self.apply_over_video(background_video, position)

    def apply_over_video(self, background_video: Union[str, VideoFileClip, CompositeVideoClip, ImageClip, ColorClip], position: Union[ScreenPosition, tuple, None] = None):
        """
        This effect will make the 'self.video' shake in the 
        provided 'position' (or in a random one in the screen).

        Applies the effect on the video used when instantiating the
        effect, but applies the effect by placing it over the 
        'background_video' provided in this method (the 
        'background_video' will act as a background video for the 
        effect applied on the initial video).

        This method will set the video used when instantiating the
        effect as the most important, and its duration will be 
        considered as that. If the 'background_video' provided 
        has a duration lower than the original video, we will
        loop it to reach that duration. If the video is shorter
        than the 'background_video', we will crop the last one
        to fit the original video duration.
        """
        if not background_video:
            raise Exception('No "background_video" provided.')
        
        if isinstance(background_video, str):
            if not file_is_video_file:
                raise Exception('Provided "background_video" is not a valid video file.')
            
            background_video = VideoFileClip(background_video)

        # If no position provided, we create a random one
        if not position:
            position = get_random_moviepy_position_in_bounds(self.video)
        elif not isinstance(position, ScreenPosition):
            if not isinstance(position, tuple) and len(position) != 2:
                raise Exception('Provided "position" is not a valid ScreenPosition enum or a (x, y) tuple.')

        background_video = super().process_background_video(background_video)

        effect = self.video.set_position(lambda t: __shake(t, position[0], position[1])).set_start(0).set_duration(self.video.duration)

        return CompositeVideoClip([
            background_video,
            effect
        ])