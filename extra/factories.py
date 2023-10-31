from Elements import *
import numpy as np
from config import Config, Paths

def get_hardcoded_reader():
    img_path = os.path.join(paths.TRAIN_BOARDS_DIR, "board13.jpg")
    corners = data_info.IMGS_CORNERS[img_path]

    reader = ShogiBoardReader(
        image_getter.Photo(img_path),
        CornerGetter.HardcodedCornerDetector(corners),
        recognizer.RecognizerNN(
            paths.MODEL_FIGURE_PATH,
            paths.MODEL_DIRECTION_PATH
        )
    )
    return reader


def get_camera_reader():
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
        image_getter.Camera(),
        CornerGetter.HSVThresholdCornerDetector(hsv_low, hsv_high),
        recognizer.RecognizerNN(
            paths.MODEL_FIGURE_PATH,
            paths.MODEL_DIRECTION_PATH
        )
    )
    return reader


def get_video_reader(video_path: str):
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
        image_getter.Video(video_path),
        CornerGetter.HSVThresholdCornerDetector(hsv_low, hsv_high),
        recognizer.RecognizerNN(
            paths.MODEL_FIGURE_PATH,
            paths.MODEL_DIRECTION_PATH
        )
    )
    return reader