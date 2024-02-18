from os import path
import os

ROOT_DIR = path.abspath(path.join(path.dirname(__file__), ".."))

CONFIG_PATH = path.join(ROOT_DIR, "config.ini")

SHOGI_NN_DIR = path.join(ROOT_DIR, "ShogiNeuralNetwork")
DATASETS_DIR = path.join(SHOGI_NN_DIR, "datasets")
ORIGINAL_CELLS_DATASET_PATH = path.join(DATASETS_DIR, "original_cells.pickle")
IMGS_EXAMPLE_DIR = path.join(SHOGI_NN_DIR, "imgs_examples")

MODELS_DIR = path.join(ROOT_DIR, "models")
MODEL_TF_FIGURE_PATH = path.join(MODELS_DIR, "reader_figure_type.model")
MODEL_TF_DIRECTION_PATH = path.join(MODELS_DIR, "reader_direction.model")
MODEL_ONNX_FIGURE_PATH = path.join(MODELS_DIR, "reader_figure_type.onnx")
MODEL_ONNX_DIRECTION_PATH = path.join(MODELS_DIR, "reader_direction.onnx")

IMGS_DIR = path.join(ROOT_DIR, "img")
TRAIN_BOARDS_DIR = path.join(IMGS_DIR, "boards")
FIGURE_ICONS_DIR = path.join(IMGS_DIR, "figures icons")

KIFU_PATH = path.join(ROOT_DIR, "kifu.kif")

SOUNDS_DIR_PATH = path.join(ROOT_DIR, "sounds")
ALARM_PATH = path.join(SOUNDS_DIR_PATH, "alarm.mp4")

def create_folders(paths: list[str]):
    for dir_path in paths:
        os.makedirs(dir_path, exist_ok=True)


create_folders([
    SHOGI_NN_DIR,
    DATASETS_DIR,
    IMGS_EXAMPLE_DIR,
    MODELS_DIR,
    IMGS_DIR,
    TRAIN_BOARDS_DIR,
    FIGURE_ICONS_DIR,
])
