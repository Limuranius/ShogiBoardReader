from mytypedconfig import section
from paths import CONFIG_PATH


@section(config_path=CONFIG_PATH, section_name="NN data")
class NN_data:
    cell_img_size: int
    board_img_size: int
    test_fraction: float
    random_translate_repeat: int
    random_translate_max_margin: float


@section(config_path=CONFIG_PATH, section_name="HSV Threshold")
class HSVThreshold:
    h_low: int
    h_high: int
    s_low: int
    s_high: int
    v_low: int
    v_high: int


@section(config_path=CONFIG_PATH, section_name="Tweaks")
class Tweaks:
    show_orig_img: bool
    show_hsv_mask: bool
    show_canny: bool
    canny_low: int
    canny_high: int
    img_scale: int


class Config:
    NN_data: NN_data
    HSVThreshold: HSVThreshold
    Tweaks: Tweaks

    def __init__(self):
        self.NN_data = NN_data()
        self.HSVThreshold = HSVThreshold()
        self.Tweaks = Tweaks()

        self.NN_data.board_img_size = self.NN_data.cell_img_size * 9


config = Config()
