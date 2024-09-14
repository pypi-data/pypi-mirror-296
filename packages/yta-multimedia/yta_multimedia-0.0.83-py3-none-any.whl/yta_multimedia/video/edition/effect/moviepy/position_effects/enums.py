from enum import Enum


class ScreenEdge(Enum):
    BOTTOM_LEFT = 'bottom_left'
    LEFT = 'left'
    TOP_LEFT = 'top_left'
    TOP = 'top'
    TOP_RIGHT = 'top_right'
    RIGHT = 'right'
    BOTTOM_RIGHT = 'bottom_right'
    BOTTOM = 'bottom'

class ScreenPosition(Enum):
    OUT_TOP_LEFT = 'out_top_left'
    """
    Out of the screen, on the top left corner, just one pixel
    out of bounds.
    """
    IN_EDGE_TOP_LEFT = 'in_edge_top_left'
    """
    The center of the video is on the top left corner, so only
    the bottom left quarter part of the video is shown (inside
    the screen).
    """
    TOP_LEFT = 'top_left'
    """
    The video is completely visible, just at the top left 
    corner of the screen.
    """
    OUT_TOP = 'out_top'
    IN_EDGE_TOP = 'in_edge_top'
    TOP = 'top'
    OUT_TOP_RIGHT = 'out_top_right'
    IN_EDGE_TOP_RIGHT = 'in_edge_top_right'
    TOP_RIGHT = 'top_right'
    CENTER = 'center'
    OUT_RIGHT = 'out_right'
    IN_EDGE_RIGHT = 'in_edge_right'
    RIGHT = 'right'
    OUT_BOTTOM_RIGHT = 'out_bottom_right'
    IN_EDGE_BOTTOM_RIGHT = 'in_edge_bottom_right'
    BOTTOM_RIGHT = 'bottom_right'
    OUT_BOTTOM = 'out_bottom'
    IN_EDGE_BOTTOM = 'in_edge_bottom'
    BOTTOM = 'bottom'
    OUT_BOTTOM_LEFT = 'out_bottom_left'
    IN_EDGE_BOTTOM_LEFT = 'in_edge_bottom_left'
    BOTTOM_LEFT = 'bottom_left'
    OUT_LEFT = 'out_left'
    IN_EDGE_LEFT = 'in_edge_left'
    LEFT = 'left'