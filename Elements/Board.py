import numpy as np
import shogi

from extra.figures import Figure, Direction, FIGURE_ICONS_PATHS
from extra.types import FigureBoard, DirectionBoard, ImageNP, Inventory
from dataclasses import dataclass
from extra import utils
import cv2


@dataclass(frozen=True)
class Board:
    figures: FigureBoard
    directions: DirectionBoard
    inventory_black: Inventory = None
    inventory_white: Inventory = None

    def to_str_figures(self):
        return utils.board_to_str(self.figures)

    def to_str_directions(self):
        return utils.board_to_str(self.directions)

    def to_str(self):
        s = "Figures:     Directions:"
        for fig_row, dir_row in zip(self.figures, self.directions):
            s += "".join([cell.value for cell in fig_row])
            s += "    "
            s += "".join([cell.value for cell in dir_row])
            s += "\n"

    def to_image(self) -> ImageNP:
        BOARD_SIZE = 1000
        FIGURE_SIZE = BOARD_SIZE // 9
        board = np.full((BOARD_SIZE, BOARD_SIZE, 3), [255, 255, 255], dtype=np.uint8)

        grid_step = BOARD_SIZE // 9
        for i in range(10):
            y = i * grid_step
            cv2.line(board, (0, y), (BOARD_SIZE, y), 0, thickness=5)
        for j in range(10):
            x = j * grid_step
            cv2.line(board, (x, 0), (x, BOARD_SIZE), 0, thickness=5)

        figure_step = BOARD_SIZE // 9
        for i in range(9):
            for j in range(9):
                y = figure_step * i
                x = figure_step * j
                figure = self.figures[i][j]
                direction = self.directions[i][j]
                if figure != Figure.EMPTY:
                    figure_img = cv2.imread(FIGURE_ICONS_PATHS[figure])
                    figure_img = cv2.resize(figure_img, (FIGURE_SIZE, FIGURE_SIZE))
                    if direction == Direction.DOWN:
                        figure_img = np.flip(figure_img, axis=0)
                    utils.overlay_image_on_image(board, figure_img, x, y)
        return board

    def to_shogi_board(self) -> shogi.Board:
        board = shogi.Board()
        board.clear()

        to_shogi_type = {
            Figure.KING: shogi.KING,
            Figure.PAWN: shogi.PAWN,
            Figure.LANCE: shogi.LANCE,
            Figure.KNIGHT: shogi.KNIGHT,
            Figure.SILVER: shogi.SILVER,
            Figure.GOLD: shogi.GOLD,
            Figure.BISHOP: shogi.BISHOP,
            Figure.ROOK: shogi.ROOK,
            Figure.PAWN_PROM: shogi.PROM_PAWN,
            Figure.LANCE_PROM: shogi.PROM_LANCE,
            Figure.KNIGHT_PROM: shogi.PROM_KNIGHT,
            Figure.SILVER_PROM: shogi.PROM_SILVER,
            Figure.BISHOP_PROM: shogi.PROM_BISHOP,
            Figure.ROOK_PROM: shogi.PROM_ROOK,
        }

        to_shogi_color = {
            Direction.DOWN: shogi.WHITE,
            Direction.UP: shogi.BLACK,
        }

        # Adding pieces on board
        for i in range(9):
            for j in range(9):
                square = shogi.SQUARES[i * 9 + j]
                figure = self.figures[i][j]
                direction = self.directions[i][j]
                if figure != Figure.EMPTY and direction != Direction.NONE:
                    piece_type = to_shogi_type[figure]
                    color = to_shogi_color[direction]
                    piece = shogi.Piece(piece_type, color)
                    board.set_piece_at(square, piece)

        # Adding pieces from inventory
        if self.inventory_black and self.inventory_white:
            for figure in Figure:
                if figure.is_droppable():
                    count_black = self.inventory_black[figure]
                    count_white = self.inventory_white[figure]
                    piece_type = to_shogi_type[figure]
                    board.add_piece_into_hand(piece_type, shogi.BLACK, count_black)
                    board.add_piece_into_hand(piece_type, shogi.WHITE, count_white)
        return board
