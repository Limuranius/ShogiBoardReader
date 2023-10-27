from extra.figures import Figure

Board = list[list[Figure]]


def get_changed_cells(old_board: Board, new_board: Board) -> list[list[bool]]:
    """Возвращает маску доски, где True - клетки, значение которых поменялось"""
    changed = [[False for _ in range(9)] for __ in range(9)]
    for i in range(9):
        for j in range(9):
            if old_board[i][j] != new_board[i][j]:
                changed[i][j] = True
    return changed


def get_changed_count(old_board: Board, new_board: Board) -> int:
    """Возвращает кол-во клеток, значение которых изменилось при переходе с old_board к new_board"""
    changed = get_changed_cells(old_board, new_board)
    changed_count = sum(map(sum, changed))
    return changed_count


def get_turn_signature(old_board: Board, new_board: Board) -> str:
    """Возвращает запись сделанного хода"""
    changed = get_changed_cells(old_board, new_board)
    changed_coords = [(i, j) for i in range(9) for j in range(9) if changed[i][j]]
    print(*changed_coords)


class BoardCounter:
    frames: list[Board]
    memorize_count = 10  # По какому кол-ву последних снимков доски формируется итоговое изображение доски
    counts: list[list[dict[Figure, int]]]  # Для каждой клетки подсчитывает кол-во встреченных фигур
    max_change_count = 2

    def __init__(self):
        self.frames = []
        cell_count = {figure: 0 for figure in Figure}
        self.counts = [[cell_count.copy() for _ in range(9)] for __ in range(9)]

    def append_board(self, board: Board):
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

    def get_max_board(self) -> Board:
        max_board = [[Figure.EMPTY for _ in range(9)] for __ in range(9)]
        for i in range(9):
            for j in range(9):
                cell_count = self.counts[i][j]
                max_figure = max(cell_count, key=cell_count.get)
                max_board[i][j] = max_figure
        return max_board

    def update(self, board: Board):
        if len(self.frames) <= self.memorize_count:
            print("Копим данные...")
            self.append_board(board)
        else:
            max_board = self.get_max_board()
            changed_count = get_changed_count(max_board, board)
            if changed_count <= self.max_change_count:
                self.append_board(board)
                self.pop_last()
            else:
                print("Я не буду это добавлять")


class BoardAnalyzer:
    counter: BoardCounter
    komadai_lower: list[Figure]
    komadai_higher: list[Figure]

    def __init__(self):
        self.counter = BoardCounter()
        self.komadai_higher = []
        self.komadai_lower = []

    def update(self, board: Board):
        old_board = self.counter.get_max_board()
        self.counter.update(board)
        new_board = self.counter.get_max_board()
        if old_board != new_board:
            print(get_turn_signature(old_board, new_board))

    def get_board(self) -> Board:
        return self.counter.get_max_board()



