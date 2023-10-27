from enum import Enum
from config import Paths
import os


class Figure(Enum):
    PAWN = "P"
    KING = "K"
    LANCE = "L"
    KNIGHT = "N"
    SILVER = "S"
    GOLD = "G"
    BISHOP = "B"
    ROOK = "R"
    EMPTY = "."


class Direction(Enum):
    UP = "U"
    DOWN = "D"
    NONE = "."


FIGURE_FOLDERS = {
    Figure.PAWN: os.path.join(Paths.IMGS_EXAMPLE_DIR, "pawn"),
    Figure.BISHOP: os.path.join(Paths.IMGS_EXAMPLE_DIR, "bishop"),
    Figure.ROOK: os.path.join(Paths.IMGS_EXAMPLE_DIR, "rook"),
    Figure.LANCE: os.path.join(Paths.IMGS_EXAMPLE_DIR, "lance"),
    Figure.KNIGHT: os.path.join(Paths.IMGS_EXAMPLE_DIR, "knight"),
    Figure.SILVER: os.path.join(Paths.IMGS_EXAMPLE_DIR, "silver"),
    Figure.GOLD: os.path.join(Paths.IMGS_EXAMPLE_DIR, "gold"),
    Figure.KING: os.path.join(Paths.IMGS_EXAMPLE_DIR, "king"),
    Figure.EMPTY: os.path.join(Paths.IMGS_EXAMPLE_DIR, "empty"),
}

FIGURE_ICONS_PATHS = {
    Figure.PAWN: os.path.join(Paths.FIGURE_ICONS_DIR, "pawn.png"),
    Figure.BISHOP: os.path.join(Paths.FIGURE_ICONS_DIR, "bishop.png"),
    Figure.ROOK: os.path.join(Paths.FIGURE_ICONS_DIR, "rook.png"),
    Figure.LANCE: os.path.join(Paths.FIGURE_ICONS_DIR, "lance.png"),
    Figure.KNIGHT: os.path.join(Paths.FIGURE_ICONS_DIR, "knight.png"),
    Figure.SILVER: os.path.join(Paths.FIGURE_ICONS_DIR, "silver.png"),
    Figure.GOLD: os.path.join(Paths.FIGURE_ICONS_DIR, "gold.png"),
    Figure.KING: os.path.join(Paths.FIGURE_ICONS_DIR, "king.png"),
    Figure.EMPTY: os.path.join(Paths.FIGURE_ICONS_DIR, "empty.png"),
}

Paths.create_folders(list(FIGURE_FOLDERS.values()))
