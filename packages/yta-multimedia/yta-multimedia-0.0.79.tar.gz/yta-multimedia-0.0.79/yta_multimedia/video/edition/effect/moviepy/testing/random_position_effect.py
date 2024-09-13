from yta_multimedia.video.edition.effect.moviepy.testing.slider import shake_at_center
from moviepy.editor import ColorClip, VideoFileClip, CompositeVideoClip, ImageClip
from typing import Union


class RandomPositionEffect:
    """
    Class created to test position effects and building objects
    to simplify their use in our system.
    """
    def __init__(self):
        pass

    # TODO: Apply the effect within a black background clip of 1920x1080
    def apply(self, video: Union[str, VideoFileClip, CompositeVideoClip, ImageClip]):
        # Background clip
        background_clip = ColorClip((1920, 1080), [0, 0, 0], duration = video.duration)

        # Effect build and to be applied
        effect = shake_at_center(video, background_clip, video.duration)

        # In this example, the provided 'video' will be shaking at the center
        # of a black background clip during the whole video.duration

        return CompositeVideoClip([
            background_clip,
            *effect
        ])


    # TODO: Apply the effect within a black background clip of 1920x1080
    # but making it transparent 'ismask = True' (?)

    # TODO: Apply the effect over another background clip


"""
We will use these effects to include some elements in our videos,
such as an icon that appears from the right, shakes at the center
and disappears from the left, or a video that appears in random
positions, changing, 5 times. Just imagine, but make it posible
and dynamic here.
"""