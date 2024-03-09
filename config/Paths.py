from os import path
import os

ROOT_DIR = path.abspath(path.join(path.dirname(__file__), ".."))

CONFIG_PATH = path.join(ROOT_DIR, "config.ini")

SHOGI_NN_DIR = path.join(ROOT_DIR, "ShogiNeuralNetwork")
DATASETS_DIR = path.join(SHOGI_NN_DIR, "datasets")
ORIGINAL_CELLS_DATASET_PATH = path.join(DATASETS_DIR, "original_cells.pickle")
DATASET_PATH = path.join(DATASETS_DIR, "dataset")

MODELS_DIR = path.join(ROOT_DIR, "models")
MODEL_TF_PATH = path.join(MODELS_DIR, "model.model")
MODEL_ONNX_PATH = path.join(MODELS_DIR, "model.onnx")

IMGS_DIR = path.join(ROOT_DIR, "img")
FIGURE_ICONS_DIR = path.join(IMGS_DIR, "figures icons")

SOUNDS_DIR_PATH = path.join(ROOT_DIR, "sounds")
ALARM_PATH = path.join(SOUNDS_DIR_PATH, "alarm.mp4")


def create_folders(paths: list[str]):
    for dir_path in paths:
        os.makedirs(dir_path, exist_ok=True)


create_folders([
    SHOGI_NN_DIR,
    DATASETS_DIR,
    MODELS_DIR,
    IMGS_DIR,
    FIGURE_ICONS_DIR,
])
