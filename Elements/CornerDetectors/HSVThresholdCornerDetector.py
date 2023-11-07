from .CornerDetector import *
import numpy as np
import cv2
from extra import utils


class HSVThresholdCornerDetector(CornerDetector):
    hsv_low: np.ndarray
    hsv_high: np.ndarray

    def __init__(self, hsv_low: tuple[int, int, int], hsv_high: tuple[int, int, int]):
        self.hsv_low = np.array(hsv_low)
        self.hsv_high = np.array(hsv_high)

    def get_corners(self, image: np.ndarray) -> Corners:
        image_hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
        mask = cv2.inRange(image_hsv, self.hsv_low, self.hsv_high)
        centers = utils.find_clusters_centers(mask, 4)
        centers = utils.order_points(centers)
        centers_tuples = (tuple(centers[0]), tuple(centers[1]), tuple(centers[2]), tuple(centers[3]),)
        return centers_tuples
