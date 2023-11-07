from extra.types import FigureBoard
from .BoardCounter import BoardCounter
from .Move import *
from .utils import get_move


class BoardMemorizer:
    counter: BoardCounter
    komadai_lower: list[Figure]
    komadai_higher: list[Figure]
    move_history: list[Move]

    def __init__(self):
        self.counter = BoardCounter()
        self.move_history = []

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
                print(move.get_signature())
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
        for i, move in enumerate(self.move_history):
            signature = move.get_signature()
            row_fmt = "{:>4} {}\n"
            s += row_fmt.format(i + 1, signature)

        with open(file_path, "w") as f:
            f.write(s)
