import cv2
from PyQt5.QtCore import QThread, pyqtSignal
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtWidgets import (
    QMainWindow,
    QRadioButton,
    QLabel,
)

from config import Paths
from .main_window import Ui_MainWindow
from .worker import Worker
from extra.types import Image
import multiprocessing


def show_image_on_label(image: Image, label: QLabel):
    height, width = image.shape[:2]
    bytes_per_line = 3 * width
    q_img = QImage(image.data, width, height, bytes_per_line, QImage.Format_BGR888)
    label.setPixmap(QPixmap(q_img))


def play_sound_in_repeat(sound_path: str):
    import playsound
    while True:
        playsound.playsound(sound_path)


class View(QMainWindow):
    IMGS_SIZE = 500

    worker: Worker

    # Image getters signals
    s_photo_imgetter_selected = pyqtSignal(str)
    s_video_imgetter_selected = pyqtSignal(str)
    s_camera_imgetter_selected = pyqtSignal()

    # Corner getter signal
    s_updated_corner_detector = pyqtSignal(str)

    # Use memorizer / not use memorizer
    s_updated_memorizer = pyqtSignal(bool)

    s_updated_first_side = pyqtSignal(str)

    worker_thread: QThread
    sound_thread: multiprocessing.Process = multiprocessing.Process()

    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.setup()

    def setup(self):
        self.hide_widgets()
        self.connect_widgets()
        self.setup_worker()
        self.update_image_getter()
        self.update_corner_detector()

    def setup_worker(self):
        self.worker = Worker()
        self.worker.images_created.connect(self.show_images)

        self.s_photo_imgetter_selected.connect(self.worker.set_photo_imgetter)
        self.s_video_imgetter_selected.connect(self.worker.set_video_imgetter)
        self.s_camera_imgetter_selected.connect(self.worker.set_camera_imgetter)

        self.s_updated_corner_detector.connect(self.worker.update_corner_detector)
        self.s_updated_memorizer.connect(self.worker.set_use_memorizer)

        self.s_updated_first_side.connect(self.worker.set_first_side)
        self.ui.comboBox_first_side.currentTextChanged.connect(self.worker.set_first_side)

        self.ui.checkBox_img_original.clicked.connect(self.worker.set_show_original)
        self.ui.checkBox_img_no_perspective.clicked.connect(self.worker.set_show_no_perspective)
        self.ui.checkBox_img_predicted_board.clicked.connect(self.worker.set_show_predicted)

        self.ui.lineEdit_photo_path.textChanged.connect(self.worker.set_photo_imgetter)
        self.ui.lineEdit_video_path.textChanged.connect(self.worker.set_video_imgetter)

        self.ui.pushButton_save_kifu.clicked.connect(self.worker.save_kifu)

        self.worker.board_is_visible.connect(self.board_visible)

    def hide_widgets(self):
        self.ui.frame_ig_photo.setHidden(True)
        self.ui.frame_ig_video.setHidden(True)
        self.ui.comboBox_first_side.setHidden(True)

    def update_image_getter(self):
        checked_option = ""
        for option in self.ui.groupBox_image_getter.children():
            if isinstance(option, QRadioButton) and option.isChecked():
                checked_option = option.text()

        self.ui.frame_ig_photo.setHidden(True)
        self.ui.frame_ig_video.setHidden(True)
        match checked_option:
            case "Photo":
                self.ui.frame_ig_photo.setHidden(False)
                img_path = self.ui.lineEdit_photo_path.text()
                self.s_photo_imgetter_selected.emit(img_path)
            case "Video":
                self.ui.frame_ig_video.setHidden(False)
                vid_path = self.ui.lineEdit_video_path.text()
                self.s_video_imgetter_selected.emit(vid_path)
            case "Camera":
                self.s_camera_imgetter_selected.emit()

    def update_corner_detector(self):
        checked_option = ""
        for option in self.ui.groupBox_corner_detector.children():
            if isinstance(option, QRadioButton) and option.isChecked():
                checked_option = option.text()
        self.s_updated_corner_detector.emit(checked_option)

    def memorizer_checked(self, use_memorizer: bool):
        self.ui.comboBox_first_side.setHidden(not use_memorizer)
        self.s_updated_memorizer.emit(use_memorizer)

    def show_images(
            self,
            full_img: Image,
            no_perspective: Image,
            predicted_board_img: Image):
        img_size = (self.IMGS_SIZE, self.IMGS_SIZE)

        full_img = cv2.resize(full_img, img_size)
        show_image_on_label(
            image=full_img,
            label=self.ui.label_img_original
        )

        no_perspective = cv2.resize(no_perspective, img_size)
        show_image_on_label(
            image=no_perspective,
            label=self.ui.label_img_no_perspective
        )

        predicted_board_img = cv2.resize(predicted_board_img, img_size)
        show_image_on_label(
            image=predicted_board_img,
            label=self.ui.label_img_predicted
        )

    def start_clicked(self):
        self.worker_thread = QThread()
        self.worker.moveToThread(self.worker_thread)
        self.worker_thread.started.connect(self.worker.run)
        self.worker_thread.start()

    def start_alarm(self):
        if not self.sound_thread.is_alive():
            self.sound_thread = multiprocessing.Process(target=play_sound_in_repeat,
                                                        args=[Paths.ALARM_PATH])
            self.sound_thread.start()

    def stop_alarm(self):
        if self.sound_thread.is_alive():
            self.sound_thread.terminate()

    def board_visible(self, is_board_visible: bool):
        print("Visible" if is_board_visible else "Not visible")
        if is_board_visible:
            self.stop_alarm()
        else:
            self.start_alarm()

    def connect_widgets(self):
        self.ui.checkBox_use_memorizer.clicked.connect(self.memorizer_checked)
        for radioButton in self.ui.groupBox_image_getter.children():
            if isinstance(radioButton, QRadioButton):
                radioButton.clicked.connect(self.update_image_getter)
        for radioButton in self.ui.groupBox_corner_detector.children():
            if isinstance(radioButton, QRadioButton):
                radioButton.clicked.connect(self.update_corner_detector)
        self.ui.pushButton_start.clicked.connect(self.start_clicked)
