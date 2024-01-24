from PyQt5.QtWidgets import QLabel
from PyQt5.QtGui import QMouseEvent
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtGui import QPixmap, QImage
from extra.types import ImageNP


def set_image_to_label(label, image: ImageNP):
    height, width = image.shape[:2]
    qimg = QImage(image.data, width, height, width * 3, QImage.Format_BGR888)
    label.setPixmap(QPixmap(qimg))


class ImageLabel(QLabel):
    presses = list[tuple[int, int]]
    clicked = pyqtSignal()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.presses = [(0, 0), (0, 0)]

    def set_image(self, image: ImageNP):
        set_image_to_label(self, image)

    def mousePressEvent(self, ev: QMouseEvent) -> None:
        self.presses.append((ev.x(), ev.y()))
        self.clicked.emit()