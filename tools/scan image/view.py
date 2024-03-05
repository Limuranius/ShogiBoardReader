import cv2
import numpy as np
from PyQt5.QtWidgets import QMainWindow, QMessageBox
from Elements.CornerDetectors import CornerDetector
from Elements.InventoryDetectors import BookInventoryDetector
from GUI.UI.scan_image import Ui_MainWindow
from extra.types import ImageNP
from PIL import ImageGrab
import webbrowser
from Elements import ShogiBoardReader

IMAGE_SIZE = 700


class View(QMainWindow):
    current_image: ImageNP

    def __init__(self, reader: ShogiBoardReader):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.setAcceptDrops(True)
        self.reader = reader
        self.setup()

    def setup(self):
        self.ui.detector_select.set_size(IMAGE_SIZE)
        self.ui.detector_select.set_reader(self.reader)
        self.ui.label_predicted_board.set_size((IMAGE_SIZE, IMAGE_SIZE))

        blank_img = np.random.randint(0, 255, size=(IMAGE_SIZE, IMAGE_SIZE, 3), dtype=np.uint8)
        self.reader.set_image(blank_img)
        self.ui.detector_select.update()
        self.ui.label_predicted_board.set_image(blank_img)
        self.ui.pushButton_to_lishogi.clicked.connect(self.on_lishogi_clicked)
        self.ui.pushButton_clipboard.clicked.connect(self.on_clipboard_clicked)

        self.ui.detector_select.corner_detector_changed.connect(self.on_corner_detector_changed)

        self.ui.comboBox_inventory_detector.currentTextChanged.connect(self.on_inventory_detector_changed)

    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls():
            event.accept()
        else:
            event.ignore()

    def dropEvent(self, event):
        files = [u.toLocalFile() for u in event.mimeData().urls()]
        self.current_image = cv2.imread(files[0])
        self.update()

    def on_clipboard_clicked(self):
        try:
            image = ImageGrab.grabclipboard()
        except Exception as e:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Critical)
            msg.setText("Error")
            msg.setInformativeText("No image in clipboard")
            msg.setWindowTitle("Error")
            msg.exec_()
            return
        self.current_image = np.array(image)
        self.update()

    def load_image(self, image: ImageNP):
        self.reader.set_image(image)
        self.reader.update()
        board = self.reader.get_board()
        board_img = board.to_image()
        self.ui.detector_select.update()
        self.ui.label_predicted_board.set_image(board_img)
        sfen = board.to_shogi_board().sfen()
        self.ui.textEdit_sfen.setText(sfen)

    def update(self):
        self.load_image(self.current_image)

    def on_corner_detector_changed(self, new_cd: CornerDetector):
        self.reader.set(corner_detector=new_cd)
        self.update()