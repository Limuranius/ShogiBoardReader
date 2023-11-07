from .CornerDetector import *
import numpy as np

class HardcodedCornerDetector(CornerDetector):
    corners: Corners

    def __init__(self, corners: Corners = None):
        self.corners = corners

    def get_corners(self, image: np.ndarray) -> Corners:
        return self.corners

    def set_corners(self, corners: Corners):
        self.corners = corners
