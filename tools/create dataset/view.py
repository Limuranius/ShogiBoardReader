from PyQt5 import QtWidgets

from extra import factories
from Elements import ShogiBoardReader
import cv2

from extra.figures import Figure, Direction
from extra.image_modes import ImageMode

from create_dataset import Ui_MainWindow
from PyQt5.QtWidgets import QMainWindow
from Skibidi import Skibidi

class View(QMainWindow):
    images_paths: list[str]
    reader: ShogiBoardReader
    cells_select = list[list[Skibidi]]

    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.setAcceptDrops(True)
        self.images_paths = []
        self.reader = factories.get_image_reader(ImageMode.ORIGINAL)
        self.setup()

    def setup(self) -> None:
        self.cells_select = [[None for _ in range(9)] for __ in range(9)]
        self.ui.grid = QtWidgets.QGridLayout(self.ui.frame_3)
        for i in range(9):
            for j in range(9):
                cell_select = Skibidi(self.ui.frame_3)
                cell_select.set_cell(Figure.EMPTY, Direction.NONE)
                self.ui.grid.addWidget(cell_select, i, j)
                self.cells_select[i][j] = cell_select

    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls():
            event.accept()
        else:
            event.ignore()

    def dropEvent(self, event):
        files = [u.toLocalFile() for u in event.mimeData().urls()]
        self.add_images_to_list(files)
        self.load_image(self.images_paths[0])

    def add_images_to_list(self, paths: list[str]):
        self.images_paths += paths
        self.update_images_list()

    def load_image(self, img_path: str) -> None:
        self.reader.set_image(img_path)
        # img = self.reader.get_full_img(show_borders=True, show_grid=True)
        img = self.reader.get_board_image_no_perspective(show_grid=True)
        img = cv2.resize(img, (600, 600))
        self.ui.full_img_label.set_image(img)

    def update_images_list(self) -> None:
        self.ui.listWidget.clear()
        for img_path in self.images_paths:
            self.ui.listWidget.addItem(img_path)