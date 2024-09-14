from yta_multimedia.video.edition.effect.moviepy.testing.slider import slide_in_shake_and_slide_out
from yta_multimedia.video.edition.effect.moviepy.testing.others import shake_at_center, shake_increasing_at_center, shake_decreasing_at_center, shake_at, shake_increasing_at, shake_decreasing_at
from enum import Enum

class PositionEffect(Enum):    
    SLIDE_IN_SHAKE_AND_SLIDE_OUT = slide_in_shake_and_slide_out
    SHAKE_AT_CENTER = shake_at_center
    SHAKE_INCREASING_AT_CENTER = shake_increasing_at_center
    SHAKE_DECREASING_AT_CENTER = shake_decreasing_at_center
    SHAKE_AT = shake_at
    SHAKE_INCREASING_AT = shake_increasing_at
    SHAKE_DECREASING_AT = shake_decreasing_at