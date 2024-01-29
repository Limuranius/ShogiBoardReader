import numpy as np
from .figures import Figure, Direction

ImageNP = np.ndarray
CellsImages = list[list[ImageNP]]
FigureBoard = list[list[Figure]]
DirectionBoard = list[list[Direction]]
Corners = tuple[tuple[int, int], tuple[int, int], tuple[int, int], tuple[int, int]]
Inventory = dict[Figure, int]
