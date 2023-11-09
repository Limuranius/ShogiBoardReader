from extra.types import FigureBoard
from .BoardCounter import BoardCounter
from .Move import *
from .utils import get_move


class BoardMemorizer:
    counter: BoardCounter
    move_history: list[Move]

    # True means that player on the lower half of the board moved first
    lower_moves_first: bool

    def __init__(self, lower_moves_first: bool = True):
        self.counter = BoardCounter()
        self.move_history = []
        self.lower_moves_first = lower_moves_first

    def update(self, board: FigureBoard):
        if not self.counter.filled:
            self.counter.update(board)
            print("Копим данные...")
            return
        curr_board = self.counter.get_max_board()
        new_board = board
        move = get_move(curr_board, new_board)
        if curr_board == new_board:
            self.counter.update(new_board)
        elif move is not None:
            self.counter.update(new_board)

            new_curr_board = self.counter.get_max_board()
            if new_curr_board != curr_board:
                self.move_history.append(move)
        else:
            print("Invalid view")

    def get_board(self) -> FigureBoard:
        return self.counter.get_max_board()

    def save_to_kifu(self, file_path: str):
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
