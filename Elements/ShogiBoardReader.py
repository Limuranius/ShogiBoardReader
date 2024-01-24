import cv2
from .FigureRecognizers import Recognizer
from .BoardMemorizer import BoardMemorizer
from .BoardMemorizer.BoardChangeStatus import BoardChangeStatus
from .BoardSplitter import BoardSplitter
from .ImageGetters import ImageGetter, Photo
from .CornerDetectors import CornerDetector
from extra.image_modes import ImageMode
from extra.types import ImageNP, FigureBoard, DirectionBoard
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

    def recognize_board_figures(self) -> FigureBoard:
        cells = self.board_splitter.get_board_cells(self.image_mode)
        predicted_figures = self.recognizer.recognize_board_figures(cells)
        return predicted_figures

    def recognize_board_directions(self) -> DirectionBoard:
        cells = self.board_splitter.get_board_cells(self.image_mode)
        predicted_directions = self.recognizer.recognize_board_directions(cells)
        return predicted_directions

    def get_full_img(self, show_borders: bool, show_grid: bool) -> ImageNP:
        return self.board_splitter.get_full_img(show_borders, show_grid)

    def get_board_image_no_perspective(self,
                                       img_mode: ImageMode = ImageMode.ORIGINAL,
                                       show_grid: bool = False) -> ImageNP:
        return self.board_splitter.get_board_image_no_perspective(img_mode, show_grid)

    def update(self) -> None:
        self.__figures = self.recognize_board_figures()
        self.__directions = self.recognize_board_directions()

        if self.memorizer is not None:
            self.memorizer.update(self.__figures, self.__directions)

    def get_last_update_status(self) -> BoardChangeStatus:
        if self.memorizer is not None:
            return self.memorizer.update_status
        else:
            return BoardChangeStatus.VALID_MOVE

    def get_board(self) -> Board:
        if self.memorizer is None:
            return Board(self.__figures, self.__directions)
        else:
            return self.memorizer.get_board()

    def set(self,
            image_getter: ImageGetter = None,
            corner_detector: CornerDetector = None,
            board_splitter: BoardSplitter = None,
            recognizer: Recognizer = None,
            memorizer: BoardMemorizer = False
            ):
        if image_getter:
            self.board_splitter.image_getter = image_getter
        if corner_detector:
            self.board_splitter.corner_detector = corner_detector
        if board_splitter:
            self.board_splitter = board_splitter
        if recognizer:
            self.recognizer = recognizer
        if memorizer != False:
            self.memorizer = memorizer

    def set_image(self, img_path: str) -> None:
        if isinstance(self.board_splitter.image_getter, Photo):
            self.board_splitter.image_getter.set_image(img_path)
        else:
            raise Exception("Can't set image on image getter other than Photo")