from PyQt5.QtCore import pyqtSlot, QVariant, QThread
from PyQt5.QtWidgets import QWidget

from Elements.Board import Board
from GUI.UI.UI_scan_image import Ui_scan_image
from Elements import ImageGetters, BoardChangeStatus
from GUI.components import combobox_values
from extra.types import ImageNP
from GUI.workers.ReaderWorker import ReaderWorker

BOARD_IMAGE_SIZE = (500, 500)
CONFIG_BOARD_IMAGE_SIZE = (250, 250)


class ScanImage(QWidget):
    use_alarm: bool
    worker: ReaderWorker
    worker_thread: QThread

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.ui = Ui_scan_image()
        self.ui.setupUi(self)

        self.worker = ReaderWorker()
        self.worker_thread = QThread()
        self.worker.frame_processed.connect(self.update_images)
        self.worker.memorizer_updated.connect(self.on_memorizer_status_update)
        # self.worker_thread.started.connect(self.worker.run)
        self.ui.corner_and_inventory_select.corner_detector_changed.connect(self.worker.set_corner_detector)
        self.ui.corner_and_inventory_select.inventory_detector_changed.connect(self.worker.set_inventory_detector)
        self.ui.photo_drop.received_content.connect(self.worker.set_photo)
        self.ui.video_drop.received_content.connect(self.worker.set_video)
        self.ui.memorizer_select.element_changed.connect(self.worker.set_memorizer)
        self.ui.checkBox_lower_moves_first.clicked["bool"].connect(self.worker.set_lower_moves_first)
        self.ui.checkBox_recognize.clicked["bool"].connect(self.worker.set_recognize_board)
        self.ui.image_getter_select.element_changed.connect(self.worker.set_image_getter)

        self.worker.moveToThread(self.worker_thread)
        self.worker_thread.start()

        self.use_alarm = False
        self.ui.image_getter_select.set_values(combobox_values.image_getter())
        self.ui.memorizer_select.set_values(combobox_values.memorizer())
        self.ui.photo_drop.set_content_type("ONE_IMAGE")
        self.ui.video_drop.set_content_type("VIDEO")
        self.ui.corner_and_inventory_select.set_size(CONFIG_BOARD_IMAGE_SIZE)
        self.ui.board_view.set_size(BOARD_IMAGE_SIZE)

    @pyqtSlot(QVariant)
    def on_image_getter_changed(self, image_getter_factory):
        image_getter = image_getter_factory()

        # Showing widgets only for chosen image getter
        self.ui.photo_drop.setVisible(False)
        self.ui.video_drop.setVisible(False)
        self.ui.memorizer_select.setVisible(False)
        if isinstance(image_getter, ImageGetters.Photo):
            self.ui.photo_drop.setVisible(True)
        if isinstance(image_getter, ImageGetters.Video):
            self.ui.video_drop.setVisible(True)
            self.ui.memorizer_select.setVisible(True)
        if isinstance(image_getter, ImageGetters.Camera):
            self.ui.memorizer_select.setVisible(True)

    @pyqtSlot(bool)
    def on_alarm_switched(self, use_alarm: bool):
        self.use_alarm = use_alarm

    @pyqtSlot(BoardChangeStatus)
    def on_memorizer_status_update(self, update_status: BoardChangeStatus):
        self.ui.label_turn_status.setText(update_status.value)
        color = "white"
        match update_status:
            case BoardChangeStatus.NOTHING_CHANGED:
                color = "white"
            case BoardChangeStatus.VALID_MOVE:
                color = "green"
            case BoardChangeStatus.INVALID_MOVE:
                color = "red"
            case BoardChangeStatus.ILLEGAL_MOVE:
                color = "orange"
        self.ui.label_turn_status.setStyleSheet(f"background-color: {color}")

    @pyqtSlot(QVariant)
    def on_photo_input(self, image: ImageNP):
        pass

    @pyqtSlot(QVariant)
    def on_video_input(self, video_path: str):
        pass

    @pyqtSlot(QVariant)
    def on_memorizer_changed(self, memorizer_factory):
        pass

    @pyqtSlot(bool)
    def on_recognize_board_switched(self, recognize_board: bool):
        pass

    @pyqtSlot(QVariant)
    def on_corner_detector_changed(self, corner_detector_factory):
        pass

    @pyqtSlot(QVariant)
    def on_inventory_detector_changed(self, inventory_detector_factory):
        pass

    @pyqtSlot(bool)
    def on_lower_moves_first_switched(self, lower_moves_first: bool):
        pass

    @pyqtSlot(ImageNP, Board)
    def update_images(
            self,
            full_img: ImageNP,
            predicted_board: Board,
    ):
        self.ui.corner_and_inventory_select.set_image(full_img)
        self.ui.board_view.set_board(predicted_board)
        self.ui.kif_recorder.set_kif(self.worker.reader.get_kif())
