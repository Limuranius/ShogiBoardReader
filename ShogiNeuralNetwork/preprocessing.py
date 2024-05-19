import cv2
import numpy as np
from extra.image_modes import ImageMode
from extra.types import CellsImages, ImageNP


def reshape_image(img: np.ndarray):
    """Converts SIZE x SIZE image to SIZE x SIZE x 1"""
    if len(img.shape) == 2:
        h, w = img.shape
        return img.reshape((h, w, 1))
    else:
        return img


def flatten(cells_imgs: CellsImages) -> list[ImageNP]:
    """Converts 9x9 2D array of images to 81 1D"""
    flat_arr = []
    for i in range(9):
        for j in range(9):
            flat_arr.append(cells_imgs[i][j])
    return flat_arr


def prepare_cells_imgs(
        cells_imgs: CellsImages,
        image_mode: ImageMode,
        cell_image_size: int,
) -> np.ndarray:
    """
    Prepares 2d array with images of board cells for input into model
    Does resizing, reshaping, rescaling and conversion to image mode
    """
    imgs = flatten(cells_imgs)
    imgs = [cv2.resize(image, (cell_image_size, cell_image_size)) for image in imgs]
    imgs = [image_mode.convert_image(image) for image in imgs]
    imgs = np.array(imgs).astype("float32") / 255
    imgs = np.reshape(imgs, (81, cell_image_size, cell_image_size, 1))
    return imgs


def prepare_cell_img(
        cell_img: ImageNP,
        image_mode: ImageMode,
        cell_image_size: int,
) -> ImageNP:
    cell_img = cv2.resize(cell_img, (cell_image_size, cell_image_size))
    cell_img = image_mode.convert_image(cell_img)
    cell_img = np.array(cell_img).astype("float32") / 255
    cell_img = np.reshape(cell_img, (1, cell_image_size, cell_image_size, 1))
    return cell_img
