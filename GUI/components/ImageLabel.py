import numpy as np
from PyQt5.QtWidgets import QLabel
from PyQt5.QtGui import QMouseEvent
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtGui import QPixmap, QImage
from extra.types import ImageNP
import cv2


def set_image_to_label(label, image: ImageNP):
    height, width = image.shape[:2]
    qimg = QImage(image.data, width, height, width * 3, QImage.Format_BGR888)
    label.setPixmap(QPixmap(qimg))


class ImageLabel(QLabel):
    presses = list[tuple[int, int]]  # x, y
    clicked = pyqtSignal()
    img_size: tuple[int, int] | None = None

    def __init__(self, *args, img_size: tuple[int, int] = None, **kwargs):
        super().__init__(*args, **kwargs)
        self.img_size = img_size
        self.presses = [(0, 0), (0, 0)]

    def set_size(self, img_size: tuple[int, int]):
        self.img_size = img_size

    def set_image(self, image: ImageNP, show_presses: bool = False):
        if self.img_size:
            image = cv2.resize(image, self.img_size)
        if show_presses:
            pts = np.array(self.presses)
            image = cv2.polylines(image, [pts], isClosed=True, color=[0, 255, 0], thickness=3)
        set_image_to_label(self, image)

    def mousePressEvent(self, ev: QMouseEvent) -> None:
        self.presses.append((ev.x(), ev.y()))
        self.clicked.emit()