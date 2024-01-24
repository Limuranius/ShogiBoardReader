from abc import ABC, abstractmethod
from extra.types import Corners, ImageNP


class CornerDetector(ABC):
    @abstractmethod
    def get_corners(self, image: ImageNP) -> Corners:
        pass
