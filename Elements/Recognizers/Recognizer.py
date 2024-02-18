from abc import ABC, abstractmethod
import numpy as np
from extra.figures import Figure, Direction


class Recognizer(ABC):
    @abstractmethod
    def recognize_figure(self, cell_img: np.ndarray) -> Figure:
        pass

    @abstractmethod
    def recognize_board_figures(self, cells_imgs: list[list[np.ndarray]]) -> list[list[Figure]]:
        pass

    @abstractmethod
    def recognize_board_directions(self, cells_imgs: list[list[np.ndarray]]) -> list[list[Direction]]:
        pass