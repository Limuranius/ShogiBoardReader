from .mytypedconfig import section


@section(section_name="NN data")
class NN_data:
    cell_img_size: int
    board_img_size: int
    test_fraction: float
    random_translate_repeat: int
    random_translate_max_margin: float
    random_rotate_repeat: int
    random_rotate_max_angle: int


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
    NN_data: NN_data
    HSVThreshold: HSVThreshold
    Tweaks: Tweaks

    def __init__(self, config_path: str):
        self.NN_data = NN_data(config_path)
        self.HSVThreshold = HSVThreshold(config_path)
        self.Tweaks = Tweaks(config_path)
