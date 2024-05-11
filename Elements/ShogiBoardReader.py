import copy
from collections import defaultdict
from Elements.Recognizers import Recognizer
from extra.figures import Figure
from .BoardMemorizer import BoardMemorizer
from .BoardMemorizer.BoardChangeStatus import BoardChangeStatus
from .BoardSplitter import BoardSplitter
from .ImageGetters import ImageGetter, Photo
from .CornerDetectors import CornerDetector
from extra.image_modes import ImageMode
from extra.types import ImageNP, FigureBoard, DirectionBoard, Inventory
from .Board import Board
from .InventoryDetectors import InventoryDetector


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

        empty_board = Board.get_empty_board()
        self.__figures = empty_board.figures
        self.__directions = empty_board.directions

    def get_full_img(
            self,
            show_borders: bool = False,
            show_grid: bool = False,
            show_inventories: bool = False,
    ) -> ImageNP:
        """
        Returns original image of board
        Can also draw borders of board and grid
        """
        return self.board_splitter.get_full_img(show_borders, show_grid, show_inventories)

    def get_board_image_no_perspective(self,
                                       img_mode: ImageMode = ImageMode.ORIGINAL,
                                       show_grid: bool = False) -> ImageNP:
        """Returns image of board without perspective and surroundings"""
        return self.board_splitter.get_board_image_no_perspective(img_mode, show_grid)

    def update(self) -> None:
        """
        Runs recognizer and memorizer to update state of board
        """
        cells = self.board_splitter.get_board_cells(self.image_mode)
        figures, directions, score = self.recognizer.recognize_board(cells)

        self.__figures = figures
        self.__directions = directions

        if self.memorizer is not None:
            self.memorizer.update(self.__figures, self.__directions, score)

    def get_last_update_status(self) -> BoardChangeStatus:
        if self.memorizer is not None:
            return self.memorizer.update_status
        else:
            return BoardChangeStatus.VALID_MOVE

    def get_board(self) -> Board:
        if self.memorizer is None:
            if self.board_splitter.get_inventory_detector() is None:
                return Board(self.__figures, self.__directions)
            else:
                inventory_black, inventory_white = self.get_inventories()
                return Board(self.__figures, self.__directions, inventory_black, inventory_white)
        else:
            return self.memorizer.get_board()

    def set_board_splitter(self, splitter: BoardSplitter) -> None:
        self.board_splitter = splitter

    def set_recognizer(self, recognizer: Recognizer) -> None:
        self.recognizer = recognizer

    def set_memorizer(self, memorizer: BoardMemorizer) -> None:
        self.memorizer = memorizer

    def get_board_splitter(self) -> BoardSplitter:
        return self.board_splitter

    def get_recognizer(self) -> Recognizer:
        return self.recognizer

    def get_memorizer(self) -> BoardMemorizer:
        return self.memorizer

    def get_cells_imgs(self, img_mode: ImageMode) -> list[list[ImageNP]]:
        return self.board_splitter.get_board_cells(img_mode)

    def get_inventories(self) -> tuple[Inventory, Inventory]:
        i1_imgs, i2_imgs = self.board_splitter.get_inventory_cells(self.image_mode)
        i1 = defaultdict(int)
        i2 = defaultdict(int)
        for img in i1_imgs:
            figure, direction = self.recognizer.recognize_cell(img)
            if figure != Figure.EMPTY:
                i1[figure] += 1
        for img in i2_imgs:
            figure, direction = self.recognizer.recognize_cell(img)
            if figure != Figure.EMPTY:
                i2[figure] += 1
        return i1, i2

    def get_kif(self) -> str:
        if self.memorizer is None:
            return ""
        else:
            return self.memorizer.get_kif()

    def __copy__(self):
        return ShogiBoardReader(
            image_mode=self.image_mode,
            board_splitter=copy.copy(self.board_splitter),
            recognizer=copy.copy(self.recognizer),
            memorizer=copy.copy(self.memorizer)
        )
