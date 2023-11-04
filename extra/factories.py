import os.path
from Elements import *
import numpy as np
from config import Config, Paths
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
        BoardSplitter.BoardSplitter(
            ImageGetters.Camera(cam_id),
            CornerGetters.HSVThresholdCornerDetector(hsv_low, hsv_high),
            board_img_size=config.NN_data.board_img_size,
            cell_img_size=config.NN_data.cell_img_size
        ),
        FigureRecognizers.RecognizerNN(
            Paths.MODEL_FIGURE_PATH,
            Paths.MODEL_DIRECTION_PATH,
            cell_img_size=config.NN_data.cell_img_size
        ),
        analyzer=None
    )
    return reader


def get_hardcoded_reader(image_mode: ImageMode, img_name: str):
    config = Config(Paths.CONFIG_PATH)
    img_path = os.path.join(Paths.TRAIN_BOARDS_DIR, img_name)
    corners = data_info.IMGS_CORNERS[img_path]

    reader = ShogiBoardReader(
        image_mode,
        BoardSplitter.BoardSplitter(
            ImageGetters.Photo(img_path),
            CornerGetters.HardcodedCornerDetector(corners),
            board_img_size=config.NN_data.board_img_size,
            cell_img_size=config.NN_data.cell_img_size
        ),
        FigureRecognizers.RecognizerNN(
            Paths.MODEL_FIGURE_PATH,
            Paths.MODEL_DIRECTION_PATH,
            cell_img_size=config.NN_data.cell_img_size
        ),
        analyzer=None
    )
    return reader


def get_video_reader(image_mode: ImageMode, video_path: str):
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
        BoardSplitter.BoardSplitter(
            ImageGetters.Video(video_path),
            CornerGetters.HSVThresholdCornerDetector(hsv_low, hsv_high),
            board_img_size=config.NN_data.board_img_size,
            cell_img_size=config.NN_data.cell_img_size
        ),
        FigureRecognizers.RecognizerNN(
            Paths.MODEL_FIGURE_PATH,
            Paths.MODEL_DIRECTION_PATH,
            cell_img_size=config.NN_data.cell_img_size
        ),
        analyzer=None
    )
    return reader
