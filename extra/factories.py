from Elements import *
from config import Paths, GLOBAL_CONFIG


def default_recognizer() -> Recognizers.Recognizer:
    return RecognizerONNX(
        model_path=Paths.MODEL_ONNX_PATH,
    )


def hsv_corner_detector():
    hsv_low = (
        GLOBAL_CONFIG.HSVThreshold.h_low,
        GLOBAL_CONFIG.HSVThreshold.s_low,
        GLOBAL_CONFIG.HSVThreshold.v_low,
    )
    hsv_high = (
        GLOBAL_CONFIG.HSVThreshold.h_high,
        GLOBAL_CONFIG.HSVThreshold.s_high,
        GLOBAL_CONFIG.HSVThreshold.v_high,
    )
    return CornerDetectors.HSVThresholdCornerDetector(hsv_low, hsv_high)


def empty_reader():
    return ShogiBoardReader(
        board_splitter=BoardSplitter(
            image_getter=None,
            corner_getter=None,
            inventory_detector=None
        ),
        recognizer=default_recognizer(),
        memorizer=None
    )


def image_reader():
    reader = ShogiBoardReader(
        board_splitter=BoardSplitter(
            ImageGetters.Photo(),
            CornerDetectors.CoolCornerDetector(),
        ),
        recognizer=default_recognizer()
    )
    return reader


def book_reader():
    reader = ShogiBoardReader(
        board_splitter=BoardSplitter(
            image_getter=ImageGetters.Photo(),
            corner_getter=BookCornerDetector(),
            inventory_detector=BookInventoryDetector()
        ),
        recognizer=default_recognizer()
    )
    return reader


def camera_reader():
    reader = ShogiBoardReader(
        board_splitter=BoardSplitter(
            image_getter=ImageGetters.Camera(),
            corner_getter=CoolCornerDetector(),
            inventory_detector=None
        ),
        recognizer=default_recognizer()
    )
    return reader

default_recognizer()