from Elements import *
import numpy as np
from config import Config, Paths


def get_camera_reader(cam_id: int):
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
