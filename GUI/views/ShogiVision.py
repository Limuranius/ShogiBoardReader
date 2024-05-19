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
        self.set_animals_images()

    def set_animals_images(self):
        def set_image(label, img_name: str):
            img = cv2.imread(os.path.join(Paths.IMGS_DIR, "top patreon members", img_name))
            label.set_image(img)

        set_image(self.ui.label_asya, "Asya.jpg")
        set_image(self.ui.label_luna, "Luna.jpg")
        set_image(self.ui.label_rich, "Rich.jpg")
        set_image(self.ui.label_alisa, "Alisa.jpg")
        set_image(self.ui.label_busya, "Busya.jpg")
        set_image(self.ui.label_kesha_kokos, "Kesha and Kokos.jpg")
        set_image(self.ui.label_matilda, "Matilda.jpg")
        set_image(self.ui.label_tosha, "Tosha.jpg")
        set_image(self.ui.label_tihon, "Tihon.jpg")
        set_image(self.ui.label_milka, "Milka.jpg")

