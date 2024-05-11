import cv2
import numpy as np
from abc import ABC, abstractmethod
from extra.utils import generate_random_image
from extra.types import ImageNP


class ImageGetter(ABC):
    @abstractmethod
    def get_image(self) -> np.ndarray:
        pass


class Photo(ImageGetter):
    img: np.ndarray

    def __init__(self, img: str | ImageNP = ""):
        if isinstance(img, str):
            self.img = cv2.imread(img)
        else:
            self.img = img
        if self.img is None:
            self.img = generate_random_image(500, 500, 3)

    def get_image(self) -> np.ndarray:
        return self.img.copy()

    def __copy__(self):
        new_img = Photo(self.img.copy())
        return new_img


class Camera(ImageGetter):
    video: cv2.VideoCapture

    def __init__(self, cam_id: int = 0):
        self.video = cv2.VideoCapture(cam_id)

    def get_image(self) -> np.ndarray:
        ret, frame = self.video.read()
        if ret:
            # frame = cv2.rotate(frame, cv2.ROTATE_90_CLOCKWISE)
            return frame
        else:
            return generate_random_image(500, 500, 3)


class Video(ImageGetter):
    video: cv2.VideoCapture
    __path: str

    def __init__(self, video_path: str = ""):
        self.video = cv2.VideoCapture(video_path)
        self.finished_playing = False
        self.__path = video_path

    def get_image(self) -> ImageNP:
        ret, frame = self.video.read()
        if ret:
            return frame
        else:
            return generate_random_image(500, 500, 3)

    def restart(self) -> None:
        self.video = cv2.VideoCapture(self.__path)

    def __copy__(self):
        return Video(self.__path)