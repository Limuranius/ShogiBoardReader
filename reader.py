import cv2
import utils
import numpy as np
from image_getter import ImageGetter
from corner_getter import CornerDetector
from config import config
from figures import Figure, Direction, FIGURE_ICONS_PATHS
from recognizer import Recognizer
from board_analyzer import BoardAnalyzer


class ShogiBoardReader:
    image_getter: ImageGetter
    corner_getter: CornerDetector
    recognizer: Recognizer
    analyzer: BoardAnalyzer

    def __init__(self, image_getter: ImageGetter, corner_getter: CornerDetector, recognizer: Recognizer):
        self.image_getter = image_getter
        self.corner_getter = corner_getter
        self.recognizer = recognizer
        self.analyzer = BoardAnalyzer()

    def get_board_image(self):
        """Возвращает изображение доски с убранной перспективой и вырезанным фоном"""
        full_img = self.image_getter.get_image()
        corners = self.corner_getter.get_corners(full_img)
        return utils.remove_perspective(full_img, np.array(corners))

    def get_board_cells(self) -> list[list[np.ndarray]]:
        # return self.get_board_cells_lab_threshold()
        return self.get_board_cells_canny()
        # return self.get_board_cells_mask()
        # return self.get_board_cells_grayscale()

    def get_board_cells_grayscale(self) -> list[list[np.ndarray]]:
        board_img = self.get_board_image()
        gray = cv2.cvtColor(board_img, cv2.COLOR_BGR2GRAY)
        return self.__get_board_cells(gray)

    def get_board_cells_canny(self) -> list[list[np.ndarray]]:
        board_img = self.get_board_image()
        canny = cv2.Canny(board_img, 250, 255)
        return self.__get_board_cells(canny)

    def get_board_cells_mask(self) -> list[list[np.ndarray]]:
        board_img = self.get_board_image()
        mask = utils.get_black_mask(board_img)
        return self.__get_board_cells(mask)

    def get_board_cells_lab_threshold(self):
        board_img = self.get_board_image()
        img_lab = cv2.cvtColor(board_img, cv2.COLOR_BGR2LAB)
        mask = img_lab[:, :, 0] < 100
        mask = mask.astype(np.uint8) * 255
        return self.__get_board_cells(mask)

    def get_board_cells_original(self) -> list[list[np.ndarray]]:
        return self.__get_board_cells(self.get_board_image())

    def __get_board_cells(self, board_img) -> list[list[np.ndarray]]:
        img_size = (config.NN_data.board_img_size, config.NN_data.board_img_size)
        cell_size = (config.NN_data.cell_img_size, config.NN_data.cell_img_size)
        board_img = cv2.resize(board_img, img_size)
        height = board_img.shape[0]
        width = board_img.shape[1]
        x_step = width // 9
        y_step = height // 9

        result = [[None for _ in range(9)] for __ in range(9)]
        for y in range(1, 10):
            for x in range(1, 10):
                x_start = x_step * (x - 1)
                x_end = x_step * x
                y_start = y_step * (y - 1)
                y_end = y_step * y
                cell_img = board_img[y_start: y_end, x_start: x_end]
                cell_img = cv2.resize(cell_img, cell_size)
                result[y - 1][x - 1] = cell_img
        return result

    def recognize_board_figures(self) -> list[list[Figure]]:
        cells = self.get_board_cells()
        return self.recognizer.recognize_board_figures(cells)

    def recognize_board_directions(self) -> list[list[Direction]]:
        cells = self.get_board_cells()
        return self.recognizer.recognize_board_directions(cells)

    def get_str_board(self):
        board = self.recognize_board_figures()
        s = ""
        for i in range(9):
            for j in range(9):
                figure = board[i][j]
                s += figure.value
            s += "\n"
        return s

    def show_board(self):
        img = self.get_board_image()
        cv2.imshow("board", img)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

    def show_cell(self, i, j):
        cells = self.get_board_cells_original()
        cv2.imshow("cell", cells[i][j])
        cv2.waitKey(0)

    def get_full_img_with_borders(self) -> np.ndarray:
        full_img = self.image_getter.get_image()
        corners = np.array(self.corner_getter.get_corners(full_img))
        cv2.polylines(full_img, [corners], True, [0, 255, 0], thickness=3)
        return full_img

    def get_digital_board(self):
        figures = self.recognize_board_figures()
        directions = self.recognize_board_directions()

        self.analyzer.update(figures)
        figures = self.analyzer.get_board()

        BOARD_SIZE = 1000
        FIGURE_SIZE = BOARD_SIZE // 9
        board = np.full((BOARD_SIZE, BOARD_SIZE, 3), [255, 255, 255], dtype=np.uint8)

        # Рисуем сетку
        grid_step = BOARD_SIZE // 9
        for i in range(10):
            y = i * grid_step
            cv2.line(board, (0, y), (BOARD_SIZE, y), 0, thickness=5)
        for j in range(10):
            x = j * grid_step
            cv2.line(board, (x, 0), (x, BOARD_SIZE), 0, thickness=5)

        # Добавляем фигуры
        figure_step = BOARD_SIZE // 9
        for i in range(9):
            for j in range(9):
                y = figure_step * i
                x = figure_step * j
                figure = figures[i][j]
                direction = directions[i][j]
                if figure != Figure.EMPTY:
                    figure_img = cv2.imread(FIGURE_ICONS_PATHS[figure])
                    figure_img = cv2.resize(figure_img, (FIGURE_SIZE, FIGURE_SIZE))
                    if direction == Direction.DOWN:
                        figure_img = np.flip(figure_img, axis=0)
                    utils.overlay_image_on_image(board, figure_img, x, y)
        return board
