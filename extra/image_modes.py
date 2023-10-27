from enum import Enum


class ImageMode(Enum):
    ORIGINAL = "original"
    CANNY = "canny"
    GRAYSCALE = "grayscale"
    GRAYSCALE_BLACK_THRESHOLD = "grayscale_black_threshold"
    LAB_THRESHOLD = "lab_threshold"
