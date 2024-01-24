import cv2
from PyQt5 import QtWidgets
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QFrame
from ImageLabel import ImageLabel
from extra.types import Figure, Direction
from extra.figures import get_figure_image
from CellSelect import CellSelect


class Skibidi(QFrame):
    __figure: Figure
    __direction: Direction

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setup()

    def setup(self):
        self.verticalLayout = QtWidgets.QVBoxLayout(self)
        self.setLayout(self.verticalLayout)
        # self.figureCombo = QtWidgets.QComboBox(self)
        # self.verticalLayout.addWidget(self.figureCombo)
        # self.directionCombo = QtWidgets.QComboBox(self)
        # self.verticalLayout.addWidget(self.directionCombo)
        self.imageLabel = ImageLabel(self)
        self.verticalLayout.addWidget(self.imageLabel)
        self.imageLabel.clicked.connect(self.on_img_clicked)

        # for figure in Figure:
        #     self.figureCombo.addItem(figure.name, figure)
        # for direction in Direction:
        #     self.directionCombo.addItem(direction.name, direction)
        # self.figureCombo.currentTextChanged.connect(self.on_figure_change)
        # self.directionCombo.currentTextChanged.connect(self.on_direction_change)

    def set_cell(self, figure: Figure, direction: Direction):
        # self.figureCombo.setCurrentText(figure.name)
        # self.directionCombo.setCurrentText(direction.name)
        self.__figure = figure
        self.__direction = direction
        self.update_image()

    def get_figure(self) -> Figure:
        return self.__figure
        # return self.figureCombo.currentData()

    def get_direction(self) -> Direction:
        return self.__direction
        # return self.directionCombo.currentData()

    def update_image(self) -> None:
        # img = get_figure_image(self.get_figure(), self.get_direction())
        img = get_figure_image(Figure.EMPTY, Direction.NONE)
        img = cv2.resize(img, (50, 50))
        self.imageLabel.set_image(img)

    def on_img_clicked(self):
        cell_select_window = CellSelect()
        cell_select_window.exec()

    # def on_figure_change(self, _):
    #     self.update_image()
    #
    # def on_direction_change(self, _):
    #     self.update_image()
