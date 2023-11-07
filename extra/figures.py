from __future__ import annotations
from enum import Enum
from config import Paths
import os


class Figure(Enum):
    PAWN = "p"
    KING = "K"
    LANCE = "l"
    KNIGHT = "n"
    SILVER = "s"
    GOLD = "G"
    BISHOP = "b"
    ROOK = "r"
    EMPTY = "."

    PAWN_PROM = "P"
    LANCE_PROM = "L"
    KNIGHT_PROM = "N"
    SILVER_PROM = "S"
    BISHOP_PROM = "B"
    ROOK_PROM = "R"

    def to_jp(self) -> str:
        translate_table = {
            self.PAWN: "歩",
            self.KING: "玉",
            self.LANCE: "香",
            self.KNIGHT: "桂",
            self.SILVER: "銀",
            self.GOLD: "金",
            self.BISHOP: "角",
            self.ROOK: "飛",

            self.PAWN_PROM: "と",
            self.LANCE_PROM: "成香",
            self.KNIGHT_PROM: "成桂",
            self.SILVER_PROM: "成銀",
            self.BISHOP_PROM: "馬",
            self.ROOK_PROM: "龍",
        }
        return translate_table[self]

    def promoted(self) -> Figure:
        promotion_table = {
            self.PAWN: self.PAWN_PROM,
            self.LANCE: self.LANCE_PROM,
            self.KNIGHT: self.KNIGHT_PROM,
            self.SILVER: self.SILVER_PROM,
            self.BISHOP: self.BISHOP_PROM,
            self.ROOK: self.ROOK_PROM,
        }
        return promotion_table[self]

    def unpromoted(self) -> Figure:
        promotion_table = {
            self.PAWN_PROM: self.PAWN,
            self.LANCE_PROM: self.LANCE,
            self.KNIGHT_PROM: self.KNIGHT,
            self.SILVER_PROM: self.SILVER,
            self.BISHOP_PROM: self.BISHOP,
            self.ROOK_PROM: self.ROOK,
        }
        return promotion_table[self]


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
