import copy

from PyQt5.QtCore import pyqtSlot, QVariant, QThread, pyqtSignal, QUrl
from PyQt5.QtMultimedia import QSoundEffect
from PyQt5.QtWidgets import QWidget

from Elements.Board import Board
from Elements.ImageGetters import Photo
from GUI.UI.UI_ScanImage import Ui_scan_image
from Elements import ImageGetters, BoardChangeStatus, ShogiBoardReader
from GUI.views.Settings import Settings
from config import Paths
from extra.types import ImageNP
from GUI.workers.ReaderWorker import ReaderWorker


class ScanImage2(QWidget):
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
        self.__request_images_signal.connect(self.__worker.send_data)
        self.__worker.moveToThread(self.__worker_thread)
        self.__worker_thread.start()
        # self.__request_data()

        # self.__alarm_sound = QSoundEffect()
        # self.__alarm_sound.setSource(QUrl.fromLocalFile(Paths.ALARM_PATH))
        # self.__alarm_sound.setLoopCount(QSoundEffect.Infinite)

    def set_memorizer_status(self, update_status: BoardChangeStatus):
        self.ui.label_memorizer_status.setText(update_status.value)
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
                self.start_alarm()
        self.ui.label_memorizer_status.setStyleSheet(f"background-color: {color}")

    @pyqtSlot(ImageNP, ImageNP, Board, str, BoardChangeStatus)
    def update_data(
            self,
            full_img: ImageNP,
            no_perspective: ImageNP,
            predicted_board: Board,
            kif: str,
            update_status: BoardChangeStatus,
    ):
        self.ui.label_full_image.set_image(full_img)
        self.ui.board_view.set_board(predicted_board)
        self.ui.kif_recorder.set_kif(kif)
        self.set_memorizer_status(update_status)

        if self.__request_sent:  # Checking that the data was sent in response to request and not some random events
            self.__request_sent = False
            if self.__continuous_request:
                self.__request_data()

    def __request_data(self):
        if not self.__request_sent:
            self.__request_sent = True
            self.__request_images_signal.emit()

    def start_stream(self):
        self.__continuous_request = True
        self.__request_data()
        self.ui.pushButton_pause.setText("Pause")

    def stop_stream(self):
        self.__continuous_request = False
        self.ui.pushButton_pause.setText("Continue")

    @pyqtSlot()
    def on_pause_clicked(self):
        if self.ui.pushButton_pause.text() == "Pause":
            self.stop_stream()
        else:
            self.start_stream()

    @pyqtSlot()
    def on_restart_video_clicked(self):
        pass

    @pyqtSlot()
    def on_settings_clicked(self):
        reader = self.__worker.get_reader()
        settings_win = Settings(copy.copy(reader))
        settings_win.reader_changed.connect(self.on_reader_changed)
        settings_win.setModal(True)
        settings_win.exec()


    @pyqtSlot()
    def on_clear_memorizer_clicked(self):
        pass

    @pyqtSlot(ShogiBoardReader)
    def on_reader_changed(self, new_reader: ShogiBoardReader):
        self.__worker.set_reader(new_reader)

        # Checking image getter type
        image_getter = new_reader.get_board_splitter().get_image_getter()
        if isinstance(image_getter, Photo):
            self.stop_stream()
        else:
            self.start_stream()

    def start_alarm(self):
        pass

    def stop_alarm(self):
        pass