from .CornerDetector import *
import numpy as np

class HardcodedCornerDetector(CornerDetector):
    corners: Corners

    def __init__(self, corners: Corners = None):
        if corners is None:
            self.corners = ((0, 0), (0, 0), (0, 0), (0, 0))
        else:
            self.corners = corners

    def get_corners(self, image: np.ndarray) -> Corners:
        return self.corners

    def set_corners(self, corners: Corners):
        self.corners = corners
