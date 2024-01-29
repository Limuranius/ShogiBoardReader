import cv2
import keras
import numpy as np
from keras import layers
from config import GLOBAL_CONFIG
from extra.image_modes import ImageMode
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


resize_and_rescale = keras.Sequential([
    layers.Resizing(CELL_IMAGE_SIZE, CELL_IMAGE_SIZE),
    layers.Rescaling(1. / 255)
])

augment = keras.Sequential([
    layers.RandomRotation(
        factor=GLOBAL_CONFIG.NeuralNetwork.rotation_factor
    ),
    layers.RandomTranslation(
        height_factor=GLOBAL_CONFIG.NeuralNetwork.height_shift_factor,
        width_factor=GLOBAL_CONFIG.NeuralNetwork.width_shift_factor
    ),
    layers.RandomZoom(
        height_factor=GLOBAL_CONFIG.NeuralNetwork.zoom_factor
    ),

])

if ImageMode(GLOBAL_CONFIG.NeuralNetwork.image_mode) in [ImageMode.GRAYSCALE, ImageMode.ORIGINAL]:
    augment.add(
        layers.RandomBrightness(
            factor=GLOBAL_CONFIG.NeuralNetwork.brightness_factor,
            value_range=[0.0, 1.0]
        )
    )
