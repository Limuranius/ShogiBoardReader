import os.path
from Elements import *
import numpy as np
from config import Config, Paths, GLOBAL_CONFIG
from ShogiNeuralNetwork import data_info
from extra.image_modes import ImageMode


def get_camera_reader(image_mode: ImageMode, cam_id: int):
    config = Config(Paths.CONFIG_PATH)
    hsv_low = np.array([
        config.HSVThreshold.h_low,
        config.HSVThreshold.s_low,
        config.HSVThreshold.v_low,
    ])
    hsv_high = np.array([
        config.HSVThreshold.h_high,
        config.HSVThreshold.s_high,
        config.HSVThreshold.v_high,
    ])

    reader = ShogiBoardReader(
        image_mode,
        BoardSplitter(
            ImageGetters.Camera(cam_id),
            CornerDetectors.HSVThresholdCornerDetector(hsv_low, hsv_high),
            cell_img_size=config.NeuralNetwork.cell_img_size
        ),
        FigureRecognizers.RecognizerNN(
            Paths.MODEL_FIGURE_PATH,
            Paths.MODEL_DIRECTION_PATH,
            cell_img_size=config.NeuralNetwork.cell_img_size
        ),
        memorizer=None
    )
    return reader


def get_hardcoded_reader(image_mode: ImageMode, img_name: str):
    config = Config(Paths.CONFIG_PATH)
    img_path = os.path.join(Paths.TRAIN_BOARDS_DIR, img_name)
    corners = data_info.IMGS_CORNERS[img_path]

    reader = ShogiBoardReader(
        image_mode,
        BoardSplitter(
            ImageGetters.Photo(img_path),
            CornerDetectors.HardcodedCornerDetector(corners),
            cell_img_size=config.NeuralNetwork.cell_img_size
        ),
        FigureRecognizers.RecognizerNN(
            Paths.MODEL_FIGURE_PATH,
            Paths.MODEL_DIRECTION_PATH,
            cell_img_size=config.NeuralNetwork.cell_img_size
        ),
        memorizer=None
    )
    return reader


def get_video_reader(image_mode: ImageMode, video_path: str, use_memorizer: bool):
    config = Config(Paths.CONFIG_PATH)
    hsv_low = np.array([
        config.HSVThreshold.h_low,
        config.HSVThreshold.s_low,
        config.HSVThreshold.v_low,
    ])
    hsv_high = np.array([
        config.HSVThreshold.h_high,
        config.HSVThreshold.s_high,
        config.HSVThreshold.v_high,
    ])

    if use_memorizer:
        memorizer = BoardMemorizer()
    else:
        memorizer = None

    reader = ShogiBoardReader(
        image_mode,
        BoardSplitter(
            ImageGetters.Video(video_path),
            CornerDetectors.HSVThresholdCornerDetector(hsv_low, hsv_high),
            cell_img_size=config.NeuralNetwork.cell_img_size
        ),
        FigureRecognizers.RecognizerNN(
            Paths.MODEL_FIGURE_PATH,
            Paths.MODEL_DIRECTION_PATH,
            cell_img_size=config.NeuralNetwork.cell_img_size
        ),
        memorizer=memorizer
    )
    return reader


def default_nn_recognizer():
    return FigureRecognizers.RecognizerNN(
        Paths.MODEL_FIGURE_PATH,
        Paths.MODEL_DIRECTION_PATH,
        GLOBAL_CONFIG.NeuralNetwork.cell_img_size
    )