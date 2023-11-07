from enum import Enum


class ImageMode(Enum):
    ORIGINAL = "ORIGINAL"
    CANNY = "CANNY"
    GRAYSCALE = "GRAYSCALE"
    GRAYSCALE_BLACK_THRESHOLD = "GRAYSCALE_BLACK_THRESHOLD"
    LAB_THRESHOLD = "LAB_THRESHOLD"
