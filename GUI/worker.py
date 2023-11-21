import numpy as np
from PyQt5.QtCore import pyqtSignal, QObject
from Elements import *
from extra.types import Image
from config import GLOBAL_CONFIG
from extra.image_modes import ImageMode
from extra import factories
from config.Paths import KIFU_PATH


class Worker(QObject):
    reader: ShogiBoardReader

    # Signal that sends created images in following order:
    # Full image, No perspective image, Predicted board image
    images_created = pyqtSignal(Image, Image, Image)

    # Signal that tells if the board is visible or obstructed
    memorizer_updated = pyqtSignal(BoardChangeStatus)

    show_original: bool = False
    show_no_perspective: bool = False
    show_predicted: bool = False

    def __init__(self):
        super().__init__()
        self.reader = ShogiBoardReader(
            image_mode=ImageMode(GLOBAL_CONFIG.NeuralNetwork.image_mode),
            board_splitter=BoardSplitter(
                image_getter=None,
                corner_getter=None,
                cell_img_size=GLOBAL_CONFIG.NeuralNetwork.cell_img_size
            ),
            recognizer=factories.default_nn_recognizer(),
        )

    def send_images(self):
        full_img = np.random.randint(low=0, high=255, size=(800, 800, 3), dtype=np.uint8)
        no_perspective = np.random.randint(low=0, high=255, size=(800, 800, 3), dtype=np.uint8)
        predicted_board_img = np.random.randint(low=0, high=255, size=(800, 800, 3), dtype=np.uint8)

        if self.show_original:
            full_img = self.reader.get_full_img(show_borders=True)
        if self.show_no_perspective:
            no_perspective = self.reader.get_board_image_no_perspective()
        if self.show_predicted:
            predicted_board_img = self.reader.get_board().to_image()
        self.images_created.emit(full_img, no_perspective, predicted_board_img)

    def update_corner_detector(self, option: str):
        corner_detector = None
        match option:
            case "HSV":
                corner_detector = factories.hsv_corner_detector()
            case "Cool":
                corner_detector = CornerDetectors.CoolCornerDetector()
        self.reader.set(
            corner_detector=corner_detector
        )

    def set_show_original(self, status: bool):
        self.show_original = status

    def set_show_no_perspective(self, status: bool):
        self.show_no_perspective = status

    def set_show_predicted(self, status: bool):
        self.show_predicted = status

    def set_use_memorizer(self, use_memorizer: bool):
        memorizer = None
        if use_memorizer:
            memorizer = BoardMemorizer(lower_moves_first=True)
        self.reader.set(
            memorizer=memorizer
        )

    def set_first_side(self, text: str):
        match text:
            case "First side: Lower":
                self.reader.memorizer.lower_moves_first = True
            case "First side: Upper":
                self.reader.memorizer.lower_moves_first = False
            case _:
                raise Exception("Unknown side option")

    def set_photo_imgetter(self, img_path: str):
        self.reader.set(
            image_getter=ImageGetters.Photo(img_path)
        )

    def set_video_imgetter(self, video_path: str):
        self.reader.set(
            image_getter=ImageGetters.Video(video_path)
        )

    def set_camera_imgetter(self):
        self.reader.set(
            image_getter=ImageGetters.Camera()
        )

    def save_kifu(self):
        self.reader.memorizer.save_to_kifu(KIFU_PATH)

    def main_loop(self):
        if self.show_predicted:
            self.reader.update()
            self.memorizer_updated.emit(self.reader.get_last_update_status())
        self.send_images()

    def run(self):
        self.reader.update()
        while True:
            self.main_loop()