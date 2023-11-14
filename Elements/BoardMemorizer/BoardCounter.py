from extra.types import Figure, FigureBoard, DirectionBoard, Direction
from Elements.Board import Board


class BoardCounter:
    __memorize_count = 10  # How many frames of board are memorized and calculated statistics on

    __figure_frames: list[FigureBoard]
    __direction_frames: list[DirectionBoard]

    __figure_counts: list[list[dict[Figure, int]]]  # Frequencies of figures in each cell based on previous frames
    __direction_counts: list[list[dict[Direction, int]]]  # Frequencies of directions

    filled: bool  # Whether memorizer finished accumulating frames

    def __init__(self):
        self.__figure_frames = []
        self.__direction_frames = []

        figure_count = {figure: 0 for figure in Figure}
        self.__figure_counts = [[figure_count.copy() for _ in range(9)] for __ in range(9)]

        direction_count = {direction: 0 for direction in Direction}
        self.__direction_counts = [[direction_count.copy() for _ in range(9)] for __ in range(9)]

        self.filled = False

    def __append_board(self, figures: FigureBoard, directions: DirectionBoard):
        self.__figure_frames.append(figures)
        self.__direction_frames.append(directions)
        for i in range(9):
            for j in range(9):
                figure = figures[i][j]
                direction = directions[i][j]
                self.__figure_counts[i][j][figure] += 1
                self.__direction_counts[i][j][direction] += 1

    def __pop_last(self):
        figures = self.__figure_frames.pop(0)
        directions = self.__direction_frames.pop(0)
        for i in range(9):
            for j in range(9):
                figure = figures[i][j]
                direction = directions[i][j]
                self.__figure_counts[i][j][figure] -= 1
                self.__direction_counts[i][j][direction] -= 1

    def get_max_board(self) -> Board:
        max_figures = [[Figure.EMPTY for _ in range(9)] for __ in range(9)]
        max_directions = [[Direction.NONE for _ in range(9)] for __ in range(9)]
        for i in range(9):
            for j in range(9):
                figure_count = self.__figure_counts[i][j]
                direction_count = self.__direction_counts[i][j]
                max_figure = max(figure_count, key=figure_count.get)
                max_direction = max(direction_count, key=direction_count.get)
                max_figures[i][j] = max_figure
                max_directions[i][j] = max_direction
        return Board(max_figures, max_directions)

    def update(self, figures: FigureBoard, directions: DirectionBoard):
        if len(self.__figure_frames) <= self.__memorize_count:
            self.__append_board(figures, directions)
        else:
            self.filled = True
            self.__append_board(figures, directions)
            self.__pop_last()
