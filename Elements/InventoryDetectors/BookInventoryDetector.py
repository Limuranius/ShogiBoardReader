from extra.types import ImageNP, Corners
from .InventoryDetector import InventoryDetector
from Elements.CornerDetectors import BookCornerDetector
from extra.utils import bounding_box_image


class BookInventoryDetector(InventoryDetector):
    def get_figure_images(self, image: ImageNP) -> tuple[list[ImageNP], list[ImageNP]]:
        i1_corners, i2_corners = self.get_inventories_corners(image)
        i1_img = bounding_box_image(image, i1_corners)
        i2_img = bounding_box_image(image, i2_corners)
        return (
            self.__split_inventory_img(i1_img),
            self.__split_inventory_img(i2_img),
        )

    def get_inventories_corners(self, image: ImageNP) -> tuple[Corners, Corners]:
        h, w = image.shape[:2]
        cd = BookCornerDetector()
        p0, p1, p2, p3 = cd.get_corners(image)
        y_min = p0[1]
        y_max = p3[1]
        x_min = p0[0]
        x_max = p1[0]
        board_width = p1[0] - p0[0]
        cell_w = board_width // 9
        offset = int(cell_w * 0.65)
        inventory_1_p0 = (min(w-1, x_max + offset), y_min)
        inventory_1_p1 = (min(w-1, x_max + offset + cell_w), y_min)
        inventory_1_p2 = (min(w-1, x_max + offset + cell_w), y_max)
        inventory_1_p3 = (min(w-1, x_max + offset), y_max)

        inventory_2_p0 = (max(0, x_min - cell_w), y_min)
        inventory_2_p1 = (max(0, x_min), y_min)
        inventory_2_p2 = (max(0, x_min), y_max)
        inventory_2_p3 = (max(0, x_min - cell_w), y_max)

        return (
            (inventory_1_p0, inventory_1_p1, inventory_1_p2, inventory_1_p3),
            (inventory_2_p0, inventory_2_p1, inventory_2_p2, inventory_2_p3),
        )

    def __split_inventory_img(self, inv_img: ImageNP) -> list[ImageNP]:
        h = inv_img.shape[0]
        cell_h = h // 9
        inv_cells = []
        for i in range(9):
            y1 = i * cell_h
            y2 = (i + 1) * cell_h
            cell_img = inv_img[y1: y2, :]
            inv_cells.append(cell_img)
        return inv_cells
