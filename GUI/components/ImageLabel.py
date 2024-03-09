import numpy as np
from PyQt5.QtWidgets import QLabel
from PyQt5.QtGui import QMouseEvent
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtGui import QPixmap, QImage
from extra.types import ImageNP
import cv2
from extra.utils import generate_random_image


def set_image_to_label(label, image: ImageNP):
    height, width = image.shape[:2]
    qimg = QImage(image.data, width, height, width * 3, QImage.Format_BGR888)
    label.setPixmap(QPixmap(qimg))


class ImageLabel(QLabel):
    resized_presses = list[tuple[int, int]]  # x, y of presses on modified image
    original_presses = list[tuple[int, int]]  # x, y of presses on original image
    clicked = pyqtSignal()

    __img_size: tuple[int, int] | None = None
    __image: ImageNP

    def __init__(self, *args, img_size: tuple[int, int] = None, **kwargs):
        super().__init__(*args, **kwargs)
        self.__img_size = img_size
        self.resized_presses = []
        self.original_presses = []
        self.__image = generate_random_image(500, 500, 3)

    def set_size(self, img_size: tuple[int, int]):
        self.__img_size = img_size
        self.set_image(self.__image)

    def set_image(self, image: ImageNP, show_presses: bool = False):
        self.__image = image
        if self.__img_size:
            image = cv2.resize(image, self.__img_size)
        if show_presses:
            h, w = image.shape[:2]
            thickness = int((h + w) / 2 * 0.01)
            pts = np.array(self.resized_presses)
            image = cv2.polylines(image, [pts], isClosed=True, color=[0, 255, 255], thickness=thickness)
        set_image_to_label(self, image)

    def mousePressEvent(self, ev: QMouseEvent) -> None:
        x, y = ev.x(), ev.y()
        orig_h, orig_w = self.__image.shape[:2]
        if self.__img_size is not None:
            h_factor = orig_h / self.__img_size[0]
            w_factor = orig_w / self.__img_size[1]
        else:
            h_factor = 1
            w_factor = 1
        orig_x = int(x * w_factor)
        orig_y = int(y * h_factor)
        self.resized_presses.append((x, y))
        self.original_presses.append((orig_x, orig_y))
        self.clicked.emit()

    def clear_clicks(self):
        self.original_presses = []
        self.resized_presses = []