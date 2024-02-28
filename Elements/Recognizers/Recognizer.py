from abc import ABC, abstractmethod
from extra.figures import Figure, Direction
from extra.types import DirectionBoard, FigureBoard, CellsImages, ImageNP


class Recognizer(ABC):
    @abstractmethod
    def recognize_cell(self, cell_img: ImageNP) -> tuple[Figure, Direction]:
        pass

    @abstractmethod
    def recognize_board(self, cells_imgs: CellsImages) -> tuple[FigureBoard, DirectionBoard]:
        pass
