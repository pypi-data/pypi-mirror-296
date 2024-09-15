from yta_multimedia.video.edition.effect.moviepy.position_effects.base_position_moviepy_effect import BasePositionMoviepyEffect
from yta_multimedia.video.edition.effect.moviepy.position_effects.enums import ScreenPosition
from yta_multimedia.video.edition.effect.moviepy.position_effects.utils import move_video_from_a_to_b, position_video_in
from yta_general_utils.file_processor import file_is_video_file
from moviepy.editor import VideoFileClip, CompositeVideoClip, ImageClip, ColorClip, concatenate_videoclips
from typing import Union
from random import randrange


class SlidePositionMoviepyEffect(BasePositionMoviepyEffect):
    """
    Effect of appearing from one edge of the screen and going to
    somewhere in the screen.
    """
    def __get_random_positions(self):
        """
        Gets random 'initial_position' and 'random_position' dict.
        """
        initial_position = ScreenPosition.OUT_LEFT
        final_position = ScreenPosition.OUT_RIGHT
        rnd = randrange(0, 3)
        if rnd == 0:
            initial_position = ScreenPosition.OUT_RIGHT
            final_position = ScreenPosition.OUT_LEFT
        elif rnd == 1:
            initial_position = ScreenPosition.OUT_TOP
            final_position = ScreenPosition.OUT_BOTTOM
        elif rnd == 2:
            initial_position = ScreenPosition.OUT_BOTTOM
            final_position = ScreenPosition.OUT_TOP

        return {
            'initial_position': initial_position,
            'final_position': final_position
        }

    def apply(self):
        """
        Applies the effect to the 'video' provided when initializing this
        effect class, and puts the video over a static black background
        image of 1920x1080.
        """
        background_video = ColorClip((1920, 1080), [0, 0, 0], duration = self.video.duration)

        return self.apply_over_video(background_video)

    def apply_over_video(self, background_video: Union[str, VideoFileClip, CompositeVideoClip, ImageClip, ColorClip]):
        """
        This effect will make the 'self.video' appear from outside
        of the screen (from the 'in_screen_edge'), will stay in
        the middle of the screen for 4/6 times of its duration, and
        will go away through the 'out_screen_edge' edge of the 
        screen. All over the provided 'background_video'.

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

        background_video = super().process_background_video(background_video)

        random_position = self.__get_random_positions()

        movement_time = background_video.duration / 6
        stay_time = background_video.duration / 6 * 4

        effect = concatenate_videoclips([
            move_video_from_a_to_b(self.video, background_video, random_position['initial_position'], ScreenPosition.CENTER, 0, movement_time),
            position_video_in(self.video, background_video, ScreenPosition.CENTER).set_start(movement_time).set_duration(stay_time),
            move_video_from_a_to_b(self.video, background_video, ScreenPosition.CENTER, random_position['final_position'], movement_time + stay_time, movement_time),
        ])

        return CompositeVideoClip([
            background_video,
            effect
        ])