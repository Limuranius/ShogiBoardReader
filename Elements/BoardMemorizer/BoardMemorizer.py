from extra.types import FigureBoard, DirectionBoard
from .BoardCounter import BoardCounter
from .Move import *
from .utils import get_move
from ..Board import Board


class BoardMemorizer:
    counter: BoardCounter
    move_history: list[Move]

    # True means that player on the lower half of the board moved first
    lower_moves_first: bool

    def __init__(self, lower_moves_first: bool = True):
        self.counter = BoardCounter()
        self.move_history = []
        self.lower_moves_first = lower_moves_first

    def update(self, figures: FigureBoard, directions: DirectionBoard) -> bool:
        """Updates board and returns True if the update is possible"""
        if not self.counter.filled:
            print("Accumulating data. Don't move anything")
            self.counter.update(figures, directions)
            return True
        curr_board = self.counter.get_max_board()
        move = get_move(
            curr_board,
            Board(figures, directions)
        )
        if curr_board.figures == figures:
            self.counter.update(figures, directions)
            return True
        elif move is not None:
            self.counter.update(figures, directions)
            new_curr_board = self.counter.get_max_board()
            if new_curr_board.figures != curr_board.figures:
                self.move_history.append(move)
            return True
        else:
            return False

    def get_board(self) -> Board:
        return self.counter.get_max_board()

    def save_to_kifu(self, file_path: str) -> None:
        s = """手合割：平手
先手：
後手：
手数----指手----消費時間--
"""
        if self.lower_moves_first:
            def notation_transform_func(x: int, y: int):
                return 10 - x, y
        else:
            def notation_transform_func(x: int, y: int):
                return x, 10 - y

        for i, move in enumerate(self.move_history):
            signature = move.get_signature(notation_transform_func)
            row_fmt = "{:>4} {}\n"
            s += row_fmt.format(i + 1, signature)

        with open(file_path, "w") as f:
            f.write(s)
