from yta_multimedia.video.edition.effect.moviepy.position_effects.objects.base_position_moviepy_effect import BasePositionMoviepyEffect
from yta_multimedia.video.edition.effect.moviepy.position_effects.enums import ScreenPosition
from yta_general_utils.file_processor import file_is_video_file
from moviepy.editor import VideoFileClip, CompositeVideoClip, ImageClip, ColorClip
from typing import Union
from random import randrange


class SlideRandomPositionMoviepyEffect(BasePositionMoviepyEffect):
    """
    Effect of appearing from TOP, BOTTOM, RIGHT or LEFT, staying
    at the center, and dissapearing from the opposite edge. This
    animation will spend 1/6 of the time in the entrance, 4/6 of
    the time staying at the center, and 1/6 of the time in the
    exit.
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

        # TODO: Rework and move to another folder as this is a complex effect
        # effect = [
        #     move_video_from_a_to_b(self.video, background_video, random_position['initial_position'], ScreenPosition.CENTER, 0, movement_time),
        #     position_video_in(self.video, background_video, ScreenPosition.CENTER).set_start(movement_time).set_duration(stay_time),
        #     move_video_from_a_to_b(self.video, background_video, ScreenPosition.CENTER, random_position['final_position'], movement_time + stay_time, movement_time),
        # ]

        return CompositeVideoClip([
            background_video,
            *effect
        ])