from tensorflow import keras
import tensorflow as tf
from .data_info import CATEGORIES_FIGURE_TYPE
from .CellsDataset import CellsDataset
from config import GLOBAL_CONFIG


def train_figure_type_model(
        train_ds: tf.data.Dataset,
        epochs: int,
        verbose=0,
) -> keras.Model:
    cell_img_size = GLOBAL_CONFIG.NeuralNetwork.cell_img_size
    model = keras.Sequential(
        [
            keras.Input(shape=(cell_img_size, cell_img_size, 1)),
            keras.layers.Conv2D(64, 3, activation="relu"),
            keras.layers.MaxPooling2D(),
            keras.layers.Conv2D(128, 3, activation="relu"),
            keras.layers.MaxPooling2D(),
            keras.layers.Conv2D(256, 3, activation="relu"),
            keras.layers.Flatten(),
            keras.layers.Dense(128, activation="relu"),
            keras.layers.Dense(len(CATEGORIES_FIGURE_TYPE), activation="softmax"),
        ]
    )

    model.compile(
        loss=keras.losses.SparseCategoricalCrossentropy(),
        optimizer=keras.optimizers.Adam(),
        metrics=["accuracy"]
    )

    model.fit(
        train_ds,
        epochs=epochs,
        verbose=verbose,
    )
    return model


def train_direction_model(
        train_ds: tf.data.Dataset,
        epochs: int,
        verbose=0,
) -> keras.Model:
    cell_img_size = GLOBAL_CONFIG.NeuralNetwork.cell_img_size
    model = keras.Sequential(
        [
            keras.Input(shape=(cell_img_size, cell_img_size, 1)),
            keras.layers.Conv2D(64, 3, activation="relu"),
            keras.layers.MaxPooling2D(),
            keras.layers.Conv2D(128, 3, activation="relu"),
            keras.layers.MaxPooling2D(),
            keras.layers.Conv2D(256, 3, activation="relu"),
            keras.layers.Flatten(),
            keras.layers.Dense(128, activation="relu"),
            keras.layers.Dense(3, activation="softmax"),
        ]
    )

    model.compile(
        loss=keras.losses.SparseCategoricalCrossentropy(),
        optimizer=keras.optimizers.Adam(),
        metrics=["accuracy"]
    )

    model.fit(
        train_ds,
        epochs=epochs,
        verbose=verbose,
    )
    return model
