from enum import Enum
from dataclasses import dataclass
from extra.types import Figure

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

    def get_signature(self) -> str:
        dest_coords_str = "{x}{y_jp}".format(
            x=self.destination[0],
            y_jp=jp_digits[self.destination[1]]
        )
        match self.move_type:
            case MoveType.DROP:
                s = "{dest}{fig_jp}打".format(
                    dest=dest_coords_str,
                    fig_jp=self.figure.to_jp()
                )
                return s
            case MoveType.MOVE | MoveType.MOVE_AND_PROMOTE:
                origin_coords_str = "{x}{y}".format(
                    x=self.origin[0],
                    y=self.origin[1]
                )
                prom_str = "成" if self.move_type == MoveType.MOVE_AND_PROMOTE else ""
                s = "{dest}{fig_jp}{prom}({origin})".format(
                    dest=dest_coords_str,
                    fig_jp=self.figure.to_jp(),
                    prom=prom_str,
                    origin=origin_coords_str
                )
                return s
