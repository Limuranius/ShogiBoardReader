from collections import defaultdict
from .FigureRecognizers import Recognizer
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

    def __recognize_board_figures(self) -> FigureBoard:
        cells = self.board_splitter.get_board_cells(self.image_mode)
        predicted_figures = self.recognizer.recognize_board_figures(cells)
        return predicted_figures

    def __recognize_board_directions(self) -> DirectionBoard:
        cells = self.board_splitter.get_board_cells(self.image_mode)
        predicted_directions = self.recognizer.recognize_board_directions(cells)
        return predicted_directions

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

        self.__figures = self.__recognize_board_figures()
        self.__directions = self.__recognize_board_directions()

        if self.memorizer is not None:
            self.memorizer.update(self.__figures, self.__directions)

    def get_last_update_status(self) -> BoardChangeStatus:
        if self.memorizer is not None:
            return self.memorizer.update_status
        else:
            return BoardChangeStatus.VALID_MOVE

    def get_board(self) -> Board:
        if self.memorizer is None:
            if self.board_splitter.inventory_detector is None:
                return Board(self.__figures, self.__directions)
            else:
                inventory_black, inventory_white = self.get_inventories()
                return Board(self.__figures, self.__directions, inventory_black, inventory_white)
        else:
            return self.memorizer.get_board()

    def set(self,
            image_getter: ImageGetter = None,
            corner_detector: CornerDetector = None,
            board_splitter: BoardSplitter = None,
            recognizer: Recognizer = None,
            memorizer: BoardMemorizer = False,
            inventory_detector: InventoryDetector = None,
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
        if inventory_detector:
            self.board_splitter.inventory_detector = inventory_detector

    def set_image(self, img_path: str) -> None:
        if isinstance(self.board_splitter.image_getter, Photo):
            self.board_splitter.image_getter.set_image(img_path)
        else:
            raise Exception("Can't set image on image getter other than Photo")

    def get_cells_imgs(self, img_mode: ImageMode) -> list[list[ImageNP]]:
        return self.board_splitter.get_board_cells(img_mode)

    def get_inventories(self) -> tuple[Inventory, Inventory]:
        i1_imgs, i2_imgs = self.board_splitter.get_inventory_cells(self.image_mode)
        i1 = defaultdict(int)
        i2 = defaultdict(int)
        for img in i1_imgs:
            figure = self.recognizer.recognize_figure(img)
            i1[figure] += 1
        for img in i2_imgs:
            figure = self.recognizer.recognize_figure(img)
            i2[figure] += 1
        return i1, i2
