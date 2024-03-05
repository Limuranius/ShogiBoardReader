from PyQt5.QtCore import pyqtSignal, QObject, pyqtSlot, QVariant
import Elements
from Elements import *
from extra.types import ImageNP


class SplitterWorker(QObject):
    __splitter: BoardSplitter

    # Signal that sends processed images in following order:
    # Full image, No perspective image
    frame_processed = pyqtSignal(ImageNP, ImageNP)

    def __init__(self):
        super().__init__()
        self.__splitter = BoardSplitter(
            image_getter=Elements.ImageGetters.Photo(),
            corner_getter=Elements.CoolCornerDetector(),
            inventory_detector=None
        )

    def send_images(self):
        full_img = self.__splitter.get_full_img(show_borders=True)
        no_perspective = self.__splitter.get_board_image_no_perspective(draw_grid=True)
        self.frame_processed.emit(full_img, no_perspective)

    @pyqtSlot(ImageNP)
    def set_image(self, image: ImageNP):
        self.__splitter.set_image(image)
        self.send_images()

    @pyqtSlot(QVariant)
    def on_corner_detector_changed(self, corner_detector_factory):
        corner_detector = corner_detector_factory()
        self.__splitter.corner_detector = corner_detector
        self.send_images()

    @pyqtSlot(QVariant)
    def on_inventory_detector_changed(self, inventory_detector_factory):
        inventory_detector = inventory_detector_factory()
        self.__splitter.inventory_detector = inventory_detector
        self.send_images()
