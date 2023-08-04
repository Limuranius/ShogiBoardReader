import pickle
from tensorflow import keras
from time import time
from config import config
import paths


FIGURE_EPOCH = 5
DIRECTION_EPOCH = 5


def load_data(paths: list[str]):
    return [
        pickle.load(open(path, "rb"))
        for path in paths
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
        paths.X_TRAIN_PATH, paths.Y_FIGURE_TRAIN_PATH,
    ])
    X_train = X_train.astype("float32") / 255

    model.fit(X_train, y_train, batch_size=32, epochs=FIGURE_EPOCH)
    model.save(paths.MODEL_FIGURE_PATH)


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
        paths.X_TRAIN_PATH, paths.Y_DIRECTION_TRAIN_PATH,
    ])
    X_train = X_train.astype("float32") / 255

    model.fit(X_train, y_train, batch_size=32, epochs=DIRECTION_EPOCH)
    model.save(paths.MODEL_DIRECTION_PATH)


def test_figure():
    model = keras.models.load_model(paths.MODEL_FIGURE_PATH)
    X_test, y_test = load_data([
        paths.X_TEST_PATH, paths.Y_FIGURE_TEST_PATH,
    ])
    model.evaluate(X_test, y_test, batch_size=32)


def test_direction():
    model = keras.models.load_model(paths.MODEL_DIRECTION_PATH)
    X_test, y_test = load_data([
        paths.X_TEST_PATH, paths.Y_DIRECTION_TEST_PATH,
    ])
    model.evaluate(X_test, y_test, batch_size=32)


s = time()
train_figure_type()
train_direction()
test_figure()
test_direction()
print(time() - s)
