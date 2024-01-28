from abc import ABC, abstractmethod
from extra.types import Corners, ImageNP


class InventoryDetector(ABC):
    @abstractmethod
    def get_figure_images(self, image: ImageNP) -> tuple[list[ImageNP], list[ImageNP]]:
        pass

    @abstractmethod
    def get_inventories_corners(self, image: ImageNP) -> tuple[Corners, Corners]:
        pass