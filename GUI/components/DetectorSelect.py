import os
import sys

from PyQt5 import QtWidgets
from PyQt5.QtCore import pyqtSignal, QLibraryInfo
from PyQt5.QtWidgets import QWidget, QFrame

from Elements import ShogiBoardReader, CornerDetectors
from Elements.CornerDetectors import CornerDetector
from GUI.components.ImageLabel import ImageLabel
from extra import factories
from extra.types import ImageNP


class DetectorSelect(QFrame):
    corner_detector_changed = pyqtSignal(CornerDetector)
    reader: ShogiBoardReader
    curr_img: ImageNP
    image_size: int

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.__setup_ui()
        self.__setup()

    def __setup_ui(self):
        self.vertical = QtWidgets.QVBoxLayout(self)
        self.full_img_label = ImageLabel(self)
        self.vertical.addWidget(self.full_img_label)
        self.select_frame = QtWidgets.QFrame(self)
        self.vertical.addWidget(self.select_frame)
        self.horizontal = QtWidgets.QHBoxLayout(self.select_frame)
        self.pushButton_fix_corners = QtWidgets.QPushButton(self.select_frame)
        self.pushButton_fix_corners.setEnabled(False)
        self.pushButton_fix_corners.setText("Set corners")
        self.horizontal.addWidget(self.pushButton_fix_corners)
        self.comboBox_corner_detector = QtWidgets.QComboBox(self.select_frame)
        self.horizontal.addWidget(self.comboBox_corner_detector)

    def __setup(self):
        self.comboBox_corner_detector.addItem("Cool")
        self.comboBox_corner_detector.addItem("Book")
        self.comboBox_corner_detector.addItem("HSV")
        self.comboBox_corner_detector.addItem("Hardcoded")
        self.comboBox_corner_detector.currentTextChanged.connect(self.__on_corner_detector_changed)
        self.pushButton_fix_corners.clicked.connect(self.__on_fix_corners_clicked)

    def set_size(self, size: int):
        self.full_img_label.set_size((size, size))
        self.image_size = size

    def set_reader(self, reader: ShogiBoardReader):
        self.reader = reader

    def __on_fix_corners_clicked(self):
        self.full_img_label.presses = []
        full_img = self.reader.get_full_img()
        self.full_img_label.set_image(full_img)
        self.full_img_label.clicked.connect(self.__full_img_clicked)

    def __full_img_clicked(self):
        full_img = self.reader.get_full_img()
        corners = self.full_img_label.presses
        if len(corners) == 4:
            orig_h, orig_w = full_img.shape[:2]
            h_factor = orig_h / self.image_size
            w_factor = orig_w / self.image_size
            orig_corners = []
            for x, y in corners:
                orig_x = x * w_factor
                orig_y = y * h_factor
                orig_corners.append((orig_x, orig_y))

            corner_detector = CornerDetectors.HardcodedCornerDetector(orig_corners)
            self.full_img_label.clicked.disconnect(self.__full_img_clicked)
            self.corner_detector_changed.emit(corner_detector)
        else:
            self.full_img_label.set_image(full_img, show_presses=True)

    def __on_corner_detector_changed(self, name: str):
        self.pushButton_fix_corners.setDisabled(True)
        match name:
            case "Cool":
                cd = CornerDetectors.CoolCornerDetector()
            case "Hardcoded":
                cd = CornerDetectors.HardcodedCornerDetector([(0, 0)] * 4)
                self.pushButton_fix_corners.setDisabled(False)
            case "HSV":
                cd = factories.hsv_corner_detector()
            case "Book":
                cd = CornerDetectors.BookCornerDetector()
        self.corner_detector_changed.emit(cd)

    def update(self):
        if self.reader.board_splitter.inventory_detector is None:
            img = self.reader.get_board_image_no_perspective(show_grid=True)
        else:
            img = self.reader.get_full_img(show_borders=True, show_grid=True, show_inventories=True)
        self.full_img_label.set_image(img)