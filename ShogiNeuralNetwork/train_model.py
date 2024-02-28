import keras
from keras import layers
import tensorflow as tf
from .data_info import CATEGORIES_FIGURE_TYPE
from config import GLOBAL_CONFIG


def train_model(
        train_ds: tf.data.Dataset,
        epochs: int,
        verbose=0,
) -> keras.Model:
    cell_img_size = GLOBAL_CONFIG.NeuralNetwork.cell_img_size

    img_input = keras.Input(shape=(cell_img_size, cell_img_size, 1), name="input")
    x = layers.Conv2D(64, 3, activation="relu")(img_input)
    x = layers.MaxPooling2D()(x)
    x = layers.Conv2D(128, 3, activation="relu")(x)
    x = layers.MaxPooling2D()(x)
    x = layers.Conv2D(256, 3, activation="relu")(x)
    x = layers.Flatten()(x)

    figure_dense = layers.Dense(128, activation="relu")(x)
    figure_pred = layers.Dense(len(CATEGORIES_FIGURE_TYPE), activation="softmax", name="figure")(figure_dense)

    direction_dense = layers.Dense(128, activation="relu")(x)
    direction_pred = layers.Dense(3, activation="softmax", name="direction")(direction_dense)

    model = keras.Model(
        img_input,
        outputs=[figure_pred, direction_pred]
    )

    model.compile(
        optimizer=keras.optimizers.Adam(),
        loss={
            "figure": keras.losses.SparseCategoricalCrossentropy(),
            "direction": keras.losses.SparseCategoricalCrossentropy(),
        },
        metrics={
            "figure": ["accuracy"],
            "direction": ["accuracy"],
        }
    )

    model.fit(
        train_ds,
        epochs=epochs,
        verbose=verbose,
    )

    return model
