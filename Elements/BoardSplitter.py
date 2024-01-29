from .ImageGetters import ImageGetter
from Elements.CornerDetectors.CornerDetector import CornerDetector
from Elements.InventoryDetectors import InventoryDetector
from extra import utils
from extra.image_modes import ImageMode
from extra.types import ImageNP
import numpy as np
import cv2


class BoardSplitter:
    image_getter: ImageGetter
    corner_detector: CornerDetector
    inventory_detector: InventoryDetector

    def __init__(self,
                 image_getter: ImageGetter,
                 corner_getter: CornerDetector,
                 inventory_detector: InventoryDetector = None):
        self.image_getter = image_getter
        self.corner_detector = corner_getter
        self.inventory_detector = inventory_detector

    def get_board_image_no_perspective(self,
                                       img_mode: ImageMode = ImageMode.ORIGINAL,
                                       draw_grid: bool = False) -> ImageNP:
        """Returns image of board without perspective and surroundings"""
        full_img = self.image_getter.get_image()
        corners = self.corner_detector.get_corners(full_img)
        img_no_persp = utils.remove_perspective(full_img, np.array(corners))
        if draw_grid:
            h, w = img_no_persp.shape[:2]
            for x in np.linspace(0, w, num=10, dtype=np.int_):
                cv2.line(img_no_persp, [x, 0], [x, h], color=[0, 255, 0], thickness=3)
            for y in np.linspace(0, h, num=10, dtype=np.int_):
                cv2.line(img_no_persp, [0, y], [w, y], color=[0, 255, 0], thickness=3)
        return img_mode.convert_image(img_no_persp)

    def get_board_cells(self, image_mode: ImageMode) -> list[list[ImageNP]]:
        """Returns 2D 9x9 list with images of cells"""
        board_img = self.get_board_image_no_perspective(image_mode)
        return self.__get_board_cells(board_img)

    def __get_board_cells(self, board_img: ImageNP) -> list[list[ImageNP]]:
        """Splits image into 81 (9x9) images of each cell"""

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
                result[y - 1][x - 1] = cell_img
        return result

    def get_full_img(
            self,
            show_borders: bool = False,
            show_grid: bool = False,
            show_inventories: bool = False
    ) -> ImageNP:
        full_img = self.image_getter.get_image().copy()
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
        if show_inventories and self.inventory_detector is not None:
            i1_corners, i2_corners = self.inventory_detector.get_inventories_corners(full_img)
            i1_corners = np.array(i1_corners)
            i2_corners = np.array(i2_corners)
            cv2.polylines(full_img, [i1_corners, i2_corners], True, color, thickness=thickness)
        return full_img

    def get_inventory_cells(self, image_mode: ImageMode) -> tuple[list[ImageNP], list[ImageNP]]:
        img = self.get_full_img()
        i1_imgs, i2_imgs = self.inventory_detector.get_figure_images(img)
        i1_imgs = [image_mode.convert_image(image) for image in i1_imgs]
        i2_imgs = [image_mode.convert_image(image) for image in i2_imgs]
        return i1_imgs, i2_imgs
