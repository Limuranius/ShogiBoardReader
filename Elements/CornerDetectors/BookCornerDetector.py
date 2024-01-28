import os

import cv2
import numpy as np
import itertools
import math
from .CornerDetector import *
from extra.types import Inventory
from config import Paths


class BookCornerDetector(CornerDetector):
    def get_corners(self, image: ImageNP) -> Corners:
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        ret, thresh = cv2.threshold(gray, 200, 255, 0)
        thresh = cv2.bitwise_not(thresh)
        contours, hier = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        areas = [cv2.contourArea(cont) for cont in contours]
        border_contour = contours[np.argmax(areas)]
        epsilon = 0.1 * cv2.arcLength(border_contour, True)
        border_contour = cv2.approxPolyDP(border_contour, epsilon, True)
        x, y, w, h = cv2.boundingRect(border_contour)
        p0 = (x, y)
        p1 = (x + w, y)
        p2 = (x + w, y + h)
        p3 = (x, y + h)
        return p0, p1, p2, p3

