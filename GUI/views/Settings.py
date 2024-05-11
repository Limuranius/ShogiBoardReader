from PyQt5.QtCore import pyqtSlot, QVariant
from PyQt5.QtWidgets import QWidget
from Elements.ImageGetters import Camera, Photo, Video
from GUI.UI.UI_Settings import Ui_settings
from Elements import ImageGetters, BoardSplitter, BoardMemorizer, ShogiBoardReader
from GUI.widgets import combobox_values
from config import GLOBAL_CONFIG
from extra.types import ImageNP


class Settings(QWidget):
    __reader: ShogiBoardReader

    def __init__(self, reader: ShogiBoardReader, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.ui = Ui_settings()
        self.ui.setupUi(self)

        self.__reader = reader

        # Sending instance of splitter to DetectorsSelect so that it also can edit same instance
        self.ui.corner_and_inventory_select.set_splitter(reader.get_board_splitter())

        # Filling combo boxes
        cams_name, cams_values = combobox_values.cameras()
        self.ui.cam_id_select.set_name(cams_name)
        self.ui.cam_id_select.set_values(cams_values)
        ig_name, ig_values = combobox_values.image_getter()
        self.ui.image_getter_select.set_name(ig_name)
        self.ui.image_getter_select.set_values(ig_values)
        mem_name, mem_values = combobox_values.memorizer()
        self.ui.memorizer_select.set_name(mem_name)
        self.ui.memorizer_select.set_values(mem_values)

        self.ui.photo_drop.set_content_type("ONE_IMAGE")
        self.ui.video_drop.set_content_type("VIDEO")

    @pyqtSlot(QVariant)
    def on_image_getter_changed(self, image_getter: ImageGetters.ImageGetter):
        splitter = self.__reader.get_board_splitter()
        splitter.set_image_getter(image_getter)

        # Showing widgets only for chosen image getter
        self.ui.photo_drop.setVisible(False)
        self.ui.video_drop.setVisible(False)
        self.ui.frame_memorizer.setVisible(False)
        self.ui.cam_id_select.setVisible(False)
        if isinstance(image_getter, ImageGetters.Photo):
            self.ui.photo_drop.setVisible(True)
            self.ui.corner_and_inventory_select.stop_continuous_update()
        if isinstance(image_getter, ImageGetters.Video):
            self.ui.video_drop.setVisible(True)
            self.ui.frame_memorizer.setVisible(True)
            self.ui.corner_and_inventory_select.start_continuous_update()
        if isinstance(image_getter, ImageGetters.Camera):
            self.ui.frame_memorizer.setVisible(True)
            self.ui.cam_id_select.setVisible(True)
            self.ui.corner_and_inventory_select.start_continuous_update()

    @pyqtSlot(QVariant)
    def on_photo_input(self, image: ImageNP):
        splitter = self.__reader.get_board_splitter()
        splitter.set_image_getter(Photo(image))

    @pyqtSlot(QVariant)
    def on_video_input(self, video_path: str):
        splitter = self.__reader.get_board_splitter()
        splitter.set_image_getter(Video(video_path))

    @pyqtSlot(QVariant)
    def on_cam_id_changed(self, camera: Camera):
        splitter = self.__reader.get_board_splitter()
        splitter.set_image_getter(camera)

    @pyqtSlot(QVariant)
    def on_memorizer_changed(self, memorizer: BoardMemorizer):
        self.__reader.set_memorizer(memorizer)

    @pyqtSlot(QVariant)
    def on_splitter_changed(self, splitter: BoardSplitter):
        pass

    @pyqtSlot(bool)
    def on_lower_moves_first_switched(self, lower_moves_first: bool):
        pass

    @pyqtSlot(bool)
    def on_alarm_switched(self, use_alarm: bool):
        GLOBAL_CONFIG.Settings.use_siren = use_alarm

    @pyqtSlot()
    def on_ok_clicked(self):
        self.close()

    @pyqtSlot()
    def on_cancel_clicked(self):
        self.close()
