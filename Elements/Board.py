import numpy as np

from extra.figures import Figure, Direction, FIGURE_ICONS_PATHS
from extra.types import FigureBoard, DirectionBoard, ImageNP
from dataclasses import dataclass
from extra import utils
import cv2


@dataclass(frozen=True)
class Board:
    figures: FigureBoard
    directions: DirectionBoard

    def to_str_figures(self):
        return utils.board_to_str(self.figures)

    def to_str_directions(self):
        return utils.board_to_str(self.directions)

    def to_str(self):
        s = "Figures:     Directions:"
        for fig_row, dir_row in zip(self.figures, self.directions):
            s += "".join([cell.value for cell in fig_row])
            s += "    "
            s += "".join([cell.value for cell in dir_row])
            s += "\n"

    def to_image(self) -> ImageNP:
        BOARD_SIZE = 1000
        FIGURE_SIZE = BOARD_SIZE // 9
        board = np.full((BOARD_SIZE, BOARD_SIZE, 3), [255, 255, 255], dtype=np.uint8)

        grid_step = BOARD_SIZE // 9
        for i in range(10):
            y = i * grid_step
            cv2.line(board, (0, y), (BOARD_SIZE, y), 0, thickness=5)
        for j in range(10):
            x = j * grid_step
            cv2.line(board, (x, 0), (x, BOARD_SIZE), 0, thickness=5)

        figure_step = BOARD_SIZE // 9
        for i in range(9):
            for j in range(9):
                y = figure_step * i
                x = figure_step * j
                figure = self.figures[i][j]
                direction = self.directions[i][j]
                if figure != Figure.EMPTY:
                    figure_img = cv2.imread(FIGURE_ICONS_PATHS[figure])
                    figure_img = cv2.resize(figure_img, (FIGURE_SIZE, FIGURE_SIZE))
                    if direction == Direction.DOWN:
                        figure_img = np.flip(figure_img, axis=0)
                    utils.overlay_image_on_image(board, figure_img, x, y)
        return board
