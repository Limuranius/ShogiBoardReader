import cv2
import numpy as np
from config import GLOBAL_CONFIG
from extra.types import CellsImages, ImageNP

CELL_IMAGE_SIZE = GLOBAL_CONFIG.NeuralNetwork.cell_img_size


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


def prepare_cells_imgs(cells_imgs: CellsImages) -> np.ndarray:
    """Prepares images of board cells for input into tf model
    Does resizing, reshaping and rescaling
    """
    imgs = flatten(cells_imgs)
    imgs = [cv2.resize(image, (CELL_IMAGE_SIZE, CELL_IMAGE_SIZE)) for image in imgs]
    imgs = np.array(imgs).astype("float32") / 255
    imgs = np.reshape(imgs, (81, CELL_IMAGE_SIZE, CELL_IMAGE_SIZE, 1))
    return imgs


def prepare_cell_img(cell_img: ImageNP) -> ImageNP:
    cell_img = cv2.resize(cell_img, (CELL_IMAGE_SIZE, CELL_IMAGE_SIZE))
    cell_img = np.array(cell_img).astype("float32") / 255
    cell_img = np.reshape(cell_img, (1, CELL_IMAGE_SIZE, CELL_IMAGE_SIZE, 1))
    return cell_img
