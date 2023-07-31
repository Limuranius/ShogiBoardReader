from os import path
import os

ROOT_DIR = path.dirname(path.abspath(__file__))

CONFIG_PATH = path.join(ROOT_DIR, "config.ini")

NN_DATA_DIR = path.join(ROOT_DIR, "NN_data")
DATASETS_DIR = path.join(NN_DATA_DIR, "datasets")
X_TRAIN_PATH = path.join(NN_DATA_DIR, "x_train_path.pickle")
X_TEST_PATH = path.join(NN_DATA_DIR, "x_test.pickle")
Y_FIGURE_TRAIN_PATH = path.join(NN_DATA_DIR, "y_figure_train_path.pickle")
Y_FIGURE_TEST_PATH = path.join(NN_DATA_DIR, "y_figure_test_path.pickle")
Y_DIRECTION_TRAIN_PATH = path.join(NN_DATA_DIR, "y_direction_train_path.pickle")
Y_DIRECTION_TEST_PATH = path.join(NN_DATA_DIR, "y_direction_test_path.pickle")
IMGS_EXAMPLE_DIR = path.join(NN_DATA_DIR, "imgs_examples")

MODELS_DIR = path.join(ROOT_DIR, "models")
MODEL_FIGURE_PATH = path.join(MODELS_DIR, "reader_figure_type.model")
MODEL_DIRECTION_PATH = path.join(MODELS_DIR, "reader_direction.model")

IMGS_DIR = path.join(ROOT_DIR, "img")
TRAIN_BOARDS_DIR = path.join(IMGS_DIR, "boards")
FIGURE_ICONS_DIR = path.join(IMGS_DIR, "figures icons")


def create_folders(paths: list[str]):
    for dir_path in paths:
        os.makedirs(dir_path, exist_ok=True)


create_folders([
    NN_DATA_DIR,
    DATASETS_DIR,
    IMGS_EXAMPLE_DIR,
    MODELS_DIR,
    MODEL_FIGURE_PATH,
    MODEL_DIRECTION_PATH,
    IMGS_DIR,
    TRAIN_BOARDS_DIR,
    FIGURE_ICONS_DIR,
])
