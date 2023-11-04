from extra.types import FigureBoard, DirectionBoard, Corners
from extra.figures import Figure, Direction
from dataclasses import dataclass


@dataclass(frozen=True)
class BoardPhotoInfo:
    img_name: str
    figures: FigureBoard
    directions: DirectionBoard
    corners: Corners


# Loading file with info
__boards: dict[str, BoardPhotoInfo] = dict()
with open("true_boards.txt", "r") as f:
    while line := f.readline():
        if line.strip() == "":
            continue
        else:
            im_name = line.strip()

            corners = []
            for _ in range(4):
                corners.append([int(i) for i in f.readline().strip().split()])
            f.readline()

            figures = []
            for _ in range(9):
                fig_row = [Figure(char) for char in f.readline().strip()]
                figures.append(fig_row)
            f.readline()

            directions = []
            for _ in range(9):
                directions_row = [Direction(char) for char in f.readline().strip()]
                directions.append(directions_row)
            f.readline()

            __boards[im_name] = BoardPhotoInfo(
                img_name=im_name,
                figures=figures,
                directions=directions,
                corners=corners
            )


def get_true_figures(img_name: str) -> FigureBoard:
    return __boards[img_name].figures


def get_true_directions(img_name: str) -> DirectionBoard:
    return __boards[img_name].directions


def get_corners(img_name: str) -> Corners:
    return __boards[img_name].corners
