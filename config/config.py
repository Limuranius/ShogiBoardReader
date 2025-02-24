from .mytypedconfig import section
from .paths import CONFIG_PATH


@section(section_name="HSV Threshold")
class HSVThreshold:
    h_low: int
    h_high: int
    s_low: int
    s_high: int
    v_low: int
    v_high: int


@section(section_name="Visuals")
class Visuals:
    show_borders: bool
    show_grid: bool
    show_inventories: bool
    lines_thickness_fraction: float


@section(section_name="Settings")
class Settings:
    use_siren: bool
    predict_board: bool


class Config:
    HSVThreshold: HSVThreshold
    Visuals: Visuals
    Settings: Settings

    def __init__(self, config_path: str):
        self.HSVThreshold = HSVThreshold(config_path)
        self.Visuals = Visuals(config_path)
        self.Settings = Settings(config_path)


GLOBAL_CONFIG = Config(CONFIG_PATH)
