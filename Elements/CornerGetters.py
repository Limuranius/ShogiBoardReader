import numpy as np
from abc import ABC, abstractmethod
from extra import utils
import cv2

Corners = tuple[tuple[int, int], tuple[int, int], tuple[int, int], tuple[int, int]]


class CornerDetector(ABC):
    @abstractmethod
    def get_corners(self, image: np.ndarray) -> Corners:
        """Возвращает координаты углов доски в следующем порядке:
        левый-верхний, правый-верхний, правый-нижний, левый-нижний"""
        pass


class HardcodedCornerDetector(CornerDetector):
    corners: Corners

    def __init__(self, corners: Corners = None):
        self.corners = corners

    def get_corners(self, image: np.ndarray) -> Corners:
        return self.corners

    def set_corners(self, corners: Corners):
        self.corners = corners


class HSVThresholdCornerDetector(CornerDetector):
    hsv_low: np.ndarray
    hsv_high: np.ndarray

    def __init__(self, hsv_low: np.ndarray, hsv_high: np.ndarray):
        self.hsv_low = hsv_low
        self.hsv_high = hsv_high

    def get_corners(self, image: np.ndarray) -> Corners:
        image_hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
        mask = cv2.inRange(image_hsv, self.hsv_low, self.hsv_high)
        centers = utils.find_clusters_centers(mask, 4)
        centers = utils.order_points(centers)
        centers_tuples = (tuple(centers[0]), tuple(centers[1]), tuple(centers[2]), tuple(centers[3]), )
        return centers_tuples
