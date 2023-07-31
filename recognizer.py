import numpy as np
from figures import Figure, Direction
from abc import ABC, abstractmethod
import tensorflow as tf
from NN_data.data_info import CATEGORIES_FIGURE_TYPE, CATEGORIES_DIRECTION
import cv2
from config import config


class Recognizer(ABC):
    @abstractmethod
    def recognize_cell_figure(self, cell_img: np.ndarray) -> Figure:
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

    def __init__(self, model_figure_path: str, model_direction_path: str):
        self.model_figure = tf.keras.models.load_model(model_figure_path)
        self.model_direction = tf.keras.models.load_model(model_direction_path)

    def recognize_cell_figure(self, cell_img: np.ndarray) -> Figure:
        CELL_IMG_SIZE = config.NN_data.cell_img_size
        cell_img = cell_img.astype("float32") / 255
        cell_img = cv2.resize(cell_img, (CELL_IMG_SIZE, CELL_IMG_SIZE))
        inp = np.reshape(cell_img, (1, CELL_IMG_SIZE, CELL_IMG_SIZE, 1))
        predictions = self.model_figure.predict(inp, verbose=0)
        index = np.argmax(predictions)
        return CATEGORIES_FIGURE_TYPE[index]

    def recognize_board_figures(self, cells_imgs: list[list[np.ndarray]]) -> list[list[Figure]]:
        CELL_IMG_SIZE = config.NN_data.cell_img_size
        cells_imgs = np.array(cells_imgs).astype("float32") / 255
        inp = np.reshape(cells_imgs, (81, CELL_IMG_SIZE, CELL_IMG_SIZE, 1))
        predictions = self.model_figure.predict(inp, verbose=0)
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
        CELL_IMG_SIZE = config.NN_data.cell_img_size
        cells_imgs = np.array(cells_imgs).astype("float32") / 255
        inp = np.reshape(cells_imgs, (81, CELL_IMG_SIZE, CELL_IMG_SIZE, 1))
        predictions = self.model_direction.predict(inp, verbose=0)
        labels = predictions.argmax(axis=1)
        labels = np.reshape(labels, (9, 9))
        result = [[Direction.NONE for _ in range(9)] for __ in range(9)]
        for i in range(9):
            for j in range(9):
                index = labels[i][j]
                direction = CATEGORIES_DIRECTION[index]
                result[i][j] = direction
        return result