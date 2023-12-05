from __future__ import annotations
from dataclasses import dataclass
from extra.types import Figure

JP_DIGITS = {
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

USI_LETTERS = "abcdefghi"


def notation_transform_lower_first(x: int, y: int):
    return 10 - x, y


def notation_transform_upper_first(x: int, y: int):
    return x, 10 - y


@dataclass(frozen=True)
class Move:
    # (x, y), 1 <= x, y <= 9
    destination: tuple[int, int]
    figure: Figure

    # (x, y), 1 <= x, y <= 9
    origin: tuple[int, int] = None

    is_drop: bool = False

    is_promotion: bool = False

    def apply_side_transformation(self, lower_moves_first: bool) -> Move:
        origin = None
        if lower_moves_first:
            if self.origin is not None:
                origin = notation_transform_lower_first(*self.origin)
            destination = notation_transform_lower_first(*self.destination)
        else:
            if self.origin is not None:
                origin = notation_transform_upper_first(*self.origin)
            destination = notation_transform_upper_first(*self.destination)
        return Move(
            origin=origin,
            destination=destination,
            figure=self.figure,
            is_drop=self.is_drop,
            is_promotion=self.is_promotion
        )

    def to_usi(self) -> str:
        if self.is_drop:
            fmt = "{fig_chr}*{x_dest_num}{y_dest_chr}"
            return fmt.format(
                x_dest_num=self.destination[0],
                y_dest_chr=USI_LETTERS[self.destination[1] - 1],
                fig_chr=self.figure.value.upper()
            )
        else:
            fmt = "{x_orig_num}{y_orig_chr}{x_dest_num}{y_dest_chr}"
            if self.is_promotion:
                fmt += "+"
            return fmt.format(
                x_orig_num=self.origin[0],
                y_orig_chr=USI_LETTERS[self.origin[1] - 1],
                x_dest_num=self.destination[0],
                y_dest_chr=USI_LETTERS[self.destination[1] - 1],
            )

    def to_kif(self) -> str:
        """
        Return signature of move

        notation_transform_func:
            Function that converts coordinates in screen coordinates system
            to coordinates in notation coordinates system
        """

        dest_coords_str = "{x}{y_jp}".format(
            x=self.destination[0],
            y_jp=JP_DIGITS[self.destination[1]]
        )
        if self.is_drop:
            s = "{dest}{fig_jp}打".format(
                dest=dest_coords_str,
                fig_jp=self.figure.to_jp()
            )
            return s
        else:
            origin_coords_str = "{x}{y}".format(
                x=self.origin[0],
                y=self.origin[1]
            )
            prom_str = "成" if self.is_promotion else ""
            s = "{dest}{fig_jp}{prom}({origin})".format(
                dest=dest_coords_str,
                fig_jp=self.figure.to_jp(),
                prom=prom_str,
                origin=origin_coords_str
            )
            return s
