import cv2
import numpy as np
from extra.figures import Figure, Direction, FIGURE_ICONS_PATHS
from .FigureRecognizers import Recognizer
from .BoardAnalyzer import BoardAnalyzer
from .BoardSplitter import BoardSplitter
from extra import utils
from extra.image_modes import ImageMode
from extra.types import Image


class ShogiBoardReader:
    board_splitter: BoardSplitter
    recognizer: Recognizer
    analyzer: BoardAnalyzer

    def __init__(self, board_splitter: BoardSplitter, recognizer: Recognizer, analyzer: BoardAnalyzer = None):
        self.board_splitter = board_splitter
        self.recognizer = recognizer
        self.analyzer = analyzer

    def recognize_board_figures(self) -> list[list[Figure]]:
        cells = self.board_splitter.get_board_cells(ImageMode.CANNY)
        return self.recognizer.recognize_board_figures(cells)

    def recognize_board_directions(self) -> list[list[Direction]]:
        cells = self.board_splitter.get_board_cells(ImageMode.CANNY)
        return self.recognizer.recognize_board_directions(cells)

    def get_str_board(self):
        board = self.recognize_board_figures()
        s = ""
        for i in range(9):
            for j in range(9):
                figure = board[i][j]
                s += figure.value
            s += "\n"
        return s

    def show_board(self):
        img = self.board_splitter.get_board_image_no_perspective()
        cv2.imshow("board", img)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

    def show_cell(self, i, j):
        cells = self.board_splitter.get_board_cells(ImageMode.ORIGINAL)
        cv2.imshow("cell", cells[i][j])
        cv2.waitKey(0)

    def get_full_img(self, show_borders: bool) -> Image:
        return self.board_splitter.get_full_img(show_borders)

    def get_board_image_no_perspective(self) -> Image:
        return self.board_splitter.get_board_image_no_perspective()

    def get_digital_board(self) -> Image:
        figures = self.recognize_board_figures()
        directions = self.recognize_board_directions()

        if self.analyzer is not None:
            self.analyzer.update(figures)
            figures = self.analyzer.get_board()

        BOARD_SIZE = 1000
        FIGURE_SIZE = BOARD_SIZE // 9
        board = np.full((BOARD_SIZE, BOARD_SIZE, 3), [255, 255, 255], dtype=np.uint8)

        # Рисуем сетку
        grid_step = BOARD_SIZE // 9
        for i in range(10):
            y = i * grid_step
            cv2.line(board, (0, y), (BOARD_SIZE, y), 0, thickness=5)
        for j in range(10):
            x = j * grid_step
            cv2.line(board, (x, 0), (x, BOARD_SIZE), 0, thickness=5)

        # Добавляем фигуры
        figure_step = BOARD_SIZE // 9
        for i in range(9):
            for j in range(9):
                y = figure_step * i
                x = figure_step * j
                figure = figures[i][j]
                direction = directions[i][j]
                if figure != Figure.EMPTY:
                    figure_img = cv2.imread(FIGURE_ICONS_PATHS[figure])
                    figure_img = cv2.resize(figure_img, (FIGURE_SIZE, FIGURE_SIZE))
                    if direction == Direction.DOWN:
                        figure_img = np.flip(figure_img, axis=0)
                    utils.overlay_image_on_image(board, figure_img, x, y)
        return board
