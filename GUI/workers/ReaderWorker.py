import numpy as np
from PyQt5.QtCore import pyqtSignal, QObject, QVariant, pyqtSlot
from Elements import *
from Elements.Board import Board
from extra.types import ImageNP
from config import GLOBAL_CONFIG
from extra.image_modes import ImageMode
from extra import factories
from config.Paths import KIFU_PATH


class ReaderWorker(QObject):
    reader: ShogiBoardReader

    # Signal that sends processed/predicted data (or None if disabled) in following order:
    # Full image, Predicted board object
    frame_processed = pyqtSignal(ImageNP, Board)

    # Signal that sends responses of memorizer
    memorizer_updated = pyqtSignal(BoardChangeStatus)

    predict_board: bool = False

    running: bool = True

    def __init__(self):
        super().__init__()
        self.reader = factories.image_reader()

    def send_images(self):
        full_img = self.reader.get_full_img(show_borders=True)
        predicted_board = self.reader.get_board()
        self.frame_processed.emit(full_img, predicted_board)

    def main_loop(self):
        if self.predict_board:
            self.reader.update()
            self.memorizer_updated.emit(self.reader.get_last_update_status())
        self.send_images()

    @pyqtSlot()
    def run(self):
        while self.running:
            self.main_loop()

    def stop(self):
        self.running = False

    @pyqtSlot(QVariant)
    def set_image_getter(self, image_getter_factory):
        image_getter = image_getter_factory()
        self.reader.set(image_getter=image_getter)
        print(type(image_getter))
        print(type(self.reader.board_splitter.image_getter))
        print()

    @pyqtSlot(QVariant)
    def set_photo(self, image: ImageNP):
        self.reader.set_image(image)

    @pyqtSlot(QVariant)
    def set_video(self, video_path: str):
        self.reader.set(image_getter=ImageGetters.Video(video_path))

    @pyqtSlot(QVariant)
    def set_memorizer(self, memorizer_factory):
        self.reader.set(memorizer=memorizer_factory())

    @pyqtSlot(bool)
    def set_lower_moves_first(self, lower_moves_first: bool):
        self.reader.memorizer.lower_moves_first = lower_moves_first

    @pyqtSlot(bool)
    def set_recognize_board(self, recognize_board: bool):
        self.predict_board = recognize_board

    @pyqtSlot(QVariant)
    def set_corner_detector(self, corner_detector_factory):
        self.reader.set(corner_detector=corner_detector_factory())

    @pyqtSlot(QVariant)
    def set_inventory_detector(self, inventory_detector_factory):
        self.reader.set(inventory_detector=inventory_detector_factory())