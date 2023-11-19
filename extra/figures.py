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
        return promotion_table[self]

    def unpromoted(self) -> Figure:
        return promotion_table[self]

    def is_promotable(self) -> bool:
        return self in promotion_table


promotion_table = {
    Figure.PAWN: Figure.PAWN_PROM,
    Figure.LANCE: Figure.LANCE_PROM,
    Figure.KNIGHT: Figure.KNIGHT_PROM,
    Figure.SILVER: Figure.SILVER_PROM,
    Figure.BISHOP: Figure.BISHOP_PROM,
    Figure.ROOK: Figure.ROOK_PROM,
}


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

    Figure.PAWN_PROM: os.path.join(Paths.FIGURE_ICONS_DIR, "promoted pawn.png"),
    Figure.BISHOP_PROM: os.path.join(Paths.FIGURE_ICONS_DIR, "promoted bishop.png"),
    Figure.ROOK_PROM: os.path.join(Paths.FIGURE_ICONS_DIR, "promoted rook.png"),
    Figure.LANCE_PROM: os.path.join(Paths.FIGURE_ICONS_DIR, "promoted lance.png"),
    Figure.KNIGHT_PROM: os.path.join(Paths.FIGURE_ICONS_DIR, "promoted knight.png"),
    Figure.SILVER_PROM: os.path.join(Paths.FIGURE_ICONS_DIR, "promoted silver.png"),
}

Paths.create_folders(list(FIGURE_FOLDERS.values()))
