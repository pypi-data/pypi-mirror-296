from yta_multimedia.video.edition.effect.moviepy.position_effects.base_position_moviepy_effect import BasePositionMoviepyEffect
from yta_multimedia.video.edition.effect.moviepy.position_effects.enums import ScreenEdge, ScreenPosition
from yta_multimedia.video.edition.effect.moviepy.position_effects.utils import get_video_move_from_pos_to_pos
from moviepy.editor import VideoFileClip, CompositeVideoClip, ImageClip, ColorClip
from typing import Union


class SlideInPositionMoviepyEffect(BasePositionMoviepyEffect):
    """
    Effect of appearing from one edge of the screen and going to
    somewhere in the screen.
    """
    def apply(self, initial_position: ScreenPosition = ScreenPosition.OUT_LEFT, final_position: ScreenPosition = ScreenPosition.CENTER):
        """
        Applies the effect to the 'video' provided when initializing this
        effect class, and puts the video over a static black background
        image of 1920x1080.
        """
        background_video = ColorClip((1920, 1080), [0, 0, 0], duration = self.video.duration)

        return self.apply_over_video(background_video, initial_position, final_position)

    def apply_over_video(self, background_video: Union[str, VideoFileClip, CompositeVideoClip, ImageClip, ColorClip], initial_position: ScreenPosition = ScreenPosition.OUT_LEFT, final_position: ScreenPosition = ScreenPosition.CENTER):
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
        # TODO: Check that 'background_video' is valid
        # TODO: Check that 'initial_position' is valid
        # TODO: Check that 'final_position' is valid

        background_video = super().process_background_video(background_video)

        effect = get_video_move_from_pos_to_pos(self.video, background_video, initial_position, final_position, 0, background_video.duration)

        return CompositeVideoClip([
            background_video,
            effect
        ])