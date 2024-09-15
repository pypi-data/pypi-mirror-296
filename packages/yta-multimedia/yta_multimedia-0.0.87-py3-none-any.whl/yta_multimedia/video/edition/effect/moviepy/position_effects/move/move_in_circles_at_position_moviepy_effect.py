from yta_multimedia.video.edition.effect.moviepy.position_effects.objects.base_position_moviepy_effect import BasePositionMoviepyEffect
from yta_multimedia.video.edition.effect.moviepy.position_effects.enums import ScreenPosition
from yta_multimedia.video.edition.effect.moviepy.position_effects.utils import get_moviepy_position, get_moviepy_position_by_coords
from yta_multimedia.video.edition.effect.moviepy.position_effects.utils.move import circular_movement
from yta_general_utils.file_processor import file_is_video_file
from moviepy.editor import VideoFileClip, CompositeVideoClip, ImageClip, ColorClip
from typing import Union


class MoveInCirclesAtPositionMoviepyEffect(BasePositionMoviepyEffect):
    """
    Effect of moving in circles surrounding the specified position.
    """
    def apply(self, position: Union[ScreenPosition, tuple] = ScreenPosition.RANDOM_INSIDE):
        """
        Applies the effect to the 'video' provided when initializing this
        effect class, and puts the video over a static black background
        image of 1920x1080.
        """
        background_video = ColorClip((1920, 1080), [0, 0, 0], duration = self.video.duration)

        return self.apply_over_video(background_video, position)

    def apply_over_video(self, background_video: Union[str, VideoFileClip, CompositeVideoClip, ImageClip, ColorClip], position: Union[ScreenPosition, tuple] = ScreenPosition.RANDOM_INSIDE):
        """
        TODO: Write better 

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

        if not isinstance(position, ScreenPosition):
            if not isinstance(position, tuple) and len(position) != 2:
                raise Exception('Provided "position" is not a valid ScreenPosition enum or a (x, y) tuple.')

        background_video = super().process_background_video(background_video)

        if isinstance(position, ScreenPosition):
            position = get_moviepy_position(self.video, background_video, position)
        else:
            position = get_moviepy_position_by_coords(self.video, background_video, position[0], position[1])

        effect = self.video.set_position(lambda t: circular_movement(t, position[0], position[1])).set_start(0).set_duration(self.video.duration)

        return CompositeVideoClip([
            background_video,
            effect
        ])