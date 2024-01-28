import cv2
import numpy as np
from abc import ABC, abstractmethod

from extra.types import ImageNP


class ImageGetter(ABC):
    @abstractmethod
    def get_image(self) -> np.ndarray:
        pass


class Photo(ImageGetter):
    img: np.ndarray

    def __init__(self, img_path: str = None):
        self.img = cv2.imread(img_path)

    def get_image(self) -> np.ndarray:
        return self.img

    def set_image(self, img: str | ImageNP):
        if isinstance(img, str):
            self.img = cv2.imread(img)
        else:
            self.img = img


class Camera(ImageGetter):
    video: cv2.VideoCapture

    def __init__(self, cam_id: int = 0):
        self.video = cv2.VideoCapture(cam_id)

    def get_image(self) -> np.ndarray:
        _, frame = self.video.read()
        frame = cv2.rotate(frame, cv2.ROTATE_90_CLOCKWISE)
        return frame


class Video(ImageGetter):
    video: cv2.VideoCapture

    def __init__(self, video_path: str):
        self.video = cv2.VideoCapture(video_path)

    def get_image(self) -> np.ndarray:
        _, frame = self.video.read()
        return frame
