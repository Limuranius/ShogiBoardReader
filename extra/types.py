import numpy as np
from .figures import Figure, Direction

Image = np.ndarray
FigureBoard = list[list[Figure]]
DirectionBoard = list[list[Direction]]
Corners = tuple[tuple[int, int], tuple[int, int], tuple[int, int], tuple[int, int]]
