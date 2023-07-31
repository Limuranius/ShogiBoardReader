import pickle
from tensorflow import keras
from time import time
from config import config


def load_data(names: list[str]):
    return [
        pickle.load(open(f"datasets/{name}.pickle", "rb"))
        for name in names
    ]


def train_figure_type():
    CELL_IMG_SIZE = config.NN_data.cell_img_size

    model = keras.Sequential(
        [
            keras.Input(shape=(CELL_IMG_SIZE, CELL_IMG_SIZE, 1)),
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

    X_train, y_train = load_data([
        "X_train", "y_figure_train",
    ])
    X_train = X_train.astype("float32") / 255

    model.fit(X_train, y_train, batch_size=32, epochs=5)
    model.save("../reader_figure_type.model")


def train_direction():
    CELL_IMG_SIZE = config.NN_data.cell_img_size

    model = keras.Sequential(
        [
            keras.Input(shape=(CELL_IMG_SIZE, CELL_IMG_SIZE, 1)),
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

    X_train, y_train = load_data([
        "X_train", "y_direction_train",
    ])
    X_train = X_train.astype("float32") / 255

    model.fit(X_train, y_train, batch_size=32, epochs=5)
    model.save("../reader_direction.model")


def test_figure():
    model = keras.models.load_model("../reader_figure_type.model")
    X_test, y_test = load_data([
        "X_test", "y_figure_test",
    ])
    model.evaluate(X_test, y_test, batch_size=32)


def test_direction():
    model = keras.models.load_model("../reader_direction.model")
    X_test, y_test = load_data([
        "X_test", "y_direction_test",
    ])
    model.evaluate(X_test, y_test, batch_size=32)


s = time()
train_figure_type()
train_direction()
test_figure()
test_direction()
print(time() - s)
