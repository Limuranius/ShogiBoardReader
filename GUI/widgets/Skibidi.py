import cv2
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QFrame
from GUI.widgets.ImageLabel import ImageLabel
from extra.types import Figure, Direction
from extra.figures import get_figure_image
from GUI.widgets.CellSelect import CellSelect


class Skibidi(QFrame):
    __figure: Figure
    __direction: Direction

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setup()

    def setup(self):
        self.verticalLayout = QtWidgets.QVBoxLayout(self)
        self.setLayout(self.verticalLayout)
        self.imageLabel = ImageLabel(self)
        self.verticalLayout.addWidget(self.imageLabel)
        self.imageLabel.clicked.connect(self.on_img_clicked)
        self.imageLabel.set_size((70, 70))

    def set_cell(self, figure: Figure, direction: Direction):
        self.__figure = figure
        self.__direction = direction
        self.update_image()

    def get_figure(self) -> Figure:
        return self.__figure

    def get_direction(self) -> Direction:
        return self.__direction

    def update_image(self) -> None:
        img = get_figure_image(self.get_figure(), self.get_direction())
        self.imageLabel.set_image(img)

    def on_img_clicked(self):
        cell_select_window = CellSelect()
        cell_select_window.choice_clicked.connect(lambda f, d: self.set_cell(f, d))
        cell_select_window.exec()

