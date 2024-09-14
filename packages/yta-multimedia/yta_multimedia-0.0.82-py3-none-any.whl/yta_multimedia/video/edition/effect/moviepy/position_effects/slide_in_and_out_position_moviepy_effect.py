from yta_multimedia.video.edition.effect.moviepy.position_effects.base_position_moviepy_effect import BasePositionMoviepyEffect
from yta_multimedia.video.edition.effect.moviepy.testing.slider import slide_in_and_slide_out
from yta_multimedia.video.edition.effect.moviepy.position_effects.enums import ScreenEdge
from moviepy.editor import VideoFileClip, CompositeVideoClip, ImageClip, ColorClip
from typing import Union


class SlideInAndOutPositionMoviepyEffect(BasePositionMoviepyEffect):
    """
    Effect of appearing from one edge of the screen, going to the
    middle and disappearing from another edge of the screen.
    """
    def apply_over_video(self, background_video: Union[str, VideoFileClip, CompositeVideoClip, ImageClip, ColorClip], in_screen_edge: ScreenEdge = ScreenEdge.LEFT, out_screen_edge: ScreenEdge = ScreenEdge.RIGHT):
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
        # TODO: Check that 'in_screen_edge' is valid
        # TODO: Check that 'out_screen_edge' is valid

        background_video = super().process_background_video(background_video)
        
        effect = slide_in_and_slide_out(self.video, background_video, background_video.duration, in_screen_edge, out_screen_edge)

        return CompositeVideoClip([
            background_video,
            *effect
        ])