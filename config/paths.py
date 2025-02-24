from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent.parent

CONFIG_PATH = ROOT_DIR / "config.ini"

SHOGI_NN_DIR = ROOT_DIR / "ShogiNeuralNetwork"
DATASETS_DIR = SHOGI_NN_DIR / "datasets"

FIGURE_DATASET_PATH = DATASETS_DIR / "figure_classification"
DIRECTION_DATASET_PATH = DATASETS_DIR / "direction_classification"
BOARD_DATASET_PATH = DATASETS_DIR / "board_segmentation" / "data.yaml"

MODELS_DIR = ROOT_DIR / "models"
FIGURE_CLASSIFICATION_MODEL_PATH = MODELS_DIR / "figure_classifier.pt"
DIRECTION_CLASSIFICATION_MODEL_PATH = MODELS_DIR / "direction_classifier.pt"
BOARD_SEGMENTATION_MODEL_PATH = MODELS_DIR / "board_segmenter.pt"

IMGS_DIR = ROOT_DIR / "img"
FIGURE_ICONS_DIR = IMGS_DIR / "figures icons"
ICONS_DIR = IMGS_DIR / "Icons"

SOUNDS_DIR_PATH = ROOT_DIR / "sounds"
ALARM_PATH = SOUNDS_DIR_PATH / "alarm.wav"
