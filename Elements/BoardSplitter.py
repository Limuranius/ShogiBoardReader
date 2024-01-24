from .ImageGetters import ImageGetter
from Elements.CornerDetectors.CornerDetector import CornerDetector
from extra import utils
from extra.image_modes import ImageMode
from extra.types import ImageNP
import numpy as np
import cv2


class BoardSplitter:
    image_getter: ImageGetter
    corner_detector: CornerDetector
    cell_img_size: int
    board_img_size: int

    def __init__(self,
                 image_getter: ImageGetter,
                 corner_getter: CornerDetector,
                 cell_img_size: int):
        self.image_getter = image_getter
        self.corner_detector = corner_getter
        self.cell_img_size = cell_img_size
        self.board_img_size = cell_img_size * 9

    def get_board_image_no_perspective(self,
                                       img_mode: ImageMode = ImageMode.ORIGINAL,
                                       draw_grid: bool = False) -> ImageNP:
        """Returns image of board without perspective and surroundings"""
        full_img = self.image_getter.get_image()
        corners = self.corner_detector.get_corners(full_img)
        img_no_persp = utils.remove_perspective(full_img, np.array(corners))
        h, w = img_no_persp.shape[:2]
        for x in np.linspace(0, w, num=10, dtype=np.int_):
            cv2.line(img_no_persp, [x, 0], [x, h], color=[0, 255, 0], thickness=3)
        for y in np.linspace(0, h, num=10, dtype=np.int_):
            cv2.line(img_no_persp, [0, y], [w, y], color=[0, 255, 0], thickness=3)
        match img_mode:
            case ImageMode.ORIGINAL:
                return img_no_persp
            case ImageMode.GRAYSCALE_BLACK_THRESHOLD:
                return utils.get_black_mask(img_no_persp)

    def get_board_cells(self, image_mode: ImageMode) -> list[list[ImageNP]]:
        """Returns 2D 9x9 list with images of cells"""
        match image_mode:
            case ImageMode.ORIGINAL:
                return self.__get_board_cells_original()
            case ImageMode.CANNY:
                return self.__get_board_cells_canny()
            case ImageMode.GRAYSCALE:
                return self.__get_board_cells_grayscale()
            case ImageMode.GRAYSCALE_BLACK_THRESHOLD:
                return self.__get_board_cells_mask()
            case ImageMode.LAB_THRESHOLD:
                return self.__get_board_cells_lab_threshold()
            case _:
                raise Exception("Unknown image_mode")

    def __get_board_cells_grayscale(self) -> list[list[ImageNP]]:
        board_img = self.get_board_image_no_perspective()
        gray = cv2.cvtColor(board_img, cv2.COLOR_BGR2GRAY)
        return self.__get_board_cells(gray)

    def __get_board_cells_canny(self) -> list[list[ImageNP]]:
        board_img = self.get_board_image_no_perspective()
        canny = cv2.Canny(board_img, 250, 255)
        return self.__get_board_cells(canny)

    def __get_board_cells_mask(self) -> list[list[ImageNP]]:
        board_img = self.get_board_image_no_perspective()
        mask = utils.get_black_mask(board_img)
        return self.__get_board_cells(mask)

    def __get_board_cells_lab_threshold(self):
        board_img = self.get_board_image_no_perspective()
        img_lab = cv2.cvtColor(board_img, cv2.COLOR_BGR2LAB)
        mask = img_lab[:, :, 0] < 100
        mask = mask.astype(np.uint8) * 255
        return self.__get_board_cells(mask)

    def __get_board_cells_original(self) -> list[list[ImageNP]]:
        return self.__get_board_cells(self.get_board_image_no_perspective())

    def __get_board_cells(self, board_img: ImageNP) -> list[list[ImageNP]]:
        """Splits image into 81 (9x9) images of each cell"""

        img_size = (self.board_img_size, self.board_img_size)
        cell_size = (self.cell_img_size, self.cell_img_size)
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

    def get_full_img(self, show_borders: bool = False, show_grid: bool = False) -> ImageNP:
        full_img = self.image_getter.get_image()
        color = [0, 255, 0]
        thickness = max(full_img.shape) // 500 + 1
        corners = np.array(self.corner_detector.get_corners(full_img))
        if show_borders:
            cv2.polylines(full_img, [corners], True, color, thickness=thickness)
        if show_grid:
            top_points = np.linspace(corners[0], corners[1], num=10, dtype=np.int_)
            right_points = np.linspace(corners[1], corners[2], num=10, dtype=np.int_)
            bottom_points = np.linspace(corners[2], corners[3], num=10, dtype=np.int_)
            left_points = np.linspace(corners[3], corners[0], num=10, dtype=np.int_)

            for p1, p2 in zip(top_points, reversed(bottom_points)):
                cv2.line(full_img, p1, p2, color, thickness)
            for p1, p2 in zip(left_points, reversed(right_points)):
                cv2.line(full_img, p1, p2, color, thickness)
        return full_img
