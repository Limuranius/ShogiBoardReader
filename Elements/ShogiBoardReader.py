import cv2
from .FigureRecognizers import Recognizer
from .BoardMemorizer import BoardMemorizer
from .BoardSplitter import BoardSplitter
from extra.image_modes import ImageMode
from extra.types import Image, FigureBoard, DirectionBoard
from .Board import Board


class ShogiBoardReader:
    image_mode: ImageMode
    board_splitter: BoardSplitter
    recognizer: Recognizer
    memorizer: BoardMemorizer

    __figures: FigureBoard
    __directions: DirectionBoard

    def __init__(
            self,
            image_mode: ImageMode,
            board_splitter: BoardSplitter,
            recognizer: Recognizer,
            memorizer: BoardMemorizer = None):
        self.image_mode = image_mode
        self.board_splitter = board_splitter
        self.recognizer = recognizer
        self.memorizer = memorizer
        self.update()

    def recognize_board_figures(self) -> FigureBoard:
        cells = self.board_splitter.get_board_cells(self.image_mode)
        predicted_figures = self.recognizer.recognize_board_figures(cells)
        return predicted_figures

    def recognize_board_directions(self) -> DirectionBoard:
        cells = self.board_splitter.get_board_cells(self.image_mode)
        predicted_directions = self.recognizer.recognize_board_directions(cells)
        return predicted_directions

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

    def get_board_image_no_perspective(self, img_mode: ImageMode = ImageMode.ORIGINAL) -> Image:
        return self.board_splitter.get_board_image_no_perspective(img_mode)

    def update(self):
        self.__figures = self.recognize_board_figures()
        self.__directions = self.recognize_board_directions()

        if self.memorizer is not None:
            self.memorizer.update(self.__figures)

    def get_board(self) -> Board:
        return Board(self.__figures, self.__directions)
