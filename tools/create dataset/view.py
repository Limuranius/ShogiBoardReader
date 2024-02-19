from PyQt5 import QtWidgets

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


BOARD_IMG_SIZE = 800


class View(QMainWindow):
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
        self.reader = factories.get_image_reader(ImageMode(GLOBAL_CONFIG.NeuralNetwork.image_mode))
        self.cells_dataset = CellsDataset()
        self.cells_dataset.load_pickle(Paths.DATASET_PATH)
        self.cells_select = []
        self.setup()

    def setup(self) -> None:
        self.ui.grid = QtWidgets.QGridLayout(self.ui.frame_3)
        for i in range(9):
            self.cells_select.append([])
            for j in range(9):
                cell_select = Skibidi(self.ui.frame_3)
                cell_select.set_cell(Figure.EMPTY, Direction.NONE)
                self.ui.grid.addWidget(cell_select, i, j)
                self.cells_select[i].append(cell_select)
        self.ui.pushButton_add.clicked.connect(self.on_add_to_dataset_clicked)
        self.ui.pushButton_skip.clicked.connect(self.on_skip_clicked)

        self.ui.detector_select.set_size(BOARD_IMG_SIZE)
        self.ui.detector_select.set_reader(self.reader)
        self.ui.detector_select.corner_detector_changed.connect(self.on_corner_detector_changed)

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

        # Showing no-perspective image of board
        self.ui.detector_select.update()

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

    def on_skip_clicked(self):
        self.images_paths.pop(0)
        self.update()

    def on_corner_detector_changed(self, new_cd: CornerDetectors.CornerDetector):
        self.reader.set(corner_detector=new_cd)
        self.update()

    def update(self):
        self.update_images_list()
        if self.images_paths:
            self.load_image(self.images_paths[0])
            self.ui.pushButton_add.setDisabled(False)
        else:
            self.ui.pushButton_add.setDisabled(True)
