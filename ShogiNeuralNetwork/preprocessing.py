import keras
import numpy as np
from keras import layers
from config import GLOBAL_CONFIG
from extra.image_modes import ImageMode


def reshape_image(img: np.ndarray):
    """Converts SIZE x SIZE image to SIZE x SIZE x 1"""
    if len(img.shape) == 2:
        h, w = img.shape
        return img.reshape((h, w, 1))
    else:
        return img


resize_and_rescale = keras.Sequential([
    layers.Resizing(GLOBAL_CONFIG.NeuralNetwork.cell_img_size, GLOBAL_CONFIG.NeuralNetwork.cell_img_size),
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
