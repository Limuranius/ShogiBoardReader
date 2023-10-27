import cv2
import numpy as np
from abc import ABC, abstractmethod


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

    def set_image(self, img_path: str):
        self.img = cv2.imread(img_path)


class Camera(ImageGetter):
    video: cv2.VideoCapture

    def __init__(self):
        self.video = cv2.VideoCapture(1)

    def get_image(self) -> np.ndarray:
        _, frame = self.video.read()
        return frame


class Video(ImageGetter):
    video: cv2.VideoCapture

    def __init__(self, video_path: str):
        self.video = cv2.VideoCapture(video_path)

    def get_image(self) -> np.ndarray:
        _, frame = self.video.read()
        return frame
