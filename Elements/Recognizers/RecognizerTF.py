import keras
import numpy as np

from ShogiNeuralNetwork import preprocessing
from ShogiNeuralNetwork.data_info import CATEGORIES_FIGURE_TYPE, CATEGORIES_DIRECTION
from extra.figures import Figure, Direction
from extra.types import CellsImages, FigureBoard, ImageNP, DirectionBoard
from .Recognizer import Recognizer


class RecognizerTF(Recognizer):
    model: keras.models.Model
    cell_img_size: int

    def __init__(self, model_path: str, cell_img_size: int):
        self.model = keras.models.load_model(model_path)
        self.cell_img_size = cell_img_size

    def recognize_cell(self, cell_img: ImageNP) -> tuple[Figure, Direction]:
        raise Exception("Not implemented")

    def recognize_board(self, cells_imgs: CellsImages) -> tuple[FigureBoard, DirectionBoard]:
        inp = preprocessing.prepare_cells_imgs(cells_imgs)
        predictions = self.model(inp).numpy()
        figure_predict = predictions[0].argmax(axis=1)
        direction_predict = predictions[1].argmax(axis=1)
        figure_predict = np.reshape(figure_predict, (9, 9))
        direction_predict = np.reshape(direction_predict, (9, 9))

        figures = [[Figure.EMPTY for _ in range(9)] for __ in range(9)]
        directions = [[Direction.NONE for _ in range(9)] for __ in range(9)]

        for i in range(9):
            for j in range(9):
                figure_label = figure_predict[i][j]
                direction_label = direction_predict[i][j]
                figure = CATEGORIES_FIGURE_TYPE[figure_label]
                direction = CATEGORIES_DIRECTION[direction_label]
                figures[i][j] = figure
                directions[i][j] = direction
        return figures, directions

