from abc import ABC, abstractmethod
from extra.types import Corners, Image


class CornerDetector(ABC):
    @abstractmethod
    def get_corners(self, image: Image) -> Corners:
        """Возвращает координаты углов доски в следующем порядке:
        левый-верхний, правый-верхний, правый-нижний, левый-нижний"""
        pass
