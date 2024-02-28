import keras
from keras import layers
from config import GLOBAL_CONFIG
from extra.image_modes import ImageMode

CELL_IMAGE_SIZE = GLOBAL_CONFIG.NeuralNetwork.cell_img_size

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
