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

    def get_inventories_corners(self, image: ImageNP) -> tuple[Corners, Corners]:
        p0, p1, p2, p3 = self.get_corners(image)
        y_min = p0[1]
        y_max = p3[1]
        x_min = p0[0]
        x_max = p1[0]
        w = p1[0] - p0[0]
        cell_w = w // 9
        offset = int(cell_w * 0.65)
        inventory_1_p0 = (x_max + offset, y_min)
        inventory_1_p1 = (x_max + offset + cell_w, y_min)
        inventory_1_p2 = (x_max + offset + cell_w, y_max)
        inventory_1_p3 = (x_max + offset, y_max)

        inventory_2_p0 = (x_min - cell_w, y_min)
        inventory_2_p1 = (x_min, y_min)
        inventory_2_p2 = (x_min, y_max)
        inventory_2_p3 = (x_min - cell_w, y_max)

        return (
            (inventory_1_p0, inventory_1_p1, inventory_1_p2, inventory_1_p3),
            (inventory_2_p0, inventory_2_p1, inventory_2_p2, inventory_2_p3),
        )
