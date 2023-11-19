from tensorflow import keras
from .Dataset import Dataset
from .data_info import CATEGORIES_FIGURE_TYPE


def train_figure_type_model(
        dataset: Dataset,
        epochs: int,
        verbose=0,
        **data_augmentation_params
) -> keras.Model:
    cell_img_size = dataset.cell_img_size
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

    datagen = dataset.get_augmented_data_generator(
        y_type="figure",
        **data_augmentation_params
    )

    model.fit(
        datagen,
        epochs=epochs,
        verbose=verbose,
    )
    return model


def train_direction_model(
        dataset: Dataset,
        epochs: int,
        verbose=0,
        **data_augmentation_params
) -> keras.Model:
    cell_img_size = dataset.cell_img_size
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

    datagen = dataset.get_augmented_data_generator(
        y_type="direction",
        **data_augmentation_params
    )

    model.fit(
        datagen,
        epochs=epochs,
        verbose=verbose,
    )
    return model
