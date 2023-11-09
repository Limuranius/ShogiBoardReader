from enum import Enum
from dataclasses import dataclass
from extra.types import Figure
from typing import Callable

jp_digits = {
    1: "一",
    2: "二",
    3: "三",
    4: "四",
    5: "五",
    6: "六",
    7: "七",
    8: "八",
    9: "九",
}


class MoveType(Enum):
    MOVE = "MOVE"
    DROP = "DROP"
    MOVE_AND_PROMOTE = "MOVE_AND_PROMOTE"


@dataclass(frozen=True)
class Move:
    move_type: MoveType
    figure: Figure
    destination: tuple[int, int]  # (x, y), 1 <= x, y <= 9
    origin: tuple[int, int] | None = None  # (x, y), 1 <= x, y <= 9

    def __post_init__(self):
        if self.origin is None and self.move_type != MoveType.DROP:
            raise Exception("Invalid move")

    def get_signature(self, notation_transform_func: Callable[[int, int], tuple[int, int]]) -> str:
        """
        Return signature of move

        notation_transform_func:
            Function that converts coordinates in screen coordinates system
            to coordinates in notation coordinates system
        """
        x_dest_notation, y_dest_notation = notation_transform_func(
            self.destination[0],
            self.destination[1],
        )

        dest_coords_str = "{x}{y_jp}".format(
            x=x_dest_notation,
            y_jp=jp_digits[y_dest_notation]
        )
        match self.move_type:
            case MoveType.DROP:
                s = "{dest}{fig_jp}打".format(
                    dest=dest_coords_str,
                    fig_jp=self.figure.to_jp()
                )
                return s
            case MoveType.MOVE | MoveType.MOVE_AND_PROMOTE:
                x_orig_notation, y_orig_notation = notation_transform_func(
                    self.origin[0],
                    self.origin[1],
                )
                origin_coords_str = "{x}{y}".format(
                    x=x_orig_notation,
                    y=y_orig_notation
                )
                prom_str = "成" if self.move_type == MoveType.MOVE_AND_PROMOTE else ""
                s = "{dest}{fig_jp}{prom}({origin})".format(
                    dest=dest_coords_str,
                    fig_jp=self.figure.to_jp(),
                    prom=prom_str,
                    origin=origin_coords_str
                )
                return s
