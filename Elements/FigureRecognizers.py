import numpy as np
from extra.figures import Figure, Direction
from abc import ABC, abstractmethod
import tensorflow as tf
from ShogiNeuralNetwork.data_info import CATEGORIES_FIGURE_TYPE, CATEGORIES_DIRECTION
import cv2
from ShogiNeuralNetwork import preprocessing
from extra.types import ImageNP, CellsImages, FigureBoard


class Recognizer(ABC):
    @abstractmethod
    def recognize_figure(self, cell_img: np.ndarray) -> Figure:
        pass

    @abstractmethod
    def recognize_board_figures(self, cells_imgs: list[list[np.ndarray]]) -> list[list[Figure]]:
        pass

    @abstractmethod
    def recognize_board_directions(self, cells_imgs: list[list[np.ndarray]]) -> list[list[Direction]]:
        pass


class RecognizerNN(Recognizer):
    model_figure: tf.keras.models.Model
    model_direction: tf.keras.models.Model
    cell_img_size: int

    def __init__(self, model_figure_path: str, model_direction_path: str, cell_img_size: int):
        self.model_figure = tf.keras.models.load_model(model_figure_path)
        self.model_direction = tf.keras.models.load_model(model_direction_path)
        self.cell_img_size = cell_img_size

    def recognize_figure(self, cell_img: np.ndarray) -> Figure:
        cell_img = cell_img.astype("float32") / 255
        cell_img = cv2.resize(cell_img, (self.cell_img_size, self.cell_img_size))
        inp = np.reshape(cell_img, (1, self.cell_img_size, self.cell_img_size, 1))

        # Figure
        predictions = self.model_figure.predict(inp, verbose=0)
        index = np.argmax(predictions)
        figure = CATEGORIES_FIGURE_TYPE[index]

        # # Direction
        # predictions = self.model_direction.predict(inp, verbose=0)
        # index = np.argmax(predictions)
        # direction = CATEGORIES_DIRECTION[index]

        return figure

    def recognize_board_figures(self, cells_imgs: CellsImages) -> FigureBoard:
        inp = preprocessing.prepare_cells_imgs(cells_imgs)
        predictions = self.model_figure(inp).numpy()
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
        predictions = self.model_direction(inp).numpy()
        labels = predictions.argmax(axis=1)
        labels = np.reshape(labels, (9, 9))
        result = [[Direction.NONE for _ in range(9)] for __ in range(9)]
        for i in range(9):
            for j in range(9):
                index = labels[i][j]
                direction = CATEGORIES_DIRECTION[index]
                result[i][j] = direction
        return result
