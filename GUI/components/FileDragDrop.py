import numpy as np
from PIL import ImageGrab
from PyQt5 import QtGui
from PyQt5.QtCore import pyqtSlot, pyqtSignal, QVariant
from PyQt5.QtWidgets import QWidget, QMessageBox
from GUI.UI.UI_FileDragDrop import Ui_fileDragDrop
import pyperclip
import cv2

ONE_IMAGE = "ONE_IMAGE"
MANY_IMAGES = "MANY_IMAGES"
VIDEO = "VIDEO"


class FileDragDrop(QWidget):
    received_content = pyqtSignal(QVariant)
    content_type: str

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.ui = Ui_fileDragDrop()
        self.ui.setupUi(self)
        self.setAcceptDrops(True)
        self.content_type = ONE_IMAGE

    def set_content_type(self, content_type: str):
        if content_type not in [ONE_IMAGE, MANY_IMAGES, VIDEO]:
            raise Exception()
        self.content_type = content_type

    @pyqtSlot(QtGui.QDragEnterEvent)
    def dragEnterEvent(self, event: QtGui.QDragEnterEvent):
        if event.mimeData().hasUrls():
            event.accept()
            self.setStyleSheet("background-color: gray")
        else:
            event.ignore()

    @pyqtSlot(QtGui.QDragLeaveEvent)
    def dragLeaveEvent(self, event: QtGui.QDragLeaveEvent):
        self.setStyleSheet("background-color: white")

    @pyqtSlot(QtGui.QDropEvent)
    def dropEvent(self, event: QtGui.QDropEvent):
        files = [u.toLocalFile() for u in event.mimeData().urls()]

        data = None
        if self.content_type == ONE_IMAGE:
            data = cv2.imread(files[0])
            if data is None:
                self.error_dialog("Could not load image")
                return
        elif self.content_type == MANY_IMAGES:
            data = []
            for path in files:
                img = cv2.imread(path)
                if img is None:
                    self.error_dialog("Could not load some of images")
                    return
                data.append(img)
        elif self.content_type == VIDEO:
            vc = cv2.VideoCapture(files[0])
            ret, frame = vc.read()
            if not ret:
                self.error_dialog("Could not load video")
                return
            data = files[0]
        self.received_content.emit(QVariant(data))

    @pyqtSlot()
    def on_paste_clicked(self):
        if self.content_type == ONE_IMAGE:
            try:
                image = ImageGrab.grabclipboard()
                if image is None:
                    self.error_dialog("Could not load image")
                    return
                image_np = np.array(image)
                data = image_np
            except Exception:
                self.error_dialog("Could not load image")
                return
        elif self.content_type == MANY_IMAGES:
            files = pyperclip.paste().split("\n")
            data = []
            for path in files:
                img = cv2.imread(path)
                if img is None:
                    self.error_dialog("Could not load some of images")
                    return
                data.append(img)
        elif self.content_type == VIDEO:
            path = pyperclip.paste()
            vc = cv2.VideoCapture(path)
            ret, frame = vc.read()
            if not ret:
                self.error_dialog("Could not load video")
                return
            data = path
        self.received_content.emit(QVariant(data))

    def error_dialog(self, text: str):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Critical)
        msg.setText("Error")
        msg.setInformativeText(text)
        msg.setWindowTitle("Error")
        msg.exec_()
