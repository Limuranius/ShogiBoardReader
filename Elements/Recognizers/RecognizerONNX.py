import numpy as np
import onnxruntime
from ShogiNeuralNetwork import preprocessing
from ShogiNeuralNetwork.data_info import CATEGORIES_FIGURE_TYPE, CATEGORIES_DIRECTION
from extra.figures import Figure, Direction
from extra.types import CellsImages, FigureBoard
from .Recognizer import Recognizer


class RecognizerONNX(Recognizer):
    model_figure: onnxruntime.InferenceSession
    model_direction: onnxruntime.InferenceSession
    cell_img_size: int

    def __init__(self, model_figure_path: str, model_direction_path: str, cell_img_size: int):
        self.model_figure = onnxruntime.InferenceSession(model_figure_path)
        self.model_direction = onnxruntime.InferenceSession(model_direction_path)
        self.cell_img_size = cell_img_size

    def recognize_figure(self, cell_img: np.ndarray) -> Figure:
        raise Exception("Not implemented")

    def recognize_board_figures(self, cells_imgs: CellsImages) -> FigureBoard:
        inp = preprocessing.prepare_cells_imgs(cells_imgs)
        predictions = self.model_figure.run(None, {"input_1": inp})[0]
        labels = predictions.argmax(axis=1)
        labels = np.reshape(labels, (9, 9))
        result = [[Figure.EMPTY for _ in range(9)] for __ in range(9)]
        for i in range(9):
            for j in range(9):
                index = labels[i][j]
                figure = CATEGORIES_FIGURE_TYPE[index]
                result[i][j] = figure
        return result

    def recognize_board_directions(self, cells_imgs: list[list[np.ndarray]]) -> list[list[Direction]]:
        inp = preprocessing.prepare_cells_imgs(cells_imgs)
        predictions = self.model_direction.run(None, {"input_2": inp})[0]
        labels = predictions.argmax(axis=1)
        labels = np.reshape(labels, (9, 9))
        result = [[Direction.NONE for _ in range(9)] for __ in range(9)]
        for i in range(9):
            for j in range(9):
                index = labels[i][j]
                direction = CATEGORIES_DIRECTION[index]
                result[i][j] = direction
        return result

