from extra.types import Figure, FigureBoard


class BoardCounter:
    frames: list[FigureBoard]
    memorize_count = 10  # How many frames of board are memorized and calculated statistics on
    counts: list[list[dict[Figure, int]]]  # Frequencies of figures in each cell based on previous frames
    filled: bool

    def __init__(self):
        self.frames = []
        cell_count = {figure: 0 for figure in Figure}
        self.counts = [[cell_count.copy() for _ in range(9)] for __ in range(9)]
        self.filled = False

    def append_board(self, board: FigureBoard):
        self.frames.append(board)
        for i in range(9):
            for j in range(9):
                figure = board[i][j]
                self.counts[i][j][figure] += 1

    def pop_last(self):
        board = self.frames.pop(0)
        for i in range(9):
            for j in range(9):
                figure = board[i][j]
                self.counts[i][j][figure] -= 1

    def get_max_board(self) -> FigureBoard:
        max_board = [[Figure.EMPTY for _ in range(9)] for __ in range(9)]
        for i in range(9):
            for j in range(9):
                cell_count = self.counts[i][j]
                max_figure = max(cell_count, key=cell_count.get)
                max_board[i][j] = max_figure
        return max_board

    def update(self, board: FigureBoard):
        if len(self.frames) <= self.memorize_count:
            self.append_board(board)
        else:
            self.filled = True
            self.append_board(board)
            self.pop_last()
