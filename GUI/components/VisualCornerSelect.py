from PyQt5.QtCore import pyqtSlot, pyqtSignal, QVariant, QThread
from PyQt5.QtWidgets import QWidget

from Elements import HardcodedCornerDetector, BoardSplitter, CoolCornerDetector
from Elements.ImageGetters import Photo
from GUI.UI.UI_VisualCornerSelect import Ui_visualCornerSelect
from extra.types import ImageNP
from GUI.components import combobox_values


class VisualCornerSelect(QWidget):
    __record_corner_clicks: bool
    __splitter: BoardSplitter

    corner_detector_changed = pyqtSignal(QVariant)
    inventory_detector_changed = pyqtSignal(QVariant)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.ui = Ui_visualCornerSelect()
        self.ui.setupUi(self)
        self.__record_corner_clicks = False
        self.__splitter = BoardSplitter(
            image_getter=Photo(),
            corner_getter=CoolCornerDetector()
        )
        self.ui.corner_detector_select.set_values(
            combobox_values.corner_detector()
        )
        self.ui.inventory_detector_select.set_values(
            combobox_values.inventory_detector()
        )

    @pyqtSlot(QVariant)
    def on_corner_detector_changed(self, corner_detector_factory):
        corner_detector = corner_detector_factory()
        if isinstance(corner_detector, HardcodedCornerDetector):
            self.ui.pushButton_set_corners.setVisible(True)
        else:
            self.ui.pushButton_set_corners.setVisible(False)
            self.__splitter.corner_detector = corner_detector
            self.corner_detector_changed.emit(QVariant(corner_detector_factory))

    @pyqtSlot()
    def on_set_corners_clicked(self):
        self.ui.image_label_original.clear_clicks()
        self.__record_corner_clicks = True

    @pyqtSlot(QVariant)
    def on_inventory_detector_changed(self, inventory_detector_factory):
        self.inventory_detector_changed.emit(QVariant(inventory_detector_factory))

    @pyqtSlot()
    def on_image_clicked(self):
        if self.__record_corner_clicks:
            corners = self.ui.image_label_original.original_presses
            if len(corners) == 4:
                corner_detector_factory = lambda: HardcodedCornerDetector(corners)
                self.__splitter.corner_detector = HardcodedCornerDetector(corners)
                self.corner_detector_changed.emit(QVariant(corner_detector_factory))
                self.__record_corner_clicks = False

    def __show_images(self, full_img: ImageNP, no_persp: ImageNP):
        self.ui.image_label_original.set_image(
            full_img,
            show_presses=self.__record_corner_clicks
        )
        self.ui.image_label_no_perspective.set_image(
            no_persp,
            show_presses=False
        )

    def set_images_fast(self, full_image: ImageNP, no_persp: ImageNP):
        self.__show_images(full_image, no_persp)

    def set_images_by_splitter(self, image: ImageNP):
        self.__splitter.set_image(image)
        full_img = self.__splitter.get_full_img(show_borders=True)
        no_persp = self.__splitter.get_board_image_no_perspective(draw_grid=True)
        self.__show_images(full_img, no_persp)

    def set_size(self, size: tuple[int, int]):
        self.ui.image_label_original.set_size(size)
        self.ui.image_label_no_perspective.set_size(size)

    def set_inventory_hidden(self, hidden: bool):
        self.ui.inventory_detector_select.setHidden(hidden)
