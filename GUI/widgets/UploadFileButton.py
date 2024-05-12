from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import QPushButton
from GUI.widgets.UploadFileDialog import UploadFileDialog, FileType
from typing import Callable


class UploadFileButton(QPushButton):
    __file_type: FileType

    # Custom function that is called after user uploaded file
    # Uploaded files are passed as argument
    __on_file_uploaded_func: Callable

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.clicked.connect(self.on_click)
        self.__file_type = FileType.ONE_IMAGE
        self.setText("Upload files")

    @pyqtSlot()
    def on_click(self) -> None:
        win = UploadFileDialog(self.__file_type)
        win.setModal(True)
        win.file_uploaded.connect(self.__on_file_uploaded_func)
        win.exec()

    def set_file_type(self, file_type: FileType) -> None:
        self.__file_type = file_type

    def connect_function(self, func: Callable) -> None:
        self.__on_file_uploaded_func = func
