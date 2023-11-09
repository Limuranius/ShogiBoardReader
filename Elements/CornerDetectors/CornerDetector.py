from abc import ABC, abstractmethod
from extra.types import Corners, Image


class CornerDetector(ABC):
    @abstractmethod
    def get_corners(self, image: Image) -> Corners:
        pass
