from ultralytics import YOLO

from ShogiNeuralNetwork.preprocessing import flatten
from extra.figures import Figure, Direction
from extra.types import CellsImages, FigureBoard, DirectionBoard, ImageNP
from .Recognizer import Recognizer


class RecognizerYOLO(Recognizer):
    model_figure: YOLO  # figure type classification model
    model_direction: YOLO  # direction classification model

    def __init__(
            self,
            figure_model_path: str,
            direction_model_path: str,
    ):
        self.model_figure = YOLO(figure_model_path, task="classify")
        self.model_direction = YOLO(direction_model_path, task="classify")

    def recognize_cell(self, cell_img: ImageNP) -> tuple[Figure, Direction]:
        result_figure = self.model_figure(cell_img, verbose=False)[0]
        result_direction = self.model_direction(cell_img, verbose=False)[0]
        figure_names = result_figure.names
        direction_names = result_direction.names
        return (
            Figure[figure_names[result_figure.probs.top1]],
            Direction[direction_names[result_direction.probs.top1]]
        )

    def recognize_board(self, cells_imgs: CellsImages) -> tuple[FigureBoard, DirectionBoard, float]:
        batch = flatten(cells_imgs)
        result_figure = self.model_figure(batch, verbose=False)
        result_direction = self.model_direction(batch, verbose=False)
        figure_names = result_figure[0].names
        direction_names = result_direction[0].names

        figures = [[Figure.EMPTY for _ in range(9)] for __ in range(9)]
        directions = [[Direction.NONE for _ in range(9)] for __ in range(9)]
        score = 0
        for i in range(81):
            y = i // 9
            x = i % 9
            fig_preds = result_figure[i].probs
            dir_preds = result_direction[i].probs
            figures[y][x] = Figure[figure_names[fig_preds.top1]]
            directions[y][x] = Direction[direction_names[dir_preds.top1]]
            score += (fig_preds.top1conf + dir_preds.top1conf) / 2

        return figures, directions, float(score)
