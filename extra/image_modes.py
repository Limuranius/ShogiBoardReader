from enum import Enum
import numpy as np
import cv2

from extra import utils


class ImageMode(Enum):
    ORIGINAL = "ORIGINAL"
    GRAYSCALE = "GRAYSCALE"
    CANNY = "CANNY"
    GRAYSCALE_BLACK_THRESHOLD = "GRAYSCALE_BLACK_THRESHOLD"
    LAB_THRESHOLD = "LAB_THRESHOLD"
    ADAPTIVE_THRESHOLD = "ADAPTIVE_THRESHOLD"

    def convert_image(self, image: np.ndarray) -> np.ndarray:
        match self:
            case ImageMode.ORIGINAL:
                return image
            case ImageMode.GRAYSCALE:
                return cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            case ImageMode.CANNY:
                gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
                return cv2.Canny(gray, 250, 255)
            case ImageMode.GRAYSCALE_BLACK_THRESHOLD:
                return utils.get_black_mask(image)
            case ImageMode.LAB_THRESHOLD:
                img_lab = cv2.cvtColor(image, cv2.COLOR_BGR2LAB)
                mask = img_lab[:, :, 0] < 100
                return mask.astype(np.uint8) * 255
            case ImageMode.ADAPTIVE_THRESHOLD:
                gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
                return cv2.adaptiveThreshold(
                    gray,
                    maxValue=255,
                    adaptiveMethod=cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                    thresholdType=cv2.THRESH_BINARY_INV,
                    blockSize=7,
                    C=10
                )
