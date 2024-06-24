import cv2
import numpy as np
import itertools
import math
from .CornerDetector import *


class MyCornerDetector(CornerDetector):
    def get_corners(self, full_image: ImageNP) -> Corners:
        try:
            image = fit_size(full_image, 500, 500)
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            gray = cv2.GaussianBlur(gray, (3, 3), 0)
            edges = cv2.Canny(gray, 50, 200)
            edges = cv2.dilate(edges, np.ones((3, 3)))
            edges = cv2.erode(edges, np.ones((5, 5)))
            edges = cv2.dilate(edges, np.ones((3, 3)))
            lines = find_lines(edges)
            a1, a2 = get_main_angles(lines)
            lines1 = find_lines_similar_angle(edges, a1)
            lines2 = find_lines_similar_angle(edges, a2)
            inter_points = lines_intersections(lines1, lines2)
            hull = cv2.convexHull(np.array(inter_points))
            epsilon = 0.1 * cv2.arcLength(hull, True)
            approx = cv2.approxPolyDP(hull, epsilon, True)[:, 0]
            scale = full_image.shape[0] / image.shape[0]
            approx = np.int32(np.float64(approx) * scale)
            corners = (
                (approx[0, 0], approx[0, 1]),
                (approx[1, 0], approx[1, 1]),
                (approx[2, 0], approx[2, 1]),
                (approx[3, 0], approx[3, 1])
            )
        except:
            corners = ((0, 0), (0, 0), (0, 0), (0, 0))
        return corners


def fit_size(img, h, w):
    size = img.shape[:2]
    f = min(h / size[0], w / size[1])
    return cv2.resize(img, (int(size[1] * f), int(size[0] * f)), interpolation=cv2.INTER_AREA)


def find_lines(mask_img):
    return cv2.HoughLines(
        mask_img,
        rho=1,
        theta=np.pi / 180,
        threshold=200
    )


def get_main_angles(lines):
    angles = lines[:, 0, 1]
    angles = np.arcsin(np.sin(angles))
    avg = angles.mean()
    a1 = angles[angles < avg].mean()
    a2 = angles[angles > avg].mean()
    return a1, a2


def find_lines_similar_angle(mask_img, angle):
    min_theta = max(0, angle - 0.02)
    max_theta = angle + 0.02

    lines = cv2.HoughLines(
        mask_img,
        1,
        np.pi / 180,
        100,
        min_theta=min_theta,
        max_theta=max_theta
    )
    return lines


def intersection(line1, line2):
    """Finds the intersection of two lines given in Hesse normal form.

    Returns closest integer pixel locations.
    See https://stackoverflow.com/a/383527/5087436
    """
    rho1, theta1 = line1[0]
    rho2, theta2 = line2[0]
    A = np.array([
        [np.cos(theta1), np.sin(theta1)],
        [np.cos(theta2), np.sin(theta2)]
    ])
    b = np.array([[rho1], [rho2]])
    x0, y0 = np.linalg.solve(A, b)
    x0, y0 = int(np.round(x0)), int(np.round(y0))
    return x0, y0


def lines_intersections(lines1, lines2):
    """Finds the intersections between two groups of lines."""
    intersections = []
    for line1 in lines1:
        for line2 in lines2:
            intersections.append(intersection(line1, line2))
    return intersections
