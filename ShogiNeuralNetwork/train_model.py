from tensorflow import keras
from .Dataset import Dataset


def train_figure_type_model(
        dataset: Dataset,
        cell_img_size: int,
        epochs: int
) -> keras.Model:
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
            keras.layers.Dense(9, activation="softmax"),
        ]
    )

    model.compile(
        loss=keras.losses.SparseCategoricalCrossentropy(),
        optimizer=keras.optimizers.Adam(),
        metrics=["accuracy"]
    )

    X_train = dataset.X_train.astype("float32") / 255
    y_train = dataset.y_figure_train

    model.fit(X_train, y_train, batch_size=32, epochs=epochs)
    return model


def train_direction_model(
        dataset: Dataset,
        cell_img_size: int,
        epochs: int
) -> keras.Model:
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

    X_train = dataset.X_train.astype("float32") / 255
    y_train = dataset.y_direction_train

    model.fit(X_train, y_train, batch_size=32, epochs=epochs)
    return model
