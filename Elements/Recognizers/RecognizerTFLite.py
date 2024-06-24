import numpy as np
from ShogiNeuralNetwork import preprocessing
from ShogiNeuralNetwork.data_info import CATEGORIES_FIGURE_TYPE, CATEGORIES_DIRECTION
from extra.figures import Figure, Direction
from extra.image_modes import ImageMode
from extra.types import CellsImages, FigureBoard, DirectionBoard, ImageNP
from .Recognizer import Recognizer
import tensorflow as tf
# import tflite_runtime.interpreter as tflite


class RecognizerTFLite(Recognizer):
    model: tf.lite.Interpreter
    cell_img_size: int
    image_mode: ImageMode

    def __init__(self, model_path: str):
        self.model = tf.lite.Interpreter(model_path=model_path)
        # self.model = tflite.Interpreter(model_path=model_path)
        self.model.allocate_tensors()

        self.input_details = self.model.get_input_details()
        self.output_details = self.model.get_output_details()

        self.cell_img_size = self.input_details[0]["shape"][1]
        self.image_mode = ImageMode.ADAPTIVE_THRESHOLD  # TODO: read from model's metadata

    def recognize_cell(self, cell_img: ImageNP) -> tuple[Figure, Direction]:
        inp = preprocessing.prepare_cell_img(
            cell_img,
            self.image_mode,
            self.cell_img_size
        )
        self.model.set_tensor(self.input_details[0]['index'], inp)
        self.model.invoke()
        figure_predictions = self.model.get_tensor(self.output_details[0]['index'])[0]
        direction_predictions = self.model.get_tensor(self.output_details[1]['index'])[0]
        figure_label = figure_predictions.argmax()
        direction_label = direction_predictions.argmax()
        figure = CATEGORIES_FIGURE_TYPE[figure_label]
        direction = CATEGORIES_DIRECTION[direction_label]
        return figure, direction

    def recognize_board(self, cells_imgs: CellsImages) -> tuple[FigureBoard, DirectionBoard, float]:
        inp = preprocessing.prepare_cells_imgs(
            cells_imgs,
            self.image_mode,
            self.cell_img_size,
        )
        self.model.resize_tensor_input(self.input_details[0]['index'], [81, self.cell_img_size, self.cell_img_size, 1])
        self.model.allocate_tensors()

        self.model.set_tensor(self.input_details[0]['index'], inp)
        self.model.invoke()
        figure_predictions = self.model.get_tensor(self.output_details[0]['index'])
        direction_predictions = self.model.get_tensor(self.output_details[1]['index'])

        figure_predict = figure_predictions.argmax(axis=1)
        direction_predict = direction_predictions.argmax(axis=1)

        figure_score = figure_predictions.max(axis=1).mean()
        direction_score = direction_predictions.max(axis=1).mean()
        score = (figure_score + direction_score) / 2

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
        return figures, directions, score
