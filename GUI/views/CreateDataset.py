import cv2
from PyQt5 import QtWidgets
from PyQt5.QtCore import pyqtSlot, QVariant

from config import GLOBAL_CONFIG
from extra import factories
from Elements import ShogiBoardReader, CornerDetectors

from extra.figures import Figure, Direction
from extra.image_modes import ImageMode

from GUI.UI.create_dataset import Ui_MainWindow
from PyQt5.QtWidgets import QMainWindow, QMessageBox
from GUI.components.Skibidi import Skibidi
from ShogiNeuralNetwork.CellsDataset import CellsDataset
from config import Paths


BOARD_IMG_SIZE = (700, 700)


class CreateDataset(QMainWindow):
    images_paths: list[str]
    reader: ShogiBoardReader
    cells_select = list[list[Skibidi]]
    cells_dataset: CellsDataset

    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.setAcceptDrops(True)
        self.images_paths = []
        self.reader = factories.image_reader(ImageMode(GLOBAL_CONFIG.NeuralNetwork.image_mode))
        self.cells_dataset = CellsDataset()
        self.cells_dataset.load(Paths.DATASET_PATH)
        self.cells_select = []
        self.setup()

    def setup(self) -> None:
        self.ui.grid = QtWidgets.QGridLayout(self.ui.frame_cell_grid)
        for i in range(9):
            self.cells_select.append([])
            for j in range(9):
                cell_select = Skibidi(self.ui.frame_cell_grid)
                cell_select.set_cell(Figure.EMPTY, Direction.NONE)
                self.ui.grid.addWidget(cell_select, i, j)
                self.cells_select[i].append(cell_select)

        self.ui.visual_corner_select.set_size(BOARD_IMG_SIZE)
        self.ui.visual_corner_select.set_inventory_hidden(True)
        self.ui.visual_corner_select.set_use_one_image(True)

    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls():
            event.accept()
        else:
            event.ignore()

    def dropEvent(self, event):
        files = [u.toLocalFile() for u in event.mimeData().urls()]
        self.add_images_to_list(files)

    def add_images_to_list(self, paths: list[str]):
        for img_path in paths:
            if self.cells_dataset.is_image_visited(img_path):
                msg = QMessageBox()
                msg.setIcon(QMessageBox.Warning)
                msg.setText("Warning")
                msg.setInformativeText(f'This image ({img_path}) has already been used.\nNot adding that.')
                msg.setWindowTitle("Warning")
                msg.exec_()
            else:
                self.images_paths.append(img_path)
        self.update()

    def load_image(self, img_path: str) -> None:
        self.reader.set_image(img_path)
        img = cv2.imread(img_path)
        self.ui.visual_corner_select.set_images_by_splitter(img)

        # Loading each predicted cell into selects
        self.reader.update()
        predicted = self.reader.get_board()
        for i in range(9):
            for j in range(9):
                figure = predicted.figures[i][j]
                direction = predicted.directions[i][j]
                self.cells_select[i][j].set_cell(figure, direction)

    def update_images_list(self) -> None:
        self.ui.listWidget.clear()
        for img_path in self.images_paths:
            self.ui.listWidget.addItem(img_path)

    @pyqtSlot()
    def on_add_to_dataset_clicked(self):
        cells_imgs = self.reader.get_cells_imgs(ImageMode.ORIGINAL)
        for i in range(9):
            for j in range(9):
                cell_img = cells_imgs[i][j]
                figure = self.cells_select[i][j].get_figure()
                direction = self.cells_select[i][j].get_direction()
                self.cells_dataset.add_image(cell_img, figure, direction)
        self.cells_dataset.add_image_hash(self.images_paths[0])
        self.images_paths.pop(0)
        self.cells_dataset.save(Paths.DATASET_PATH)
        self.update()

    @pyqtSlot()
    def on_skip_clicked(self):
        self.images_paths.pop(0)
        self.update()

    @pyqtSlot(QVariant)
    def on_corner_detector_changed(self, corner_detector_factory):
        new_cd = corner_detector_factory()
        self.reader.set(corner_detector=new_cd)
        self.update()

    def update(self):
        self.update_images_list()
        if self.images_paths:
            self.load_image(self.images_paths[0])
            self.ui.pushButton_add.setDisabled(False)
        else:
            self.ui.pushButton_add.setDisabled(True)
