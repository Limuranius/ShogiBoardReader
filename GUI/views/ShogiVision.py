from PyQt5.QtWidgets import QMainWindow
from GUI.UI.UI_ShogiVision import Ui_MainWindow
from config import Paths
import cv2
import os


class ShogiVision(QMainWindow):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        cat_img = cv2.imread(os.path.join(Paths.IMGS_DIR, "cat.jpg"))
        self.ui.label_cat.set_image(cat_img)
