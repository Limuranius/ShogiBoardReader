import multiprocessing

from PyQt5.QtCore import pyqtSlot, QVariant, QThread, QTimer, pyqtSignal
from PyQt5.QtWidgets import QWidget

from Elements.Board import Board
from GUI.UI.UI_scan_image import Ui_scan_image
from Elements import ImageGetters, BoardChangeStatus
from GUI.components import combobox_values
from config import Paths
from extra.types import ImageNP
from GUI.workers.ReaderWorker import ReaderWorker

BOARD_IMAGE_SIZE = (500, 661)
CONFIG_BOARD_IMAGE_SIZE = (250, 250)


class ScanImage(QWidget):
    __use_alarm: bool = False
    __sound_thread: multiprocessing.Process = multiprocessing.Process()

    __worker: ReaderWorker
    __worker_thread: QThread

    # Signal that is sent to worker to request images
    __request_images_signal = pyqtSignal()

    # if True, then request for images has already been sent and another on will not be made
    __request_sent: bool = False

    # if True, then requests will be made repeatedly, else only once
    __continuous_request: bool = False

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.ui = Ui_scan_image()
        self.ui.setupUi(self)

        self.__worker = ReaderWorker()
        self.__worker_thread = QThread()
        self.__worker.frame_processed.connect(self.update_data)
        self.ui.corner_and_inventory_select.corner_detector_changed.connect(self.__worker.set_corner_detector)
        self.ui.corner_and_inventory_select.inventory_detector_changed.connect(self.__worker.set_inventory_detector)
        self.ui.photo_drop.received_content.connect(self.__worker.set_photo)
        self.ui.video_drop.received_content.connect(self.__worker.set_video)
        self.ui.memorizer_select.element_changed.connect(self.__worker.set_memorizer)
        self.ui.checkBox_lower_moves_first.clicked["bool"].connect(self.__worker.set_lower_moves_first)
        self.ui.checkBox_recognize.clicked["bool"].connect(self.__worker.set_recognize_board)
        self.ui.image_getter_select.element_changed.connect(self.__worker.set_image_getter)
        self.__request_images_signal.connect(self.__worker.send_data)
        self.ui.cam_id_select.element_changed.connect(self.__worker.set_image_getter)
        self.__worker.moveToThread(self.__worker_thread)
        self.__worker_thread.start()
        self.__request_data()

        cams_name, cams_values = combobox_values.cameras()
        self.ui.cam_id_select.set_name(cams_name)
        self.ui.cam_id_select.set_values(cams_values)

        ig_name, ig_values = combobox_values.image_getter()
        self.ui.image_getter_select.set_name(ig_name)
        self.ui.image_getter_select.set_values(ig_values)

        mem_name, mem_values = combobox_values.memorizer()
        self.ui.memorizer_select.set_name(mem_name)
        self.ui.memorizer_select.set_values(mem_values)

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
        self.ui.frame_memorizer.setVisible(False)
        self.ui.cam_id_select.setVisible(False)
        if isinstance(image_getter, ImageGetters.Photo):
            self.ui.photo_drop.setVisible(True)
            self.__continuous_request = False
        if isinstance(image_getter, ImageGetters.Video):
            self.ui.video_drop.setVisible(True)
            self.ui.frame_memorizer.setVisible(True)
            self.__continuous_request = True
        if isinstance(image_getter, ImageGetters.Camera):
            self.ui.frame_memorizer.setVisible(True)
            self.ui.cam_id_select.setVisible(True)
            self.__continuous_request = True
        self.__request_data()

    @pyqtSlot(bool)
    def on_alarm_switched(self, use_alarm: bool):
        self.__use_alarm = use_alarm

    def set_memorizer_status(self, update_status: BoardChangeStatus):
        self.ui.label_turn_status.setText(update_status.value)
        color = "white"
        match update_status:
            case BoardChangeStatus.NOTHING_CHANGED:
                color = "white"
                self.stop_alarm()
            case BoardChangeStatus.VALID_MOVE:
                color = "green"
                self.stop_alarm()
            case BoardChangeStatus.INVALID_MOVE:
                color = "red"
                self.start_alarm()
            case BoardChangeStatus.ILLEGAL_MOVE:
                color = "orange"
                self.start_alarm()
            case BoardChangeStatus.ACCUMULATING_DATA:
                color = "lime"
                self.stop_alarm()
            case BoardChangeStatus.LOW_CERTAINTY:
                color = "yellow"
                self.stop_alarm()
        self.ui.label_turn_status.setStyleSheet(f"background-color: {color}")

    @pyqtSlot(QVariant)
    def on_photo_input(self, image: ImageNP):
        pass

    @pyqtSlot(QVariant)
    def on_video_input(self, video_path: str):
        pass

    @pyqtSlot(QVariant)
    def on_memorizer_changed(self, memorizer_factory):
        memorizer = memorizer_factory()
        self.ui.kif_recorder.setVisible(memorizer is not None)

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

    @pyqtSlot(QVariant)
    def on_cam_id_changed(self, camera_factory):
        pass

    @pyqtSlot(ImageNP, ImageNP, Board, str, BoardChangeStatus)
    def update_data(
            self,
            full_img: ImageNP,
            no_perspective: ImageNP,
            predicted_board: Board,
            kif: str,
            update_status: BoardChangeStatus,
    ):
        self.ui.corner_and_inventory_select.set_images_fast(full_img, no_perspective)
        self.ui.board_view.set_board(predicted_board)
        self.ui.kif_recorder.set_kif(kif)
        self.set_memorizer_status(update_status)

        if self.__request_sent:  # Checking that the data was sent in response to request
            self.__request_sent = False
            if self.__continuous_request:
                self.__request_data()

    def __request_data(self):
        if not self.__request_sent:
            self.__request_sent = True
            self.__request_images_signal.emit()

    def start_alarm(self):
        if not self.__use_alarm:
            return
        if not self.__sound_thread.is_alive():
            self.__sound_thread = multiprocessing.Process(target=play_sound_in_repeat,
                                                          args=[Paths.ALARM_PATH])
            self.__sound_thread.start()

    def stop_alarm(self):
        if self.__sound_thread.is_alive():
            self.__sound_thread.terminate()


def play_sound_in_repeat(sound_path: str):
    import playsound
    while True:
        playsound.playsound(sound_path)
