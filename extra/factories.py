import os.path
from Elements import *
from config import Config, Paths, GLOBAL_CONFIG
from extra.image_modes import ImageMode


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


def get_camera_reader(image_mode: ImageMode, cam_id: int):
    reader = ShogiBoardReader(
        image_mode,
        BoardSplitter(
            ImageGetters.Camera(cam_id),
            hsv_corner_detector(),
            cell_img_size=GLOBAL_CONFIG.NeuralNetwork.cell_img_size
        ),
        FigureRecognizers.RecognizerNN(
            Paths.MODEL_FIGURE_PATH,
            Paths.MODEL_DIRECTION_PATH,
            cell_img_size=GLOBAL_CONFIG.NeuralNetwork.cell_img_size
        ),
        memorizer=None
    )
    return reader


def get_hardcoded_reader(image_mode: ImageMode, img_name: str):
    config = Config(Paths.CONFIG_PATH)
    img_path = os.path.join(Paths.TRAIN_BOARDS_DIR, img_name)
    corners = true_boards.get_corners(img_name)

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
    if use_memorizer:
        memorizer = BoardMemorizer()
    else:
        memorizer = None

    reader = ShogiBoardReader(
        image_mode,
        BoardSplitter(
            ImageGetters.Video(video_path),
            # hsv_corner_detector(),
            CornerDetectors.CoolCornerDetector(),
            cell_img_size=GLOBAL_CONFIG.NeuralNetwork.cell_img_size
        ),
        FigureRecognizers.RecognizerNN(
            Paths.MODEL_FIGURE_PATH,
            Paths.MODEL_DIRECTION_PATH,
            cell_img_size=GLOBAL_CONFIG.NeuralNetwork.cell_img_size
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


def get_image_reader(image_mode: ImageMode):
    config = Config(Paths.CONFIG_PATH)

    reader = ShogiBoardReader(
        image_mode,
        BoardSplitter(
            ImageGetters.Photo(),
            CornerDetectors.CoolCornerDetector(),
            cell_img_size=config.NeuralNetwork.cell_img_size
        ),
        FigureRecognizers.RecognizerNN(
            Paths.MODEL_FIGURE_PATH,
            Paths.MODEL_DIRECTION_PATH,
            cell_img_size=config.NeuralNetwork.cell_img_size
        )
    )
    return reader
