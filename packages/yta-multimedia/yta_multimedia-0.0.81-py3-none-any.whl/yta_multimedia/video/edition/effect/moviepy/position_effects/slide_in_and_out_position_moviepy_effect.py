from yta_multimedia.video.edition.effect.moviepy.position_effects.base_position_moviepy_effect import BasePositionMoviepyEffect
from yta_multimedia.video.edition.effect.moviepy.testing.slider import slide_in_shake_and_slide_out
from moviepy.editor import VideoFileClip, CompositeVideoClip, ImageClip, ColorClip
from typing import Union


class SlideInAndOutPositionMoviepyEffect(BasePositionMoviepyEffect):
    def apply_over_video(self, background_video: Union[str, VideoFileClip, CompositeVideoClip, ImageClip, ColorClip]):
        """
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
        background_video = super().__process_background_video(background_video)
        
        # TODO: Remove the shake, please
        effect = slide_in_shake_and_slide_out(self.video, background_video, background_video.duration)

        # In this example, the provided 'video' will be shaking at the center
        # of a black background clip during the whole video.duration

        return CompositeVideoClip([
            background_video,
            *effect
        ])