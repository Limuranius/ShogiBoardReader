from .mytypedconfig import section
from .Paths import CONFIG_PATH


@section(section_name="Neural Network")
class NeuralNetwork:
    cell_img_size: int
    test_fraction: float
    width_shift_factor: float
    height_shift_factor: float
    rotation_factor: float
    zoom_factor: float
    figure_epochs: int
    batch_size: int
    direction_epochs: int
    image_mode: str
    brightness_factor: float


@section(section_name="HSV Threshold")
class HSVThreshold:
    h_low: int
    h_high: int
    s_low: int
    s_high: int
    v_low: int
    v_high: int


@section(section_name="Tweaks")
class Tweaks:
    show_orig_img: bool
    show_hsv_mask: bool
    show_canny: bool
    canny_low: int
    canny_high: int
    img_scale: int


class Config:
    NeuralNetwork: NeuralNetwork
    HSVThreshold: HSVThreshold
    Tweaks: Tweaks

    def __init__(self, config_path: str):
        self.NeuralNetwork = NeuralNetwork(config_path)
        self.HSVThreshold = HSVThreshold(config_path)
        self.Tweaks = Tweaks(config_path)


GLOBAL_CONFIG = Config(CONFIG_PATH)
