from PyQt5.QtCore import pyqtSlot, pyqtSignal, QVariant, QThread
from PyQt5.QtWidgets import QWidget

from Elements import HardcodedCornerDetector
from GUI.UI.UI_VisualCornerSelect import Ui_visualCornerSelect
from extra.types import ImageNP
from GUI.components import combobox_values
from GUI.workers.SplitterWorker import SplitterWorker


class VisualCornerSelect(QWidget):
    __record_corner_clicks: bool
    __worker: SplitterWorker
    __worker_thread: QThread

    corner_detector_changed = pyqtSignal(QVariant)
    inventory_detector_changed = pyqtSignal(QVariant)
    __set_image_signal = pyqtSignal(ImageNP)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.ui = Ui_visualCornerSelect()
        self.ui.setupUi(self)
        self.__record_corner_clicks = False

        # Worker setup
        self.__worker = SplitterWorker()
        self.__worker_thread = QThread()
        self.__worker.frame_processed.connect(self.on_splitter_send)
        self.corner_detector_changed.connect(self.__worker.on_corner_detector_changed)
        self.inventory_detector_changed.connect(self.__worker.on_inventory_detector_changed)
        self.__set_image_signal.connect(self.__worker.set_image)
        self.__worker.moveToThread(self.__worker_thread)
        self.__worker_thread.start()

        self.ui.corner_detector_select.set_values(
            combobox_values.corner_detector()
        )
        self.ui.inventory_detector_select.set_values(
            combobox_values.inventory_detector()
        )

    @pyqtSlot(ImageNP, ImageNP)
    def on_splitter_send(self, full_img: ImageNP, no_persp: ImageNP):
        self.ui.image_label_original.set_image(
            full_img,
            show_presses=self.__record_corner_clicks
        )
        self.ui.image_label_no_perspective.set_image(
            no_persp,
            show_presses=False
        )

    def set_image(self, image: ImageNP):
        self.__set_image_signal.emit(image)

    @pyqtSlot(QVariant)
    def on_corner_detector_changed(self, corner_detector_factory):
        corner_detector = corner_detector_factory()
        if isinstance(corner_detector, HardcodedCornerDetector):
            self.ui.pushButton_set_corners.setVisible(True)
        else:
            self.ui.pushButton_set_corners.setVisible(False)
            self.corner_detector_changed.emit(QVariant(corner_detector_factory))

    @pyqtSlot(QVariant)
    def on_inventory_detector_changed(self, inventory_detector_factory):
        self.inventory_detector_changed.emit(QVariant(inventory_detector_factory))

    @pyqtSlot()
    def on_set_corners_clicked(self):
        self.ui.image_label_original.clear_clicks()
        self.__record_corner_clicks = True

    @pyqtSlot()
    def on_image_clicked(self):
        if self.__record_corner_clicks:
            corners = self.ui.image_label_original.original_presses
            if len(corners) == 4:
                corner_detector_factory = lambda: HardcodedCornerDetector(corners)
                self.corner_detector_changed.emit(QVariant(corner_detector_factory))
                self.__record_corner_clicks = False

    def set_size(self, size: tuple[int, int]):
        self.ui.image_label_original.set_size(size)
        self.ui.image_label_no_perspective.set_size(size)

    def set_inventory_hidden(self, hidden: bool):
        self.ui.inventory_detector_select.setHidden(hidden)
