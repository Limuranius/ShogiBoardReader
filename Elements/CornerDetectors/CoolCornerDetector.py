import cv2
import numpy as np
import itertools
import math
from .CornerDetector import *


class CoolCornerDetector(CornerDetector):
    def get_corners(self, image: Image) -> Corners:
        try:
            corners = detect_corners(image)
            corners = (
                (corners[0, 0], corners[0, 1]),
                (corners[1, 0], corners[1, 1]),
                (corners[2, 0], corners[2, 1]),
                (corners[3, 0], corners[3, 1])
            )
        except Exception as e:
            corners = (
                (0, 0),
                (0, 0),
                (0, 0),
                (0, 0),
            )
        return corners


def detect_corners(raw_img):
    img = fit_size(raw_img, 500, 500)
    rect = convex_poly_fitted(img)
    scale = raw_img.shape[0] / img.shape[0]
    rect = np.int32(normalize_corners(rect) * scale)
    return rect


def fit_size(img, h, w):
    size = img.shape[:2]
    f = min(h / size[0], w / size[1])
    return cv2.resize(img, (int(size[1] * f), int(size[0] * f)), interpolation=cv2.INTER_AREA)


def edge(img):
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    edges = cv2.Canny(gray, 50, 150)
    return edges


def line(img, threshold=80, minLineLength=50, maxLineGap=5):
    edges = edge(img)
    lines = cv2.HoughLinesP(edges, 1, np.pi / 180, threshold, 200, minLineLength, maxLineGap)
    return lines


def contours(img):
    edges = edge(img)
    contours = cv2.findContours(edges, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)[0]
    min_area = img.shape[0] * img.shape[1] * 0.2
    large_contours = [c for c in contours if cv2.contourArea(c) > min_area]
    return large_contours


def convex(img):
    convexes = []
    for cnt in contours(img):
        convex = cv2.convexHull(cnt)
        convexes.append(convex)
    return convexes


def convex_poly(img):
    cnts = convex(img)
    polies = []
    for cnt in cnts:
        arclen = cv2.arcLength(cnt, True)
        poly = cv2.approxPolyDP(cnt, 0.02 * arclen, True)
        polies.append(poly)
    return [poly[:, 0, :] for poly in polies]


def select_corners(polies):
    p_selected = []
    p_scores = []
    for poly in polies:
        choices = np.array(list(itertools.combinations(poly, 4)))
        scores = []
        for c in choices:
            line_lens = [np.linalg.norm(c[(i + 1) % 4] - c[i]) for i in range(4)]
            base = cv2.contourArea(c) ** 0.5
            score = sum([abs(1 - l / base) ** 2 for l in line_lens])
            scores.append(score)
        idx = np.argmin(scores)
        p_selected.append(choices[idx])
        p_scores.append(scores[idx])
    return p_selected[np.argmin(p_scores)]


def convex_poly_fitted(img):
    polies = convex_poly(img)
    poly = select_corners(polies)
    return poly


def normalize_corners(v):
    rads = []
    for i in range(4):
        a = v[(i + 1) % 4] - v[i]
        a = a / np.linalg.norm(a)
        cosv = np.dot(a, np.array([1, 0]))
        rads.append(math.acos(cosv))
    left_top = np.argmin(rads)
    return np.roll(v, 4 - left_top, axis=0)
