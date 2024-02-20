from Elements import *
from config import Paths, GLOBAL_CONFIG
from extra.image_modes import ImageMode


def default_recognizer() -> Recognizers.Recognizer:
    return RecognizerONNX(
        model_path=Paths.MODEL_ONNX_PATH,
        cell_img_size=GLOBAL_CONFIG.NeuralNetwork.cell_img_size
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


def empty_reader(image_mode: ImageMode):
    return ShogiBoardReader(
        image_mode=image_mode,
        board_splitter=BoardSplitter(
            image_getter=None,
            corner_getter=None,
            inventory_detector=None
        ),
        recognizer=default_recognizer(),
        memorizer=None
    )


def image_reader(image_mode: ImageMode):
    reader = ShogiBoardReader(
        image_mode=image_mode,
        board_splitter=BoardSplitter(
            ImageGetters.Photo(),
            CornerDetectors.CoolCornerDetector(),
        ),
        recognizer=default_recognizer()
    )
    return reader
